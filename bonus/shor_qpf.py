# shor_qpf.py

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Operator
import numpy as np

# NOTE: Les imports d'arithmétique avancée (ModularExponentiation, ModularMultiplication)
# sont omis car ils causent des erreurs d'environnement dans la version actuelle de Qiskit.
# L'Oracle est traité comme une ABSTRACTION (boîte noire) pour ne pas bloquer l'avancement.


class QuantumPeriodFinder:
    """
    Construit le circuit quantique pour la Recherche de Période (QPF) de Shor.
    """
    def __init__(self, M, a, nc, nd):
        self.M = M
        self.a = a
        self.nc = nc
        self.nd = nd
        # na est mis à 0, car nous n'utilisons pas le composant complet nécessitant un auxiliaire
        self.na = 0

        # 1. Définition des registres
        self.qr_compteur = QuantumRegister(nc, name='compteur')
        self.qr_donnees = QuantumRegister(nd, name='donnees')
        self.cr_mesure = ClassicalRegister(nc, name='mesure')

        # Le circuit final
        self.qc = QuantumCircuit(self.qr_compteur, self.qr_donnees, self.cr_mesure)

        # 2. Construction du circuit
        self._build_initialization()
        self._build_modular_exponentiation()  # L'implémentation est une abstraction
        self._build_iqft()
        self._build_measurement()

    def _build_initialization(self):
        """
        Étape 1 : Superposition du Registre de Compteur et initialisation du Registre de Données à |1>.
        """
        # Superposition sur le Registre de Compteur
        self.qc.h(self.qr_compteur)

        # Initialisation du Registre de Données à |1>
        self.qc.x(self.qr_donnees[0])
        self.qc.barrier()

    def _build_modular_exponentiation(self):
        """
        Étape 2 : Oracle d'Exponentiation Modulaire Contrôlée (U_f).

        - Cas général : abstraction (bloc vide avec un joli label).
        - Cas spécial : M=15, nd=4, a dans {2,7,8,13} -> on utilise Oracle15.
        """
        # Cas spécial : M = 15, nd = 4 -> on peut utiliser un vrai oracle
        if self.M == 15 and self.nd == 4 and self.a in (2, 7, 8, 13):
            print("\n[Oracle15] Utilisation de l'oracle concret pour M=15.")
            oracle = Oracle15(self.M, self.a, self.nc, self.nd)
            oracle.apply(self.qc, self.qr_compteur, self.qr_donnees)
        else:
            # Cas général : oracle abstrait (boîte noire)
            op_label = f"U_{self.a}^{{x}} mod {self.M} (ORACLE ABSTRAIT)"
            oracle_placeholder = QuantumCircuit(
                self.nc + self.nd,
                name=op_label
            ).to_instruction()

            # Application du bloc sur les registres (Compteur et Données)
            self.qc.append(oracle_placeholder,
                           list(self.qr_compteur) + list(self.qr_donnees))

        self.qc.barrier()

    def _build_iqft(self):
        """
        Étape 3 : Transformée de Fourier Quantique Inverse (IQFT) sur le Registre de Compteur.
        """
        self.qc.barrier()
        # Création de l'opérateur QFT inverse
        iqft_op = QFT(self.nc).inverse().to_instruction()
        iqft_op.label = "IQFT"

        # Application sur le Registre de Compteur
        self.qc.append(iqft_op, self.qr_compteur)
        self.qc.barrier()

    def _build_measurement(self):
        """
        Étape 4 : Mesure du Registre de Compteur dans le Registre Classique.
        """
        # Mesure les qubits du registre de compteur (qr_compteur) dans le registre classique (cr_mesure)
        self.qc.measure(self.qr_compteur, self.cr_mesure)

    def get_circuit(self):
        """Retourne le circuit quantique complet."""
        return self.qc


class Oracle15:
    """
    Oracle concret pour M=15, basé sur la multiplication mod 15.
    On agit sur le registre de données (4 qubits) avec :
        |y> -> |k * y mod 15>
    et on contrôle cette opération par les qubits du registre compteur.
    """

    def __init__(self, M, a, nc, nd):
        if M != 15:
            raise ValueError("Oracle15 ne supporte que M = 15.")
        if nd != 4:
            raise ValueError("Oracle15 suppose nd = 4 (registre de données sur 4 qubits).")
        self.M = M
        self.a = a
        self.nc = nc
        self.nd = nd

    def _mul_const_mod15_operator(self, k):
        """
        Construit l'opérateur unitaire U_k sur 4 qubits qui réalise :
            |y> -> |k * y mod 15>
        pour y < 15, et laisse l'état |15> invariant.
        """
        dim = 2 ** self.nd  # 16
        U = np.zeros((dim, dim), dtype=complex)

        for basis in range(dim):
            if basis < self.M:
                target = (basis * k) % self.M
            else:
                # on laisse |15> inchangé pour garder une permutation bijective
                target = basis
            U[target, basis] = 1.0

        return Operator(U)

    def apply(self, qc: QuantumCircuit, qr_compteur, qr_donnees):
        """
        Applique l'oracle complet sur (qr_compteur, qr_donnees) dans le circuit qc.
        Pour chaque bit j du compteur, on applique une multiplication contrôlée :
            a^(2^j) mod 15
        """
        for j in range(self.nc):
            exp = 2 ** j
            k = pow(self.a, exp, self.M)   # k = a^(2^j) mod 15

            op = self._mul_const_mod15_operator(k)
            gate = op.to_instruction()
            gate.name = f"{self.a}^{exp} mod {self.M}"

            # Contrôle sur le qubit de compteur j
            controlled_gate = gate.control(1)

            # Ordre : [qubit_compteur_j, tous les qubits de données]
            qc.append(controlled_gate, [qr_compteur[j]] + list(qr_donnees))
