# Hidden-field Jacobi readout: exact scoped falsifier

2026-11-14. Parent derivation and full 157-line independent review checked:
`audits/reviews/2026-11-14-hidden-field-mechanism-selection.md`.
This rejects a specified measurement/readout, not collective reconstruction.

Native problem: q=p^n, odd p, unknown invertible Fp-linear L:V->Fq,
F(x)=chi(Lx) off zero, F(0)=1. Recover a norm circuit/normalized field
algebra up to scalar/Frobenius ambiguity. Chosen coherent sign queries and
fresh pure copies of q^-1/2 sum F(x)|x> are DISTINCT access models.
The desired clock is poly(n,log p,log(1/eta)). No hidden multiplication,
Singer coset oracle, dual-character correction or source inverse is supplied.
Prior corpus and literature/baseline contract: HIDDEN_FIELD_CHARACTER_ADMISSION.md.
Its written chosen-sign classical comparator costs O(p n log(n/eta)) queries
and poly(n,p) work for p>=65536n^2, for EVERY L. It does not simulate copies
or give polylog(p) reconstruction. This comparator remains the strongest
verified native baseline; unknown quantum/classical decoding is not hardness.

## Mechanism and decisive test

Publicly project x!=0, success 1-1/q, to obtain h(x)=chi(Lx), h(0)=0,
normalized by sqrt(q-1). Three copies are linearly transformed to
(s=x+y+z,x,y); Fourier-measure x,y as b,c, retaining s. The hoped-for
advantage was a poly(n,log p) multiplication-tensor sample/decoder.
The circuit itself is cheap, but the information/output claim is false.

Define beta_t analytically by Tr(beta_t Lx)=t.x, and h*(t)=chi(beta_t).
The Gauss transform is gamma h*(t)/sqrt(q-1), |gamma|=1. Fourier-transform
s as well: the joint amplitude is exactly

    gamma^3 h*(t)h*(t+b)h*(t+c)/(q-1)^(3/2).

Hence Pr(b,c)=(q-|{0,-b,-c}|)/(q-1)^3, independent of L. Conditional t is
uniform outside those public excluded points. Retaining the phase state
may retain information; measuring/discarding it as proposed does not decode
the field. This proof uses the dual map only analytically, never as advice.

At b=c=0 the success probability is (q-1)^-2 and the retained state is
the original h up to global phase. Directly,
h*h=chi(-1)(q delta_0-1), h*h*h=chi(-1)q h. More generally the r-copy
zero-erasure success is (q-1)^(1-r); odd r returns h. Even an available
chosen-oracle reflection would pay order q amplification at r=3 and return
no new tensor. Copies alone supply no such reflection. Finite-bit Fourier
compilation perturbs the complete instrument, not this ideal information law.

The independent cubic-derivative alternative is also unadmitted: eight
distinct additive shifts give a squarefree degree-eight character sum,
zero-frequency mean <=7/sqrt(q)+8/q, not a quadratic phase polynomial.
Bounded correlation means have paid classical chosen-sign estimators.
The complete Fourier output law and copy-only decoding remain UNKNOWN.

An independent explicit diagonal-cubic endpoint is classically recovered
by generic extension-field Hessian pencils in randomized poly(n,log p).
CSA minimal-module/idempotent work is already closed written under GRH
in CSA_MINIMAL_MODULE.md; no new cyclic-field construction is required.
These comparisons avoid continuing a known missing receiver by inertia.

## Disposition and next operation

The specified Jacobi label/zero-erasure route is FALSIFIED as a new decoder.
General hidden-field reconstruction remains OPEN; no new algorithm, speedup,
novelty, lower bound or generic measurement no-go is claimed. No paid API
request is warranted without a new operation on the retained phase states.
One exact Sage q=9,25 control completed at audits/controls/hidden_field_jacobi;
identity/shear, all1412 marginals and32708 triple outcomes checked once,
terminal/reaped0. Zero-branch probabilities1/64,1/576; direct convolutions
return the input. This checks conventions, not the all-input identities.
Independent physical direction selection now checks the actual dissipative
preparation theorem before admitting a native algorithmic hypothesis.
