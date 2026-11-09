# Arbitrary signed Pauli: cancellations, exact cubic kernel and paid gap

Completed 2026-11-07; requested under the 2026-11-06 audit path.
Independent mathematical review. No quantum learner or parameter sweep
was run. Only the displayed cutoff inequality was checked by integer
arithmetic. The parent owns the complete learner and source review.

## 1. Scope and the first counterexample

Native input consists of fresh exact copies of

    C exp(-i*pi*P/8)|H>^n,

where C is an unknown Clifford and P is any signed Hermitian Pauli,
including partial or empty support. Let w be its support size and k the
number of Y factors. Signs of P are retained in interference; they do not
change the bounds below. There is no chosen-state evaluator, inverse
source, hidden support or supplied Clifford frame.

The unqualified claim that every P has the canonical cubic kernel is
FALSE. Already w=1, P=Y sends |H> to |+>; P=-Y sends it to |0>, up to
global phase. The actual Bell support has two points, while the formal
envelope has all three non-Y labels. An additional affine equation appears.
Thus local affine permutations of the envelope do NOT establish equality
of the actual Bell laws or actual supports.

What is established below is narrower and sufficient for a constructive
extension:

* For w>=25, every degree<=3 vanishing space equals that of the formal
  envelope, with uniform cubic violation probability at least 1/1024.
* For w<=24, each positive active-core Bell atom is at least 4^-24/12.
  After adjoining arbitrarily many inactive H sites, every nonzero
  quadratic support witness has probability at least 4^-24/48.

Both bounds are uniform in n, all Pauli letters, the sign of P and the
unknown Clifford. The small-weight constant is extremely conservative;
it supplies an asymptotic polynomial clock, not a practical claim.

Corpus been-tried and baselines were checked before the extension. No
exact catalog entry was returned. The relevant baseline remains the
actual Haug/Aguilar Clifford-product learner and the already reviewed
one-rotation cubic extraction, not a rare-label detector. No novelty,
classical lower bound or generic MPS learner is inferred.

## 2. Transpose-sensitive exact Bell identity

Work first before C. Let W_v be the standard Hermitian Pauli at binary
label v=(x,z), and write

    q(v)=sum_i x_i z_i,  omega(p,v)=[p,v],
    r=q(p)=k mod2,  ell(v)=r+omega(p,v).

For signed P=+/-W_p, P^T=(-1)^r P. Let U=c I-i s P, with
c=cos(pi/8), s=sin(pi/8). Direct multiplication, including this transpose,
gives

    U^T W_v U = W_v                         if ell(v)=1,
                (W_v-i W_v P)/sqrt(2)       if ell(v)=0.    (1)

Indeed the W_v coefficient is c^2-(-1)^ell s^2 and the W_v P coefficient
is -i c s(1+(-1)^ell). The formula uses ell, NOT merely commutation with
P when P has odd Y parity.

Let b(v)=2^(-n/2)<H^n|W_v|H^n>, which is real and positive on

    B={(x,z): (x_i,z_i)!=(1,1) for every i},

and zero off B. Its squared modulus is the product law mu, with local
probabilities I=1/2, X=Z=1/4, Y=0. Define the formal mixture

    rho(v)=mu(v)                              if ell(v)=1,
           (mu(v)+mu(v+p))/2                  if ell(v)=0.  (2)

Since ell(v+p)=ell(v), rho is normalized. Its support is exactly

    S_p=(B union (B+p)) intersect {q=0}.                    (3)

For v outside B but v+p in B, the identity
q(v+p)=q(v)+q(p)+omega(p,v) says that ell(v)=q(v), proving the extra
q=0 restriction in (3).

When ell=0 and both base amplitudes are nonzero, W_v P is a REAL phase
times W_(v+p) if r=0, and an IMAGINARY phase times W_(v+p) if r=1.
Consequently:

* r=0: the two amplitudes are in quadrature, so the actual law nu=rho.
* r=1: on the overlap O=B intersect (B+p), the probability can be
  (b(v)+b(v+p))^2/2 or (b(v)-b(v+p))^2/2.
