# Word-Span Decision, Not A Granted Receiver

Conditional research target and finite reference; external review pending.
No efficient decision circuit, recovery algorithm or quantum speedup exists
in this module. Dense projectors are diagnostics, not oracle access.

## Actual Code-Membership Statistic

Use the original native word map f_A(w) and the actually prepared word state
psi_b(w)=chi_q(beta_w.b)/sqrt(D), D=3^M for one cohort. For each supported
frequency sigma, let r_sigma be the uniform normalized vector on that fibre.
The label-only projector Pi_A=sum_sigma |r_sigma><r_sigma| tests membership
in their span. It does not output the secret, compile a chosen preimage or
promise a coherent normalized word-to-frequency encoder.

If b=A*s exactly, every phase within a fibre is chi_q(sigma.s), so
Pi_A psi_b=psi_b regardless of balance, empty frequencies or the secret.
For IID uniform raw null values b, all distinct beta_w characters are
orthogonal. The averaged null state is I/D and acceptance is
rank(Pi_A)/D<=q^n/3^M. Neither IID public labels nor balanced fibres is
needed for this bound; independence/uniformity of null values IS needed.
The identity density statement assumes a fixed mask (or one independent of
raw null values). A data-adaptive mask need not preserve that density. Span
ACCEPTANCE nevertheless remains invariant: the added phase chi_q(f_A(w).m)
is constant within each fibre, so its diagonal unitary commutes with Pi_A.
Thus the span null trace bound still holds for adaptive masks without claiming
the masked null state itself is identity. Prefix-only effects do not inherit
this whole-root commutation automatically.

For frozen original errors e, mean word error square is
(2/3)*sum_j(e_a^2+e_c^2-e_a*e_c)<=sum_i e_i^2. Since the ideal state lies
in the span, rejection is bounded by squared vector displacement, not a
generic square-root trace loss. The phase inequality and pi^2<10 give

    E source_rejection <= min(1, 80*M*V/q^2).

This uses true marginal moments, permits correlations/data dependence,
and does not resample errors per word. An effect E_A within operator norm
epsilon of Pi_A has a conditional decision gap at least
1-80*M*V/q^2-q^n/3^M-2epsilon-2delta, where delta bounds each ensemble's
actual preparation trace distance. The moment is a SOURCE promise, not
the moment observed on successful fixtures. Operator-norm approximation is SUFFICIENT,
not necessary: an efficient source-ensemble test with its own proof is also
worth searching. Actual state-preparation/gate errors still need charging.
M=n*r+12 suffices for a small null bound; the earlier cubic bank and exact
receiver normalization are not prerequisites by fiat.

## No Free Projection

The raw comparison J is not this effect. Even perfectly balanced rows
have J^*J positive eigenvalues1/q^n, while the span projector has eigenvalue1.
A small supported condition number does not remove this absolute scale.
Cheap label computation, a group twirl density or a reflection about one
known seed does NOT supply the span test. Generic singular-value amplification
must charge its scale. A strong span test might also help coherent row
processing under additional fibre-size/access promises: it is not proved
strictly easier. The target is broadened, not declared solved.

Finite controls independently retain entire original word/fibre tables and
exact cyclotomic expectation coefficients. Their circuits are not scalable;
bounded-noise examples are already subject to the new classical decoder.
The independent checker reconstructs all378 actual word rows and their
cyclotomic probabilities, verifies distinct raw-value characters, and checks
both effect and input-preparation losses. A complete three-point mixture
has uniform individual raw values but perfectly dependent codewords: its
acceptance is1, versus1/3 for the actual IID null. Uniform marginals alone
cannot justify the null model. Tiny injective maps also correctly have
Pi=I, null acceptance1 and no advantage.

## Reconsider Fixed-Bank Full Recovery

[Micciancio and Peikert, Section3 Theorem3.1](https://eprint.iacr.org/2011/501)
offers a prime-power Gaussian search-to-decision route with a noise-width
increase and polynomial sample expansion. Its indexed primary statement
was checked; the full adapted proof remains unaudited.
This is a KNOWN reduction, not a new result from this repository. The scalar
alpha_search*q>=2sqrt(n) field is a necessary interface check, not proof
that every remaining worst-case lattice reduction condition holds. The n8
profile fails that check; n32,n64,n128 pass it. Actual source and decision
oracle availability remain false on every profile.

For q=3^r choose h(n)=ceil(log2(n+2)), a legitimate omega(sqrt(log n))
function, and alpha_search=alpha_decision/h^2. The ledger checks the selected
prime-power parameter inequalities, rather than claiming SAME-width
recovery from the current fixed bank. A slightly narrower hard Gaussian
source plus a larger paid polynomial bank can still be a high-impact target.
No distinguisher or independent extra source data is supplied here.

Ideally widen the continuous source by fresh Gaussian width squared
alpha_decision^2-alpha_search^2 BEFORE rounding. If only rounded originals
are given, their normalized displacement is<=1/(2q). Condition on old data
and smooth with independent fresh Gaussian additions: the resulting joint
TV squared is<=11*m/[28*q^2*(alpha_decision^2-alpha_search^2)].
This is a bounded coupling loss, not exact widening. Auxiliary noise is
not a fresh ORIGINAL sample; disjoint original blocks, sampler/precision
losses and average-to-worst-case oracle handling need a complete audit.

Thus primitive or bounded-valuation Fourier output is one possible route,
not a universal prerequisite for a groundbreaking Gaussian decision idea.
The highest-impact missing object is still a constructive source-compatible
decision mechanism or receiver. Try to falsify proposed span circuits with
the raw-scale and known-seed countercontrols before accepting any signal.

## Next Mechanism To Test

Try an explicitly costed local collision Hamiltonian instead of a free
global projector. Its ground space contains fibre-constant codewords, but
its actual null acceptance depends on connected COMPONENTS, not only fibre
rank. Disconnected graphs can invalidate the proposed test. Random original
labels also make short exact collision moves rare at growing roots; count
that before attempting a circuit. This is a scoped mechanism audit, not a
lower bound against arbitrary collective quantum measurements.
The [actual paired-source follow-up](NATIVE_WORD_LOCAL_DECISION.md) now
implements that audit and its matched local classical statistic. It
deprioritizes exact logarithmic-support moves, not every decision mechanism.

    python theorems/native_word_span_decision.py --write
    node research/certificates/native_word_span_decision_crosscheck.js
    python -m pytest -q tests/test_native_word_span_decision.py
