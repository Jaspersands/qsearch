# Unambiguous Decoding: A Sharper Worst-Syndrome Transfer Bound

## Status And Research Decision

Proposed written deduction, checked in bounded signed statevector controls,
NOT independently reviewed or formally verified. No novelty claim, compiled
large circuit, hardness result or quantum advantage is established.

The previous Schur/AG pass compares the PUBLISHED expression Q, not all
quantum algorithms. The refinement here must be checked before treating
that negative result as a reason to abandon the entire AG family. Neither
result applies to the native inverse-trace predicate.

The constructive question is precise: does retaining the decoder's
error-free-or-failure property avoid the generic |V| loss in a worst-case
Regev reduction? The argument below says yes, through a target-state overlap
identity. This is not a new circuit-search pipeline.

## Primary Context

[Ragavan-Shutty, 2610.00502v1](https://arxiv.org/html/2610.00502v1)
provides the pair isometry, Schur-square relinearization and the retained-label
reduction used here. Its generic worst-case analysis has a code-size loss.
The extra hypothesis below is that an accepted decode is never incorrect.

Unambiguous decoding in Regev reductions is existing research, including
[Chailloux-Tillich, Section 6.2](https://arxiv.org/html/2310.20651#S6.SS2).
Their work also warns against treating arbitrary successful quantum decoders
as interchangeable in a reduction. Related worst-case overlap analysis
appears in [Horinaga-Yamakawa](https://arxiv.org/abs/2607.14650), already used
elsewhere in this project. This pass has not established that the particular
identity or its specialization is absent from the literature.

## 1. Exact Transfer Lemma

Let V=rowspan(B) have size N=q^k. For an efficiently preparable normalized
source |A>, put |phi_c>=X^c F^dagger|A>, c in V. Include the blank decoder
work registers in these states. For a desired syndrome s, choose the
character coefficients chi_s(c) so that F applied to

    |a_s> = (1/sqrt(N)) sum_c chi_s(c)|phi_c>

is supported on B y=s and on A. Set lambda_s=||a_s||^2. For a uniform set
source this is N times the probability that a uniform element of A has
syndrome s. It is also the corresponding eigenvalue of the translation Gram
matrix. When lambda_s>0, the normalized target is |t_s>=|a_s>/sqrt(lambda_s).

Let U be a coherent decoder with orthogonal successful output sectors
Pi_c and a separate failure sector. Require EXACT unambiguity on the stated
ensemble:

    Pi_c U|phi_d> = 0 whenever c != d.

Define |eta_c>=Pi_c U|phi_c>, p_c=||eta_c||^2, and p_bar=average_c p_c>0.
Then <eta_c|eta_d>=0 for c!=d, and

    <phi_d|U^dagger eta_c> = delta_dc p_c.             (2)

The existing retained-label circuit prepares the coherent sum of known
c and noisy states, runs U, tests equality with c, and restarts if that
test fails. Acceptance probability is p_bar independently of s. After
acceptance it erases the retained copy with the decoded label and applies
U^dagger. Its normalized state is

    |b_s> = 1/sqrt(N*p_bar) sum_c chi_s(c) U^dagger|eta_c>.

Equation (2), including its ZERO cross terms, gives

    <t_s|b_s> = sqrt(p_bar/lambda_s),
    fidelity(t_s,b_s) = p_bar/lambda_s.               (3)

After F, measuring a valid original-relation output succeeds with probability
at least (3). A final verifier can reject invalid outcomes. No claim of
uniform conditional output is made: components orthogonal to the target can
also be valid outputs. The tests exhibit a strict inequality here.

No equal-p_c assumption is needed. No Gram inverse or enumeration of V is
used by the circuit. Positivity also forces p_bar<=lambda_s for every s;
a zero target fiber is incompatible with p_bar>0 under unambiguity. This
prevents using the lemma to prepare an empty intersection.

## 2. Full-Support Specialization

Take A=(F_q minus {0})^m. Its Gram entries are

    G_cd = (-1/(q-1))^wt(c-d).

Define

    A_tail = sum_{c in V, c != 0} (q-1)^(-wt(c)),
    E = sum_{c in V, c != 0} q^dim(W[Z(c)])/(q-1)^wt(c),
    W = span(V*V).

Character diagonalization bounds lambda_s<=1+A_tail for every syndrome,
and A_tail<=E. The pair/relinearization decoder has p_bar>=1-E. It is
unambiguous because the true (c,c*c) always solves the relaxation; uniqueness
can never produce a different c. The implementation must return FAILURE
when the relaxation is not unique, not select a convenient arbitrary solution.
On invalid pair transcripts it may fail as well; such transcripts have no
amplitude in the ideal ensemble.

For E<1 the resulting ideal success bound is therefore

    success >= (1-E)/(1+A_tail) >= (1-E)/(1+E).       (4)

This replaces use of Q=2*q^k*E as a sufficient failure bound in this special
setting. The same known circuit is being analyzed more precisely. The
conclusion is not applicable to arbitrary decoders with small error rates.

Resource accounting: a known positive lower bound p0<=1-E gives expected
at most 1/p0 retained-label trials. Each uses source preparation, the
coherent decoder, field arithmetic and an inverse decoder. A cap
O(log(1/delta)/p0) bounds abort probability by delta. Compile to total
preselection error O(delta*p0), and postselection/output error O(delta),
to obtain the ideal bound minus O(delta). The primary pair implementation
cost remains polynomial in m,q,log(1/delta), not just log(q). No exponentially
large Gram computation is hidden in the algorithm; E may be bounded by a
separate proof rather than evaluated explicitly.

## 3. Adversarial Countercheck

Removing unambiguity is genuinely invalid. Take eight orthonormal input
states and U=diag(I4, I4-J4/2). This is a real orthogonal decoder. Its
average correct-label probability is 5/8. Run the same retained-label
protocol for the uniform target. The actual target fidelity is 1/10,
not the incorrectly inferred (5/8)/1. Thus decoder success alone cannot
justify (3). The exact rational countercontrol checks this, including U^tU=I.

Other potential gaps checked or kept explicit:

- Do not take absolute values of antisymmetric pair amplitudes. The signs
  reproduce the negative local Gram overlaps and are retained in the controls.
- Do not measure the decoded c or pair transcripts. Only the success/equality
  flag is measured; labeled workspace is coherently erased before U^dagger.
- A signed Fourier character is required for nonzero target syndromes.
- A small or singular Gram eigenvalue does not permit p_bar>lambda_s.
- Approximate circuits are compared with an ideal unambiguous circuit; an
  arbitrary noisy decoder is not declared exactly unambiguous.
- Passing a function a numerical E is not a proof of the decoder guarantee.
  The analytic bound helper does not admit candidates to any registry.

## 4. Exact And Numerical Controls

The only dense simulations are fixed F3 repetition-code controls, lengths
1 through 4 (at most 81 amplitudes). These are deliberately classically
easy checks of the formula, NOT evidence for asymptotic advantage.

An oriented pair incidence matrix, completed to a local 3-by-3 unitary,
implements the signed pair measurement exactly up to floating-point roundoff.
Integer Gram numerators check unambiguity exactly. For all three syndromes,
direct inverse-pair-unitary plus Fourier simulation agrees with (3).

| length | actual p_bar | E | old Q | certified bound (4), using A_tail |
|--------|--------------|---|-------|----------------------------------|
| 3 | 3/4 | 3/4 | 9/2 | 1/5 |
| 4 | 7/8 | 3/8 | 9/4 | 5/9 |

Both old Q values are vacuous. At length 4, syndrome 1, target fidelity is
14/15 whereas valid-output probability is about0.941799. This specifically
checks that a useful target overlap is not the entire output law.
Length1 has no accepted branch; no division by zero or false guarantee is
issued. The three-syndrome native relation is always the original one.

## 5. Reopened Comparison, Not A Claimed Speedup

For standard AG V=ev_D L(G), d>=2g+1, m>2d, use k=d-g+1 and w=2d-g+1.
The same Riemann-Roch shortening calculation gives the sufficient estimate

    E <= (q^k-1) q^w / (q-1)^m,
    A_tail <= (q^k-1)/(q-1)^(m-d).

Thus the refined decoder criterion can reach roughly

    m*log_q(q-1) > 3d-2g+2,

whereas the proved deterministic cubic completion is guaranteed when
m>3d-g+1. For growing genus these sufficient regions need not coincide.
This does NOT prove the classical algorithm fails below its guarantee;
individual annihilators, auxiliary-code variants and other attacks can work.

Do not populate this apparent gap with synthetic parameters and call them
curves. A valid asymptotic family must simultaneously provide:

1. Actual explicit smooth curves, enough distinct rational evaluation points,
   and efficient input/Riemann-Roch construction in the charged model.
2. A prime-field regime or a rigorous response to extension-field linear
   ansatz attacks; known easy large-field regimes must also be excluded.
3. Bounds giving E bounded below1 by an inverse-polynomial margin, or o(1),
   with actual q-dependent constants and the full input size charged.
4. Stronger classical tests than the cubic union bound: actual annihilator
   rank, auxiliary evaluation codes, explicit algebraic reconstruction and
   generic full-support solvers on the SAME input relation.
5. Independent adversarial review of (2)-(4), comparison with prior USD and
   worst-case OPI results, and a genuine reason this solves a useful problem.

Next decisive work is the matched classical/parameter feasibility comparison
for this narrower gap, not larger repetition-code simulations. The native
inverse-trace single-symbol pair obstruction remains valid and unchanged.
