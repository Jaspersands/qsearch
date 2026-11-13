# A specified quadratic-field palette misses quaternion S-unit norm lifts

2026-11-14. Independent proof/source check and one exact p=43 control.
No network, API, Git, parameter scan, or shared-status edit.
Primary: `audits/sources/integral_quaternion_selection/page.txt`, Page,
arXiv:1405.6674; locators below use physical LF from `split('\n')`.

## 1. The all-prime obstruction is valid for the stated palette

Let A=(2,3)_Q, with i^2=2, j^2=3, ij=-ji, k=ij. Its reduced norm is

    nrd(a+b i+c j+d k)=a^2-2b^2-3c^2+6d^2.

Since (i+j)^2=5, the proposed embedded fields are E_2=Q(i), E_3=Q(j),
E_5=Q(i+j). Reduced norm restricted to each E_d is its quadratic field norm.
For EVERY prime p=43 mod120, quadratic reciprocity gives

    (2/p)=-1  [p=3 mod8],
    (3/p)=-1  [p=7 mod12],
    (5/p)=-1  [p=3 mod5].

These primes divide none of 2,3,5. Thus each E_d/Q is unramified and inert
at p, and for every nonzero z in E_d,

    v_p(N_(E_d/Q)(z))=2 v_(unique prime above p)(z) is even.

This holds for fractional elements, negative valuations and arbitrary other
prime support. Central factors q in Q^* have nrd(q)=q^2, also of even
valuation. Reduced norm is multiplicative despite noncommutativity.
Consequently EVERY finite ordered product and inverse of elements from
these three fields and Q^* has even norm valuation at p, and cannot have
reduced norm p. Arbitrarily many factors or very large binary exponents do
not help. Allowing arbitrary sums is a different operation, not covered.
The progression contains infinitely many primes by Dirichlet's theorem;
the obstruction itself is proved separately for every prime in it.

## 2. The missing quaternion elements and ideals really exist

A splits at the real place since 2>0, so it satisfies Page's Eichler
condition (LF117–119). Its only finite ramified primes are 2 and 3:
(2,3)_2=(2,3)_3=-1, and all other finite local symbols are +1. Thus the
reduced discriminant is 6 and every prime under discussion splits in A.

For ANY maximal order O, Page Theorem 2.2 (LF131–140), with S={p}, states

    nrd: O[1/p]^* -> Z[1/p]^*

is surjective: there are no ramified real places imposing a sign condition.
In particular an S-unit of reduced norm exactly p exists. This is an
existence theorem; no polynomial algorithm or compact constructor is
inferred from it.

Page Theorem 2.3 (LF143–152) identifies right-ideal classes with Cl_A(Q),
which is the ordinary trivial class group because A is real-split.
An integral right O-ideal I of reduced norm (p) exists: under
O/pO=M_2(F_p), take the preimage of the right ideal of matrices whose
columns lie in one fixed line. Locally its determinant ideal is (p), and
at every other prime it is O. Theorem 2.3 makes I=alpha O principal.
Since I is integral, alpha lies in O and nrd(alpha)=+/-p. Theorem 2.2 at
S=empty supplies a unit of norm -1 if a sign correction is needed.
Hence there is even an integral generator of norm +p; its inverse is
bar(alpha)/p, so it is in O[1/p]^*. The palette obstruction is not a
nonexistence obstruction for either the required norm lift or its ideal.

## 3. Dependent characters remove this particular obstruction

Replacing E_5 by E_6=Q(sqrt(6)) changes the conclusion about simultaneous
inertness: chi_6=chi_2 chi_3 away from 2,3, so all three characters cannot
be -1. In particular E_6 is split at EVERY p=43 mod120. This is a fixed
dependent palette, not an adaptively chosen field. More generally, an
odd-cardinality product relation among quadratic characters precludes an
all-inert unramified Frobenius pattern for that palette.

E_6 embeds in the SAME A by sqrt(6)=2j+k, since (2j+k)^2=6. At p=43,

    beta=7+2j+k,                nrd(beta)=49-6=43.

Thus the replacement actually supplies the control-prime norm lift.
Choose a maximal order containing Z[1,i,j,k]; then beta is integral and
beta^-1=(7-2j-k)/43. The original palette cannot express this element
as a multiplicative word, by Section 1, although its coordinates are simple.
No global completeness, uniform S-unit basis, prescribed local action, or
clock for the alternative palette is established. Splitting at one of its
fields removes only the simultaneous-inertness valuation obstruction.

## 4. Source and control disposition

Page P1Search (LF581–603) chooses commutative suborders adaptively and proves
termination by eventual enumeration. Its runtime Proposition 4.6 explicitly
uses Heuristics 4.4–4.5 (LF823–865), including a uniform-distribution
assumption on produced unit images. Our proof does not refute that algorithm
or that local transitivity claim: it tests a fixed-palette NORM-LIFT step,
not generation of a norm-one/congruence subgroup.

`audits/controls/quaternion_palette/check.py` and `result.json` are stable.
The only control prime is 43. Sage/PARI verifies discriminant 6, local
Hilbert symbols, inert degrees (1,2) for 2,3,5, splitting for 6, the explicit
norm-43 witness, and an actual containing maximal order with basis

    1, i, (1+i+j)/2, (i+k)/2.

Beta has integral coordinates (5,-3,4,2); beta O has index 1849 and reduced
norm ideal (43). The initial invocation stopped at a Sage cached-API error
because `maximal_order(order_basis=...)` needs a tuple, not a list. Correcting
only that argument and rerunning the SAME control terminated with exit 0;
the execution note and source/script hashes are saved and verified.
No finite PASS is used to infer Section 1's all-prime statement.

Disposition: the specified {sqrt(2),sqrt(3),sqrt(5)} multiplicative palette
cannot compile all required quaternion S-unit norm lifts. This does not
rule out all finite palettes, adaptive fields, norm-one lifts, general
quaternion principalization, or constructive ternary integral isometry.
