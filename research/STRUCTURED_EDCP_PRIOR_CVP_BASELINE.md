# Structured EDCP: A Prior-Aware Classical Lattice Decoder

Date: 2026-09-24. LOCAL DERIVATION / REVIEW PENDING.

This pass derives a concrete baseline for the actual local Fourier data and
a Gaussian coefficient secret prior. It reuses the repository's exact Babai
helper in bounded trials. It does not provide a scaling guarantee, a verified
MLWE attack, a new quantum algorithm, or production integration.

The EDCP/LWE connection is already established in
[Brakerski, Kirshanova, Stehle and Wen](https://arxiv.org/abs/1710.08223).
The structured source and its balanced coefficient evaluation are from
[Wen and Zheng](https://eprint.iacr.org/2026/155.pdf), especially Definitions
16-17 and Theorem 4. This note specifies the local baseline and its error
accounting; it is not a claim to have discovered that connection.

## 1. Why The Existing Subset-Sum Embedding Is Not The Baseline

The repository already has exact-rational LLL/Babai and fiber-entanglement
analyses for scalar DCP subset sums. Their Boolean witnesses and uniform
target distributions are not the Gaussian coefficient prior considered here.
Reuse arithmetic helpers, not those source contracts or success statistics.

From `research/STRUCTURED_EDCP_LOCAL_READOUT_BASELINE.md`, local measurements
give

    Y_(l,i) = q^i*<a_l,s> + E_(l,i) mod Q,  Q=q^d+1.

The true noise is the SQUARE of a periodized Fourier Gaussian amplitude.
Replacing it by a periodized Gaussian probability requires a bound; section 2
provides one. The source reduction's secret is a coefficient Gaussian passed
through balanced evaluation, not uniform over all Q^n possible secrets.

If the secret coefficient vector is v in Z^(n*d), write

    s_j = sum_(k=0)^(d-1) q^k*v_(j,k) mod Q.

This agrees with the source's balanced coefficient reduction whenever every
coefficient lies in ( -q/2, q/2 ]. For odd q and R_s=(q-1)/2, a Gaussian
probability prior proportional to exp(-pi*||v||^2/r_s^2) leaves that box with
probability at most

    n*d*r_s^2/(pi*R_s) * exp(-pi*R_s^2/r_s^2).

Charge this prior-tail event when replacing the full source prior by the
unwrapped evaluation model. Unsigned coefficient residues are NOT a valid
substitution: at q=5,d=2, coefficients (-1,0) evaluate to 25 modulo 26,
whereas unsigned residues (4,0) evaluate to 4.

## 2. A Charged Wrapped-Gaussian Approximation

Set u=e/Q and

    H(u)=sum_(k in Z) exp(-pi*sigma^2*(u+k)^2),
    D(u)=sum_(k in Z) exp(-2*pi*sigma^2*(u+k)^2).

The actual periodized-source readout law is nu(e) proportional to H(e/Q)^2.
Let nu0(e) be proportional to D(e/Q). It is the law modulo Q of an INTEGER
discrete Gaussian with probability width

    r_e = Q/(sqrt(2)*sigma),
    Pr[integer error=z] proportional to exp(-pi*z^2/r_e^2).

Let X(u)=H(u)^2-D(u), which is nonnegative. Summing cross terms over all
residues gives

    sum_e X(e/Q) / sum_e D(e/Q)
      = sum_(delta != 0) exp(-pi*sigma^2*delta^2/2)
          * Z_(delta/2)/Z_0,
    Z_c = sum_(j in Z) exp(-2*pi*sigma^2*(j/Q+c)^2).

The shifted lattice Gaussian sum Z_c is maximized at c=0, by Poisson
summation and positivity of its Fourier coefficients. Therefore the ratio
is at most

    rho = 2*exp(-pi*sigma^2/2)/(1-exp(-3*pi*sigma^2/2)).

The actual law is a mixture of nu0 and the normalized positive cross terms.
It follows that

    TV(nu,nu0) <= rho/(1+rho).                                (1)

For Q even the lattice shift delta/2 always lies on the 1/Q grid, so the
exact cross-term ratio equals sum_(delta!=0) exp(-pi*sigma^2*delta^2/2).
For d*L independent measured coordinates, total variation is at most
d*L*rho/(1+rho). Add physical source, periodization and QFT errors from the
preceding note separately. No assumption about the eventual decoder is needed
to transfer a success probability by this total-variation bound.

This approximation is NOT exact at finite sigma. At Q=10,sigma=1 the total
variation exceeds 0.05. Discarding interference without charging it would
already misstate that small instance.

## 3. The Exact Weighted Graph Lattice

Put r=n*d, m=L*d. Build the INTEGER matrix F of shape m by r:

    F_((l,i),(j,k)) = a_(l,j)*q^(i+k) mod Q.

Then F*v mod Q is exactly the predicted local measurement vector. Columns
are not independent random LWE samples: the geometric powers are retained.

Under the nu0 model, let v have probability width r_s and the integer error
e have width r_e independently. For observed y, the posterior of the joint
integer variables (v,k), with e=y-F*v-Q*k, is proportional to

    exp(-pi*(||v||^2/r_s^2 + ||y-F*v-Q*k||^2/r_e^2)).

With w=r_e/r_s, define the column basis and target

    B_w = [ w*I_r    0   ],     t = (0_r,y),
          [   F     Q*I_m ]

so that

    t-B_w*(v,k) = (-w*v,e),
    ||t-B_w*(v,k)||^2 = w^2*||v||^2+||e||^2.

Thus JOINT-lift MAP is exactly weighted CVP. The dimension is
D=d*(n+L), and det(B_w)=w^r*Q^m. Constant module rank n does not make
this a constant-dimensional integer program: there are m modular lift
variables and n*d secret coefficient variables.

An efficiently computed lattice vector is only a decoder candidate. Neither
writing down this basis nor solving the corresponding REAL least-squares
problem solves integer CVP. The latter would discard the modular carries.

### Joint MAP Is Not Marginal MAP

The most probable SECRET sums the posterior over its possible noise lifts
and coefficient representatives. Minimizing one squared distance instead
selects the largest individual joint term. Those objectives can differ.

A direct countercontrol uses modulus 5, scalar coefficient v with Gaussian
probability width r_s=3, sigma=2, label a=1 and observation y=2. Joint-lift
MAP selects v=1; summing over lifts and coefficient aliases makes secret 2
more probable than secret 1 by a factor approximately 1.12043454.
This is an objective-scope counterexample, not a new candidate family.

The CVP baseline remains legal and useful, but do not label it exact
marginal maximum likelihood or infer information failure from its failure.
Bounding the dominant-posterior term versus the full posterior is a separate
possible route to certifying it in a particular source regime.

## 4. Precision, Prior Weighting And Implementable Baselines

For an integer or rational weight w_hat=p/D0, use the integer column basis

    [ p*I_r       0      ]
    [ D0*F     D0*Q*I_m ]

and target (0,D0*y). This represents the weighted lattice after a global
scale factor D0, preserving the intended nearest-vector objective. The
integer entry bit lengths are O(log Q+log p+log D0); the decoder needs
polynomially many entries, not a Q-sized table.

A changed weight corresponds to prior width r_s'=r_e/w_hat. It is not
silently the same prior. For upward rounding w_hat>=w and a coefficient box
|v_i|<=R_s, let

    Delta = pi*r*R_s^2*(w_hat^2/r_e^2 - 1/r_s^2).

The ratio of unnormalized restricted-prior probabilities lies between
exp(-Delta) and 1. The two NORMALIZED restricted priors consequently have
total variation at most 1-exp(-Delta). Add excluded prior mass separately
when using a full Gaussian. Rational weights can make this charge small;
do not assume an unknown CVP decision gap makes rounding harmless.

The bounded trials used the simple heuristic W=ceil(w), without claiming
Bayes optimality for the original prior. The box-based prior-error upper
bounds were 0.0336532 for q=17,d=4,r_s=2 and 0.000551934 for
q=5,d=8,r_s=1.5. These conservative charges are retained, not erased because
the numerical weight differences look small.

The directly reusable routine is `exact_babai_nearest_plane` in
`theorems/dcp_subset_sum_affine_cvp_baseline.py`. It expects ROW basis vectors,
so apply LLL to B_w TRANSPOSE, with the rational scaling above when needed.
Validate every output's first r coordinates and its modular graph relation.
The planted secret is used only to score reference trials, never by the
decoder, basis reduction, nearest-plane step or parameter selection.

A meaningful next comparison is LLL/Babai versus bounded list decoding and
BKZ on this SAME source. Charge list width, reduction block size, dimension,
bit precision, memory and preprocessing. An exact exponential CVP solver is
a useful small reference, not a supplied polynomial subroutine.

## 5. What Increasing q Does And Does Not Buy

For smooth Gaussian priors and errors, with the exact weight w, the planted
residual has expected squared norm approximately D*r_e^2/(2*pi). Meanwhile

    det(B_w)^(1/D) = Q/(sqrt(2)*sigma*r_s)^(r/D).

Its typical radius divided by sqrt(D)*det(B_w)^(1/D) therefore scales as

    (sqrt(2)*sigma*r_s)^(r/D)/(2*sqrt(pi)*sigma).

If sigma=d^b and r_s=d^c with fixed n,L, the power of d is

    -b+(b+c)*n/(n+L) = (c*n-b*L)/(n+L).

The huge modulus Q cancels from this normalized volume comparison. Increasing
q alone therefore does not improve THIS ratio or supply a better reduced
basis. These are a determinant identity and Gaussian-moment proxy, NOT a
shortest-vector lower bound, a uniqueness theorem, or an LLL success theorem.
The lattice is highly structured; applying a random-lattice heuristic as a
proof would be unjustified. Adding blocks changes both information and D.

## 6. Bounded Verification And Outcomes

Thirty numerical distribution checks covered Q in {5,10,17,26,65} and
sigma in {0.6,1,1.4,2,3,4}. All satisfied the cross-term identity and (1).
At Q=26 the observed TV values and bounds were:

| sigma | Actual TV | Bound |
|---:|---:|---:|
| 1 | 0.07771199 | 0.29554044 |
| 2 | 0.003159799 | 0.003720989 |
| 3 | 1.428371e-6 | 1.449893e-6 |
| 4 | 2.430692e-11 | 2.432312e-11 |

Forty-eight planted bounded trials used n=1, sigma=4 and the ACTUAL local
Fourier noise nu, not an uncharged Gaussian substitute. Secret coefficients
were sampled from the indicated Gaussian probability prior conditioned on
the balanced coefficient box. Labels were independent uniform; none were
selected using the secret or retained only after successful recovery.

| q,d,r_s | L | Lattice Dimension | Recovered / 8 | Zero Predictor / 8 | Definite CVP Misses |
|---|---:|---:|---:|---:|---:|
| 17,4,2 | 1 | 8 | 3 | 0 | 3 |
| 17,4,2 | 2 | 12 | 7 | 0 | 1 |
| 17,4,2 | 3 | 16 | 8 | 2 | 0 |
| 5,8,1.5 | 1 | 16 | 4 | 0 | 4 |
| 5,8,1.5 | 2 | 24 | 4 | 0 | 4 |
| 5,8,1.5 | 3 | 32 | 4 | 1 | 4 |

A definite CVP miss means Babai returned a vector farther from the target
than the KNOWN planted lattice point; that is an optimization failure, not
missing information. Other incorrect secrets might reflect posterior
ambiguity, weight approximation, or an optimization failure not certified
by this one comparison. Successful coefficient and evaluated-secret counts
coincided in these trials. Eight trials per point are not a reliable scaling
estimate and no asymptotic inference is made from them.

Reproduction contract: case order is the table order; NumPy default_rng seed
20260924+case_index; W=7383 and 46036 respectively; SymPy exact LLL delta=3/4;
the existing exact-rational Babai helper; draws per trial are labels, secret
coefficients, then noise residues. Noise references used a Q-entry positive
table from H with image indices -3,...,3, whose omitted tail is negligible
here. This DENSE SOURCE REFERENCE is not a scalable sampler or a decoder
resource claim. The CVP calculation itself does not use that table.

All 48 instances passed exact determinant, planted-residual, coefficient
divisibility and output graph-relation checks. Another 32 exact checks covered
n=2 at (q,d,L)=(3,2,1),(3,2,2),(5,4,1),(5,4,2), validating vector-module
evaluation and the same lattice identities. The unsigned-secret and
joint-versus-marginal MAP countercontrols both failed the intended false claim.

No production module, CLI workflow, registry promotion, bulk test suite or
new commit was produced. The first helper import needed the repository's
normal `core` and `theorems` paths; the corrected bounded run finished normally.

## 7. Handoff And Research Decision

GEMINI: implement `theorems/structured_edcp_prior_cvp.py` using the existing
exact arithmetic helper. Preserve source conventions, actual-noise versus
surrogate-noise distinction, prior tails, rational weights, determinant and
modular checks, and the MAP counterexample. Implement a scalable verified
noise sampler before running large cases; never quietly reuse the Q-entry
reference generator. Keep decoder inputs independent of scoring secrets.
Record reduction failures and definite optimization misses separately from
information failures. Connect the actual secret prior to the source audit.

MAIN MODEL: do not reinterpret small Babai successes as a breakthrough or its
failures as a hardness result. Seek a source-specific integer operation that
beats this baseline with a stated success guarantee, or a collective quantum
measurement with better total cost. Prior-aware inference is now a concrete
weighted-lattice problem rather than an unspecified classical competitor.
The remaining question is how to solve it, not whether a cost function can
be written down.
