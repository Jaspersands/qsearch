# Independent review: quadratic Legendre reconstruction

5 November 2026. Mathematical composition review, not an implementation or
priority determination. The center-plus-width construction below survives
this review. It gives a bounded-error subexponential quantum upper bound
under the stated Q2 access. It does not give polynomial time, novelty, a
proved speedup or classical hardness. A stronger chosen-query classical
baseline must accompany it.

## 1. Exact native promise and source boundary

The public input is an odd prime p. The hidden object is a monic
irreducible polynomial f(X)=X^2+bX+c over F_p. Set

    a=-b/2, d=a^2-c, g(x)=chi(f(x))=chi((x-a)^2-d).

Here d is a nonzero nonsquare, chi is the quadratic character, and g(x)
is always +1 or -1. The promised oracle is the ordinary reversible
BIT-OUTPUT Q2 oracle |x,z> -> |x,z XOR L_f(x)>, where (-1)^L_f(x)=g(x).
Phase kickback, coherent fingerprint computation and inverse queries then
cost a constant number of these native calls. Follow-up correction: an
uncontrolled diagonal phase oracle also suffices via the one-query public
reference compiler below. Copies alone do not supply that coherent query
construction. Classical-only Q1 access, full values f(x), and extension-field
queries remain distinct input models. Output b,c and verify
them using charged native queries.

All claims below are uniform for every such hidden f. Randomness is in
public fingerprint/verification points and in the algorithms, not a hidden
random-key assumption. Finitely many small primes can be handled by direct
enumeration at constant asymptotic cost.

The full proof of Russell--Shparlinski, quant-ph/0212016, Section 4 and
Theorem 6, constructs a few-query state and proves existence of a POVM.
It does not implement that POVM in polynomial time. No efficient receiver
is imported from its query bound.

## 2. Reflection fingerprints and the exact dihedral source

Choose L independent uniform public offsets x_j in F_p and define

    F(t,0) = (g(x_j+t))_j,
    F(t,1) = (g(-x_j+t))_j.

Reflection symmetry gives F(t,1)=F(2a-t,0) exactly. For t!=u, the two
shifted irreducible monic quadratics are distinct and coprime. Their
product is squarefree of degree four. The standard quadratic-character
bound gives

    |sum_x g(x+t)g(x+u)| <= 3 sqrt(p).

Thus one random offset has agreement probability at most
rho=(1+3/sqrt(p))/2. For p>=37 this is at most 3/4. A union bound over
fewer than p^2/2 pairs proves that L=O(log p+log(1/delta)) makes
t -> F(t,0) injective with probability at least 1-delta. This is GLOBAL
injectivity on the entire group domain, not a promise about just the
queries eventually made. Conditioned on this good event, the hiding
oracle is exact, including on coherent superpositions. There is no
additional fingerprint-collision error for each sieve query.

Fix group coordinates and their multiplication as

    (t,b)(u,c) = (t+(-1)^b u, b+c),  b,c in F_2.

Let s=2a and H={(0,0),(s,1)}. The raw F is constant precisely on the
RIGHT cosets H(t,0)={(t,0),(s-t,1)}. For the translation-register Fourier
sampling convention below, first compose F with group inversion:

    F'(t,0)=F(-t,0),  F'(t,1)=F(t,1).

Then F'(t,0)=F'(t+s,1), and no other identifications occur on the good
event. A fresh uniform group query and output measurement therefore give

    (|t,0>+|t+s,1>)/sqrt(2).

Using the positive-exponent QFT on the first register and measuring its
label k yields k uniform in F_p and the exact phase qubit

    (|0>+exp(2*pi*i*k*s/p)|1>)/sqrt(2),

up to a common phase. These are the ordinary dihedral phase states.
The k=0 outcome is retained or explicitly treated as uninformative by the
known algorithm; it is not silently renormalized away. Fresh preparations
have their full L-query cost charged. No consumed quantum packet is
recreated for free.

Kuperberg's primary full text, quant-ph/0302112, Theorem 1.1 gives
2^O(sqrt(log N)) time and queries; its introduction also charges that much
quantum space. Section 5, Algorithm 2, explicitly treats N that are not
powers of two and describes the general cyclic QFT and odd-factor
automorphisms. Hence N=p is in scope. The proof is not being transferred
from only the N=2^n special case. The paper uses its own right-coset and
group-coordinate conventions; the inversion above is a paid conversion
that proves the required phase source in the convention used here.