* Outside O, nu=rho EXACTLY in either parity and for either sign of P.

In particular, nu has no support outside S_p. Equal destructive amplitudes
can remove points of S_p, but all such removals are confined to O.

## 3. The entire interference region has exponentially small mass in w

On O, q(v)=q(v+p)=0, hence ell(v)=0 automatically. Also O+p=O. Thus

    rho(O)=mu(O)= (1/2)^k (3/4)^(w-k) <= (3/4)^w.          (4)

The factors are exact: an active X or Z letter allows I and that letter,
of total base mass 3/4; an active Y allows X and Z, of total mass 1/2.
An inactive site contributes mass 1. This bound charges ACTIVE weight w,
not the total number of registers n.

For any event E, nonnegativity and exact equality off O give

    nu(E) >= rho(E outside O) >= rho(E)-rho(O).              (5)

No pointwise lower bound inside O, total-variation assumption, or assertion
that the overlap has no cancellation is needed for (5). It remains valid
even if every overlap outcome were deleted.

## 4. Product anti-concentration and the envelope gap

A Boolean polynomial of total degree D that is nonzero on B has

    Pr_mu[f=1] >= 4^-D.                                    (6)

One direct proof reduces modulo x_i z_i=0. The tensor-product function
basis at a site is {1,x_i,z_i}. Choose a variable from a highest-degree
nonzero monomial and difference the two local labels I and X, or I and Z.
This gives a nonzero degree-(D-1) function on the remaining sites.
Whenever that difference is 1, at least one of those two local values is
1 and has probability at least 1/4. Induct; the degree-zero case is 1.
This argument is about finite product support, not unrestricted-cube
degree or an assumed Fourier bound.

Suppose f of degree<=D is nonzero on S_p. If it is nonzero on B, (2) gives

    Pr_rho[f=1] >= 4^-D/2.

Otherwise the polynomial

    g(u)=(1+ell(u))*f(u+p)

has degree<=D+1 and is nonzero on B: any witness in S_p outside B
translates to such a u. Therefore in this case

    Pr_rho[f=1] >= Pr_mu[g=1]/2 >= 4^-(D+1)/2.

Uniformly,

    gamma_D(rho) >= 2^(-2D-3).                              (7)

This proof applies directly to arbitrary p, including its affine ell and
inactive sites. It does NOT compare product masses through an unknown
local affine permutation; such a comparison could lose a factor
exponential in w.

Combining (4), (5), (7), every degree<=3 polynomial nonzero on S_p satisfies

    Pr_nu[f=1] >= 1/512-(3/4)^w >= 1/1024,   w>=25.         (8)

The cutoff is justified without floating-point rounding:

    1024*3^25=867623536069632 < 4^25=1125899906842624.

At 24 the same crude inequality fails; this is not a counterexample to
the underlying kernel statement at 24. Since support(nu) is contained in
S_p, (8) proves BOTH directions of

    K_D(nu)=K_D(S_p),  D<=3, w>=25.                         (9)

It also gives the constant sample gap, not merely equality of kernels.
Affine Clifford Bell relabeling preserves Boolean degree and transports
the law, so (8)--(9) hold in the observed frame.

## 5. Canonical envelope geometry and the recovered physical axis

For each active site choose F_i in Sp(2,2) taking p_i to Z. Let Y=(1,1)
and define the affine map

    g_i(v)=F_i v + Y + F_i Y.

It fixes Y, hence permutes the other three labels, preserves B_i and
preserves q_i (which is exactly the indicator of Y). Moreover
g_i(v+p_i)=g_i(v)+F_i p_i. Use the identity map on inactive sites. Their
product g_0 therefore maps S_p to

    S_(Z^w) times B_(n-w).                                  (10)

These local affine maps can also be realized by one-qubit Clifford Bell
permutations, but their existence is used only for the support algebra;
the actual rotated states and product weights need not coincide.

For w>=25, the active factor has exactly the canonical K1,K2,K3 by (9).
In particular it has no affine stabilizer equation and only the universal
quadratic q on that factor. The existing quadratic product-cut procedure
can isolate this active irreducible block from the inactive H sites.
Applying the already reviewed all-w cubic Lie/Macaulay algorithm to
that block yields w+1 candidate axes, including the physical Pauli axis.

