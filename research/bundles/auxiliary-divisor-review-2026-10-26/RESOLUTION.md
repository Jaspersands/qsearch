# Independent Construction Review And Corrected Cost Ledger

The separate auxiliary-construction-check-2026-10-26/REVIEW.md accepts
Sections3-5 of REVIEW.md under explicit geometric/arithmetic access. Its
source snapshot hash is preserved because REVIEW.md is not edited here.

Retain these scoped conclusions:

- For every degree-(2g+1) input class on the specified levels e>=16,
  a suitable auxiliary divisor exists. Zero same-code cube annihilator
  does not imply absence of all auxiliary-code witnesses.
- For e>=32, the two-list search is correct despite biased prime-class
  distributions, under exact independent uniform PRIME sampling. The
  second-moment guarantee is at least15/71, stronger than the stated1/5.
- Rational halving is expected polynomial under exact group order,
  uniform Jacobian sampling, bounded arithmetic and a perfect evaluable
  order-2 Tate/Frey-Ruck pairing. Its saturation argument needs no prior
  torsion basis and no high-order pairing or odd-part discrete logarithm.

Use the expanded runtime, not an interpretation hiding recurring costs:

    T_setup + O(2^(r_2/2)) *
      (T_prime(b)+T_prime(c)+r_2*T_pair+T_class+poly(r_2))
      + T_half + T_divisor_and_auxiliary_matrix + T_native_solve.

Setup includes representation construction/recovery, required order/zeta,
and certified torsion/presentation data. Every newly sampled prime still
requires mod-2 class labels and pairing evaluations. Storage includes
O(2^(r_2/2)) represented primes and their labels. Primitive costs retain
their dependence on representation size unless that size is proved
polynomial in g and log(q). Known order alone does not supply Bruin's
uniform sampler; its concrete input also includes the zeta polynomial
and truncated graded algebra. Sampling only a current subgroup is invalid.

The independent finite-group controls were also rerun by the parent:
all62 half/nondivisibility targets and24 mixed-order recombination targets
passed; biased birthday moments and exact cutoff inequalities passed.
These are controls of the abstract reduction, not Jacobian implementations.

No actual higher-level auxiliary divisor was computed. No logarithmic
rational2-rank bound, polynomial matrix-only constructor, classical
hardness or quantum advantage is established. The new matrix-geometry
note identifies a possible way to remove part of the access debt, not
an already assembled end-to-end attack.