Consequently the center a can be recovered with bounded error in
2^O(sqrt(log p)) time, native Q2 queries and quantum space, including the
polylogarithmic fingerprint overhead. This is the original large-space
bound. No polynomial-space bound is asserted here.

## 3. Constant-success width recovery after the correct center

Let S={z in F_p:chi(z)>=0}, including zero, and s_0=|S|=(p+1)/2. Uniform
preparation over S is paid: squaring is a bijection from the integers
0,...,(p-1)/2 onto S. A reversible canonical square-root computation
erases the original index. A known quadratic nonresidue suffices for
Tonelli--Shanks; it can be found by charged random classical trials.
Uniform interval preparation has polynomial-logarithmic cost at the
required precision, or constant-success charged rejection.

Given the correct a, querying a+sqrt(z) and uncomputing the canonical
square root prepares

    |v_d> = (1/sqrt(s_0)) sum_(z in S) chi(z-d)|z>.

Both square-root signs give the same g-value. Since d is a nonsquare,
z-d is never zero on S. No unknown root of the hidden polynomial is
supplied or computed at this step.

Define C[y,z]=chi(y-z), and let J be the p-by-p all-ones matrix. The
Legendre correlation identity gives

    C C^dagger=pI-J,  C1=C^dagger1=0,  J^2=pJ.

Therefore U=C/sqrt(p)+J/p is unitary for EVERY odd prime. In particular,
one must not treat C as real symmetric when p=3 mod 4: then it is real
skew-symmetric, but the displayed adjoint identity remains correct.

For F|z>=p^(-1/2) sum_k exp(2*pi*i*k*z/p)|k>, the diagonal entries of
F U F^dagger are 1 at k=0 and (tau_p/sqrt(p))*chi(k) otherwise. The
canonical quadratic Gauss phase is 1 for p=1 mod 4 and i for p=3 mod 4.
Thus an additive QFT, known character computation and these complex phases
implement U with polynomial-logarithmic overhead. The zero-frequency
entry is 1, not chi(0)=0; omitting this correction would destroy unitarity.

At the desired output d the exact amplitude is

    <d|U|v_d> = chi(-1)*sqrt(s_0/p) + T/(p sqrt(s_0)),
    T = sum_(z in S) chi(z-d).

Using 1_S(z)=(1+chi(z)+1_[z=0])/2, the ordinary shifted-character sum
and sum_z chi(z(z-d))=-1 give

    T=(-1+chi(-d))/2=-(1+chi(-1))/2.

Accordingly, the success probability is exactly

    p=3 mod 4:  s_0/p;
    p=1 mod 4:  (sqrt(s_0/p)-1/(p sqrt(s_0)))^2.

Both are bounded below by an absolute positive constant. The looser
bound (s_0/p)(1-1/sqrt(p))^2 used in the proposed derivation is also valid.
Recover b=-2a and c=a^2-d. A returned square d, including zero, can be
rejected immediately. Correctness of this width calculation is conditional
on the center being correct; final verification must not assume that event.

## 4. Verification, clocks and total resources

For a fixed hidden irreducible f and any distinct irreducible candidate h,
the same degree-four bound makes one fresh uniform test agree with
probability at most rho. Choosing O(log p+log(1/delta)) public validation
points and querying their native values excludes every wrong candidate
simultaneously with probability at least 1-delta, by a union bound over
fewer than p^2/2 candidates. The validation set can therefore safely be
reused for adaptively produced candidates on its global good event.
Alternatively, fresh independent validation points can be used per attempt
with a union bound over a fixed attempt budget. This is bounded-error
verification, not a perfect identity test from a few evaluations.

On good fingerprint and validation events, a constant-success center run
followed by constant-success width recovery accepts the true key with
constant probability and accepts no wrong key. Use a predetermined
O(log(1/delta)) attempt budget and return ABORT if it is exhausted.
Truncate the imported randomized sieve at its justified resource budget;
do not turn repeated failure into an unbounded search or a correctness
claim. For constant final error, the total bound remains

    time, native Q2 queries, quantum space: 2^O(sqrt(log p)).

