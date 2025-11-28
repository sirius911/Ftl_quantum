import matplotlib.pyplot as plt
import qiskit
from qiskit import QuantumCircuit
from qiskit_aer import QasmSimulator
from Oracle import Base_Oracle


def dessine_circuit(qc, n_qubits, name):
    try:
        circuit_title = f"Deutsch-Jozsa (n={n_qubits}) | Oracle: {name}"

        figure = qc.draw(output='mpl', initial_state=True, fold=-1)
        figure.suptitle(circuit_title, fontsize=14)
        plt.show()

    except ImportError:
        print("Matplotlib non installé. Affichage textuel du circuit :")
        print(qc.draw(output='text', fold=-1))


def run_deutsch_jozsa(oracle_obj):
    """
    Exécute l'algorithme de Deutsch-Jozsa pour déterminer si l'Oracle est Constant ou Balancé.

    :param n_qubits: Nombre de qubits de données.
    :param oracle_obj: Une instance de la classe Oracle (héritant de Base_Oracle).
    :returns: Chaîne "CONSTANT" ou "BALANCÉ".
    """
    n_qubits = oracle_obj.n_qubits

    if not isinstance(oracle_obj, Base_Oracle):
        raise TypeError("L'objet Oracle doit hériter de Base_Oracle.")

    # print(f"Algorythme de Deutsch-Jozsa sur {oracle_obj}")
    oracle_obj.dessine()

    # N qubits de données + 1 qubit auxiliaire
    total_qubits = n_qubits + 1
    qc = QuantumCircuit(total_qubits, n_qubits)
    data_qubits = list(range(n_qubits))
    qubit_auxiliaire = n_qubits

    # 1. Préparation initiale des états

    # Initialisation du qubit auxiliaire à l'état |->
    qc.x(qubit_auxiliaire)  # |1>
    qc.h(qubit_auxiliaire)  # |->

    # Superposition sur le registre de données |x>
    qc.h(data_qubits)

    # 2. Application de l'Oracle (intégration de l'objet fourni)
    qc = oracle_obj.append_to_circuit(qc)  # Appel de la méthode de l'Oracle

    # 3. Interférence
    qc.h(data_qubits)

    # 4. Mesure
    # Mesure du registre de données (les n premiers qubits)
    qc.measure(data_qubits, data_qubits)

    # 5. Affichage du circuit total
    print("\nVisualisation du circuit complet:")
    # print(qc.draw(output='text', initial_state=True, fold=-1))
    dessine_circuit(qc, n_qubits, oracle_obj.name)

    input("Appuyez sur Entrée pour lancer la simulation quantique...")

    # --- SIMULATION ---
    simulator = QasmSimulator()
    compiled_circuit = qiskit.transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1)  # Un seul tir suffit pour DJ

    result = job.result()
    counts = result.get_counts(qc)

    print("\nCounts bruts :")
    print(counts)

    # --- Analyse et Résultat ---

    # L'algorithme DJ réussit si l'état |00...0> est le résultat de la mesure.
    # Si la mesure de |x> est |00...0>, alors f est CONSTANTE.
    # Si la mesure de |x> est un état non-nul (ex: |010...>), alors f est BALANCÉE.

    result_key = '0' * n_qubits

    if result_key in counts:
        conclusion = "CONSTANT"
    else:
        conclusion = "BALANCÉ"

    print("\n[Circuit généré]")
    print(qc.draw(output='text', fold=-1))

    print(f"Mesure du registre |x> : {list(counts.keys())[0]}")
    print(f"✅ CONCLUSION: L'Oracle est {conclusion}.")

    return conclusion


if __name__ == "__main__":

    # --- Test 1 : Oracle Simple ---
    from Oracle import Simple_Oracle
    try:
        oracle_simple = Simple_Oracle()
        print(f"\n--- TEST 2: Oracle Simple (N={oracle_simple.n_qubits}) ---")
        run_deutsch_jozsa(oracle_simple)
    except Exception as e:
        print(f"Erreur lors de l'exécution du test 1: {e}")

    # --- Test 2 : Oracle Balancé (f(x)=x_0) ---
    from Oracle import BalancedOracleX0
    try:
        balanced_oracle_test = BalancedOracleX0()
        print(f"\n--- TEST 2: Oracle Balancé (N={balanced_oracle_test.n_qubits}) ---")
        run_deutsch_jozsa(balanced_oracle_test)
    except Exception as e:
        print(f"Erreur lors de l'exécution du test 2: {e}")

    # --- Test 3 : Oracle Constant (f(x)=1) ---
    from Oracle import ConstantOracle1
    try:
        constant_oracle_test = ConstantOracle1()
        print(f"\n--- TEST 1: Oracle Constant (N={constant_oracle_test.n_qubits}) ---")
        run_deutsch_jozsa(constant_oracle_test)
    except Exception as e:
        print(f"Erreur lors de l'exécution du test 1: {e}")

    # --- Test 4 : Oracle Correcteur ---
