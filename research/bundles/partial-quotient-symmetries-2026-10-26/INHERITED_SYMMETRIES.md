# Partial Quotients Already Have Eight Useless Symmetries

2026-10-26. New deduction for the actual interpolation construction,
conditional only on the native quotient interface already assumed there.
Exact matrix controls are not geometric execution or independent review.

## Scientific Question

The preceding leakage pass leaves partial CRT quotient automorphisms as
a possible classical attack on the SAME prime-degree IsERP input. Before
running that experiment, which automorphisms are guaranteed by construction
and therefore cannot be counted as evidence of a useful escape?

Answer: EVERY partial quotient has a faithful inherited quaternion group
of order eight. All its pulled-back corners are already known. Neither
nontrivial automorphisms nor an automorphism count of eight is progress.
Even additional automorphisms need not escape: the terminal quotient has
a much larger group and the previous closure theorem still applies.

## 1. Universal Copy Symmetries

Use X=E0^4 x E^4, Phi=phi I4 and the paper's four-square matrix A4. Define
the integer orthogonal matrices

    Iq = [[0,-1,0,0], [1,0,0,0], [0,0,0,-1], [0,0,1,0]],
    Jq = [[0,0,-1,0], [0,0,0,1], [1,0,0,0], [0,-1,0,0]].

They square to -I4, anticommute, and commute with A4 for EVERY integer
four-square witness (a,b,c,d). Thus

    Q8 = {+I4,-I4,+Iq,-Iq,+Jq,-Jq,+(Iq Jq),-(Iq Jq)}

acts by polarized product automorphisms U_B=diag(B,B) on X. These are
ordinary signed permutations of copies, with no unknown elliptic maps,
target-order basis, rational denominator or field extension.

This is exactly the group of integer orthogonal matrices commuting with
ALL four-square matrices at once. The regular quaternion action is cyclic
on the first standard basis vector. A commuting matrix is determined by
its first column; an integral unit column has exactly one entry +/-1.
The eight displayed matrices realize all possibilities. The centralizer
of ONE special four-square witness can be larger; that distinction matters.

## 2. Descent To Every Partial Quotient

For every divisor D of the auxiliary M, the D-primary graph kernel is

    K_D = {(A4^T P, Phi P) : P in E0^4[D]}.

For B in Q8, direct commutation gives

    U_B (A4^T P, Phi P) = (A4^T B P, Phi B P).

So U_B preserves K_D as a subgroup scheme. If v_D:X->Y_D is the actual
D-polarized quotient, there is a unique automorphism b_B of Y_D with

    b_B v_D = v_D U_B.

It is polarized: pulling b_B^dagger b_B back through v_D gives D I,
and cancellation in Hom^0 gives b_B^dagger b_B=I. It is defined over the
same base field as v_D, since the entire equality is. The descent is
faithful: if b_B=1 then v_D(U_B-I)=0, and an isogeny has no nonzero
homomorphism from the connected X into its finite kernel. Thus B=I.

This holds even when D is even. The actions of +I and -I coincide on
2-torsion, but the descended automorphisms of the variety remain different.
Counting their actions only on the quotient kernel would be a false merge.

## 3. Every Guaranteed Symmetry Is Uninformative

The same extraction as in the leakage report gives

    L_B = v_D^dagger b_B v_D = D U_B.

Its source/target cross-corners vanish, and its target corners are 0 or
the scalar +/-D. Therefore neither of the two native escape gates can
fire. All sums, products and adjoints of these pulled-back maps remain in
the known category. Since D is prime to q, no auxiliary scalar cancellation
can reveal a hidden q-denominator.

More generally, EVERY polarized automorphism U of X preserving K_D
descends with this same formula. U is monomial within the two elliptic
isomorphism types and has only already-known units in its corners. The
entire inherited stabilizer, not just Q8, is uninformative after adjoining
cheap target units. A useful partial symmetry must fail to lift to such
an integral polarized product automorphism. That is NECESSARY, not sufficient.

If a verified COMPLETE automorphism list for Y_D has exactly eight
elements, Q8 exhausts it and this particular automorphism-harvest attempt
fails. An incomplete search returning eight elements proves no such thing.
If the list has more than eight, apply the actual native escape gates; do
not count the surplus as progress. At D=M the product endpoint already
supplies a counterexample to that optimistic rule.

## 4. Recognition Without Dividing By A Large D

Do not ask for pointwise inverse evaluation of v_D or divide an arbitrary
endomorphism by D merely to recognize inherited b. Compare the two known
native maps L=v_D^dagger b v_D and D U instead.

Each elliptic corner of L has degree at most D^2 because L^dagger L=D^2 I.
The same bound holds for D U. A difference corner has degree at most
4D^2 by the degree-norm triangle inequality. Equality on full elliptic
T-torsion with gcd(T,p)=1 and T>2D therefore forces equality: a nonzero
map killing E[T] has degree at least T^2. Test the bounded list of corners
on small-prime CRT torsion. The product T may be large but every selected
prime and point-field computation must have the previously charged
polynomial bit bounds. Do NOT enumerate all T-torsion.

This comparison works in the native evaluator model and does not access
the unknown target order. It is a proposed workflow, not executed here.
The local test helper only compares supplied matrices and must not be
reported as a native automorphism recognizer.

## 5. Revised Experiment And Stop Rules

1. Remove cheaply solvable inputs first. For the prime-degree family this
   includes special-j units and any genuinely available target map with
   reduced discriminant not divisible by q^2: it cannot be in R because
   theta^-1(R)=Z+q O0. As a further example, if a supersingular target
   admits an efficiently computed F_p model, its transported p-Frobenius
   has discriminant -4p and triggers the one-map selector for odd q!=p.
   Pay for the model isomorphism. Generic j in F_(p^2)\F_p does not supply
   this endomorphism, and scalar p^2-Frobenius is useless.
2. Retain the exact native graph kernel and each actual quotient map.
   Enumerate COMPLETE geometric automorphism groups with the published
   represented-PPAV interface, not random Tate matrices.
3. Identify the inherited stabilizer and report useful maps, not group
   cardinality. Apply the source-coordinate target/cross escape tests to
   all remaining candidates. Record every cost and degree.
4. A certified escape invokes the classical recovery from the preceding
   report. Eight inherited automorphisms or extra non-escaping ones give
   a failed specific attack, not a hardness certificate or quantum signal.
5. A hitting theorem must concern genuinely escaping symmetries under an
   explicit samplable native input/query distribution. The construction's
   guaranteed Q8 supplies no lower bound on that probability.

There is still no constructed native escape or useful-symmetry probability
bound. A full source backend is enormous in this fixed-dimensional model;
do not silently replace it by local split-coordinate experiments. This
pass rules out a misleading progress metric rather than demonstrating a
new classical or quantum algorithm.

## Sources And Boundaries

The interpolation matrices and quotient contract are taken from
Corte-Real Santos, Piasecki and Wesolowski,
[Theorem 7.1 / Algorithm 6](https://eprint.iacr.org/2026/1142), retained
44-page PDF, pp.36-39. The inherited-Q8 deduction and the experiment
decision above are our derivations, not claims quoted from that paper.
The preceding leakage report gives the native escape/selection arguments.
No novelty claim is made for quaternion regular-representation identities.

The new code verifies universal commutation, the graph intertwining
identity, group cardinality, and failure of the native-pattern escape
gates in supplied local coordinates. It also tests special witnesses with
larger centralizers and terminal extra automorphisms which still do not
escape. It never constructs Y_D or its geometric automorphism list.