Field arithmetic, coherent fingerprint construction, verification and the
width stage contribute polynomial factors in log p. QFT approximation
errors can be made small compared with the inverse number of uses; their
required precision has O(sqrt(log p)+log(1/delta)) extra bits, still within
the stated overhead. There is no QRAM table of p or p^2 unknown values.

## 5. Stronger chosen-query classical baseline

The center/width decomposition also improves the elementary full-data
O(p) reconstruction baseline. This improvement is a constructive upper
bound, not a hardness or priority claim.

First let B=ceil(sqrt(p)). Store F(t,0) for t=0,...,B-1, and compare them
with F(jB,1) for j=0,...,B-1. Every s=2a in [0,p-1] has a representation
s=t+jB with those bounds. On the global fingerprint-injectivity event,
any match returns the correct s=t+jB mod p. This stage uses O(sqrt(p)*L)
native classical queries, polynomial-logarithmic work per evaluation and
O(sqrt(p)*L) bits of fingerprint storage. It does not need birthday luck.

After a is known, choose a known nonsquare eta and write d=eta*r^2. Define

    h(x)=g(a+x),  phi(x)=chi(x^2-eta).

Then h(x)=phi(x/r). Both are even functions. Work in
G=F_p^*/{+1,-1}, sampled uniformly by canonical signed representatives.
For O(log p) public independent nonzero y_j, set

    H1(u)=(h(u*y_j))_j,  H0(v)=(phi(v*y_j))_j.

For v,w not equal modulo sign, the corresponding quadratic polynomials
have squarefree quartic product. The same character bound, with the
zero input excluded, gives a constant-below-one agreement probability for
all sufficiently large p. A union bound makes H0 injective on G with
high probability. Exactly H1(u)=H0(u/r).

Take two independent uniformly sampled sets U,V in G, each of size
ceil(sqrt(|G|)). Their shifted intersection U/r intersect V is nonempty
with constant probability: its failure probability is at most
exp(-|U||V|/|G|). A fingerprint match gives r^2=(u/v)^2 and hence d.
Repeat within a fixed error budget and verify the final polynomial.
No primitive root, factorization of p-1 or discrete-log advice is used.

Total expected classical time, chosen queries and storage are
O(sqrt(p)*polylog(p)); fixed-budget bounded-error versions have the usual
logarithmic repetition factor. This baseline does not apply to a passive
sample-only model without paying its different data access. It does not
match the subexponential quantum bound, and its failure on a finite run
would not prove hardness. Its priority should be checked before any claim
of a new classical attack.

## 6. Cheap falsifiers for the earlier two-copy proposal

Let M=p(p-1)/2 be the number of irreducible monic quadratics, and define
|psi_f>=p^(-1/2) sum_x chi(f(x))|x>. For distinct f,h, put
sigma_fh=sum_x chi(f(x)h(x)). It is an odd integer, since all p summands
are nonzero signs. Hence the two-copy columns have overlap
(sigma_fh/p)^2>0 and cannot be columns of an isometry, notwithstanding
the affine invertibility of (b,c)->(f(x),f(y)) for x!=y.

The x=y sector is independent of f and has probability 1/p. Removing it
is cheap, but the remaining normalized overlap is

    (sigma_fh^2-p)/(p(p-1)),

which is still nonzero because the prime p is not an integer square.
For example, over F_5, f=X^2+2 and h=X^2+X+1 are irreducible and
sigma_fh=-3: the overlaps are 9/25 before projection and 1/5 afterwards.
This only refutes an exact-isometry interpretation, not approximate
collective discrimination.

For the specific controlled-candidate inversion construction, prepare a
uniform label f, apply the inverse known preparation of |psi_f>^tensor2
to |psi_h>^tensor2, and herald the data register being zero. Its exact
success probability is

    P_h=(1/M)*(1+sum_(f!=h) (sigma_fh/p)^4).

The Weil bound gives 1/M<=P_h<=1/M+81/p^2, hence Theta(p^-2). The
correct-label JOINT probability is exactly 1/M. Amplitude amplification
of this construction therefore costs Theta(p), exponential in log p.
This is not a lower bound against other implementations of a PGM.