To check orientation, if the unknown external Clifford has linear action
F_C, the canonical frame is related to the observed one by linear part
F_C F_0^(-1). The canonical target is F_0 p, so its recovered candidate is
F_C F_0^(-1)F_0 p=F_C p, not an inverse-transpose label. This conclusion
uses the kernel geometry and covariance, not an unperformed canonicalizing
Clifford or an assumed invariant H state.

Do not apply the full n-qubit irreducible-block Lie formula directly when
there are inactive sites: their independent quadratic cut equations must
first be handled by the existing product decomposition.

## 6. Nonzero interference cannot be arbitrarily close to zero

Every positive base Bell probability on w active sites is a power of 2
and is at least 4^-w. Thus the ratio of unequal positive base amplitudes
has absolute value at least sqrt(2), after putting the larger first.
For a destructive pair,

    (a-b)^2/2 >= ((sqrt(2)-1)^2/2)*min(a^2,b^2)
               > min(a^2,b^2)/12.                          (11)

The last inequality is exact: 17>12 sqrt(2), since 289>288. Equal
constructive, one-amplitude, quadrature and unchanged probabilities are
larger. Therefore every NONZERO active-core probability satisfies

    nu_core(v) >= 4^-w/12.                                 (12)

Equivalently, every nonzero mixed probability is at least
(3-2sqrt(2))/3>1/18 of its formal-mixture probability. Equal destructive
amplitudes are the sole zero mechanism. These pointwise statements are
additional checks; they are not needed for the large-w deletion proof.

## 7. Small active blocks and a global quadratic gap

For w<=24 define the fixed constant

    c=4^-24/12.

The core law may have extra affine or quadratic relations, but each of its
positive atoms is at least c by (12). The unscrambled full law is exactly
nu_core times the product H law on inactive sites. Treat the entire core
as ONE finite variable; do not multiply c once per core qubit.

Claim: every degree<=2 Boolean polynomial nonzero on this product support
has violation probability at least

    gamma_small=c/4=4^-24/48.                               (13)

Proof. Expand the polynomial in the inactive tensor basis {1,x_i,z_i},
with coefficients that are functions of the core. Discard coefficients
vanishing identically on core support. If a surviving inactive degree-2
coefficient exists, total degree<=2 makes it a nonzero CONSTANT in the
core. Every core restriction is then a nonzero inactive polynomial, so
(6) gives probability>=1/16. Otherwise every core restriction has inactive
degree<=1. Some core point has a nonzero restriction; its probability is
at least c, and (6) gives conditional probability>=1/4. Since c<=1/4,
both cases imply (13). The coefficient functions on the core may be
arbitrary; no product assumption inside the core is used.

The same argument includes affine witnesses. Under an unknown Clifford,
pull back the witness: Boolean degree stays <=2, so the bound persists.
This pays exact structural affine/quadratic learning for the small-w
branch. Once the known product learner removes stabilizers and splits
irreducible blocks, every block has size at most 24, because the native
state was a w-qubit core times single-qubit H factors. Ordinary bounded-
block tomography then pays approximation. There is no need to prove the
canonical cubic kernel or recover P on this branch. Empty support is
just a global phase and is covered by the same product route.

## 8. Disposition and interfaces retained for the parent

The proposed arbitrary-P extension passes the stated cancellation and
support-gap tests with the split at w=25. The actual all-weight
same-support/same-K3 claim is explicitly rejected by the w=1 Y example.
Large-w kernels and their inverse-polynomial source clock are proved by
deleting the entire small overlap; small-w structure uses its own fixed
atom bound. Neither proof treats a tiny exact mismatch as hardness.

The full learner still has to state how its existing quadratic/stabilizer
decoder identifies the applicable block branch, cap all unpromised calls,
and compose tomography/candidate verification errors. The parent already
owns those source contracts. This review supplies no unknown-state inverse,
classical evaluator, sampled rare sector, physical implementation, or
novelty claim. Only this review file was authored in this subtask.
