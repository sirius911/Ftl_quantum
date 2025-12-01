import sys
import qiskit
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from utils.results_utils import afficher_resultats

SHOTS = 1024


def print_introduction_ex02(backend_name):
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "="*70)
    print("   EXERCICE 02 : BRUIT QUANTIQUE (SUR IBM QUANTUM)")
    print("="*70)
    print("  ** Objectif ** : Exécuter le circuit 'État de Bell (Intrication)' "
          f"sur ordinateur quantique ({backend_name})")
    print("   pour mesurer l'effet du bruit quantique (erreurs).")
    print("-" * 70 + "\n")

# ---------------------------------------------------------
# DÉBUT DU PROGRAMME
# ---------------------------------------------------------


# 1. Connexion et choix du Backend
try:
    service = QiskitRuntimeService()
    backend = service.least_busy(simulator=False, operational=True)

    if backend is None:
        print("❌ Aucune machine quantique réelle n'est disponible pour le moment.")
        exit()

    backend_name = backend.name

except Exception as e:
    print("❌ ERREUR : La connexion au backend a échoué. Assurez-vous que le 'setup_ibm.py' a réussi.")
    print(f"Détail : {e}")
    exit()

print_introduction_ex02(backend_name)

# 2 Qubits (q0, q1) et 2 Bits classiques (c0, c1)
circuit = qiskit.QuantumCircuit(2, 2)

# 1. Création de la superposition sur q0
circuit.h(0)

# 2. Création de l'intrication (CNOT: q0 contrôle q1)
circuit.cx(0, 1)

# 3. Mesure des deux qubits dans les deux bits classiques
# [q0, q1] -> [c0, c1]
circuit.measure([0, 1], [0, 1])

# Affichage du circuit
print("\n[1] Visualisation du circuit :")
print(circuit.draw(output='text', initial_state=True, cregbundle=False))


# 3. Transpilation (Adaptation à la machine)
pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
compiled_circuit = pm.run(circuit)

# 4. Soumission du Job via la Session
print(f"\n[2] Job Sampler soumis à {backend_name} avec {SHOTS} tirs (mode job, sans Session).")
print("ATTENTION : Cette étape met le job en file d'attente (peut prendre du temps).")

try:
    # On utilise directement le backend comme mode d'exécution
    sampler = Sampler(mode=backend)
    # On fixe le nombre de tirs par défaut
    sampler.options.default_shots = SHOTS  # équivalent de tes 1024 shots :contentReference[oaicite:3]{index=3}

    # Soumission du job au vrai QPU
    job = sampler.run([compiled_circuit])

    print(f"ID du Job: {job.job_id()}")
    print(f"Statut : {job.status()}")
    print("\n--- ATTENTE DES RÉSULTATS ---")

    # Attente des résultats
    result = job.result()

    print("result Brut : ", result)

    pub_result = result[0]
    bitarray = pub_result.data.c
    counts = bitarray.get_counts()

    print("\nCounts bruts :")
    print(counts)

    afficher_resultats(
        counts,
        backend_name=backend_name,
        titre=f"Résultats 'Etat de Bell' — {backend_name}",
        afficher_graphique=True,
    )

except Exception as e:
    print(f"\n❌ ERREUR LORS DE LA SOUMISSION DU JOB: {e}")
    print("Vérifiez l'état de la machine sur la page IBM Quantum Experience.")
