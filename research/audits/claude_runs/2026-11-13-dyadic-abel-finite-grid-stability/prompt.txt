# New parent derivation: coordinate tubes to finite-grid stability

This is a NEW specific proof obligation after the six compiler tasks; not a
retry of any source/high-degree, native-content or whole-loop request.

Native f monic squarefree Z[x], deg2g+1, p2, D=v2disc f, growingg/B.
Existing original lattice E=2L and sigma:Z2^g->U subset E are paid by the
attached note. Need sampling h+2sigma(z), and shifted halves q+sigma(z), on
an EXACT finite integer grid, uniformly in h; NO enumeration of support
fields or all half signs. The following coordinate Haar reset is a parent
proof proposal under separate internal review, not an accepted API assumption:

Use the proof-only Abel trace cover with total field degreesg. There are
<=2^A0 charts, A0=3g+gM+2gNc, Nc=4D+12, M=2ceil(log2g)+4.
Each scaled chart has integral Abel derivative and image Haar density<=1.
Affine free coordinate scale is at most a=3D+10. Infinity chart w satisfies
w²=uF(u), u=1/x, and covers the remaining locus. Any degree-d local field
has discriminant exponent d_E<=d(1+ceil log2d). In an integral basis containing1,
the embedding matrix determinant has valuation d_E/2. Subtracting two rows
shows SOME coefficient of sigma(z)-tau(z) has valuation<=d_E/2. Plus map
has coefficient2 on1. Thus even DEPENDENT conjugate collisions are paid.

If all infinity parameters have v2(w)<=s then all x poles<=2s and y poles
<=(2g+1)s. Large positive affine x-collision implies equally deep
(y_i-y_j)(y_i+y_j) because f integral. On infinity charts, x collision implies
u collision, hence (w_i-w_j)(w_i+w_j) deep. Mixed affine/infinity x-collisions
have negative valuation. Linear one-Z2-coordinate tube bounds then show
x collision depth>2s has mass <=2^(poly(g,D)-s), even within one closed point.
Lagrange interpolation gives coefficient pole loss <=(6g-3)s on the good set.
One candidate bound is mu{beta_coord>(6g-3)s}<=2^(A-s),
A=A0+a+g(1+ceil log2g)+3+2ceil log2g. Divide by mu(U)=2^(-gR-H)
to obtain an all-coset coordinate reset independent of incoming height.
This by itself is Haar only, not constructive materialization or finite-grid.

New task: extend the good set to pay branch proximity and derive an EXPLICIT
polynomial LOCAL STABILITY DEPTH in formal logarithmic coordinates. A possible
route: also bound v2(y_i)<=s_branch via the free-y tube or monic f(x) root
sublevel bound (degree2g+1 paid); then use x_i as local coordinates. On a
2^A-sized x-perturbation, y_i=sqrt(f(x_i)) has a convergent binomial expansion
whose coefficient losses are bounded by pole/branch caps. The Abel differential
has entries Tr_E/Q2[x_i^j/(2y_i) dx_i] (basis order reversed is harmless).
Its determinant is a Vandermonde times embedding determinant divided by product
2y_i. Pair separation/poles/field discriminants give a polynomial inverse loss.
Pay ALL nonlinear Taylor bounds, integration denominators, and the actual
injective formal-group domain; nonsingular derivative alone gives NO uniform
radius. A smooth integral affine chart plus Neron mapping property may prove
formal subgroup membership without computing a model, but do not assume a
supplied Neron lattice. If this route fails, identify the exact unpaid datum.

Then try to prove: if P belongs to this good set, adding any group element
whose standard differential log lies in2^Q Z2^g, within the known injective
formal subgroup, preserves a slightly weakened good bound with Q polynomial
in g,D,s,s_branch. For Haar z and finite integer z0=z mod2^m, sigma(z)-sigma(z0)
is in2^m U, log depth>=R+m. Choose a paid m to couple the Haar-good event to
finite-grid-good event. Account for multiplication by2 on h and all halves,
and a union bound over rational2torsion without enumerating it. State EXACT
quantifiers and the weaker task achieved: this does NOT select a good RR
chart, bound Stoll Smith invariants, or implement a half. Deliver the useful
lemma/proof or native falsifier, not another overview. No tools available.