There is also a paid extension-field factorization, but it does not remove
this issue. Embed the native |psi_f> in F_(p^2). For either root alpha of f,
chi_(p^2)(x-alpha)=chi_p(f(x)) on x in F_p. The known convolution unitary
U_q=C_q/p+J_q/p^2 has root amplitude (1-p^-2)/sqrt(p), since
sum_x chi_p(f(x))=-1. Root success is 2(1-p^-2)^2/p; amplification gives
O(sqrt(p)*polylog(p)) cost. This matches the classical exponent above.
Applying two such transforms to two copies gives only Theta(p^-2) success
on the ordered conjugate root pair. It is not a polynomial-time decoder.

## Review decision and limits

Accept the center-to-dihedral and constant-success width composition under
standard bit-output Q2 access, with the exact scope and error accounting
above. Priority is unverified. Keep novelty, speedup, hardness,
polynomial-time decoding, polynomial quantum space and Q1
transfer claims false. The strongest constructive classical baseline
identified in this review is O(sqrt(p)*polylog(p)), not only O(p).

No new numerical or circuit experiment was run for this review. The
algebraic examples above are exact derivations. Primary quantum sources
read: `../sources/legendre_prf/russell_shparlinski_0212016.txt`, Section 4;
`../sources/legendre_prf/kuperberg_0302112.txt`, Theorem 1.1, introduction
resource statement, and Section 5 Algorithm 2. Parent-side Sage checks and
separate prior-art review are distinct evidence and should be linked
without representing them as this reviewer's executed tests.

## Translation-Fourier block supplement

Independent algebra follow-up checked the positive-QFT formula
omega^(ka)B_k(r,d) and p^(-3/2) normalization in the topic note. For k!=0,
B_k(r,d)=B_1(kr,k^2d), and B_k is even in r and real. Irreducibility gives
B_k(0,d)=delta_(k,0)/sqrt(p); folding +/-r with sqrt2 leaves a square
nonzero-k width block. This is the block in the chosen organization, not a
universal decoder requirement or a supplied unitary. Measuring k erases
the center information. No paid conversion from toolbox A_gamma to this
block or its polar isometry was found, and no impossibility follows.

The separate exact Sage control at p37/43 completed after the pre-run
41-to43 correction and one Sage API fix. It checks composition identities,
not an implemented Kuperberg sieve or an end-to-end quantum decoder.

## Corrected oracle boundary and concrete affine circuit

Independent follow-up accepted the reference compiler H_B, CSWAP(X,R),
uncontrolled U_g(R), CSWAP(X,R), H_B with R=x0. Its exact action is
 g(x0)|x,B XOR L_g(x) XOR L_g(x0),x0>,
valid on arbitrary coherent or entangled inputs with one phase query.
The fixed global complement preserves all fingerprints. Relative candidate
verification has agreement (1+sigma S_fh/p)/2, bounded using |S_fh|<=3sqrt(p).
Raw phase access does not have an ordinary classical sign-query model;
retain the saved classical attack's original bit interface. Copies alone
do not supply this construction; no copies-only impossibility is claimed.
The old contrary phase-only assertion is superseded, while the original
bit-oracle upper bound remains valid. Separate p5/7 exact circuit control
passed2558 basis cases, with1248 omitted-swap negative failures.

The independently derived affine-evaluation/projection circuit has clean
block K_off/alpha, alpha=(p-1)sqrt(p(p-1))/p. Its irreducible-column herald
and reverse correct-label probabilities are1/(p-1)^2. The toolbox root-ratio
cleanup does not remove this specific circuit's missing evaluations. A
uniform perfect-square input also rules out a constant-normalization block
for the unrestricted ALL-monic matrix, not for the native irreducible
restriction. No alternate constant-normalization circuit was found.

The homogeneous-line supplement was independently checked: positive 2D QFT
sends every balanced projective coloring to its perpendicular-line coloring,
with zero at0. Normalized direct Fourier probabilities are exactly
1/(p^2-1) off zero, while the amplitudes still retain the coloring. The p7
plus-set{0,1,3} has no reflection center and is a nonquadratic example. The
original bit oracle pays the homogeneous PHASE preparation in one query
using |+>/|-> routing. The relative-bit compiler does not by itself fix the
absolute infinity orientation; the phase-only recovery extension uses no
homogeneous lift. No general readout or decoder impossibility is asserted.
