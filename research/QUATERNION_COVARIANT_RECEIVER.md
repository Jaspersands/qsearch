# Quaternion Receiver: Covariant Gaussian Source

Date: 2026-10-30. Status: reviewed source and receiver-interface derivations;
bounded regression controls. Reviews are automated, not human peer review.
No quantum receiver or speedup is implemented. This continues
QUATERNION_COMPACT_ORBIT_SOURCE.md using its explicit norm-exact input,
right-coset convention, reconstruction radius, and classical baselines.

## Question And Candidate Mechanism

Given the public normalized ideal lattice L_I=O*a on a YES input, can a
measurement recover H*a, H=O^1, with polynomial copies, gates, and
classical work? The proposed mechanism is coherent nonabelian orbit
estimation on a finely resolved lattice state, not ordinary position
sampling. Covariant-POVM existence, pointwise likelihood, or a dense
measurement matrix does not establish the required algorithm.

The original straddle source has useful quantitative separation but is
not exactly covariant under rotations. The Gaussian variant below removes
that representational mismatch. Its finite-bit approximation must retain
coherence and charge every precision and normalization step. Gaussian
lattice states are established machinery, not claimed original here; see
[EHKS, Section 5 and introduction](https://www.cse.psu.edu/~sjh26/units-stoc.pdf).

## 1. An Exactly Covariant Continuous Source

Use N=4d and a lattice L in R^N. Let

```text
w_s(x)=exp(-pi*||x||^2/s^2),
Z_L=sum_(x in L) w_s(x)^2,
phi_nu(u)=nu^(-N/2)*exp(-pi*||u||^2/(2nu^2)),
A_L(u)=Z_L^(-1/2)*sum_(x in L) w_s(x)*phi_nu(u-x),
Psi_L=A_L/||A_L||.
```

The packet is L2-normalized. Its overlap is
`<phi_nu(. -x),phi_nu(. -y)>=exp(-pi*||x-y||^2/(4nu^2))`.
Thus Z_L is NOT the exact normalizer of the overlapping-packet sum.
With rho_t(L)=sum_x exp(-pi*||x||^2/t^2), Cauchy--Schwarz gives

```text
1 <= ||A_L||^2 <= rho_(2nu)(L).
```

For U(g)f(u)=f(u*g), with blockwise quaternion multiplication, U is a
homomorphic unitary representation and
`Psi_(L*g)=U(g^-1)Psi_L`. The packets are radial, so this is exact in
continuous L2, unlike a fixed-grid identity. In particular
`Psi_(L_I*g)=Psi_(O*a*g)` on YES inputs. Since the Fourier transform of
phi_nu never vanishes, equality of two such normalized Gaussian sums
implies equality of their weighted discrete lattice measures. The mass
at the origin fixes the proportionality constant. Their supports agree,
so the exact stabilizer of the O source remains H, not a larger continuous
group. Positivity also rules out an extra nontrivial global phase.

## 2. Finite-Bit Approximation Without A Hidden Normalizer

The following bounds explain how a clean finite-grid preparation can
approximate this covariant source. They do not claim an infinite-dimensional
physical operation or arbitrary-accuracy preparation at fixed old widths.
Choose s,nu and the grid spacing h for the requested error budget.

Use a public lower bound lambda_0 for the shortest vector of BOTH supplied
lattices, for example the minimum reciprocal inverse-basis spectral norm.
This remains valid on NO instances. For any lattice with this minimum,
disjoint-ball counting gives

```text
rho_(sqrt(8)*nu)(L)-1
 <= sum_(j>=1) (2j+3)^N*exp(-pi*j^2*lambda_0^2/(8nu^2)) <= eta
```

whenever `pi*lambda_0^2/(8nu^2)>=N*log(5)+log(2/eta)`, 0<eta<=1.
Here `(2j+3)<=5^(j^2)` and a geometric majorant bound the final sum.
Only logarithms of these scales enter register lengths. In particular
rho_(2nu)(L)-1<=eta as well.

Choose T>=1 so
`p=N*erfc(sqrt(pi)*T)` is below the allocated squared-error budget.
For a packet center m, first compute a dyadic approximation m_tilde with
`||m_tilde-m||<=e<=h`. Retain FULL grid cells in each coordinate indexed by

```text
k=floor(m_tilde_i/h)-M,...,floor(m_tilde_i/h)+M,
M=ceil(T*nu/h)+1,       0<h<=nu.
```

Their union includes [m_i-T*nu,m_i+T*nu] and lies within distance
T*nu+4h of the TRUE m_i. Let chi_m be phi_nu(. -m) restricted to this box,
and let p_m be its excluded squared mass. Then 0<=p_m<=p. Require

```text
(T*nu+4h)*sqrt(N)*max(||M_O^-1||,||M_I^-1||) <= 1/8.
```

This both separates the retained boxes of distinct lattice points and
allows coherent inverse-basis rounding from every occupied grid cell.
All packet boxes are unions of full cells. Avoid partial terminal cells:
an arbitrarily short partial cell would invalidate the simple relative-
precision bound used next.

Prepare the normalized packet chi_m/sqrt(1-p_m) by its cell probability
integrals. Its Cartesian factors are ordinary one-dimensional Gaussian
integrals. Each retained full cell has unnormalized mass at least
`(h/nu)*exp(-pi*(T+4)^2)`; each conditional root has mass close to one.
All nonempty prefix denominators therefore have polynomially bounded
logarithmic inverse. Reversible prefix-conditioned rotations require
polynomial time in log(nu/h), T^2, input bits and requested precision,
not enumeration of the grid. The normalizer p_m can depend on m; it is
computed and uncomputed, not presumed constant or left as workspace.

This dyadic choice repairs a numerical issue found by independent review:
polynomial-time precision access alone does not give the exact floor of
an arbitrary real m_i/h, and a sharply truncated packet is discontinuous
when its window changes. The actual circuit integrates the Gaussian
centered at m_tilde. Compare it to the TRUE-center Gaussian restricted
to the SAME selected window. Their normalized L2 distance is at most
`sqrt(2pi/(1-p))*e/nu`. Distinct windows are disjoint, so this error does
not accumulate with the number of lattice points. No straddle Lipschitz
claim is applied to the sharp cutoff. For D sequential rotations and
minimum nonempty prefix mass q_star, integral absolute precision of order
`q_star*epsilon_int^2/D^2` suffices; its bit cost is polynomial.

Use the already reviewed broad coherent Klein construction for the
coefficient weights. Map each coefficient to its translated packet,
uncompute point-generation workspace, then erase coefficients by the
inverse-basis rounding above. Distinct retained boxes give an isometry
from coefficient labels to the physical cell labels, so coefficient
preparation error is not amplified by the number of lattice points.

### Why Packet Tails Do Not Multiply By The Number Of Points

Writing c_x=w_s(x)/sqrt(Z_L), the omitted tail functions
t_x=phi_nu(. -x)-chi_x are nonnegative. Their diagonal Gram entries are
at most p, and off-diagonal entries are at most the full Gaussian overlap.
The off-diagonal row sum is at most eta. The Schur/Young bound gives

```text
||sum_x c_x*t_x|| <= sqrt(p+eta).
```

The separately normalized retained packets have disjoint support. Their
normalization changes the sum by at most p in L2. Normalizing A_L changes
it by at most eta/2. Consequently the unit-norm retained source F_L obeys

```text
||F_L-Psi_L|| <= sqrt(p+eta)+p+eta/2.
```

This bound is uniform under rotations and basis changes. A triangle
bound involving sum_x |c_x| would be unacceptable and is not used.

### Why Digitization Does Not Require Differentiating A Sharp Cutoff

Define Q_h f as the step function whose value in a cell C is
`h^(-N/2)*||f||_(L2(C))`. For nonnegative functions Q_h preserves norm
and is nonexpansive in L2. It is a mathematical comparison map, not a
claimed linear quantum operation. Disjoint retained boxes make the actual
prepared cell state exactly the step encoding of F_L.

For smooth nonnegative f, the cube Poincare inequality gives
`||Q_h f-f|| <= sqrt(2)*h*||grad f||/pi`.
The uncut source is smooth. Its Gaussian derivative Gram kernel is

```text
<grad phi_x,grad phi_y>
 = (pi*N/(2nu^2)-pi^2*||x-y||^2/(4nu^4))
   *exp(-pi*||x-y||^2/(4nu^2)).
```

Using `u*exp(-u)<=2/e*exp(-u/2)`, the previous theta bound gives

```text
||grad Psi_L||^2 <= pi*(N/2+1)*(1+eta)/nu^2.
```

Compare Q_h F_L first to Q_h Psi_L by nonexpansiveness, then compare
Q_h Psi_L to Psi_L by this gradient bound. This proves total ideal
approximation error at most

```text
sqrt(p+eta)+p+eta/2
 + (sqrt(2)*h/pi)*sqrt(pi*(N/2+1)*(1+eta))/nu
 + sqrt(2pi/(1-p))*e/nu.
```

Taking p,eta=O(epsilon^2) and h/nu=O(epsilon/sqrt(N)) suffices, with
separate budgets for coefficient, embedding, Gaussian-integration and
rotation errors. No H1 claim is made for the sharply truncated packets.
Every finite query label must specify a reversibly computable rotation;
arbitrary analogue queries are not part of the input model. Uniform
vector-norm error with a consistent phase convention is required for
coherent superpositions of query labels.

## 3. Separation And Reconstruction Are Retained

Choose nu further so the retained packet diameter
`delta=2*(T*nu+4h)*sqrt(N)` satisfies the arithmetic separation conditions
in QUATERNION_COMPACT_ORBIT_SOURCE.md. The proper-subgroup proof uses
nonnegative normalized disjoint packets and their support radius, not
the special trigonometric form. It therefore applies to F_L. The ideal
Gaussian overlap differs by at most twice the approximation bound.
Choose that bound below the margin to 3/4, or reduce the old tail budget.
The exact inverse-basis reconstruction radius is unchanged.

This supplies a covariant analytical model with a controlled finite
encoding. It does not supply an efficient covariant measurement, Fourier
transform over SU(2)^d, or a circuit implementing a dense square-root POVM.

## 4. Cartesian Fourier Readout Has A Classical Simulator

This is a scoped falsifier for the continuous position/momentum laws,
not a general dequantization of the coherent source or an automatically
verified finite-QFT implementation. Let Lambda=L^*, use the Fourier
convention exp(-2pi*i*k.x), and normalize the ACTUAL overlapping source.
Poisson summation gives the exact momentum density

```text
p_F(k) proportional to exp(-4pi*nu^2*||k||^2)
              *(sum_(y in Lambda) exp(-pi*s^2*||k-y||^2))^2.
```

Keep all the cross terms. Put A=s^2+2nu^2 and c=s^2/A. Completing the
square shows that the Fourier amplitude is another Gaussian comb on
c*Lambda, with packet and coefficient widths

```text
nu_prime^2=1/(2A),      s_prime^2=s^2/(2nu^2*A).
```

Dropping only the off-diagonal INTENSITY terms defines the normalized law

```text
Y drawn from D_(Lambda,r),      r=sqrt(A)/(2nu*s),
K=c*Y+G,                      G normal(0,I/(4pi*A)).
```

Denote this law Q_F. Its lattice width is approximately 1/(2nu), while
the added noise scale is 1/s. Neither operation requests narrow dual
lattice samples. In particular c is not silently replaced by 1.

### Exact Interference Bound

Expand an ordered cross pair y,y+u and complete around their midpoint.
The integrated cross intensity divided by diagonal intensity is exactly

```text
R_F=sum_(u in Lambda, u!=0) exp(-pi*s^2*||u||^2/2)
                     *rho_r(Lambda+u/2)/rho_r(Lambda).
```

Poisson summation gives rho_r(Lambda+t)<=rho_r(Lambda). Hence
`R_F<=E_s=rho_(sqrt(2)/s)(Lambda)-1`. All cross intensities are
nonnegative, so p_F is a mixture of Q_F and a normalized cross-term law:

```text
TV(p_F,Q_F) <= R_F/(1+R_F) <= E_s/(1+E_s).
```

This bounds the retained interference rather than asserting it is zero.
The same argument in position space gives distance at most
`Gamma_nu/(1+Gamma_nu)`, where Gamma_nu=rho_(2nu)(L)-1, from the law
`X+Z`, with X drawn from D_(L,s/sqrt(2)) and independent
Z normal(0,nu^2*I/(2pi)). Fine lattice peaks have not been replaced by
one featureless continuous Gaussian.

### Public-Basis Cost

For a supplied basis M, let b be its maximum Gram--Schmidt length. Let
b_dual be the maximum Gram--Schmidt length of the explicitly computed
dual basis M^(-T). Define theta(t)=sum_j exp(-pi*t^2*j^2). Successive
shifted theta sums are bounded by centered sums. Applying this to the
REVERSED dual basis, whose Gram--Schmidt lengths are the reversed
reciprocals of the primal lengths, gives

```text
E_s <= theta(s/(sqrt(2)*b))^N-1,
Gamma_nu <= theta(1/(2nu*b_dual))^N-1.
```

Sampling D_(Lambda,r) is ordinary broad public-basis Gaussian sampling,
as in [Gentry--Peikert--Vaikuntanathan, Section 4](https://www.cs.toronto.edu/~vinodv/GentryPeikertV-STOC2008.pdf).
No short hidden frame is supplied. For t=r/b_dual, put
`xi=2*sum_(j>=1) exp(-pi*t^2*j^2)`. A conservative sequential-sampler
TV bound is `((1+xi)/(1-xi))^N-1` when xi<1, plus errors of its
one-dimensional conditional samplers. The latter have finite-bit
Gaussian-integration/rejection implementations; charge their accuracy.

For 0<epsilon<=1, sufficient bounds for these errors are

```text
H=sqrt(log(32N/epsilon)/pi),
s/(sqrt(2)*b)>=H,       1/(2nu*b_dual)>=H.
```

Use maxima over BOTH public bases. The source's very broad coefficient
width already exceeds the first bound. Its inverse-erasure bound gives
`1/(2nu*b_dual)>=4sqrt(N)` even without the extra T factor, since
b_dual<=||M^-1||. Smaller requested errors are met by shrinking nu.
Only polynomial-bit scales are needed. The fact that a public basis is
skew, rather than the hidden rotated short frame, does not invalidate
this argument: the sampler uses that actual public basis and its dual.

Compare distributions in the SAME output bins. Source approximation,
tail truncation, binning/finite-QFT aliases and arithmetic precision are
separate errors. No finite-QFT alias theorem is implemented or certified
by this note's bounded tests; a physical finite-readout comparison must
supply it, not silently identify atomic and continuous distributions.
For T independent or classically adaptive fresh-copy
position/momentum readouts, uniform per-readout TV error zeta yields
transcript error at most T*zeta. Thus any classical transporter estimator
fed ONLY these records transfers to this classical simulator with the
same success up to that error.

This does not simulate coherent query superpositions, arbitrary quantum
preprocessing, conditional residual states after measurements, or
collective/nonabelian POVMs. It rejects the ordinary Cartesian-readout
shortcut for the stated Gaussian source, not all Gaussian encodings.

## 5. A Valid Swap-Wreath Reduction

There is a correct alternative to the invalid inversion automorphism.
Let W=(G x G) semidirect C_2, with the nontrivial bit SWAPPING the two
coordinates. Fix multiplication

```text
(x,y,b)*(u,v,c)=((x,y)*swap_b(u,v), b xor c).
```

Write phi(g)=Psi_(O*g), so the public ideal source is phi(a*g). Define

```text
Phi(x,y,0)=phi(x) tensor phi(a*y),
Phi(x,y,1)=phi(a*y) tensor phi(x).
```

Two public source calls and a controlled SWAP implement this function.
Neither evaluation of a nor application of an unknown-a unitary is used.
Under this convention the odd branch must NOT instead exchange x and y
inside the source calls.

The hidden subgroup is

```text
K_even=H x (a^-1*H*a) x {0},
K_odd =(H*a) x (a^-1*H) x {1},
K=K_even union K_odd,          |K|=2|H|^2.
```

Indeed s_a=(a,a^-1,1) has square 1 and conjugates
(h,a^-1*j*a,0) to (j,a^-1*h*a,0). The displayed set is a subgroup,
and direct substitution gives Phi(k*w)=Phi(w): it hides RIGHT cosets
K*w. Any odd element (u,v,1) supplies u in H*a; v need not equal u^-1.
The first coordinate is sufficient for the exact generator verifier.

For the ideal covariant Gaussian source, its coset-faithful equality
proved in Section 1 implies equality of Phi states exactly on these
cosets. Positive real amplitudes remove reciprocal tensor-factor phases.
For a merely invariant state-valued function this distinctness would
require an additional promise. The finite classical-label counterpart
is [Dinh--Moore--Russell, Section 2, Proposition 2](https://sites.santafe.edu/~moore/mceliece-qic.pdf);
the compact state-valued version here still needs a receiver theorem.

The two-register overlap is the product of the individual source
overlaps. Outside radius r from K at least ONE factor is separated,
so t tensor copies give at most (3/4)^t, not necessarily (3/4)^(2t).
They require 2t fresh preparations. If each source call has uniform ket
error e including finite-query precision and clean workspace, then the
t-copy ket error is at most 2te, invariance error at most 4te, and
separated overlap at most (3/4)^t+4te. Common source widths and registers
must be chosen after allocating this budget.

Distinct quantum labels are NOT orthogonal HSP labels. For a finite
query superposition with amplitudes c_w, discarding the source produces
matrix entries `c_w*conj(c_w')*<Phi(w')|Phi(w)>^t`, not a coset-indicator
matrix. A rounded SU(2)^d grid is also not automatically a finite group.
Thus this is a callable approximate COMPACT STATE-VALUED HSP reduction,
not a completed finite-group Fourier-sampling algorithm.

## 6. Actual Covariant Likelihood And Recovery Probability

Use normalized Haar measure. Decompose the cyclic representation as
`direct_sum_lambda V_lambda tensor M_lambda`, with
`d_lambda=product_sigma (2*j_sigma+1)`. If a block of the normalized
reference state has Schmidt coefficients sqrt(p_lambda,a), let
rho_lambda and tau_lambda be its unnormalized reduced states on the
representation and multiplicity spaces respectively. Then the orbit
frame operator is

```text
Omega=integral U(g)|Psi><Psi|U(g)^dagger dg
     =direct_sum_lambda (I/d_lambda) tensor tau_lambda.
```

On its support the square-root seed is Omega^(-1/2)Psi. In Schmidt
coordinates it replaces each sqrt(p_lambda,a) by sqrt(d_lambda).
For the right-parameterized orbit Psi_g=U(g^-1)Psi, the covariant
square-root measurement has likelihood density

```text
A(t)=sum_lambda sqrt(d_lambda)*Tr(D_lambda(t)*sqrt(rho_lambda)),
p(g_hat | g)=|A(g_hat*g^-1)|^2,
integral_G |A(t)|^2 dt=1.
```

This agrees with the pure-state maximum-likelihood construction of
[Chiribella et al., Section IV](https://wordpress.qubit.it/wp-content/uploads/publications-dariano/PhysRevA_70_062105.pdf).
For infinitely many blocks, A is interpreted in L2; the formal seed need
not be a Hilbert-space vector and the peak can diverge. A finite circuit
requires a charged truncation and its error bound.

The quantity that matters is instead

```text
E_eta={t : min_(h in H) D(t,h)<=eta},
P_eta=integral_(E_eta) |A(t)|^2 dt.
```

Scalar representation weights Tr(rho_lambda) alone do not determine it.
The full matrices sqrt(rho_lambda), their orientation, cross-irrep
interference, and multiplicity frames enter. For one SU(2) chord ball,
put theta=2*arcsin(eta/2). On a spin-l component of
`D_j tensor conjugate(D_k)`, the ball-integration operator acts by

```text
b_l(eta)=2/(pi*(2l+1)) * integral_0^theta
                           sin(u)*sin((2l+1)*u) du.
```

Product-ball coefficients multiply across embeddings. If the balls
around H are disjoint, H-bi-invariance gives
`P_eta=|H|*integral_(B_eta(1)) |A(t)|^2 dt`; otherwise use the union.
The peak only gives the UPPER bound P_eta<=volume(E_eta)*p(1).
Maximum likelihood need not maximize ball success. On multiple copies,
recompute the representation blocks of Psi^(tensor k); the likelihood
is not simply |A(t)|^(2k).

A useful exact warning is a maximally entangled single-spin probe.
For spin dimension D=2j+1 its density is |chi_j(t)|^2, with peak D^2.
Yet its probability in the identity ball of angular radius theta is

```text
P(theta)=theta/pi-sin(2D*theta)/(2pi*D).
P(1/D)=(1-sin(2)/2)/(pi*D).
```

Thus the peak grows while probability in the desired inverse-spin ball
vanishes. For integer spin, adding the equal antipodal cap doubles this
probability, not its asymptotic order. This is a countercontrol for that
probe, not a lower bound on multi-irrep quaternion-source receivers.

## 7. Relevant Available Primitives

[Iyer--Jain--Jordan--Somma 2026, Theorem 1.1 and Section 5.1](https://arxiv.org/pdf/2602.15180)
provides prescribed SU(2) spin-j rotations in the binary magnetic basis
with gate complexity polynomial in log(2j+1) and log(1/epsilon).
This is a useful published preprint construction: high spin alone is NOT
a rotation-cost obstruction. It does not perform the group Fourier
transform, supply an unknown-a unitary, or compute the source's
representation/multiplicity coordinates and polar maps.

[Prakash et al. 2026, Theorem 3.15](https://arxiv.org/pdf/2610.03581)
gives a clean Hahn/Clebsch--Gordan block construction costing
`O(B*polylog((B+alpha+beta+1)/epsilon))`, where B is block size, not
its bit length. That construction is insufficient for unrestricted
binary-large spins, but it is not a lower bound on other constructions.
The paper also provides more efficient transforms for other polynomial
families. Do not call every orthogonal-polynomial transform efficient.

[Burchardt et al. 2025, Theorem 1](https://arxiv.org/pdf/2509.22640)
concerns the U(D) Schur transform of D-level qudits. Treating a spin-j
register as a D-level qudit does not automatically turn that transform
into SU(2) angular-momentum coupling. Likewise,
[Holt--Subramanian 2026, Theorems 7.1 and 7.13](https://arxiv.org/pdf/2609.38085v2)
solve specified FINITE-group symmetry problems with group-QFT assumptions;
their normal-core result is not this compact transporter receiver.
These recent results are used only at their stated promises, not as
independently certified implementations.

Known reference-frame alignment constructions also choose their probe
before the unknown rotation acts. The present source does not grant
that access. A constant-gap expander twirl would not, on its own, bound
the smallest nonzero eigenvalue of Omega or implement its inverse square
root with acceptable normalization.

## 8. Polynomial-Size Informative Records Via Global Clifford Shadows

An efficient dedicated covariant POVM is not the only possible receiver.
Apply the existing [Huang--Kueng--Preskill classical-shadow protocol](https://preskill.caltech.edu/pubs/preskill-2020-predicting.pdf)
to the actual finite q-qubit source. Random GLOBAL q-qubit Clifford
circuits, followed by computational-basis measurement, have polynomial
gate and record costs. Their rank-one fidelity estimators have variance
at most 3. This does not hold with the same dimension-independent bound
for an arbitrary replacement by independent single-qubit Pauli measurements.

The following specialization already works for the previous straddle
source, whose Lipschitz constant L is explicitly reviewed; it does not
need a new Gaussian-orbit Lipschitz claim. Let each prepared finite state
approximate the corresponding ideal ket to error e<=1/128. Use common
registers and a net of G at chord mesh `1/(8*max(1,L))`. A net of size
`M<=(1+C*max(1,L))^(4d)` suffices for an absolute constant C.
Since log(L) is polynomial in input bits, log(M) is polynomial as well.

For each fixed net point g_j, denote its normalized, actually prepared
reference state by phi_j. If a source measurement uses Clifford C_i and
has outcome b_i, define the formal score

```text
X_j(i)=(D+1)*|<phi_j|C_i^dagger|b_i>|^2-1,     D=2^q.
E[X_j]=f_j=<phi_j|rho_I|phi_j>,                Var(X_j)<=3.
```

The full Clifford ensemble is a unitary 3-design. Its moment identities
give, for any normalized rho_I,
`E[X_j^2]=D*(1+2f_j)/(D+2)<=3`. Split records into k independent groups
of 768 and take median group means. Chebyshev bounds each bad group by
1/4 at additive error 1/8; Hoeffding and a union bound give simultaneous
accuracy for every j with failure at most delta, when k is odd and
`k>=8*log(M/delta)`. This is an explicit conservative bound, not an
optimal sampling constant or a claim of implementation.

The 768 bound treats the scores as exact real numbers. For numerical
evaluation, use 3072 copies per group to allocate 1/16 to statistical
error and another 1/16 to score computation. The total 1/8 bound and
the reconstruction margin below are then unchanged. This changes a
constant in the copy bound, not the unresolved score-evaluation cost.

A nearest net reference differs in ket norm from the actual source by
at most `1/8+2e<=9/64`, so its fidelity is at least `1-(9/64)^2`.
A reference farther than the separation radius r from H*a has overlap
at most `3/4+2e<=49/64`, hence fidelity at most `(49/64)^2`.
The largest estimated score has true fidelity at least

```text
1-(9/64)^2-1/4 = 2991/4096 > 2401/4096 = (49/64)^2.
```

Thus an exhaustive decoder of these records identifies a reference
within r, sufficient for exact reconstruction when r is chosen below
the reconstruction radius. The number of copies and the QUANTUM
data-acquisition circuit are polynomial. This argument avoids both the
invalid coarse-net approximation and the assumption that all neighboring
fine-net states are mutually separated.

### The Remaining Computational Task

No polynomial decoder has been supplied. The net can have exponentially
many entries. Even evaluating one score from a succinct reference
preparation requires its overlap with a supplied stabilizer state;
an efficient preparation circuit does not automatically make that
amplitude classically computable. Computing X_j to additive zeta needs
the squared overlap to error zeta/(D+1). That needs polynomially many
precision BITS, but need not admit polynomial computation or shot cost.

Hence the sharper open problem is: recover a norm-q generator from these
polynomial-size Clifford records, or design a structured measurement with
an efficiently exploitable statistic. A dense/exhaustive score computation
is an existence argument only. The Cartesian simulator in Section 4 does
not simulate these global-Clifford measurements; conversely, failure to
simulate them is not evidence of an end-to-end speedup. This is reuse of
an established shadow theorem, not a newly discovered quantum algorithm.

## 9. Decision And Next Constructive Test

FOLLOW-UP: QUATERNION_RECEIVER_CLASSICAL_FILTER.md now tests the proposal
below. Additive orbit overlaps and matching-width passive joint-parity
means have classical estimators. The finite source is computationally
tractable in its computational basis. Neither result simulates complete
Clifford/parity records or supplies their nonlinear decoder. Do not keep
the original parity-feature proposal marked as an untested opportunity.

Ordinary Cartesian readout is deprioritized: it has a matched classical
simulation. Generic global-Clifford records are informative and efficiently
acquired, but the only decoder supplied here is exhaustive. The covariant
formula still requires the ACTUAL source matrices and a usable polar map;
the swap-wreath oracle still requires a compact state-valued receiver.
No current route is an end-to-end polynomial algorithm.

A more structured next test is Hermite-basis number parity after known
mode rotations, including joint correlations across embeddings. In an
oscillator model, four real modes split into two fundamental SU(2)
doublets. Fixed occupation n_a carries spin j_a=n_a/2; their product
basis can be retained without assuming efficient large-spin coupling.
Total occupation is invariant and cannot reveal orientation. Mode parity
`(-1)^(j_a+J_axis)` is bounded and avoids conditioning on a single rare
high-number outcome. But useful inverse-polynomial gaps, a controlled
Hermite cutoff and an affordable decoder must still be proved on the
actual lattice source. Check a classical simulator before accepting any
apparent signal. This is a next-test specification, not an asserted gap.

Failure of one receiver does not prove a general lower bound. Conversely,
information in polynomially many states or classical records is not an
efficient decoder. The known shadow and rotation primitives are reused,
not claimed as discoveries. No candidate is admitted by this pass.
