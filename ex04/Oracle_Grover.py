from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
import numpy as np


class Base_Grover_Oracle:
    """
    Classe de base pour l'Oracle de Grover (U_omega).
    Agit uniquement sur les n qubits de données (pas de qbit auxiliaire).
    """
    def __init__(self, n_qubits: int, name="BaseGroverOracle"):
        """
        Initialise l'Oracle.
        :param n_qubits: Le nombre total de qubits (Y dans l'énoncé, minimum 2).
        """
        if n_qubits < 2:
            raise ValueError("L'algorithme de Grover nécessite au moins 2 qubits.")

        self.n_qubits = n_qubits
        self.name = name
        # Tous les qubits sont des qubits de données pour Grover
        self.all_qubits = list(range(n_qubits))
        self._oracle_circuit = self._build_oracle()

    def _build_oracle(self):
        """Méthode abstraite pour construire le circuit U_omega."""
        # Dans Grover, il n'y a pas de qubit auxiliaire, donc le circuit n'a que n_qubits
        simple_name = f"U_omega_n{self.n_qubits}"
        return QuantumCircuit(self.n_qubits, name=simple_name)

    def append_to_circuit(self, main_circuit):
        """
        Ajoute l'Oracle au circuit principal.
        """
        if main_circuit.num_qubits != self.n_qubits:
            raise ValueError(f"Circuit principal a {main_circuit.num_qubits} qubits, attendu {self.n_qubits}.")

        # On utilise .to_gate() pour encapsuler l'Oracle
        main_circuit.barrier(label=f"Oracle {self.name}")
        main_circuit.append(self._oracle_circuit.to_gate(), self.all_qubits)
        main_circuit.barrier()
        return main_circuit

    # Méthodes utilitaires (à ajouter à la classe)
    def get_circuit(self):
        return self._oracle_circuit

    def dessine(self):
        figure = self._oracle_circuit.draw(output='mpl', fold=-1)
        figure.suptitle(f"Oracle de Grover: {self.name}", fontsize=12)
        plt.show()

    def __str__(self):
        return f"Oracle de Grover '{self.name}' sur {self.n_qubits} qubits."

    def draw(self):
        return self._oracle_circuit.draw(output='text', initial_state=True, cregbundle=False)

# ----------------------------------------------------------------------
# EXEMPLE D'ORACLE GROVER : Marque l'état |11...1>
# ----------------------------------------------------------------------


class OracleGrover11(Base_Grover_Oracle):
    def __init__(self, n_qubits):
        solution_str = '1' * n_qubits
        super().__init__(n_qubits, name=f"Solution |{solution_str}>")

    def _build_oracle(self):
        qc = super()._build_oracle()

        # L'Oracle U_omega pour |11...1> est le Multi-Controlled Z (MCZ)

        if self.n_qubits == 2:
            qc.cz(0, 1)  # CZ est le MCZ pour n=2
        elif self.n_qubits > 2:
            # Construction du MCZ (Multi-Controlled Z) sans qubit auxiliaire :
            # 1. H sur le dernier qubit (la "cible" virtuelle pour le Z)
            target_qubit = self.n_qubits - 1
            control_qubits = self.all_qubits[:-1]

            qc.h(target_qubit)
            # 2. MCX (Toffoli généralisé)
            qc.mcx(control_qubits, target_qubit)
            # 3. H sur le dernier qubit
            qc.h(target_qubit)

        return qc


# ----------------------------------------------------------------------
# ORACLE GROVER DYNAMIQUE (Marque un nombre décimal donné)
# ----------------------------------------------------------------------

class OracleGroverSpecific(Base_Grover_Oracle):

    def __init__(self, target_decimal: int):

        if target_decimal < 0:
            raise ValueError("La cible doit être un nombre positif (index >= 0).")

        # 1. CALCUL DYNAMIQUE de n_qubits
        # N = ceil(log2(target_decimal + 1))
        if target_decimal == 0:
            # Pour le cas 0, log2(1)=0, mais nous devons respecter la contrainte N >= 2
            n_qubits = 2
        else:
            # Calcul du nombre minimal de qubits requis
            n_qubits = int(np.ceil(np.log2(target_decimal + 1)))
            # Assurer N >= 2
            n_qubits = max(n_qubits, 2)

        # 2. Conversion en binaire sur le bon nombre de bits
        binary_target = format(target_decimal, f'0{n_qubits}b')
        self.binary_target = binary_target

        super().__init__(n_qubits, name=f"Solution |{binary_target}> (Dec {target_decimal})")

    def _build_oracle(self):
        qc = super()._build_oracle()

        x_qubits = []
        # ... (Le corps de la méthode _build_oracle reste le même, utilisant self.n_qubits) ...
        # (La logique du MCZ fonctionne quelle que soit la taille n_qubits)

        # 1. Appliquer X sur les qubits qui doivent être à '0'
        for i in range(self.n_qubits):
            if self.binary_target[-1 - i] == '0':
                qc.x(i)
                x_qubits.append(i)

        # 2. Appliquer le Multi-Controlled Z (MCZ)
        target_qubit = self.n_qubits - 1
        control_qubits = self.all_qubits[:-1]

        # MCZ = H * MCX * H
        qc.h(target_qubit)
        # Utilisation de mcx qui gère n qubits de contrôle
        qc.mcx(control_qubits, target_qubit)
        qc.h(target_qubit)

        # 3. Annuler les X (Correction de l'erreur précédente pour la liste vide)
        if x_qubits:
            qc.x(x_qubits)

        return qc
