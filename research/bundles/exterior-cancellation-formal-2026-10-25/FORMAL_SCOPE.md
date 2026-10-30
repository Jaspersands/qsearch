# Exterior Compression: Formal Algebraic Scope

2026-10-25. This bundle formalizes the coordinate-compression argument
behind the preceding classical public-label cancellation implementation.
It does not formalize the whole SDE solver, the Python program, or an
end-to-end quantum algorithm. The new argument has not received a new
independent human or reasoning-agent review.

## Why This Check

The previous arithmetic bundle replaced a full tensor dependence problem
with fewer exterior coordinates. Its finite tests cannot establish that
projection never loses an equation. This is an all-dimension algebraic
obligation with direct consequences for the claimed public sample bank.
Checking it is useful; adding more scalar seeds would not settle it.

The collision framework comes from Ivanyos and Santha,
[On solving systems of diagonal polynomial equations over finite fields](https://arxiv.org/abs/1503.09016).
The present exterior adaptation is a local derivation, not a certified
novel algorithm or a best-known complexity claim. Kernel verification
does not establish novelty.

This pass also inspected the native source and full HDQI output-sampling
gaps. Existing modular-norm controls do not acquire the required carries;
existing flux and marginal estimators do not give the full output law.
No justified new end-to-end construction emerged from that triage. The
formal check below is a limited reduction of proof risk, not resolution
of those much more important research gaps.

## Concrete Mathematical Objects

Let F be any field and E an F-vector space. The implementation's d-dimensional
basis space is represented as E x F, with dim(E)=d-1. Let l:E->F be linear
and z nonzero. Define

    lambda(x,t) = l(x) + z*t
    pi(x,t) = x
    i(x) = (x, -z^-1*l(x)).

`contraction` is mathlib's actual left contraction on the exterior algebra,
realized as the Clifford algebra of the zero quadratic form. It is not
an abstract operation with the required identities assumed as axioms.
`closedDegree lambda j` is the actual kernel of this contraction restricted
to the actual j-th exterior power.

For the arithmetic code, l has coefficients zeta_0,...,zeta_(d-2) and
z=zeta_(d-1), all nonzero power-class representatives. Exterior projection
pi retains exactly the basis cells omitting the last coordinate. The
identification with the Python sparse-coordinate representation is
explained here but is NOT a machine-checked equivalence of programs.

## Checked Deductions

1. Contraction squares to zero.
2. For P(v)=v-lambda(v)*e, exterior(P)(T)=T-e wedge D(T).
   This identity does not require lambda(e)=1. That extra condition is
   required for its image to be closed.
3. For closed T, exterior(i)(exterior(pi)(T))=T. Hence projection is
   injective on the closed subspace; a projected linear relation between
   closed children is also a relation in the full exterior algebra.
4. The degree-j closed subspace is linearly equivalent to exterior^j E.
   Its dimension is choose(dim E,j). For r equation rows the dimension is
   r*choose(dim E,j), including zero rows and degrees above dim E.
5. More than that many closed row vectors have a nontrivial common scalar
   dependence. The theorem treats an indexed family, not a set with
   duplicate children silently removed.
6. Every closed homogeneous vector in degree j>dim E is zero.
7. Right-wedge contraction obeys

       D(T wedge v) = D(T) wedge v + lambda(v)*involute(T).

   The actual grading involution handles signs; homogeneity is not needed
   for this identity. Consequently, if D(T_a)=0 and
   sum_a a_a*lambda(v_a)*T_a=0, then
   D(sum_a a_a*T_a wedge v_a)=0. Substituting a_a=rho_a^d and
   lambda(v_a)=zeta_(t_a) gives the update used in the previous derivation.

The proof works over arbitrary fields, including characteristic two. It
does not divide by a degree or a factorial. The SDE application still
has its original odd-prime and power-class assumptions; this stronger
linear-algebra fact does not remove those arithmetic requirements.

## Formal Assumption Falsifiers

Two existential counterexamples are also proved over any field, not
tested at a few primes. Both use T=the embedded vector (0,1) in F x F:

- If lambda=0, then T is nonzero and closed, but pi(T)=0. The nonzero
  dropped-coordinate coefficient cannot be omitted.
- If lambda(x,t)=t, then T is nonzero, pi(T)=0 and D(T) is nonzero.
  Injectivity cannot be extended to arbitrary, nonclosed children.

These counterexamples are already included in the full declaration audit.

## What Remains Outside Lean

- The entire recursive leaf data structure, preservation of a positive
  distinguished ORIGINAL leaf, and disjointness through accumulation.
- The representation of those signed leaves by the algebraic vectors,
  and the recursive degree invariant that supplies the top-degree input.
- Gaussian-elimination code, power-class selection, root extraction,
  sign absorption, scalar Fermat rows, and original-degree lifting.
- The complete bank recurrence, runtime, sampling failure probabilities,
  random-source assumptions, and bit-level reversible resource accounting.
- Python refinement/equivalence, the previous receipt's numerical claims,
  the complete Rees receiver, and any native application or quantum advantage.

In particular, an algebraic vector can be zero while its original support
is nonempty. Neither a nontrivial dependence coefficient nor the proved
top-degree zero establishes a nonzero SDE witness by itself. The separate
support induction is still essential. The finite arithmetic checks test
that invariant but do not formally prove its universal preservation.

The degree-d collision bank B_d(r)=product_j(r*choose(d-1,j)+1) remains
a written recurrence using the now-checked dimension lemma. Growing d
is still expensive. This pass supplies no improved asymptotic bank and
does not remove the native-source/reduction obstruction.

## Reproducibility And Trust Boundary

`verify.py` compiles the source afresh into this bundle's `.build`, then
uses `Audit.lean` to inspect all 21 theorems and eight definitions/abbreviations.
Only propext, Classical.choice and Quot.sound are allowed. Every warning,
missing or duplicate declaration, unexpected diagnostic, or other axiom
fails verification. The source disables implicit undeclared variables.

The pinned runtime is Lean 4.35.0 and mathlib commit
56a005855ea17e0b0958f73ec801ae140b0a1679. It reuses the existing local
mathlib cache from rees-formal-core-2026-10-24; it does not rebuild or
independently authenticate the compiler and all transitive cached imports.
This has the usual Lean compiler/kernel and installed-library trust boundary.
The row-dimension/dependence elaboration options change unification only;
they do not introduce axioms or turn off kernel checking.

The deterministic receipt binds six source/document files, the runtime
configuration, the previous arithmetic receipt, and its original five
source hashes. The verifier checks those frozen arithmetic bytes but does
not rerun the arithmetic replay itself. The separate replay command does.
The verification log records exactly which tests and commands were run.

No main repository, registry, CLI, UI, Git, staging copy or migration state
is modified by this isolated bundle. Main-repository validation was not run.
