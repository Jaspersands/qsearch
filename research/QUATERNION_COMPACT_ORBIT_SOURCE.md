# A Compact Quaternion Orbit Source

Date: 2026-10-30. Status: independently reviewed ideal-state separation
and approximate preparation arguments; bounded controls, not a compiled
quantum oracle or an efficient receiver. No new algorithmic speedup or
novelty claim. The source is a concrete constructive continuation of
[the norm-target audit](QUATERNION_NORM_SLICE_AND_LOCAL_FLAGS.md).

## Scientific Question

Can the actual norm-exact quaternion ideal input supply a global quantum
orbit source without preparing a shortest vector first? Yes at the level
of the broad, finely encoded lattice signatures below. Their separation
has an arithmetic proof. The unresolved step is an efficient end-to-end
receiver recovering the global transporter, not a presumed universal
failure of Gaussian state preparation. The subsequent
[receiver analysis](QUATERNION_COVARIANT_RECEIVER.md) supplies polynomial-
size global-Clifford measurement records but no polynomial decoder; it
also gives an exactly covariant Gaussian analytical variant and a
classical simulator for its ordinary Cartesian readouts.

This uses the established broad Gaussian/straddle construction of
[Eisentrager--Hallgren--Kitaev--Song (EHKS), Section 5](https://www.cse.psu.edu/~sjh26/units-stoc.pdf).
Their Theorem 5.7 proves separation for number-field log-unit orbits and
Section 6 supplies an ABELIAN receiver. Neither theorem automatically
solves the compact nonabelian transporter here. The old blanket SU(2)
commutant/circuit claim remains retracted in NONABELIAN_BARRIER_SCOPE_AUDIT.

## 1. Actual Input And Group Action

F is a totally real field of degree d, B/F a totally definite quaternion
algebra, and O an explicit unital O_F-order. The field structure, integral
bases, order multiplication and real embeddings are input data, not hidden
advice. At each real embedding identify B with Hamilton quaternions so that
reduced norm is the Euclidean squared norm. Put N=4d and

```text
||x||^2 = Tr_(F/Q)(nrd(x)),
G = product_sigma SU(2), acting by x -> xg on the RIGHT,
H = O^1 = {u in O : nrd(u)=1}.
```

For a full locally principal LEFT ideal I and explicit totally positive q,
verify nrd(I)=q O_F. On a norm-exact YES instance I=O alpha,
nrd(alpha)=q. Normalize the public ideal lattice blockwise:

```text
L_I = { (sigma(x)/sqrt(sigma(q)))_sigma : x in I },
a_sigma = sigma(alpha)/sqrt(sigma(q)),
L_I = O a,       a in G.
```

Finding any representative of H a finds a valid generator after undoing
the normalization. The Gaussian encoding can be evaluated from the public
basis of L_I without knowing alpha. Native Hawk uses right ideals; use
conjugation to translate this convention explicitly.

The stabilizer is exact: O g=O iff g in H. If O g=O, applying g to 1 puts
g in O, and norm one gives inverse conjugate(g) in O. Conversely such a
unit preserves O. H is finite, with |H|<=max(120,16d^2). Small cardinality
alone does not give its enumeration or the circuit for a group measurement.

**General cardinality argument (30 October correction).** The previous
attribution to Hawk Appendix B was too broad: its Proposition B.25 has
additional presentation hypotheses. The bound in the present generality
follows instead from the standard finite-subgroup classification of SU(2),
as recorded in [Wright, Section 2.3.1](https://www.math.stonybrook.edu/alumni/2013-Evan-Wright.pdf),
and this elementary cyclotomic argument. First use the FULL Minkowski
embedding: O is discrete and norm-one elements lie in a compact product
of unit spheres. Hence H is finite. At any one real place the ring map
B -> B tensor_(F,sigma) R is injective and embeds H into SU(2). This
does not assert that all of O has discrete image at that single place.

An element u of exact order M generates Q[u]=Q(zeta_M) inside F[u].
Total definiteness makes B a division algebra, so F[u] is a field of
degree at most two over F, and phi(M)<=2d. The Euler product gives

```
phi(M)^2/M = product_(l^e exactly divides M) l^(e-2)*(l-1)^2 >= 1/2,
M <= 2*phi(M)^2 <= 8d^2.
```

Every odd-prime factor in the product is at least one; only l=2,e=1
contributes 1/2. Finite SU(2) subgroups are cyclic, binary dihedral,
or have order 24,48,120. A binary dihedral group of order 4m contains
an element of order 2m, so its order is at most 16d^2. This proves the
stated bound for any totally definite quaternion order over F. Dewey
the 2nd independently checked the injection, field, and numerical steps.
This is a local deduction, not a new unit enumeration algorithm.

## 2. Signature And Precise Parameters

Let b_1,...,b_N be a Z-basis of O, A=max_i ||b_i||. Choose s>=4A. Write
str_nu for EHKS's product straddle encoding: in one coordinate t=x/nu-k,
k=floor(x/nu), the state is
`cos(pi*t/2)|k> + sin(pi*t/2)|k+1>`.
The tensor product over N coordinates is normalized and two such packets
have zero overlap if their centers are at distance at least 2nu*sqrt(N).

Define the ideal, infinite-dimensional source

```text
|f(g)> = Z^(-1/2) sum_(x in O) exp(-pi*||x||^2/s^2) |str_nu(xg)>,
Z = sum_(x in O) exp(-2pi*||x||^2/s^2).
```

Nonzero x in O has totally positive integral reduced norm. AM--GM gives
`||x||^2 >= d*Norm(nrd(x))^(1/d) >= d`. Therefore distinct points in O g
are at least sqrt(d) apart. The grid condition below makes their packet
supports disjoint, proving that Z really is the normalizer. Merely writing
Z as the sum of squared amplitudes would be wrong for overlapping packets.

Choose 0<tau<=1/576 and

```text
R >= max(2, s*sqrt(((N/2)*log(2)+log(1/tau))/pi)),
delta = 2nu*sqrt(N) <= (1/8)*R^(-3d),
r = R^(d-1)*delta.
```

Use the bi-invariant block metric
`D(g,h)=max_sigma ||R(g_sigma)-R(h_sigma)||_op`; right multiplication by a
quaternion has operator norm equal to its quaternion length.

**Separation lemma.** If `min_(h in H) D(g_1*g_2^-1,h)>r`, then

```text
|<f(g_1)|f(g_2)>|
  <= 1/(1+exp(-pi/8)) + 2sqrt(tau) < 3/4.
```

Also `f(hg)=f(g)` for h in H: these are RIGHT cosets H g, with left-H
invariance. Tensoring t independent preparations reduces the separated
overlap to at most (3/4)^t. No receiver complexity follows from this fact.

## 3. Arithmetic Proof Of Separation

It suffices to analyze geometric near pairs `||xg-y||<=delta`, where
`g=g_1*g_2^-1`, x,y in O, and ||x||,||y||<=R. Rotating the geometric
condition preserves distances. We do NOT assert that a fixed straddle
grid or its inner products are rotation covariant.

Suppose one such pair has x nonzero. Every conjugate of
`nrd(x)-nrd(y)` has absolute value at most `delta*(2R+delta)<1`. This
difference is an algebraic integer. If nonzero, its absolute field norm
would be a positive integer strictly below one. Hence nrd(x)=nrd(y).
Set

```text
g_0=x^-1*y,     alpha=nrd(x),     D_0=Norm_(F/Q)(alpha).
```

Then g_0 lies in B and has reduced norm one. Moreover,

```text
1 <= D_0 <= R^(2d),
g_0 = (1/D_0)*(D_0/alpha)*conjugate(x)*y in (1/D_0)O.
```

Here conjugate(x)=trd(x)-x lies in O, and D_0/alpha is in O_F by the
monic polynomial of the nonzero algebraic integer alpha. That factor is
central; no noncommuting quaternion factors have been exchanged.

The product of the squared lengths of x's d embeddings is D_0>=1, and
each length is at most R. Thus every inverse block has length at most
R^(d-1), giving `D(g,g_0)<=R^(d-1)*delta=r`.

For ANY other short near pair x',y',

```text
x'*g_0-y' in (1/D_0)O,
||x'*g_0-y'|| <= delta*(1+R^d)
               < sqrt(d)*R^(-2d)
               <= lambda_1((1/D_0)O).
```

Consequently y'=x'g_0 exactly. All short matches therefore come from the
same additive subgroup `J=O intersect O*g_0^-1`. If g is farther than r
from H, then g_0 is not in H and J is proper. Norms and Gaussian weights
of each matched pair agree exactly.

For any proper additive subgroup J of O, some basis vector b is outside
J. The cosets J and J+b are disjoint. With
`rho(S)=sum_(x in S) exp(-2pi*||x||^2/s^2)`, pair x and -x to obtain

```text
rho(J+b) >= exp(-2pi*||b||^2/s^2)*rho(J),
rho(J)/rho(O) <= 1/(1+exp(-2pi*A^2/s^2))
              <= 1/(1+exp(-pi/8)) < 2/3.
```

This does not require J to have full rank. It also handles the case of NO
nonzero short near pair: the origin still matches, but its mass is bounded
by taking J={0}. Omitting this case would incorrectly set the overlap to
zero. Zero cannot match a nonzero lattice point because delta<sqrt(d).

Finally, for the squared-amplitude probability distribution, Poisson
summation gives `rho_s(O)/rho_(s/sqrt(2))(O)<=2^(N/2)`. Markov's inequality
therefore bounds

```text
Pr(||x||>R) <= 2^(N/2)*exp(-pi*R^2/s^2) <= tau.
```

Removing the two tail components changes the inner product by at most
2sqrt(tau), by Cauchy--Schwarz. On the truncated components, the matched
weights are equal, so the proper-subgroup bound is a PROBABILITY mass, not
its square root. Combining these bounds proves the lemma.

## 4. Clean Finite-Bit Preparation

Broad state preparation is not a shortest-vector operation. It must still
be compiled with common widths, controlled errors and clean workspace.
Let M be either public embedded basis (O or L_I), and r_G=s/sqrt(2) the
PROBABILITY Gaussian width. For Gram--Schmidt vectors b_i^*, put
`r_i=r_G/||b_i^*||`. A reverse coherent Klein construction uses centers
`c_i=-sum_(j>i) mu_(j,i)*z_j` and positive square-root amplitudes.
Its joint probability is

```text
p_K(z)=exp(-pi*||Mz||^2/r_G^2) /
       product_i rho_(r_i)(Z-c_i).
```

The shifted theta normalizers, often omitted in a naive coherent sampler,
are uniformly close to r_i when r_i is large: Poisson summation bounds
their relative error by `2*sum_(k>=1) exp(-pi*r_i^2*k^2)`. Choose all r_i
large enough to make the accumulated probability and amplitude errors
smaller than the allocated oracle error. The maximum Gram--Schmidt length
and all coefficient centers have polynomial-bit descriptions. Right
rotations preserve the Gram matrix, so this coefficient preparation is
the SAME for every queried g, not a secret-dependent sampler.

One can deliberately choose the much wider `min r_i >= C*N/epsilon^2`
for a sufficiently large fixed C. This still uses polynomially many bits
in log(1/epsilon). It avoids an uncharged exact discrete-Gaussian CDF:
for `f(t)=r_i^-1 exp(-pi*(t-c_i)^2/r_i^2)`, bin-integrated probabilities
over `[j-1/2,j+1/2]` differ from the normalized discrete Gaussian by TV at
most 2/r_i. This follows from `integral |f'|=2/r_i` and normalization.
The accumulated conditional TV is at most `2N/min r_i`, and square-root
state distance is at most its sqrt(2) multiple. Gaussian integrals admit
the [Grover--Rudolph construction](https://arxiv.org/abs/quant-ph/0208112);
the integrals must be evaluated deterministically to the charged precision,
not supplied by an uncharged statistical oracle.

An arbitrary fixed coefficient box is NOT sufficient to justify the
controlled Gaussian integrals. Its allowed interval can be far from a
conditional mean, leaving an extremely small conditional normalization.
The independent preparation review identified this gap. Use centered
conditional windows instead:

```text
z_i=floor(c_i)+k,   |k|<=M_i=ceil(K*r_i)+2,
beta=epsilon^2/(128N),   K=O(sqrt(log(N/epsilon))).
```

Choose K so each discarded continuous Gaussian tail has mass <=beta.
Every root normalization is then >=1-beta. First-exclusion coupling costs
at most N*beta in TV, hence sqrt(2N*beta)<=epsilon/8 in ket distance.
This is a bound for the actual sequential bin distribution being truncated,
not an unproved transfer of the target lattice's tail bound.

Every retained bin has unnormalized mass at least
`r_i^-1*exp(-pi*(K+4)^2)`. Thus every nonempty prefix node in the
Grover--Rudolph tree has a denominator at least this large. Its logarithmic
inverse is O(log(r_i)+K^2), not proportional to r_i. Empty nodes are
detected exactly. Recentered, scaled integration endpoints lie in
[-K-4,K+4]; a rigorously truncated Gaussian power series evaluates the
integrals to the required precision in polynomial time. Charge extra
bits for cancellation and square-root sensitivity near rotation
probabilities zero or one. The circuit computes each rotation reversibly
from the queried prefix; it does not enumerate the tree's leaves.

For sufficiently large r_min, every retained branch satisfies
`|z_i-c_i|<=(K+1)*r_i`. Gram--Schmidt orthogonality gives

```text
||Mz||^2=sum_i ||b_i^*||^2*(z_i-c_i)^2,
||Mz||<=r_G*sqrt(N)*(K+1),
||z||<=||M^-1||*r_G*sqrt(N)*(K+1).
```

These bounds supply finite polynomial-bit coefficient registers, including
for skew input bases. They are support bounds for the centered-window
construction, not an exact Gaussian cutoff. Embeddings, Gram data and
conditioning must have polynomial-time precision access from the explicit
rational/algebraic input. An unrepresented analogue rotation is not an
allowed oracle query.

After preparing z, compute the straddle state at M_g z and uncompute
the point-generation workspace while z is still available. Recover z
from each supported grid point k by rounding `M_g^-1*(nu*k)`, subtract
it from the coefficient register, and uncompute reconstruction workspace.
Require, with margin for arithmetic error,

```text
nu*sqrt(N)*max(||M_O^-1||,||M_I^-1||) <= 1/8.
```

All retained lattice points have polynomial-bit coordinates. Compute their
embeddings, centers and controlled rotations finely enough that the final
state error, including workspace, is <=epsilon uniformly in the finitely
encoded query. Point accuracy of order epsilon*nu/poly(N) suffices for
the straddle step; charge the controlled arithmetic and the entire tree
depth when allocating rotation errors. The basis O and normalized ideal
generally have DIFFERENT Gram matrices: prepare their coefficient states
separately, with a common sufficiently broad s. Only rotation of a fixed
basis leaves its Gram matrix unchanged.
Keeping the original coefficient register would destroy basis-independent
oracle equality. No random seed, measured sample transcript or conditional
normalizer may remain as hidden garbage.

The resulting proof-level construction is polynomial in the explicit input
bits, log(1/epsilon), and log(1/nu), with widths chosen for this error
budget. It does NOT establish arbitrary-accuracy preparation at every
previously fixed narrower width. It has been independently reviewed as
an argument, not compiled or machine-formalized. The ideal-state lemma
does not rely on an arbitrary supplied sampler being clean. Any later
backend must independently verify this contract and its error budget.

### Lipschitz And Coherent Query Precision

The fixed grid need not be rotation covariant to control precision. Inside
a grid cell, the straddle derivative has squared norm
`pi^2/(4nu^2)` in each coordinate and is orthogonal to the packet. The
different coordinate derivatives are orthogonal. Packets AND their
one-sided derivative supports lie within nu*sqrt(N) of their centers;
the lattice separation makes these supports disjoint across x in O.

Along an absolutely continuous group path, let
`v(t)=max_sigma ||dot(g_sigma(t))||_op`. Almost everywhere,

```text
||dot(f(g(t)))||^2 <= (pi^2/(4nu^2))*E[||x||^2]*v(t)^2,
E[||x||^2] <= N*s^2/(4pi),
L_path = s*sqrt(pi*N)/(4nu).
```

The moment inequality follows by differentiating Poisson summation for
the theta series at probability width s/sqrt(2): the dual-lattice second
moment is a nonnegative subtraction from N*s^2/(4pi). No smoothing
assumption is needed. At a grid boundary the packet is continuous but
its left and right derivatives differ; they give no extra variation
term. Integrate the bound for finite sums and pass to the uniformly
Gaussian-tail-controlled limit rather than differentiating every point
of the infinite sum by fiat.

For the max-block chord metric D, simultaneous shortest paths in SU(2)
have length `2*arcsin(D/2) <= (pi/2)*D`. Consequently

```text
||f(g)-f(h)|| <= (pi/2)*L_path*D(g,h).
```

A finite query label must specify g by uniformly reversible polynomial-time
precision computation. A group-valued approximation with chord error
`eta<=2*epsilon_rep/(pi*L_path)` incurs ket error <=epsilon_rep. This
costs polynomially many bits in log(s), log(1/nu), N and log(1/epsilon_rep).
Raw rounded matrices need not lie in G; either normalize with controlled
conditioning or bound their packet-position errors directly. Uniform
VECTOR-norm error, a consistent phase convention and clean workspace make
this bound valid on arbitrary superpositions of the retained query labels.
Per-label fidelity up to an arbitrary label-dependent phase is insufficient.

## 5. Transporter Promise And Reconstruction

Use common s,nu and output registers for both public bases. On a YES input,

```text
f_I(g)=f_O(a*g).
```

For epsilon-accurate preparations this equality has at most 2epsilon
vector-norm error. Tensor amplification must budget at most t*epsilon
preparation error on each t-copy side, rather than treating the approximate
overlap as exactly the ideal exponential bound.

This is a nonabelian hidden TRANSPORTER/shift promise, not automatically an
abelian HSP. Inversion is not an automorphism of SU(2), so the usual
generalized-dihedral semidirect-product shortcut is invalid without a
separate reduction. A source oracle is not an unknown-unitary oracle that
can apply a to arbitrary chosen probes.

If a receiver returns a_hat within max-block error
`eta < 1/(4sqrt(d)*||M_I^-1||)` of some u*a, u in H, then inverse-basis
rounding recovers the exact lattice vector u*alpha. Verify ideal membership
and nrd=q exactly. This is a polynomial-bit recovery radius and a verifier,
not a way to find a_hat. Choose the grid further so r is below this radius.

NO inputs need not obey the shift promise. Any proposed decision reduction
must have bounded runtime on them and reject outputs failing the exact
verification; it may not assume a YES oracle on every input.

## 6. Strong Classical Attacks On Moment Readout

Let R_a be the block-diagonal right multiplication matrix. Matching-width
position moments satisfy `M_k(I)=R_a^(tensor k) M_k(O)`. Covariance gives
linear equations in the 4d quaternion coordinates:

```text
C_I[sigma,tau]*R(a_tau) = R(a_sigma)*C_O[sigma,tau].
```

Cross-block terms can synchronize rotations even when individual diagonal
blocks are scalar. For fixed tensor degree, single-block matching is a
constant-dimensional bounded-degree polynomial problem, with conditioning
and identifiability still charged. Odd moments vanish by central symmetry;
fourth moments are not universally informative (Hurwitz fourth moments
are radial). Do not infer full state isotropy from these facts.

For the natural power-of-two order, the lattice is scaled cubic. Writing
`L_I=sqrt(d)*U Z^(4d)` with U orthogonal and coefficient fourth cumulant
kappa_4, its full fourth cumulant has the form

```text
K_4=d^2*kappa_4*sum_j u_j^(tensor 4),
K_4(.,.,v,v)=d^2*kappa_4*U*diag((u_j dot v)^2)*U^T.
```

A generic contraction with distinct eigenvalues recovers the short axes
by ordinary matrix diagonalization, GIVEN accurate nonzero moments. Each
recovered axis yields an exact-norm generator after reconstruction. This
is not an input-only classical polynomial algorithm unless moment
evaluation, signal size, spectral gaps and precision are affordable.

Broad discrete Gaussians can have extremely small cumulants. In one
dimension, the probability distribution proportional to exp(-pi*x^2/16)
has standardized fourth cumulant about 2.99e-18, yet its integer-frequency
character exp(2pi*i*x) is identically one. Fine lattice coherence has not
disappeared. Position moments of the actual straddle state also need the
packet-error correction; substituting a continuous Gaussian loses the
very information a new receiver would have to use.

Single-block natural-order moments have an additional limitation: roots
of unity make the cyclic phase invisible below degree 4d. Full mixed-block
cumulants can avoid that ambiguity. A receiver based only on an informative
low-order tensor must first survive these classical contractions.

## 7. The Next Decisive Experiment

This section's original covariant-measurement question is refined by
QUATERNION_COVARIANT_RECEIVER.md. An efficient dedicated covariant POVM
is sufficient but no longer the only explicit route: global-Clifford
shadows give efficient data acquisition, leaving computational decoding.

[Chiribella et al., Section IV](https://wordpress.qubit.it/wp-content/uploads/publications-dariano/PhysRevA_70_062105.pdf)
give optimal maximum-likelihood covariant measurements for specified
pure-state group orbits. That supplies a measurement TEMPLATE, not a
polynomial circuit or a success bound inside an arithmetic recovery ball.
Our fixed straddle grid is not exactly covariant; using this template
requires a controlled covariant packet variant or an approximation proof.
For a continuous covariant replacement, the homomorphic convention on kets
is `U(g)|x>=|x*g^-1>`; sending centers to x*g composes in the reverse
order. Keep that convention distinct from the right-coset convention.

The next question is whether a measurement using fine coherent structure
can achieve probability >=2/3 of reaching the radius in Section 5 with
polynomially many copies, gates, and classical work. Derive the actual
representation/multiplicity weights and probability mass, not merely the
likelihood at one point. Charge truncation, precision and basis transforms.
Classical covariance/cumulant recovery is the first falsifier; a source
with affordable useful moments is not automatically a quantum advantage.

For certified scaled-cubic inputs, also compare the published
[Aggarwal--Chen--Kumar--Shen ZLIP algorithm, Section 8](https://ir.cwi.nl/pub/35122/35122.pdf):
its quantum time is 2^(0.417N+o(N)), with exponential QRAM/classical space,
not polynomial time. Do not extend that promise to arbitrary overorders.
QuaILLL and exact weighted SVP remain relevant classical comparators.

No speedup candidate is admitted here. A failure of one covariant
measurement would reject that measurement, not prove a general compact
group quantum lower bound. The useful advance is a native, quantitatively
separated source with a specific receiver problem still to solve.

## 8. Verification Scope

The six-agent pass separated source/preparation review, classical moments,
integral descent, primary literature, the Goppa alternative, and independent
exact controls. These are automated mathematical reviews, not external
human peer review or proof-assistant certification.

`tests/test_quaternion_orbit_signature.py` checks a Hamilton-order rotation
with intersection index 25, its eight-unit stabilizer, the nonzero Gaussian
overlap, the actual EHKS trigonometric packet, clean versus retained-label
states, coarse-grid normalization failure, and nonabelian inversion.
`tests/test_quaternion_orbit_moments.py` checks exact cumulant recovery,
low-degree phase ambiguity and tail-bounded numerical cumulant sizes.
`tests/test_quaternion_integral_descent.py` checks the matched integral
YES/NO equations in the companion note. None implements growing-degree
Gaussian preparation, a quantum experiment, or the missing receiver.

The EHKS local source snapshot is `literature_cache/ehks_2014_units_stoc.pdf`,
SHA-256 `c7667a168f429b1fba679ba8afaa12582cfda408298c6c23e7688b85bd178671`.
