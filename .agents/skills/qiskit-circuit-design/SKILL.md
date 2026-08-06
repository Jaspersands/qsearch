---
name: qiskit-circuit-design
description: Workflows and patterns for Qiskit 1.x quantum circuit construction, Aer simulation, transpilation, and statevector analysis.
---

# Qiskit 1.x Development Guide

This skill provides reference patterns and best practices for Qiskit 1.0+, `qiskit-aer`, statevector manipulation, and unitary matrix extraction.

---

## 1. Circuit Construction & Gate Operations

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import numpy as np

# Create register-based circuits
qr = QuantumRegister(3, 'q')
cr = ClassicalRegister(3, 'c')
qc = QuantumCircuit(qr, cr)

# Standard gate operations
qc.h(qr[0])
qc.cx(qr[0], qr[1])
qc.rz(np.pi / 4, qr[2])
qc.cz(qr[1], qr[2])

# Custom controlled gates & parameters
from qiskit.circuit import Parameter
theta = Parameter('θ')
qc.rx(theta, 0)
```

---

## 2. Unitary Matrix & Statevector Extraction

In Qiskit 1.0+, use `qiskit.quantum_info` for statevector and unitary matrix calculations:

```python
from qiskit.quantum_info import Statevector, Operator

# Extract unitary matrix of circuit (without measurements)
qc_no_meas = QuantumCircuit(2)
qc_no_meas.h(0)
qc_no_meas.cx(0, 1)

unitary_op = Operator(qc_no_meas)
unitary_matrix = unitary_op.data  # 4x4 numpy array

# Calculate statevector directly
state = Statevector.from_instruction(qc_no_meas)
print("Fidelity:", state.fidelity(Statevector.from_label('00')))
```

---

## 3. Aer Simulation (Qiskit-Aer 0.14+)

```python
from qiskit_aer import AerSimulator
from qiskit import transpile

sim = AerSimulator()

# Prepare circuit with measurements
qc_meas = qc_no_meas.copy()
qc_meas.measure_all()

# Transpile for Aer backend
compiled_circuit = transpile(qc_meas, sim)

# Execute job
result = sim.run(compiled_circuit, shots=1024).result()
counts = result.get_counts()
print("Counts:", counts)
```

---

## 4. Transpilation & Optimization

```python
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# Level 3 optimization for minimal gate count
pm = generate_preset_pass_manager(optimization_level=3, basis_gates=['u1', 'u2', 'u3', 'cx'])
optimized_qc = pm.run(qc_no_meas)
print("Depth:", optimized_qc.depth())
print("Gate count:", optimized_qc.count_ops())
```

---

## 5. Matrix Distance & Verification

```python
def matrix_fidelity(U: np.ndarray, V: np.ndarray) -> float:
    """Calculates normalized trace distance / fidelity between two unitary matrices."""
    dim = U.shape[0]
    trace_val = np.abs(np.trace(np.dot(U.conj().T, V)))
    return (trace_val / dim) ** 2

def is_unitary(M: np.ndarray, tol: float = 1e-9) -> bool:
    """Checks if M * M^dagger == I."""
    identity = np.eye(M.shape[0], dtype=complex)
    return np.allclose(np.dot(M, M.conj().T), identity, atol=tol)
```
