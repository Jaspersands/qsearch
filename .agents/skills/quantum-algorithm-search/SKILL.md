---
name: quantum-algorithm-search
description: Specialized workflows for quantum circuit synthesis (QSearch), Dihedral Hidden Subgroup Problem (DCP), coset analysis, character theory, and quantum error correcting codes.
---

# Quantum Algorithm Search Workflows

This skill provides references and architectural guidelines for `qsearch.py`, `coset_state_workbench.py`, character shift analysis, and algebraic code search tools in this repository.

---

## 1. QSearch & Unitary Synthesis

`qsearch.py` implements numerical and evolutionary quantum circuit synthesis (decomposing arbitrary target unitaries into parameterized target gate sequences).

### Core Synthesis Flow
- **Target Unitary $U$:** $2^n \times 2^n$ target matrix in $SU(2^n)$.
- **Cost Function:** Hilbert-Schmidt distance or trace distance:
  $$f(\theta) = 1 - \frac{1}{d} \left| \text{Tr}(U^\dagger U_{\text{circuit}}(\theta)) \right|$$
- **Solvers:** Multi-start L-BFGS-B, SPSA, or Levenberg-Marquardt optimizer for parameter fitting.

### Verification Pattern
```python
import numpy as np

def verify_synthesis(target_u: np.ndarray, approx_u: np.ndarray, tol: float = 1e-6) -> bool:
    """Verifies synthesis fidelity between target matrix and reconstructed circuit matrix."""
    dim = target_u.shape[0]
    overlap = np.abs(np.trace(target_u.conj().T @ approx_u)) / dim
    print(f"Synthesis Overlap: {overlap:.8f}")
    return float(overlap) >= (1.0 - tol)
```

---

## 2. Dihedral Hidden Subgroup Problem (DCP) & Coset States

DCP analysis (`dcp_*.py`) involves states of the form:
$$|\psi_k\rangle = \frac{1}{\sqrt{2}} (|0\rangle + e^{2\pi i k s / N} |1\rangle)$$

### Key Components
- **Pretty Good Measurement (PGM):** Gram matrix block-encodings for optimal state distinguishability.
- **Marker / Vulnerable Coordinate Decoders:** Filtering carrier registers to isolate phase bits.
- **Subset Sum & Two-Adic Reductions:** LLL basis reduction & CVP solvers for extracting the hidden shift $s$.

---

## 3. Quantum & Classical Error Correcting Codes

Modules `goppa_code_search.py`, `bch_code_search.py`, `tanner_code_search.py`, and `cfi_*.py`:
- **Parity Check Matrix $H$:** Matrix over $\mathbb{F}_q$ defining $\mathcal{C} = \{x : H x^T = 0\}$.
- **Syndrome Decoding:** Computing $s = H r^T$ and solving low-weight error patterns.
- **Code Invariants:** Syzygy modules, Schur filtration, automorphism groups, and weight enumerators.

---

## 4. SymPy & Character Theory

- **Character Tables:** Group representation character evaluation for symmetric groups $S_n$ and wreath products.
- **Jucys-Murphy Elements:** $\sum_{i < j} (i, j)$ spectral decompositions for coset state spaces.
