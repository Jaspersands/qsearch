# Native Level3: Conditional Phase Lift, Not A Complete Receiver

CORRECTED2026-10-13. The former full-recovery and universal tree-barrier
claims are withdrawn. Historical code, report, document, tests and checker
are preserved in quarantine/nil3_claimed_receiver/. Their positive flags
were not evidence of an implemented quotient receiver.

## What Was Wrong

The former "end-to-end simulation" set recovered_s0=s0 and recovered_s1=s1.
It generated an ideal residual directly from s2, rather than obtaining it
from original samples with lawful known-parameter gates. These are
oracle-assisted fixtures, not recovery of unknown data.

It also replaced the actual ring O/(pi^3), O=Z[zeta3], pi=zeta3-1, with
F3[pi]/(pi^3). Those rings differ. Since pi^2=-3*zeta3, the native quotient
has characteristic9, with additive group Z9 x Z3. In its power-basis chart,

    ideal HNF=(9,6,3), three times1=(3,0)!=0,
    pi^2=(6,0).

The incorrect coordinate program sets three times1 to0. Worse, its
purported hidden generator with x=2,y=z=0,t=1 cubes to z=2, not identity.
The true native generator(-s,1) cubes to identity because
1+zeta3+zeta3^2=0. The corrected producer uses the existing
cyclotomic_rescaling_gate.py and NativeGroup backend, with all carries paid.

## The Honest Constructive Component

INPUT: original ideal native qutrit samples and their public labels, plus
ACTUALLY KNOWN lower quotient values s mod pi^2. This pass does not supply
the procedure that learns those lower values.

For each coordinate, choose the canonical level2 representative l and
lift it into the level3 ring. The unknown residual is pi^2*u, u inF3.
The original supplied state is

    |psi_a^s>=1/sqrt3 sum_j chi_a(lambda_j*s)|j>,
    lambda=(0,1,1+zeta3).

Using ONLY public a and known l, apply

    D(a,l)=diag_j chi_a(-lambda_j*l).

All exponents are exact multiples of1/9 in the actual native chart.
Since zeta3 acts trivially on pi^2 and lambda_j*pi^2=j*pi^2, the residual is

    1/sqrt3 sum_j omega3^(j*k)|j>,
    k=sum_i central_character(a_i)*u_i mod3.

The central coefficient is computed by the existing exact pairing:
central_character(a)=3*pairing(a,pi^2,level3) mod3. In this chart it is
2*(a0+a1) mod3, not an unspecified free label digit. Fourier measurement
reveals k deterministically for an IDEAL sample with the CORRECT known lower
premise. Wrong lower information can yield a non-deterministic residual.

The new conditional_phase_lift(sample,known_lower) never takes an unknown
top secret. SuppliedPhaseSample holds the public label and the input state
used for numerical circuit conformance. The only true secrets appear in
producer/test fixtures that generate original samples. This is not a grant
of physical classical access to unknown state amplitudes.

recover_top_digits(samples,known_lower,rng) uses a finite supplied batch,
records actual simulated measurement outcomes, solves full-rank F3 equations,
and charges all consumed samples. Insufficient labels return UNKNOWN/no
recovered digits, not a free extra source, pseudoinverse guess or postselection.
There is no assignment of an unknown secret to a recovered output.

The report checks ALL729 scalar combinations: nine known lower
representatives, three residual digits, and27 original labels. Each retains
source exponents, correction exponents, exact residual phases and numerical
Fourier conformance. Three vector batches use independent original labels
and explicit known lower inputs. These are CONDITIONAL recovery experiments,
not complete StateHSP or LWE algorithm executions.

Universal hardware compilation, finite precision, noisy source composition,
and a complete lower-quotient receiver remain open. No quantum speedup is
admitted. A correct conditional lift is reusable research machinery, not
a Shor-level result.

## The Tree Ledger Is Not A No-Go Theorem

For a SPECIFIED disjoint recursion spending W=(n+1)^2 children per level,
its literal accounting is n^2*W^(r-2). Every FIXED r gives polynomial growth
in n of degree2r-2: r4 is not "mild superpolynomial", and fixed r8 is not
exponential in n. If r grows with n, that chosen formula can be
superpolynomial.

No claim is made that every algorithm must use this tree, each level must
spend this many inputs, reuse/compression is impossible, or LWE is hard.
An implementation upper-cost ledger cannot establish a universal necessary
copy lower bound. NEG-CENTRAL-DESCENT-TREE-DILATION-BARRIER is quarantined
because it bundled that generality with the invalid positive receiver claim.

## Exact Replay And Remaining Debt

The replacement independent checker reads this report, pins source and
derivation hashes, replays the actual mixed-characteristic ring, checks
original-state phase correction and full-rank reconstruction, and rejects
promotion to a complete receiver. It does not certify the absent lower stage.

NEXT: implement and verify actual lower-quotient state creation/recovery
from original native inputs with the existing central-character gap contract.
A citation to a bounded-class HSP algorithm is not a compiler for this
particular StateHSP interface. Keep sample conditioning, tensor workspace,
caller gates and representation access explicit. Growing native depth remains
a separate open target rather than a proved global impossibility.
