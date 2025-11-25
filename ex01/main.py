import qiskit
import matplotlib.pyplot as plt
from qiskit_aer import QasmSimulator


SHOTS = 500  # Le nombre de tirs pour l'expérience


simulator = QasmSimulator()
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

input("Appuyez sur Entrée pour lancer la simulation quantique...")

# Exécution
print(f"\n[2] Exécution de {SHOTS} tirs sur le simulateur...")
compiled_circuit = qiskit.transpile(circuit, simulator)
job = simulator.run(compiled_circuit, shots=SHOTS)
result = job.result()
counts = result.get_counts(circuit)

# Analyse des résultats
print("\n[3] Résultats obtenus :")
print(f"   Comptes bruts : {counts}")

total_shots = sum(counts.values())

# Conversion des comptes en probabilités pour l'affichage
probabilities = {key: val / total_shots for key, val in counts.items()}

print("\n[4] Conclusion :")
print(f"   Résultats : {probabilities}")

if '01' not in counts and '10' not in counts:
    print("   SUCCESS : Les états |01> et |10> sont absents. L'intrication est maximale.")
else:
    # On laisse une marge de tolérance pour l'affichage des probabilités
    prob_01 = probabilities.get('01', 0)
    prob_10 = probabilities.get('10', 0)
    if prob_01 < 0.05 and prob_10 < 0.05:
        print("   SUCCESS : Les états |01> et |10> sont négligeables. L'intrication est prouvée.")
    else:
        print("   WARNING : Présence significative d'états non-intriqués. Vérifiez le circuit.")


# Graphique
print("\nAffichage de l'histogramme des probabilités...")
figure = qiskit.visualization.plot_histogram(probabilities, title="Exercice 01: État de Bell (Intrication)")
ax = figure.axes[0]
ax.set_ylabel("Probabilité")
plt.show()
