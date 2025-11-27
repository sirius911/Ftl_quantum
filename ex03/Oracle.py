from qiskit import QuantumCircuit

# --- PARAMÈTRE DE L'EXERCICE ---
MAX_TOTAL_QUBITS = 4
MAX_DATA_QUBITS = MAX_TOTAL_QUBITS - 1  # n maximum = 3


class Base_Oracle:
    """
    Classe de base garantissant la bonne interface pour l'Oracle.
    TOUS les oracles du correcteur hériteront de cette classe.
    """
    def __init__(self, n_qubits, name="BaseOracle"):
        """
        Initialise l'Oracle.
        :param n_qubits: Nombre de qubits de données.
        """
        if n_qubits < 1 or n_qubits > MAX_DATA_QUBITS:
            raise ValueError(f"Le nombre de qubits doit être entre 1 et {MAX_DATA_QUBITS}.")

        self.n_qubits = n_qubits
        self.name = name
        self.total_qubits = n_qubits + 1
        self.data_qubits = list(range(n_qubits))
        self.qubit_auxiliaire = n_qubits
        self._oracle_circuit = self._build_oracle()  # Doit être implémenté par la sous-classe

    def _build_oracle(self):
        return QuantumCircuit(self.total_qubits, name=self.name)

    def append_to_circuit(self, main_circuit):
        """
        Méthode publique utilisée par l'algorithme DJ pour insérer l'Oracle.
        """
        if main_circuit.num_qubits != self.total_qubits:
            raise ValueError(f"Circuit principal a {main_circuit.num_qubits} qubits, attendu {self.total_qubits}.")

        # Compose l'Oracle avec le circuit principal
        # main_circuit.compose(self._oracle_circuit, inplace=True)
        main_circuit.barrier()
        main_circuit.append(self._oracle_circuit.to_gate(), self.data_qubits + [self.qubit_auxiliaire])
        main_circuit.barrier()
        return main_circuit

    def get_circuit(self):
        return self._oracle_circuit
    
    def dessine(self):
        figure = self._oracle_circuit.draw(output='mpl', fold=-1)
        figure.suptitle(f"Oracle: {self.name}", fontsize=12)

    def __str__(self):
        return f"Oracle '{self.name}'.\n{self._oracle_circuit.draw(output='text')}"


# ----------------------------------------------------------------------
# EXEMPLE D'ORACLE CONSTANT (f(x) = 1) - Simule l'un des oracles du sujet
# ----------------------------------------------------------------------
class ConstantOracle1(Base_Oracle):
    def __init__(self):
        super().__init__(3, name="f(x) = 1 (constant): Inverse le qubit auxiliaire")

    def _build_oracle(self):
        qc = super()._build_oracle()
        # f(x) = 1 (constant): Inverse le qubit auxiliaire
        qc.x(self.qubit_auxiliaire)
        return qc


# ----------------------------------------------------------------------
# EXEMPLE D'ORACLE BALANCÉ (cf. sujet)
# ----------------------------------------------------------------------
class BalancedOracleX0(Base_Oracle):
    def __init__(self):
        super().__init__(3, name="f(x) = x_0 (balancé): CNOT du q0 vers l'ancilla")

    def _build_oracle(self):
        qc = super()._build_oracle()
        qc.x(0)
        qc.x(1)
        qc.x(2)
        qc.cx(0, self.qubit_auxiliaire)
        qc.cx(1, self.qubit_auxiliaire)
        qc.cx(2, self.qubit_auxiliaire)
        return qc


# ----------------------------------------------------------------------
# ORACLE POUR TESTER L'INTERFAGE
# Pour l'évaluation, le correcteur importera l'Oracle qu'il souhaite tester.
# Par exemple, il écrira : from Oracle_Secret_Test import MySecretOracle
# ----------------------------------------------------------------------
class Simple_Oracle(Base_Oracle):
    """
    Cas spécifique où n=1 qubit. f(x) = NOT(x).
    """
    def __init__(self):
        super().__init__(1, name="f(x) = NOT(x) pour n=1")

    def _build_oracle(self):
        qc = super()._build_oracle()

        # 1. On inverse le qubit de données (x -> NOT(x))
        qc.x(0)

        # 2. On applique le CNOT de NOT(x) vers le qubit auxiliaire (y XOR NOT(x))
        qc.cx(control_qubit=0, target_qubit=self.qubit_auxiliaire)

        # 3. On remet le qubit de données dans son état initial (NOT(x) -> x)
        qc.x(0)

        return qc
