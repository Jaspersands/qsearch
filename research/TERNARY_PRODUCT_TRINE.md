# Native Product-Trine Readout And Joint Classical Baseline

LOCAL DERIVATIONS / REVIEW PENDING. Explicit measurement access and a scoped
record bound, not an efficient native decoder, a general LOCC lower bound,
an accepted algorithm candidate or a novelty claim.

## What This Changes

The full-root paired covariant measurement already has a physical two-register
QFT implementation. It also admits an exact randomized ONE-qutrit realization.
This reduces measurement workspace, not the unresolved classical decoding cost.
Fixed inverse-F3 measurements have a different record law; their exact joint
posterior can nevertheless reuse the existing cyclotomic likelihood algebra.
The implementation explicitly separates algebra reuse from generative-model
reuse. Local readout gates do not imply small word-basis coherence radius.

## Randomized Physical Compiler

Let q=3^r, Q=q/3, and let psi be ANY normalized qutrit state. Independently
sample public alpha,beta uniformly in Z_q using 2r random trits. Apply

    diag(1,chi_q(-alpha),chi_q(-beta)), inverse F3, measure z in F3.
    Report y=(alpha+Q*z,beta+2Q*z) modq.

For fixed y,z the unique settings are alpha=y1-Qz, beta=y2-2Qz. The branch
probability is

    |psi0+psi1*chi_q(-y1)+psi2*chi_q(-y2)|^2/(3*q^2).

Consequently E_(y,z)=E_y/3, with E_y=v_y*v_y^dagger/q^2 and
v_y=(1,chi_q(y1),chi_q(y2)). Root orthogonality gives sum_y E_y=I.
The extra pointer z is uniform and independent of the input conditional on y.
Retaining settings and pointer therefore supplies no more classical input
information than y plus an independent random trit. For the native phase
qutrit this is EXACTLY the existing paired covariant noise law.

There are no clean quantum ancillas, unknown-state inverse, chosen source
labels, full q^2 table or postselection. Public phases still require synthesis:
diagonal/F3 operator-norm errors e_D,e_F and settings-distribution TV error g
give outcome TV at most min(1,e_D+e_F+g), by unitary telescoping, pure-state
trace distance and measurement contraction. Source-preparation error is not
included. The gate recipe is not hardware gate export. Arbitrary input-state
controls compare every branch against the actual existing two-register gate
tape through q=27. Linearity of the effect identity covers mixed inputs too.

## Fixed Product Fourier Records And Exact Joint Decoder

With alpha=beta=0, one native qutrit with rows a,c produces only z, with

    p(z|s)=|1+chi_q(a.s)*omega^(-z)+chi_q(c.s)*omega^(-2z)|^2/9.

For each fixed observation this equals (q^2/3) times the paired covariant
likelihood at the synthetic outcome (Qz,2Qz). This constant cancels from a
Bayesian posterior, but MUST NOT be used to transfer the distribution or its
copy bounds. `TrineRecord` is a separate validated type. The private adapter
calls the existing exact 7-term sparse phase expansion and restores the actual
one-digit observations and model tag, even when the reference budget runs out.
Zero-likelihood data has no posterior; undecided numerical ordering has no
fabricated trit certificate. Distinct ancestor IDs are necessary, not sufficient
to establish statistical independence. The generic 7^(M/2) expansion remains
exponential, with its storage, update and join costs charged.

## All-Secret Gram And Copy Gate

Take the reference distribution Q0 uniform on IID full a,c and on z in F3.
The likelihood density L_s=3p(z|s) has one identity and the six A2 root terms.
Character orthogonality over a,c,z implies EXACTLY

    <L_s-1,L_t-1>_Q0 = 0 for s != t,
                       2/3 for s=t !=0,
                       2 for s=t=0.

Indeed the 36 root pairs require u*s+a*t=v*s+b*t=0 modq and
u+2v+a+2b=0 mod3. Nonparallel root rows have unit determinant, forcing s=t=0.
Parallel equal rows would require s=-t, but fail the z condition; opposite
rows require s=t. At zero there are 18 admissible ordered pairs, not six.
This covers nonprimitive secrets over the composite ring as well.

For M independent original records, off-diagonal product Gram entries remain
zero, while the centered diagonal is d=(5/3)^M-1 for every nonzero secret
and d0=3^M-1 at zero. Blindly importing the existing covariant Gram is wrong.

Here is a bound for ANY classical joint classifier h_t in [0,1], sum_t h_t=1,
under ALL uniform secrets, G=q^n. Define, over nonzero secrets,

    B_t=sum_(s!=0) [(3/G)*1(s_j mod3=t)-1/G]*(L_s^(M)-1).

Each B_t has reference mean zero and squared norm at most 2d/G. Its contribution
to correctness minus 1/3 is (1/3) E_Q0 sum_t h_t B_t. Replacing h_t with
h_t-1/2, bounding by 1/2 and using Cauchy-Schwarz bounds that contribution by
sqrt(d/(2G)). The omitted zero term is

    (1/G) E_Q0 h_0*(L_0^(M)-1) <= TV(P_0,Q0)/G
                                      = (1-3^(-M))/G.

The equality uses L_0^(M)=3^M*1(all digits zero); labels remain uniform.
Hence mean least-trit advantage is at most

    min(2/3, sqrt(((5/3)^M-1)/(2G)) + (1-3^(-M))/G).

At the current M=nr-2 native budget this decays exponentially. Unlimited
classical postprocessing cannot rescue this SPECIFIC readout. A polynomial
surplus of copies is not excluded by this inequality. Other bases, adaptive
LOCC, collective quantum measurements, chosen labels, retained sieve laws and
worst-case per-label statements are outside its scope.

## Physical Countercontrol: Local Marginals Are Not Enough

At q=81,n=1,r=4,M=2, choose the legal native full rows (1,2),(26,52).
Each single-qutrit secret-trit twirl is I/3. Nevertheless separate inverse-F3
readouts have informative JOINT outcomes. At output (0,0), the trit-conditional
probabilities are 19/81,4/81,4/81, and complete joint MAP success is 19/27.
All six single-output marginals remain 1/3. Native labels are reconstructed
through the actual ideal chart; dense physical twirls keep ALL 81 secrets.
Exact cyclotomic character counts and the joint posterior independently agree.

This is a prespecified source-valid mathematical countercontrol, NOT a generated
oracle problem, an IID source guarantee or a proposed algorithm. The final
tensor-product rank-one effects have word Hamming radius M=2 despite using
zero entangling readout gates. Thus a radius-one final-effect bound must not be
misrepresented as an exclusion of every local-gate measurement.

## Next Decision And Falsifiers

Do not repeat fixed product Fourier readouts at M=nr-2 expecting a population
weak learner. Do not treat the simple randomized compiler as solving decoding.
Investigate label-dependent measurement policies or collective observables
that change the Gram/source-access calculation; charge their source copies
and compare them with this exact joint classical baseline. Alternatively,
investigate the sample surplus at which randomized covariant records become
algorithmically decodable, without substituting chosen labels for IID labels.

Falsifiers are mismatched arbitrary-input branch effects, an incorrect exact
zero/nonprimitive-secret Gram, posterior disagreement with actual likelihoods,
or loss of the claimed joint signal under the real all-secret native twirl.
Finite checks support the algebra but do not constitute a proof or novelty
review. No claim promotion is authorized.

```
python theorems/ternary_product_trine.py --write
node research/certificates/ternary_product_trine_crosscheck.js
python -m pytest -q tests/test_ternary_product_trine.py
```
