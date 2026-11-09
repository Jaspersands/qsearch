# Relative norm tensor support: independent composition review

2026-11-07. Reviewed the current `RELATIVE_NORM_TENSOR_SUPPORT.md`, starting
from STATE/TRAPS. Read the actual Lenstra--Silverberg Theorems 1.10--1.11,
field Proposition 8.2 and integer endpoint proof, and Biasse--Song v2
Theorem 1, the adjustable complete-generation statement in Theorem 5,
Proposition 2, compact-output Proposition 7 and Sections 8.2/8.6. The older
rational-norm and monomial-descent notes were used only for the stated
tensor-discriminant and torsion/atom interfaces. No previous ACCEPT label
was used as a mathematical premise. No new finite experiment, backend,
network/API call or Git action was performed.

**Verdict: ACCEPT the entire stated polynomial-BIT composition under its
explicit GRH and published primitive contracts.** Both degrees may grow;
the supplied maximal-order tables, embedding and expanded target are
charged input. The tensor factors are proof objects, not supplied advice or
computed fields. The result is an exact relative-norm decision with compact
positive witness and bounded failure probability. This review establishes
neither priority nor a classical separation, and does not execute the
quantum algorithm or certify an integral/short/expanded solution.

## 1. Exact relative support, including integral weights

Let `L tensor_K L=product E_j`, with both labelled embeddings of L into each
factor. They agree on K. Consequently each paired norm ratio y_j(b) has
relative norm exactly one in K, by norm transitivity. Equality only after
the absolute norm would be insufficient, but is not what this construction
uses. Non-Galois L/K causes no problem here.

At a K-prime q outside rational S, L/K is unramified because the rational
prime is unramified in L/Q. Write the local residue degrees as f_i. For
each ordered pair i,j, the tensor of the corresponding unramified local
extensions consists of gcd(f_i,f_j) copies of degree lcm(f_i,f_j) over K_q.
A prime in such a component has the two norm pushforwards

    (f_j/gcd(f_i,f_j)) e_i,  (f_i/gcd(f_i,f_j)) e_j.

These are normalized PRIME-IDEAL valuations, with residue degrees rather
than absolute degrees. Both lie over the same q because the embeddings
agree on K. Every pair occurs among completions of the global E_j factors.

The displayed pair differences generate the full integer kernel. Indeed,
for `g=gcd f_i`, `h_i=f_i/g`, choose integers b_i with `sum b_i h_i=1`.
For any integer z with `sum h_i z_i=0`,

    z=sum_{i,j} b_i z_j (h_i e_j-h_j e_i).

Each parenthesized term is an integer multiple, up to sign, of the primitive
pair difference: the multiplier is gcd(f_i,f_j)/g. No saturation step or
division of a divisor by a nonunit integer is hidden here.

If N(x)=a and a is an S-unit of K, the divisor of x outside S is in this
kernel at every q. Lifting its finite support through the pair differences
gives fractional divisors D_j on E_j. Class generation by primes above S
provides divisors A_j supported above S such that D_j+A_j=(b_j). Norms of
A_j stay above S. Dividing x by the product of the paired norm ratios of
b_j removes all outside-S valuations and preserves the EXACT norm a.
This proves the support equality. Ordinary class groups suffice; no real
sign or narrow-class obstruction survives a correction whose norm is
identically one in K. There is no local-to-global norm-solvability inference.

## 2. Polynomial payment of support

The quotient map `L tensor_Q L -> L tensor_K L` imposes the elements
`k tensor 1-1 tensor k`. A quotient of a product of fields selects whole
factors. Thus every relative tensor factor is one of the absolute tensor
factors, including its multiplicity as a labelled factor when relevant.

The supplied integral basis gives an actual order
`A=O_L tensor_Z O_L` of discriminant `D_L^(2N)`. In the maximal product
order B, the index-discriminant identity is

    |D_L|^(2N)=[B:A]^2 product_j |D_Ej|.

Every factor discriminant therefore has logarithm at most
`2N log |D_L|`. The statement needs neither a relative integral free basis
nor an auxiliary maximal-order computation. It also avoids the possibly
exponential degree of a normal closure.

The actual GRH bound in Biasse--Song Section 8.2 is prime-ideal norm at most
`48(log|D_Ej|)^2`. The note's integer B0 dominates this bound. Every such
prime ideal lies above a rational prime at most B0. Enumerating ALL rational
primes up to B0 is polynomial numerically in the charged parameters; this
is not an exponentially large loop disguised by binary notation. The GRH
assumption is needed for the auxiliary fields even though they are never
constructed. The mathematical support theorem itself is unconditional under
its class-support hypothesis.

For the target, choose a nonzero rational integer c with ca integral in K.
At primes not dividing c or the nonzero integer `|N_K/Q(ca)|`, all valuations
of a vanish. Thus the stated denominator-and-integral-norm support works
without assuming that absolute norm detects cancellation. All integers
factored have polynomial bit length, and Shor factoring is charged.

