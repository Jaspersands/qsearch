# Full Physical Output Sampling With An Explicit Interference Budget

Date: 2026-10-24. LOCAL, UNREVIEWED theorem and classical implementation.
No universal dequantization, hardness, novelty or quantum speedup claim.

## 1. Scientific Question And Exact Target

The preceding pass estimates decoded Pauli observables but does not sample
the full physical output. An additive prefix-probability estimator cannot
be converted to such a sampler without paying for tiny denominators. This
pass instead uses a direct joint proposal, never sequential conditioning.

Use exactly the public physical Pauli input and deterministic decoder of
../hdqi-decoded-observables-2026-10-24/DECODED_OBSERVABLES.md. Write the binary
Pauli map B=[X;Z], where X,Z are n-by-m matrices. Its actual output is

    |Psi>=sum_y psi_y |R(y)> |P(y)>,
    R(y)=y xor Dec(By), psi_y=a_y/sqrt(Z_hat).              (1)

The target law measures BOTH physical halves in the computational basis
and optionally records R. Discarding the right half and R gives the physical
Gibbs-register output law of this actual circuit. It need not equal the
desired Gibbs law unless the separate decoder/thermal guarantees hold.

The existing Bell-label pushforward theorem does not give this law: Bell
measurements and computational-basis measurements are different tasks.
A one-site Z Hamiltonian already falsifies that substitution.

