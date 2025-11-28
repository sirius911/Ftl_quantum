import qiskit
import matplotlib.pyplot as plt
from qiskit_aer import QasmSimulator


# 2. Configuration du simulateur
simulator = QasmSimulator()

# 3. Création du circuit
# L’instruction définit un circuit quantique, nommé circuit, et déclare le nombre de bits quantiques (ici 1)
# suivi du nombre de bits classiques (ici 1 également, pour la mesure).
circuit = qiskit.QuantumCircuit(1, 1)

# 4. Application de la porte
circuit.h(0)  # Porte Hadamard

# 5. Mesure : on mesure le qubit numéro 0 et on envoie le résultat sur le bit classique numéro 0
circuit.measure(0, 0)

# 6. Affichage du circuit
print("\n[1] Visualisation du circuit à l'état initial:")
print(circuit.draw(output='text', initial_state=True, cregbundle=False))
circuit.draw(output='mpl', initial_state=True, fold=-1).show()

input("Appuyez sur Entrée pour lancer la simulation quantique...")

# 7. Exécution
shots = 500
print(f"\n[2] Exécution de {shots} tirs (shots) sur le simulateur...")
compiled_circuit = qiskit.transpile(circuit, simulator)
job = simulator.run(compiled_circuit, shots=shots)

result = job.result()
counts = result.get_counts(circuit)

# 8. Analyse des résultats pour le correcteur
print("\n[3] Résultats obtenus :")
print(f"   Nombre de 0 mesurés : {counts.get('0', 0)}")
print(f"   Nombre de 1 mesurés : {counts.get('1', 0)}")

prob_0 = (counts.get('0', 0) / shots) * 100
prob_1 = (counts.get('1', 0) / shots) * 100

print("\n[4] Conclusion :")
print(f"   Nous avons {prob_0:.1f}% de '0' et {prob_1:.1f}% de '1'.")
if 40 < prob_0 < 60:
    print("   SUCCESS : Le résultat est proche de 50/50. La superposition est prouvée.")
else:
    print("   WARNING : Écart statistique inhabituel (relancez le programme).")

# 9. Graphique
print("\nAffichage de l'histogramme...")
# Conversion des comptes bruts en probabilités (valeurs entre 0 et 1)
probabilities = {key: val / shots for key, val in counts.items()}

# 1. On récupère l'objet 'figure' renvoyé par la fonction plot_histogram
figure = qiskit.visualization.plot_histogram(probabilities, title="Superposition (Hadamard)")

# 2. On accède au premier (et unique) axe du graphique pour modifier le label Y
ax = figure.axes[0]
ax.set_ylabel("probalities")

# 3. On affiche le tout
plt.show()
