# Ambient Section Potential: Universal Degree Origin

2026-10-21. Status: written input-degree proof with a kernel-checked
filtration lemma and independently checked universal BCH coefficients.
Not a complete HSP algorithm, a new BCH theorem, or a speedup admission.

## 1. The Scientific Question

The full-jet candidate targets an explicit finite-dimensional nilpotent
Lie algebra L over F_p, fixed class c, with N=[L,L] of class at most three.
Input access is an ordinary coherent hiding function on exp(L), not an
evaluator for a hidden polynomial. Initially H intersects exp(N) trivially;
intersection learning and arbitrary-H recursion are separate steps.

The compiler proof requires potential degrees D,D,c with D=c-2. The
public frontend computes the full center of N, but checking that center
on basis vectors does not prove that the actual section potential has
those degrees. This pass supplies the missing mathematical argument and
tests the exact source word. No candidate or benchmark campaign is added.

The hoped-for end result remains quantum polynomial time in dim(L) and
log(p) for each fixed c in the stated scope. This pass only establishes
an input-origin premise. It provides no new classical-hardness evidence.
The explicit-object stabilizer baselines in CLASS_THREE_APPLICATION_AUDIT.md
remain applicable, and a useful hard application is still missing.

## 2. Exact Word And Filtration Proof

Use the single proof-only linear projection pi onto the image of H and
its linear lift a into N. The public section s is linear in Lie coordinates.
Set

```
X(q)=s(q-pi(q)), Y(q)=s(pi(q)), Z(q)=a(pi(q)),
g(q)=exp(X(q)) exp(Y(q)+Z(q)) exp(-X(q)-Y(q)).
```

This is exactly the common section word already used by CosetMatrixSource.
X,Y,Z are linear in q; Z lies in N. They are witnesses in the proof, not
operational inputs to the quantum receiver.

For class c and p>c, the truncated BCH/Lazard logarithm Q=log(g) is a
rational linear combination of Lie words of lengths at most c. All
denominators are products of integers at most c and are invertible in F_p.
Its linear part is Z, since X+(Y+Z)-X-Y=Z. Every other word is a bracket,
so Q lies in N. Substituting linear inputs into a length-k word gives a
homogeneous quotient polynomial of degree k. Each of its coefficients is
a sum of length-k brackets and hence belongs to gamma_k(L).

Now suppose k>=c-1. A right-nested word of length k is in gamma_(c-1)(L).
For x in that space and u,v in L, both [u,[v,x]] and [v,[u,x]] belong to
gamma_(c+1)(L)=0. Jacobi therefore gives [[u,v],x]=0. By linearity,
x commutes with every member of N=[L,L]. For c>=3 these high words also
belong to N. Thus they lie in the ACTUAL center C=Z(N).

Every A or B coordinate in the direct decomposition N=A+B+C vanishes on
C, so its degrees c-1 and c vanish identically. Consequently

```
deg Q_A <= c-2,  deg Q_B <= c-2,  deg Q_C <= c.
```

This proves the origin of the assumptions used by ClassThreePhaseBounds.
No value of Q, pi or a is queried, learned, interpolated or given as advice.
Choosing an arbitrary smaller central subspace is not sufficient.

## 3. What Is Actually Checked

`formal/Formal/AmbientPotentialFiltration.lean` proves nested-word
membership in the actual Mathlib lower central series, high-degree
centrality against the span of all brackets, and the projected and
unprojected scalar-polynomial bounds. It uses the LieRing/LieAlgebra
axioms and a supplied nilpotency bound. Mathlib index zero is gamma_1.
Five headline axiom guards are included in the default build.

`theorems/ambient_section_potential.py` computes
`log(exp(X) exp(Y+Z) exp(-X-Y))` over the truncated free associative
algebra over Q. It proposes a right-nested Lie expansion using the
Dynkin-Specht-Wever projection, then independently expands every bracket
as AB-BA and verifies EVERY associative word coefficient. The verifier
also compares the claimed associative target with the actual exp/log
calculation, rejecting mutually consistent but unrelated certificates.
The linear part is checked to be exactly Z.

