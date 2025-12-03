from qiskit import QuantumCircuit, transpile
from qiskit_aer import QasmSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
import numpy as np
import sys
from pathlib import Path
from Oracle_Grover import Base_Grover_Oracle
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
# Ajouter le dossier parent (projet/) au PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from utils.results_utils import afficher_resultats, dessine_circuit  # noqa: E402

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))


def build_diffuser(n_qubits: int) -> QuantumCircuit:
    """Construit l'opérateur de diffusion D = H^n * U0 * H^n."""
    qc = QuantumCircuit(n_qubits, name="Diffuser")

    # 1. H^n
    qc.h(range(n_qubits))

    # 2. U0 (Inversion de phase sur l'état |00...0>)

    # a. X^n : |00...0> -> |11...1>
    qc.x(range(n_qubits))

    # b. MCZ : Applique un flip de phase -1 si l'état est |11...1>
    if n_qubits == 2:
        qc.cz(0, 1)
    else:
        # MCZ sur n qubits (implémenté avec Toffoli encadré de H)
        target_qubit = n_qubits - 1
        control_qubits = list(range(n_qubits - 1))

        qc.h(target_qubit)
        qc.mcx(control_qubits, target_qubit)
        qc.h(target_qubit)

    # c. X^n : Annule les X initiaux
    qc.x(range(n_qubits))

    # 3. H^n final
    qc.h(range(n_qubits))
    print(qc.draw(output='text', initial_state=True, cregbundle=False))
    dessine_circuit(qc, n_qubits, "Diffuseur de Grover")

    return qc.to_instruction()


def run_grover_search(oracle_obj: Base_Grover_Oracle, backend_name: str = 'simulator'):
    """
    Exécute l'algorithme de Grover.

    :param oracle_obj: Une instance de la classe Oracle de Grover.
    :param backend_name: 'simulator' ou le nom d'un backend IBMQ.
    :returns: L'état solution trouvé.
    """
    n_qubits = oracle_obj.n_qubits
    N = 2**n_qubits
    SHOTS = 1024

    # Calcul du nombre d'itérations R = floor(pi/4 * sqrt(N))
    num_iterations = int(np.floor(np.pi / 4 * np.sqrt(N)))

    print(f"\n--- Algorithme de Grover (N={n_qubits} qubits, {N} états) ---")
    print(f"Oracle testé : {oracle_obj.name}")
    print(f"Nombre optimal d'itérations : {num_iterations}")

    print("Affichage du circuit de l'Oracle...")
    print(oracle_obj.draw())
    oracle_obj.dessine()

    # 1. Création du circuit
    qc = QuantumCircuit(n_qubits, n_qubits)

    # 2. Initialisation à la superposition |s>
    qc.h(range(n_qubits))
    qc.barrier(label='Init')

    # 3. Construction du Diffuseur
    diffuser_instruction = build_diffuser(n_qubits)

    # 4. Itérations de Grover
    for i in range(num_iterations):
        # Application de l'Oracle (U_omega)
        qc.append(oracle_obj.get_circuit().to_gate(), range(n_qubits))

        # Application du Diffuseur (D)
        qc.append(diffuser_instruction, range(n_qubits))

        qc.barrier(label=f"Iteration {i+1}")

    # 5. Mesure
    qc.measure(range(n_qubits), range(n_qubits))

    # Affichage du circuit (comme dans deutsch_jozsa.py)
    title = f"Algorithme de Grover (n={n_qubits}) | {oracle_obj.name}"
    dessine_circuit(qc, n_qubits, title=title, save=None)

    qc_transpiled = transpile(qc, basis_gates=['u', 'cx', 'id', 'measure'])

    # --- SIMULATION ET EXÉCUTION ---
    if input("Appuyez sur Entrée pour lancer la simulation quantique "
             "ou Quantique pour envoyer au serveur quantique...") != "Quantique":
        # --- SIMULATION ---
        backend_name = "Simulation locale (QasmSimulator)"
        simulator = QasmSimulator()
        job = simulator.run(qc_transpiled, shots=SHOTS)
        result = job.result()
        counts = result.get_counts(qc)

    else:
        try:
            service = QiskitRuntimeService()
            backend = service.least_busy(simulator=False, operational=True)

            if backend is None:
                print("❌ Aucune machine quantique réelle n'est disponible pour le moment.")
                return

            backend_name = backend.name

        except Exception as e:
            print("❌ ERREUR : La connexion au backend a échoué. Assurez-vous que le 'setup_ibm.py' a réussi.")
            print(f"Détail : {e}")
            return

        # Transpilation (Adaptation à la machine)
        pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
        compiled_circuit = pm.run(qc)
        sampler = Sampler(mode=backend)
        sampler.options.default_shots = SHOTS
        # Soumission du job au vrai QPU
        job = sampler.run([compiled_circuit])
        ident_job = job.job_id()
        print(f"ID du Job: {ident_job}")
        print(f"Statut : {job.status()}")
        print("\n--- ATTENTE DES RÉSULTATS (Ctrl + C pour passer)---")
        try:
            result = job.result()
        except KeyboardInterrupt:
            print("❌ Attente interrompue. \n"
                  f"Vous pourrez récupérer les résultats plus tard avec 'read_result.py {ident_job}'")
            circuit_title = f"Deutsch-Jozsa (n={n_qubits}) | Oracle: {oracle_obj.name}"
            file_name = f"job/{ident_job}.png"
            dessine_circuit(qc=qc,
                            n_qubits=n_qubits,
                            title=circuit_title,
                            save=file_name)
            return
        except Exception as e:
            print("❌ ERREUR lors de la récupération des résultats.")
            print(f"Détail : {e}")
            return

        pub_result = result[0]
        bitarray = pub_result.data.c
        counts = bitarray.get_counts()

    print("\nCounts bruts :")
    print(counts)

    # --- ANALYSE DES RÉSULTATS ---
    solution_trouvee = max(counts, key=counts.get)

    afficher_resultats(
        counts,
        backend_name=backend_name,
        titre=f"Résultats de Grover pour {oracle_obj.name}",
        afficher_graphique=True
    )
    solution_decimal = int(solution_trouvee, 2)
    print(f"\nL'état le plus mesuré est : |{solution_trouvee}>")
    print(f"Le rang trouvé dans la liste (index décimal) est : {solution_decimal}")
    print(f"✅ CONCLUSION: La recherche de Grover a trouvé la solution |{solution_trouvee}> (index {solution_decimal}).")

    return solution_trouvee


