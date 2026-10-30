# Handoff: Bounded Filtered HDQI Parent

Read FILTERED_PARENT.md before using any receipt. This is a constructive
access repair and a sharply stated gap target, NOT a quantum algorithm
discovery or a verified speedup. Its machinery adapts Leng--Jiang--Lin's
known KMS/DLL parent factorization. No novelty certification is made.

## What Is Now Explicit

On m coefficient qubits, filtered Pauli constraints have the unique pilot
kernel. Their LCU normalization is exp(1/8), so the parent normalization is
at most m exp(1/4). Construction uses known Pauli strings, graph CZ gates,
scalar probability/phase preparation and REAL-time Hamiltonian simulation.
No unknown-state or imaginary-time inverse oracle is assumed.

The note proves analytic quadrature and path-derivative bounds. Conditional
on an inverse-polynomial gap along the entire beta path, standard adiabatic
preparation starts at the known vacuum; no external warm start is granted.

## Highest-Reasoning Next Task

Prove or refute a uniform global gap for beta^2(d+1)<=kappa_0. The +1
guards isolated vertices: the Gaussian-filter parent has an exact
one-qubit gap exp[-(beta J)^2] cosh(beta J), which closes at large beta
even though that commuting target is an easy product state.

The previous raw/flat star obstructions cannot simply be transferred to
this DIFFERENT parent. Test rare sectors and high excitation modes, not
only the low-order single-excitation band. A pairwise sector gap is not the
full-system gap. Consider a global Dirichlet-form comparison, retaining
all operator weights and the true inner product. Do not assume thermal
correlation decay implies a uniform spectral gap.

A successful gap theorem must then be connected to a useful physical
HDQI target/decoder or operational output. Classical partition functions
are already tractable in the small-kappa regime. That is not a quantum
advantage target. The existing predecessor-uniform classical baseline
still applies to its family.

## Routine Work For Gemini

Only after the Desktop migration finishes and the destination is verified:

- Integrate this directory together with its dependency bundle
  hdqi-parent-gap-2026-10-23; the new module imports its canonical graph model.
- Preserve both sources' hashes and explicit no-speedup/no-execution flags.
- Expose controls only if useful; do not add a generic workbench or promote
  positive finite gaps into a proof status or accepted speedup candidate.
- A future circuit implementation should follow the explicit real-time
  LCU, not the dense eigensolver used as the reference here. Charge scalar
  loader, phase arithmetic, controlled Hamiltonian simulation, ancillas,
  quadrature and adiabatic errors separately.
- Do not execute enormous conservative resource grids by default. The
  resource ledger is not an experiment launch instruction.

## Reproduction

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
      PYTHONPYCACHEPREFIX=/tmp/qsearch-hdqi-filter-pycache \
      PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python \
      -m pytest -q -p no:cacheprovider -W error test_filtered_parent.py \
      ../hdqi-parent-gap-2026-10-23/test_parent_gap.py

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
      PYTHONPYCACHEPREFIX=/tmp/qsearch-hdqi-filter-pycache \
      /opt/anaconda3/bin/python filtered_parent.py --output receipt.json

The combined suite has 87 tests. The exact two-frequency low-temperature
control is intentional: ordinary floating-point diagonalization can leak
spurious zero-frequency components and swamp an extremely small true gap.
The 1e-11 diagnostic floor is not a rigorous eigenvalue error enclosure.

No new independent reviewer was used. The earlier authorized Rees review
does not cover this construction. Do not mark these local proofs reviewed.