Factoring the finite algebra `O_L/p O_L` and lifting its maximal ideals
works also at ramified rational primes. It uses the supplied maximal-order
table, not Dedekind factorization in an unchecked power basis. There are at
most N resulting primes per rational prime, with norm bit length at most
N log p. Hence every parameter of the complete S-unit call is polynomial.

## 3. Complete units, torsion and small-atom norms

The actual Biasse--Song theorem is for arbitrary growing-degree number
fields and compact S-unit generators. Theorem 5 supplies an adjustable
complete-generation event; Proposition 2 extracts a basis at the charged
precision, and Proposition 7 supplies polynomial-size exact compact atoms.
A merely independent or finite-index list cannot substitute for this event.
Use the stated finite clocks and output-size caps. Malformed or zero atoms
must be rejected before negative powers or norm-lattice solving; the exact
zero test is immediate from expanded coordinates, and LS also checks units.

The full roots of unity are genuinely required for a relative target. The
cyclotomic enumeration pays them: `phi(w)<=N` and `phi(w)^2>=w/2` give
`w<=2N^2`. For each bounded t, the explicit Q-algebra `L[T]/Phi_t` has
polynomial dimension/table size. Actual LS Theorem 1.10 gives the factor
maps. A factor of Q-dimension N has relative degree one, so its injection
of L is invertible by rational linear algebra and the image of T gives a
primitive t-th root in L. The largest successful t is exactly w. Its
expanded coordinates are polynomial size. This needs neither a supplied
torsion generator nor a torsion discrete-log oracle.

The proposed L/K basis construction is valid: adjoining a vector outside
the current K-span increases its Q-dimension by exactly m. It stops after
d vectors. Products with the supplied K-basis form an invertible N-by-N
rational coordinate matrix; determinants bound its inverse bit size.
Multiplication by any expanded atom is K-linear, and its d-by-d K determinant
is its relative norm. Determinant arithmetic over the explicit growing K
has polynomial bit cost and output coordinate size. No compact generator
is expanded in this step.

Thus the complete labelled tuple `(N(beta_l))_l,a` consists of nonzero
expanded SMALL elements of K. Compact source exponents remain integer
columns p_j. Norms of atoms that are not individually S-units must remain
in the tuple: cancellation in a compact product is allowed and not lost.

## 4. Full integral endpoint and failure accounting

Actual LS Theorem 1.11(i), with Proposition 8.2 for fields, computes the
full relation kernel of an arbitrary finite labelled tuple in the explicit
Q-algebra. Its degree and tuple length are not fixed parameters. It uses
expanded atoms, not compact huge powers. Its kernel retains roots of unity
and all integral congruences; replacing it by a saturation would be wrong.

For a basis matrix R of this kernel, the displayed equation

    sum_j z_j (p_j,0)-e_(J+1)=R h

is exactly `N(product_j u_j^z_j)=a`. Integer HNF/SNF decides it and returns
polynomial-bit exponents when feasible, since the matrix dimensions and
entry bit lengths are polynomial. Redundant generators do not affect the
equivalence. Flattening the compact source products multiplies and adds
polynomial-bit integers; it does not expand a large field element.

On the complete source event, the support theorem makes infeasibility
equivalent to nonsolvability anywhere in L*. A positive result instead has
an independent deterministic classical certificate: recompute the small
atom norms, their LS relation lattice and the displayed membership. This
does not rely on GRH, unit completeness or the output atoms actually being
S-units. The a=0 and d=1 cases are handled separately as stated.

The union bound for complete S-units and the capped factoring/finite-field
calls does not require independence of their success events. Torsion,
relative determinants, LS and integer solving are deterministic under the
stated inputs. Randomized factor routines require verified capped restarts
with logarithmic confidence overhead; clock exhaustion counts as failure,
not as a retry-until-success algorithm. The existing input promises do not
silently supply units, class groups or a norm witness.

## 5. Decisive falsifiers and scope

The strongest cheap obstructions are addressed by specific steps above:

* For residue degrees (2,3,5), the fixed star at the degree-two prime has
  even last two coordinates. The kernel vector (1,1,-1) is missed. The
  all-pairs integral argument is necessary.
* For degrees (2,4), using the unprimitive vector (4,-2) misses (2,-1).
  The gcd division in the local tensor norm calculation is necessary.
* In Q(i), `(2+i)/(2-i)` has absolute norm one but nonzero opposite
  valuations above 5. Analogous split primes can lie above any fixed small
  cutoff. The target's absolute norm alone cannot determine support.
* In Q(zeta_8)/Q(i), `N(zeta_8)=-i` whereas `N(-1)=1`.
  The rational-norm shortcut of retaining only -1 does not transfer.
* The relation kernel of the singleton i is `4Z`; saturation is Z and
  destroys exact phase equality. Real logs or saturated kernels cannot
  certify this endpoint.

None is a counterexample to the written construction. Prior classical
relative-norm algorithms and the same support reduction with classical
S-units remain the matched comparators. Biasse--Song Section 8.6 explicitly
states its norm application for Galois L/K and discusses the general
normal-closure cost; that source-scope fact is not a novelty certificate.
Primary priority comparison and the parent's finite PARI control are
separate. No control is needed to infer the quantified support proof, and
no passing control would establish the full quantum implementation.
