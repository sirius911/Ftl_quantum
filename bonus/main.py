# main.py

import sys
from pathlib import Path
import random
from qiskit import transpile
from qiskit_aer import Aer
from math import log2, ceil, gcd as pgcd
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from utils.results_utils import dessine_circuit  # noqa: E402

# Import de notre classe QPF
from shor_qpf import QuantumPeriodFinder


# --- Fonctions Classiques Utiles ---
def find_period_classical(a, M):
    """
    Calcule classiquement la période r telle que a^r mod M = 1.
    """
    if pgcd(a, M) != 1:
        return 0

    r = 1
    result = a % M
    while result != 1:
        r += 1
        result = (result * a) % M
        if r > M:
            return 0
    return r


def continued_fraction_algorithm(m_val, N_power, max_den):
    """
    Algorithme des Fractions Continues pour trouver la meilleure approximation r/s de m/2^nc.
    """
    q = m_val / N_power
    convergents = [[0, 1], [1, 0]]
    a_float = q

    for _ in range(20):
        a_i = int(a_float)

        new_r = a_i * convergents[-1][0] + convergents[-2][0]
        new_s = a_i * convergents[-1][1] + convergents[-2][1]

        if new_s > max_den:
            break

        convergents.append([new_r, new_s])

        if a_float == a_i:
            break

        a_float = 1.0 / (a_float - a_i)

    return [c[1] for c in convergents[2:]]