# --- Exécution du programme de test ---
if __name__ == "__main__":

    # Test avec N=3 qubits (8 éléments)
    N_TEST = 3

    # --- Test 1 : Oracle marquant l'état |111> ---
    # Import des Oracles
    from Oracle_Grover import OracleGrover11
    try:
        oracle_test_111 = OracleGrover11(N_TEST)
        print(f"\n--- TEST 1: Recherche de |{ '1' * N_TEST }> ---")
        run_grover_search(oracle_test_111)
    except Exception as e:
        print(f"Erreur lors de l'exécution du test 1: {e}")

    # Vous pouvez ajouter ici un autre test avec un Oracle marquant un autre état (ex: |010>)

    # Import du nouvel Oracle
    from Oracle_Grover import OracleGroverSpecific

    # --- Demande utilisateur ---
    N_TEST = 10
    MAX_DECIMAL = 2**N_TEST - 1

    while True:
        try:
            user_input = input(f"\nEntrez le nombre (0 à {MAX_DECIMAL}) à rechercher : ")
            target_decimal = int(user_input)

            if 0 <= target_decimal <= MAX_DECIMAL:
                break
            else:
                print(f"Erreur : Veuillez entrer un nombre dans la plage 0 à {MAX_DECIMAL}.")
        except ValueError:
            print("Erreur : Veuillez entrer un nombre entier valide.")

    # --- Test 1 : Recherche du nombre de l'utilisateur ---
    try:
        oracle_test = OracleGroverSpecific(target_decimal)
        print(f"\n--- TEST DYNAMIQUE: Recherche de {target_decimal} ---")

        # Lancement de l'algorithme
        run_grover_search(oracle_test)

    except Exception as e:
        print(f"Erreur lors de l'exécution du test: {e}")
