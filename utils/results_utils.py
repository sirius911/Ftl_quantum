# results_utils.py
from collections import OrderedDict
from typing import Dict, Iterable, List, Optional
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit


def _trier_labels_binaires(labels: Iterable[str]) -> List[str]:
    """
    Trie les bitstrings en ordre binaire :

    0, 1, 00, 01, 10, 11, 000, 001, ...
    """
    def key_fn(lbl: str):
        # Si c'est bien une chaîne de bits, on la trie par longueur puis valeur binaire
        if all(ch in "01" for ch in lbl):
            return (len(lbl), int(lbl, 2))
        # fallback au cas où ce ne serait pas un bitstring pur
        return (len(lbl), lbl)

    return sorted(labels, key=key_fn)


def afficher_resultats(
    counts: Dict[str, int],
    backend_name: Optional[str] = None,
    titre: str = "Résultats de mesure",
    afficher_graphique: bool = True,
):
    """
    Affiche un résumé texte + un histogramme matplotlib des résultats de mesure.

    - counts : dict des comptages bruts
        ex: {'0': 512, '1': 480} ou {'10': 78, '00': 495, '11': 375, '01': 76}
    - backend_name : nom du backend (optionnel, pour l'affichage)
    - titre : titre du graphique
    - afficher_graphique : si False, ne trace pas le graphique (utile pour des scripts non interactifs)

    Retourne un dict de probabilités (valeurs entre 0 et 1) dans l'ordre trié.
    """
    if not counts:
        print("⚠ Aucun résultat à afficher (dict counts vide).")
        return {}

    shots = sum(counts.values())
    labels_triees = _trier_labels_binaires(counts.keys())

    print("\n--- RÉSULTATS DE MESURE ---")
    if backend_name:
        print(f"Backend : {backend_name}")
    print(f"Nombre total de tirs : {shots}\n")

    for lbl in labels_triees:
        c = counts[lbl]
        p = c / shots * 100
        print(f"  {lbl} : {c:4d}  ({p:5.1f} %)")

    # Probabilités (0–1) dans l'ordre trié
    probabilities = OrderedDict(
        (lbl, counts[lbl] / shots) for lbl in labels_triees
    )

    if afficher_graphique:
        # Histogramme avec matplotlib
        fig, ax = plt.subplots()

        x_positions = range(len(labels_triees))
        values = list(probabilities.values())

        ax.bar(x_positions, values)
        ax.set_xticks(list(x_positions))
        ax.set_xticklabels(labels_triees)

        ax.set_ylim(0, 1.0)
        ax.set_ylabel("Probabilité")
        ax.set_title(titre)

        # Affiche les valeurs en % au-dessus de chaque barre
        for x, v in zip(x_positions, values):
            texte = f"{v*100:.1f}%"

            if v >= 0.999:  # ~ 100%
                # texte au milieu de la barre
                ax.text(
                    x,
                    v / 2,          # milieu de la barre
                    texte,
                    ha="center",
                    va="center",
                    color="white",   # optionnel: lisible sur fond bleu
                    fontweight="bold",
                )
            else:
                # cas normal : un peu au-dessus de la barre
                ax.text(
                    x,
                    v + 0.01,
                    texte,
                    ha="center",
                    va="bottom",
                )

        plt.tight_layout()
        plt.show()

    return probabilities


def dessine_circuit(qc: QuantumCircuit, title: str, save: str = None):
    """
    Affiche le circuit quantique et le sauvegarde si un nom de fichier est fourni.

    :param qc: Le circuit Qiskit à dessiner.
    :param name: Le nom de l'Oracle pour le titre.
    :param save: Le nom du fichier pour la sauvegarde (ex: 'dj_circuit.png'). 
                 Si None, seule l'affichage est effectué.
    """
    try:

        # 1. Générer la figure Matplotlib
        figure = qc.draw(output='mpl', initial_state=True, fold=-1)
        figure.suptitle(title, fontsize=14)
        plt.show()

        # 2. Sauvegarder la figure si 'save' est spécifié
        if save is not None:
            # Utilisez bbox_inches='tight' pour éviter que le titre ou les étiquettes ne soient coupés
            figure.savefig(save, bbox_inches='tight')
            print(f"✅ Circuit sauvegardé sous : {save}")

    except ImportError:
        # Fallback si Matplotlib n'est pas installé
        print("Matplotlib non installé. Affichage textuel du circuit :")
        print(qc.draw(output='text', fold=-1))

    except Exception as e:
        # Gérer les autres erreurs (ex: chemin invalide pour la sauvegarde)
        print(f"❌ Erreur lors de l'affichage/sauvegarde du circuit : {e}")