These are universal coefficient identities, not finite-field truth-table
fits. Live generation succeeded for c=4,5,6,7; tests also cover c=1,2,3.
The nonzero coefficient counts at each final homogeneous degree are:

| Class cap c | Associative words at degree c | Right-nested terms at degree c |
|---|---:|---:|
| 4 | 58 | 40 |
| 5 | 176 | 116 |
| 6 | 490 | 326 |
| 7 | 1465 | 963 |

Certificate construction grows exponentially with c, independently of p
and input dimension. Expanding linear quotient inputs is polynomial in
their dimension only for FIXED c. This is not an improvement to the huge
two-erasure resource bound and not a growing-class/DCP algorithm.

The Python coefficient checker and the abstract BCH/Lazard-to-group
identification are NOT formalized in Lean. The Lean result handles the
resulting Lie-word polynomial shape, rather than assuming its final
projected degree. A full Python refinement and one composed source-to-
output theorem remain absent. The ambient input must be a genuine Lie
algebra: PublicLieAlgebra's arbitrary callable alone does not certify
bilinearity or Jacobi. The matrix fixtures satisfy those axioms independently.

## 4. Decisive Falsifiers

The 17 tests in `tests/test_ambient_section_potential.py` include exact
matrix exponential/logarithm comparisons in UT5 through UT8, including a
127-bit prime. Known-witness fixtures are explicitly separated from the
public certificate generator. Every coefficient of the UT7 section
example is checked against its lower-central filtration space and the
frontend's adapted N=A+B+C basis. Degrees D=4 and c=6 are both attained.

For a concrete smaller-center failure, take in ut_7

```
X=q0*(E23+E34+E45+E56+E67), Y=q1*E12, Z=0.
```

This is a legitimate slice of the transverse source for H=exp(<E12>).
The coefficient of q0^4*q1 in Q is E16/30. It lies in Z(N), but not
Z(L). Using C=Z(L) leaves this degree-five term outside C and violates
the proposed noncentral bound D=4. The degree-four coefficient is itself
noncentral in N, so D cannot simply be reduced. Replacing q0 by q0^2
makes it degree seven: linear sections/projections are necessary.

A separate UT8 negative control uses a perfectly valid class-six
universal certificate on a class-seven input and misses a nonzero E18
term. The coefficient certificate does not certify the input class.
Altered, duplicated and unrelated coefficient certificates, invalid primes
and p<=c are rejected. No finite example is promoted to an algorithm.

## 5. Prior Art And Remaining Work

BCH/Lazard and the [Dynkin-Specht-Wever lemma](https://arxiv.org/html/2407.20718v1)
are established mathematics, not discoveries here. The
[Lazard correspondence](https://arxiv.org/abs/1405.4654) is an explicit
dependency for passing from the Lie polynomial to the group word.

The current targeted literature check does not establish novelty. The
[constant-class, constant-prime result](https://arxiv.org/abs/2304.08376)
does not itself provide the requested uniform large-prime bound.
[Morales's stated families](https://arxiv.org/html/2608.05321v2) also do
not directly subsume the nonmetabelian exponent-p controls here: an
abelian-by-cyclic group is metabelian, while a quasi-Hamiltonian group of
exponent p is abelian. For the latter observation, any two cyclic order-p
subgroups have a subgroup product of order at most p^2 and thus commute.
These distinctions are not a comprehensive prior-art or novelty certificate.

Next prioritize composition of the existing ordinary-oracle, central/B
Fourier, GL and erasure stages, probabilistic rank, adaptive freshness and
complete resource/error accounting. Executable general-prime SDE and a
useful external application remain open. Do not repeat local polynomial
degree fixtures or describe these lemmas as a Shor-level algorithm.