Sparse-operation classical simulation is established prior art; see
[Van den Nest](https://arxiv.org/html/0911.1624). The construction here uses
sampled SIGN MEANS rather than assuming efficient exact pilot amplitude
evaluation. No generic simulation principle is claimed as new.

## 2. Enumerating The Interfering Labels, Not Inverting A Decoder

For a measured right-half string b and left-half string a, the contributing
Pauli labels have Xy=a xor b. For a fixed residue R and this X syndrome,
define the fiber

    F(R,u)={y: R(y)=R, Xy=u}.

Distinct labels in a fiber have DISTINCT full B syndromes. Indeed, equal
By and equal R imply equal y. Put

    k=rank(B)-rank(X)=dim Z(ker X), L=2^k.                 (2)

There are at most L possible Z syndromes at a fixed X syndrome, hence every
fiber has size at most L. The rank is computed from the explicit Pauli list,
not inferred from pilot samples or from decoder performance.

Given any representative y0, set R=R(y0), s0=B y0. Enumerate h in the
subspace Z(ker X). For each syndrome s=s0 xor (0,h), compute

    y=R xor Dec(s),

and retain it only if B y=s. This lists the EXACT fiber containing y0 with
L forward decoder calls. No inverse decoder, amplitude oracle or search
over all 2^m pilot labels is needed. The argument holds for bad decoders too.
The decoder is assumed total, deterministic and efficiently computable;
its actual runtime is charged. A decoder callback is not itself a complexity
certificate.

RREF of the row list of B's columns, with X coordinates preceding Z,
directly gives a basis of im(B) intersect ({0} x F_2^n): keep its rows with
zero X part. The implementation reuses the repository's exact prime-field
row-reduction helper at p=2. Rank computation is polynomial; enumeration
is explicitly EXPONENTIAL in k.

## 3. Joint Proposal And Exact Interference Envelope

For now use the exact product envelope q and conditional means r_y from
the signed-word construction:

    psi_y=sqrt(C) s_y sqrt(q_y) r_y, C=Z_commuting/Z_hat.

Draw y0~q, draw b uniformly from n bits, and output the provisional event
(R(y0), a=b xor Xy0, b). Its proposal probability is

    h(R,a,b)=Q_F/2^n, Q_F=sum_(y in F) q_y.

Write the ordered physical product as P(y)=i^p X^x Z^z. Its amplitude on
the measured pair contributes i^p (-1)^(z.dot(b)). Include the known
coupling/length sign s_y in a phase theta_y(b) in {1,-1,i,-i}. Define

    S_F=sum_(y in F) sqrt(q_y),
    A_F(b)=sum_(y in F) sqrt(q_y) r_y theta_y(b).

The target event probability is C |A_F(b)|^2/2^n, and

    |A_F(b)|^2<=S_F^2<=L Q_F.                            (3)

Thus accept the provisional event through a first factor S_F^2/(L Q_F).
To estimate its remaining interference, choose y in F with weights
sqrt(q_y)/S_F, draw one independent conditional word sign sigma at y,
and let zeta=theta_y(b)*sigma. This is a unit complex number and

    E[zeta]=A_F(b)/S_F.

With K independent zeta draws, use a SECOND acceptance probability
|sum zeta|^2/K^2. It is always in [0,1], including for complex phases.
Its exact mean is |E zeta|^2+(1-|E zeta|^2)/K. It is NOT unbiased.

Let D=sum_y q_y r_y^2=1/C and Z_S=sum_F S_F^2. The output is the mixture
of the true target and a normalized positive envelope, with contamination

    alpha=Z_S/[(K-1)D+Z_S].                              (4)

The normalization identity used here is

    sum_(F,b) |A_F(b)|^2/2^n=sum_y q_y r_y^2=D.           (5)

For distinct labels in the same fiber the Z syndromes differ; uniform b
annihilates the cross term. This is also the isometry of the actual decoder
circuit, not a decoder-success assumption. Moreover D<=Z_S<=L. Therefore
the success probability of one full trial is at least D/L, and (4) gives
alpha<=L/[(K-1)D]. No particular rare event probability is divided out.

## 4. Rational Probabilities And A Full Error Budget

Use eps,delta in (0,1/4], the analytic integer bound C_bar from the preceding
passes, and rational truncated word/proposal laws q',r' with

    eta=eps^2/(16384 m C_bar^2).

Compute rational LOWER square roots w_y of q'_y with relative error at most
nu<=eps/(64 C_bar), using the preceding integer-square-root routine. Zero
probabilities are omitted; positive probabilities retain positive weights.
Now use Q_F=sum_F q'_y, S_F=sum_F w_y and weights w_y/S_F. All proposal,
first-stage and second-stage acceptance probabilities are exactly rational.
Because w_y<=sqrt(q'_y), the bound S_F^2<=L Q_F still holds exactly.

The finite weighted success vector on pilot labels is

    v_w(y)=s_y w_y r'_y.

The preceding count-truncation proof gives distance at most eps/(16 C_bar)
from v'(y)=s_y sqrt(q'_y)r'_y to the exact vector
v(y)=a_y/sqrt(Z_commuting). Weight rounding adds at most nu in Euclidean
norm. Thus

    ||v_w-v||<=5eps/(64 C_bar),
    D_w=||v_w||^2>=1/(2 C_bar).

Normalizing and applying the actual decoder isometry and measurement gives
TV at most 5eps/(32 sqrt(C_bar))<eps/4. This comparison does not depend on
the number of trials or on the probabilities of individual outputs.

The same exact mixture calculation applies to w_y,r'_y. Its envelope obeys
D_w<=Z_S<=L sum_y w_y^2<=L. Choose

    K=1+ceil(8 C_bar L/eps),
    r=ceil(log_2(1/delta)), T=2 C_bar L r.                 (6)

Then alpha<=eps/4, and trial success is at least 1/(2 C_bar L). After at
most T independent trials, failure probability is <=exp(-r)<=delta. Return
explicit FAILURE if all trials reject. Conditional on success, the output
has TV error less than eps/2<eps from the exact actual-decoder output law.

Worst-case work is T fiber enumerations and at most T*K signed words, with
finite word lengths, rational bit costs, Pauli arithmetic and L forward
decoder evaluations per enumeration charged. The source-residue calculation
costs one further decoder call per trial. Large k is rejected BEFORE its
fiber is expanded. All random draws assume independent random bits; seeded
PRNG executions are reproducibility checks, not proofs of independence.

## 5. Scope And Falsifiers

This is a polynomial classical full-output sampler when C_bar is polynomial,
k=O(log(input size)), and the decoder is polynomial. It samples the measured
joint law directly, rather than falsely deriving it from additive Pauli
estimates. It preserves physical Y/product phases and correctly handles
noninjective B, bad decoders and zero source probabilities.

The criterion is BASIS DEPENDENT: it concerns the requested physical
computational basis. Arbitrarily rotating that basis changes the problem.
The actual maximum fiber may be much smaller than 2^k; the current bound
is sufficient, not necessary. For n independent commuting Z generators,
k=n and this generic enumerator refuses, although the physical output is
just an easy product thermal distribution. This explicitly falsifies any
interpretation of large k as a hardness certificate.

Do not confuse missing source phases with incoherent probability addition.
For one Z generator and a correct decoder, the left marginal is thermal
and biased, whereas sampling a Bell label and forgetting its phase gives
a uniform computational marginal. The finite controls check this difference.

Generic high-rank measurements remain open. The recent DQI literature also
warns against equating a mixing barrier with a quantum advantage: the
[shattered-phase paper](https://arxiv.org/abs/2609.40345) gives a classical
Prange-based sampler in a regime where stable algorithms fail. The
[MCMC comparison](https://arxiv.org/abs/2607.28120) is empirical, not a
general polynomial mixing theorem. Neither is used as a proof of (6).

## 6. Decision

Rule out a sampling-advantage claim based only on small measurement-fiber
rank plus polynomial sign cost. A remaining candidate must specify an
operational output beyond this theorem, pay for its quantum source/decoder,
and survive direct classical attacks. In particular, high rank by itself
does not qualify. The next research choice should compare a concrete
high-rank sampling task against the broader degree-scale preparation problem,
not continue adding finite low-rank examples.

## 7. Independent Shortcut: Commuting Input And A Linear Decoder

A separate construction samples the physical LEFT register for EVERY k
when all physical P_i commute and the decoder is an explicitly supplied
linear map D with B D B=B. This is not an assertion about the joint two-half
law above. The right-inverse condition is checked on every generator column;
linearity is part of the matrix representation, never inferred from samples.

The commuting pilot is the exact product of normalized
cosh(beta J_i/2)|0>-sinh(beta J_i/2)|1>. Its X_i expectation is

    t_i=-tanh(beta J_i).

Let z range over the diagonal subgroup K={z:(0,z) in im B}, whose dimension
is the same k as above, and put h=D(0,z). Then Bh=(0,z). Since all generators
commute and square to identity, P(y xor h)=P(y)P(h), with NO omitted
commutation phase. Write P(h)=(-1)^e(z) Z^z. The decoder-pullback formula
therefore gives

    E[(-1)^(z.dot(output))]=(-1)^e(z) prod_i t_i^h_i.     (7)

The phase e is linear on K: both h and P(h) multiply linearly here. For
z outside K the expectation is zero. This covers every diagonal Fourier
character, not merely single-bit marginals.

Choose a basis z_1,...,z_k of K. Independently draw bits W_i with
E[(-1)^W_i]=t_i. Set the right-hand sides

    b_j=e(z_j) xor (h_j.dot(W)), h_j=D(0,z_j).

Finally draw a uniform solution x to the k independent binary equations
z_j.dot(x)=b_j. Such a solution always exists. Characters outside K vanish
under its uniform free variables; characters in K have exactly (7).
Uniqueness of the finite Fourier transform proves equality of the ENTIRE
left-register output law. Cost is polynomial binary arithmetic, with no
2^k enumeration, sign-ratio penalty, Markov chain or rare conditioning.

For finite rational inputs use retained E_i,O_i at x_i=beta|J_i|/2 and

    t'_i=-sign(J_i) 2E_i O_i/(E_i^2+O_i^2).

These are exact rational biases in [-1,1]. With parity-weight tail at most
eta, the earlier e-E<=eta, o-O<=eta/2, e<2,o<1 bounds give numerator error
<=4eta and denominator error <=5eta. The ratio error is <=9eta, so each
coin TV error is <=5eta. Taking eta=eps/(16m) yields output TV <eps by
product coupling and deterministic/randomized classical postprocessing.
Independent free-variable bits are included in that postprocessing.

This shortcut again targets the ACTUAL decoder output. A linear decoder
need not successfully recover most pilot labels, and then its output may
not approximate the desired Gibbs state. Conversely, a diagonal commuting
input with an efficient NONLINEAR decoder does not inherit this theorem.
Neither does a noncommuting input or joint purification measurement.
The implementation rejects a purported linear decoder that fails BDB=B.

The updated research boundary excludes ordinary linear syndrome decoding
on commuting Hamiltonians as a basis for a left-output sampling advantage.
High rank alone is insufficient even when the low-rank enumerator refuses.

