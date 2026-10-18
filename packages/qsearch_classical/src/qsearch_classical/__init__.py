"""Classical solvers from the Q-Search research loop, packaged for reuse.

The modules are generated from theorems/ by packages/qsearch_classical/sync.py and keep
their original names. Groups:

- prime character OPI (instance construction and attacks): prime_character_opi,
  prime_character_norm_attack, prime_character_morse_attack, prime_character_exterior_bound,
  prime_character_capacity_source, prime_character_finite_readout;
- polar Gibbs source: polar_conditional_sampler, polar_source_design;
- Jacobi sums: jacobi_surface_reconstruction, jacobi_known_norm_reduction.

Reports are read and written under $QSEARCH_CLASSICAL_ROOT (default: the current
directory), at research/classical_baselines/<module>.json.
"""

__version__ = "0.1.0"

PRIME_CHARACTER = (
    "prime_character_opi",
    "prime_character_norm_attack",
    "prime_character_morse_attack",
    "prime_character_exterior_bound",
    "prime_character_capacity_source",
    "prime_character_finite_readout",
)
POLAR = ("polar_conditional_sampler", "polar_source_design")
JACOBI = ("jacobi_surface_reconstruction", "jacobi_known_norm_reduction")