def run_shor_qpf(M, a, nc, nd, simulator_backend, graphics=False):
    # --- Phase Quantique (Construction et Exécution) ---
    print("\n--- PHASE QUANTIQUE (QPF) ---")

    qpf = QuantumPeriodFinder(M, a, nc, nd)
    qc = qpf.get_circuit()

    # Décomposition du circuit (pour voir les vraies portes, y compris Modular Exponentiation)
    qc_decomposed = transpile(qc, basis_gates=['u', 'cx', 'rz', 'x', 'h', 'measure', 'id'])

    print("\nCIRCUIT LISIBLE (ABSTRAIT) ---")
    print(qc.draw(output='text', fold=-1))

    print("\n - CIRCUIT DÉCOMPOSÉ (NON ABSTRAIT) ---")
    print("⚠️ ATTENTION : Le circuit décomposé contient "
          f"{qc_decomposed.size()} portes et {qc_decomposed.depth()} couches.")
    if input("Voulez-vous afficher le circuit décomposé complet ? (o/N) : ") == "o":
        print(qc_decomposed.draw(output='text', fold=50))

    if graphics:
        dessine_circuit(qc=qc,
                        title="Quantum Period Finder (QPF) - Circuit Abstrait",
                        save=None)

    # ------------------------------------------------------------------
    # MESURE m : CAS SPÉCIAL (M=15, a=2) vs CAS GÉNÉRAL (simulation)
    # ------------------------------------------------------------------
    from_quantum = False
    r_theorique = None

    if M == 15 and a == 2:
        # 🧪 Cas jouet : on exécute VRAIMENT le circuit
        from_quantum = True
        print("\n[CAS SPÉCIAL] Exécution réelle du circuit QPF pour M=15, a=2.")

        # On transpile pour le simulateur Aer
        qc_sim = transpile(qc, simulator_backend)

        shots = 2048 * 2
        job = simulator_backend.run(qc_sim, shots=shots)
        result = job.result()
        counts = result.get_counts()

        print("\nRésultats de mesure quantique (registre compteur) :")
        print(counts)

        # On prend le bitstring le plus probable
        m_binary = max(counts, key=counts.get)
        m_val = int(m_binary, 2)
        N_power = 2 ** nc
    else:
        # --- RÉSULTAT THÉORIQUE / SIMULÉ (Généralisation) ---
        r_theorique = find_period_classical(a, M)

        if r_theorique == 0:
            print("❌ La période théorique n'a pas pu être trouvée. Impossible de simuler la mesure.")
            return 0

        N_power = 2 ** nc  # 2^nc

        # Simuler le résultat de mesure m autour du pic s=1 (m/2^nc ~ 1/r)
        m_ideal = N_power / r_theorique
        simulated_m = max(1, round(m_ideal) - 1)
        m_val = simulated_m
        m_binary = format(m_val, f'0{nc}b')

    # --- PHASE CLASSIQUE (Post-Traitement) ---
    print("\n--- PHASE CLASSIQUE (Post-Traitement) ---")
    print(f"1. Résultat de la mesure quantique (m) : {m_val} (binaire : {m_binary})")

    if from_quantum:
        print("   (obtenu par exécution du circuit QPF sur le simulateur)")
    else:
        print(f"   (Basé sur une période théorique r={r_theorique})")

    # 2. Fractions Continues pour m / 2^nc
    r_candidates = continued_fraction_algorithm(m_val, N_power, max_den=M)

    print(f"2. Valeur (m / 2^nc) : {m_val}/{N_power} ≈ {m_val / N_power:.6f}")
    print(f"3. Candidats pour la période (r) par Fractions Continues (dénominateurs < {M}): {r_candidates}")

    # 4. Vérification de la période
    r_final = 0
    for r_cand in r_candidates:
        if r_cand > 0 and (a ** r_cand) % M == 1:
            r_final = r_cand
            break

    if r_final == 0:
        print("4. ❌ Échec de la vérification : Aucune période r n'a été trouvée.")
        return 0

    print(f"4. ✅ Période trouvée (r) : {r_final} (Vérif: {a}^{r_final} mod {M} = {(a**r_final) % M})")

    # 5. Calcul des Facteurs
    if r_final % 2 != 0:
        print("5. ❌ La période r est impaire. L'algorithme échoue (recommencer avec un autre 'a').")
        return r_final

    x = a ** (r_final // 2)
    p = pgcd(x - 1, M)
    q = pgcd(x + 1, M)

    print(f"5. Calcul des facteurs avec r/2 = {r_final // 2}:")
    print(f"   - x = a^(r/2) = {a}^{r_final // 2} = {x}")
    print(f"   - Facteur 1 (p) : PGCD({x - 1}, {M}) = {p}")
    print(f"   - Facteur 2 (q) : PGCD({x + 1}, {M}) = {q}")

    if p in (1, M) or q in (1, M):
        print("   ➤ ⚠️ Facteurs triviaux : la tentative ne fournit pas une factorisation non triviale.")
    else:
        print(f"   ➤ ✅ Factorisation possible : {M} = {p} * {q}")

    return r_final


# --- Exécution du programme de test ---
if __name__ == "__main__":

    # 1. Lecture de M depuis les arguments de la ligne de commande
    if len(sys.argv) < 2:
        print("Erreur : Veuillez fournir le nombre M à factoriser en argument.")
        print("Exemple d'exécution : python main.py 21")
        sys.exit(1)

    try:
        M = int(sys.argv[1])
    except ValueError:
        print("Erreur : L'argument M doit être un entier valide.")
        sys.exit(1)

    # 2. Vérification M (doit être un nombre composé)
    if M < 4:
        print("Erreur : M doit être un nombre composé (M >= 4).")
        sys.exit(1)

    # Démarrage de la boucle de Shor (répéter si échec ou facteurs triviaux)
    tentative = 0
    while True:
        tentative += 1
        print("\n==================================================")
        print(f"🔄 Tentative de Factorisation Classique/Quantique n°{tentative}")
        print("==================================================")

        # 3. CHOIX ALÉATOIRE DE 'a' et vérification PGCD (pour forcer l'étape quantique)
        print("⏳ Recherche d'une base 'a' copremière avec M...")
        a = 0
        while True:
            if M == 15:
                if input("Voulez-vous utiliser la base 'a=2' pour M=15 ? \n "
                         "Vous aurez alors un Véritable Oracle Quantique et non simulé ?(o/N) : ") == "o":
                    a = 2
                else:
                    a = random.choice([7, 8, 11, 13])
            else:
                a = random.randint(2, M - 1)

            # Vérification de l'étape 2 du Shor classique (PGCD)
            g = pgcd(a, M)

            if g == 1:
                print(f"✅ Base 'a' trouvée : {a}. PGCD({a}, {M}) = 1.")
                break  # On passe à l'étape quantique
            elif g != 1 and g != M:
                # Facteurs triviaux trouvés (ex: a=9, M=21 -> PGCD=3). On sort immédiatement
                f1 = g
                f2 = M // g
                print(f"❌ Facteur trivial trouvé par PGCD: M={M} = {f1} * {f2}. Algorithme terminé prématurément.")
                sys.exit(0)  # Sortie pour ne pas lancer la partie quantique

        # 4. Calcul des tailles de registres
        nd = ceil(log2(M))
        nc = 2 * nd

        print("-" * 50)
        print(f"🔢 Nombre à factoriser (M) : {M}")
        print(f"🎲 Base choisie (a) : {a}")
        print(f"⚙️ Tailles : n_d={nd}, n_c={nc} (Total={nc + nd} qubits)")
        print("-" * 50)

        simulator = Aer.get_backend('aer_simulator')

        print("⏳ Démarrage de la Recherche de Période Quantique (QPF)...")

        try:
            # run_shor_qpf retourne la période r (ou 0 en cas d'échec total)
            r = run_shor_qpf(M, a, nc, nd, simulator)

            if r > 0:
                print(f"\n🎉 ALGORITHME DE SHOR TERMINÉ (Tentative {tentative})")

                # Vérifier si la factorisation a réussi
                # La fonction run_shor_qpf affiche les facteurs,

                # Pour confirmer la réussite sans changer run_shor_qpf :
                # On teste si a^(r/2) mod M est -1 (M-1)
                x = a**(r // 2)
                if r % 2 == 0 and x % M != M - 1:
                    # Si r est pair ET x mod M n'est pas M-1, on a réussi à factoriser.
                    # On affiche le succès final
                    f1 = pgcd(x - 1, M)
                    f2 = pgcd(x + 1, M)
                    if f1 != 1 and f2 != 1 and f1 != M and f2 != M:
                        print(f"\n\n\n⭐ ⭐ ⭐ SUCCÈS COMPLET après {tentative} tentative(s) ! ⭐ ⭐ ⭐")
                        print(f"Facteurs : {M} = {f1} * {f2}")
                        sys.exit(0)

            # Si r est 0 ou si les facteurs étaient triviaux, la boucle continue
            print("⚠️ Échec de la factorisation ou résultats triviaux. Relance de l'algorithme avec un nouveau 'a'.")

        except Exception as e:
            print(f"Erreur lors de l'exécution du QPF : {e}")
            print("Relance de l'algorithme avec un nouveau 'a'.")
