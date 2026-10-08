# Collective Weak-Trit Gate For Quantum Label Access

LOCAL DERIVATION / REVIEW PENDING. This is a sample/access tradeoff, not a
general quantum lower bound, new algorithm, or novelty claim. Independent
finite certificates do not replace external review of the theorem.

## Statement And Scope

Use M ORIGINAL even-native samples at level2r, with integer-embedded secret
s uniform in Z_(3^r)^n. Set q=3^r and D=3^M. Their state is

    psi_s = D^(-1/2) sum_x chi_q(s.F(x)) |x>,
    F(x) = sum_i (0,a_i,c_i)[x_i].

All a_i,c_i are independent uniform full vectors in Z_q^n. This is the
actual native source coordinate representation, not a generated oracle.
Let a quantum receiver depend arbitrarily on every label MODULO b=3^ell,
where 0<=ell<r. It may use arbitrary collective POVMs, known ancillas,
outcome feedback and label-independent public randomness. The FINAL
classical decoder may inspect ALL full labels and perform unlimited work.

The complete quantum measurement must be invariant under changing higher
label digits while preserving the low prefix. An operation computing full
F(x) for a chirp is not low-controlled merely because its matrix K used few
label bits. Feedback that consults higher label digits before more quantum
operations also violates the premise. Policy declarations alone are not proof.

Put S=3^(n(r-ell)). Then raw mean advantage for guessing s_1 mod3 obeys

    Pr(correct least trit) - 1/3
      <= min(2/3, sqrt(((5/3)^M-1)/S) + (1-3^(-M))/S).

The bound holds conditional on ANY fixed low-label record, averaged over
its complete uniform high lifts and the full secret prior. It is therefore
also a full-IID source-average bound, but is NOT a bound on a chosen full
frequency cohort, a retained sieve distribution, a nonuniform secret prior,
or an extra source/evaluator oracle. Every original and every raw abort must
be charged. For a joint ideal-source approximation of trace distance eta,
measurement contraction can add eta to raw correctness; marginal error
claims alone do not justify a joint source error budget.

This extends two earlier LOCAL derivations: the fixed product-POVM weak gate
in `TERNARY_BLIND_PRODUCT_GATE.md`, and the arbitrary collective low-label
L4 FULL-SECRET gate in `TERNARY_GAUSSIAN_DRIVE.md`. Full recovery alone does
not settle whether a useful weak trit can be inferred. Here the weak target,
collective effects, adaptive measurement and partial-label aliasing are kept.

## Conditional Character Covariance

Fix all low rows. Write a_i=a_i0+b*A_i and c_i=c_i0+b*C_i, with the high
vectors A_i,C_i independent uniform modulo Q=q/b. Quantum effects E_y are
constant with respect to these high lifts, although they can depend on every
low row. Use reference mass mu_y=Tr(E_y)/D, not uniform outcome mass. Null
effects may be omitted. Positivity and completeness give mu_y>0 and sum mu=1.

For secret s NONZERO modulo Q, the high phases per copy are independent
uniform roots of order at least3. Consequently E_high p_y(s)=mu_y.
Expand two Born probabilities in original word pairs. Each copy supplies
simplex differences from e_0=(0,0),e_1=(1,0),e_2=(0,1).

Nonparallel nonzero A2 roots have determinant +/-1, so high-character
orthogonality forces both secret residues to zero. Parallel roots have only
the ratios +1 and -1; a zero root paired with a nonzero root forces a zero
secret residue. Therefore, away from the high kernel, centered covariance
vanishes unless

    s = t modulo Q,    or    s = -t modulo Q.

This holds over composite ternary roots and includes nonprimitive secrets;
it does not silently assume a field or remove all nonunits. Because Q is
odd, a nonzero residue is different from its negative. Each residue/sign
block contains at most2h full-secret hypotheses, h=b^n. Alias coefficients
can carry low-label phases and may have either sign. Do not import diagonal
Gram orthogonality or omit the opposite-residue block.

## Sharp Fourth Moment And Arbitrary Positive Effects

For independent root phases z,w of order at least3,

    E|a+z*b+w*c|^4
      = |a|^4+|b|^4+|c|^4 + 4(|ab|^2+|ac|^2+|bc|^2).

For nonnegative A,B,C the gap to (5/3)(A+B+C)^2 is exactly

    [(A-B)^2+(A-C)^2+(B-C)^2]/3.

Condition one input at a time; Cauchy bounds cross terms, and induction gives
E|p_f|^4 <= (5/3)^M ||f||_2^4 even for an ENTANGLED coefficient vector f.
Fixed low phase rotations preserve its norm and the bound. There is no
quartic alias: exponent differences lie in [-2,2], below root order3.

For a positive effect, spectral decomposition and Minkowski extend this from
rank-one effects to arbitrary rank:

    E_high[p_y(s)^2] <= (5/3)^M * mu_y^2,
    Var_high[p_y(s)] <= A_M * mu_y^2,    A_M=(5/3)^M-1.

The normalized aggregate Gram is

    C_(s,t) = sum_y E_high[(p_y(s)-mu_y)(p_y(t)-mu_y)] / mu_y.

Its diagonal is at most A_M. Cauchy bounds every within-block entry by A_M,
and all cross-block entries are zero. Gershgorin, or block row norms, gives
||C|| <=2h A_M. Arbitrary source-label-independent outcome feedback produces
one positive complete collective POVM on the original batch, so it is covered
without assuming a product measurement or independent output records.

## Kernel And Three-Class Decision

The high kernel K={s:s=0 modulo Q} has h secrets and prior mass h/q^n=1/S.
DO NOT postselect it away. For analysis, replace each kernel input by I/D.
Its measured likelihood becomes the reference mass. Each original kernel
state is pure; its trace distance from I/D is1-1/D. Thus this replacement
changes raw decision success by at most(1-1/D)/S, even when the decoder uses
all full label records. It is an analytical comparison, not a granted channel.

For target t in F3, use contrast weights

    w_t(s) = (3/q^n)1[s_1 mod3=t] - 1/q^n,
    sum_s w_t(s)^2 = 2/q^n.

Restricting the weights to nonkernel secrets cannot increase this squared
norm. The contrast L2 norm under high lifts and reference output masses is
at most sqrt(4h A_M/q^n). Each contrast integrates to zero by measurement
completeness. Replace each classifier indicator by h_t-1/2 and apply Cauchy.
The three-class mean advantage of the modified channel is at most
sqrt(h A_M/q^n)=sqrt(A_M/S). Add the charged kernel replacement term to
obtain the statement. No computational restriction on the decoder was used.

## What It Does And Does Not Force

At M=nr+O(log(nr)), read fractions satisfying

    ell/r < 1 - log(5/3)/log(3) = approximately0.5350264793

with a constant margin have exponentially small weak advantage. Reading only
half the label trits remains screened at this copy budget, even with arbitrary
collective measurement and unrestricted final classical inference.

This is NOT a necessity for high-label quantum control at EVERY polynomial
copy budget. Increasing M by a constant factor can make the bound vacuous.
Ignoring the small kernel term, a constant desired advantage requires roughly
2.1506601031*n*(r-ell) copies under this bound. That is still polynomial.
More copies do not automatically supply an efficient decoder, but they are a
legal escape and must not be rejected by this theorem. Gate-passed means only
that this necessary bound did not rule the parameters out.

The producer uses exact integer comparisons for requested advantage. Huge
fractions are stored as factored base/exponent expressions; floating values
are NONAUTHORITATIVE and may underflow. The kernel term is included, not
dropped in finite small cases. Full quantum label access is outside this
screening API, not a failed candidate.

## Controls And Attempted Refutation

Nine exact two-copy controls include Bell bases, real entangled bases,
prefix-controlled entangled bases, a genuinely second-digit-controlled basis,
rank-three coarse Bell effects, adaptive second-copy basis selection, and a
real flat product frame. Every effect has positive rank-one factors summing
exactly to identity. This is a PSD certificate, not a numerical eigenvalue test.

Exact source-character Grams include q3,q9,q27,q81 and dimension2. Small
cases additionally enumerate ALL uniform high lifts and raw original Born
probabilities, with ALL secrets in the classical MAP score. The q81 case is
an exact character calculation without its43,046,721-element label census.
The real flat frame saturates the universal two-copy covariance bound32/9;
a smaller universal covariance constant would need another premise.

Independent replay certifies factors, completeness, word-pair character
covariance, residue/sign sparsity and finite operator row bounds. It also
checks exact large-parameter screening and the one-site positive-square
identity. This is finite algebra, not a machine-checked general proof.

Full-label information-optimal measurements remain a genuine escape. Nine
original-IID full-label PGM references at r4/r5/r6 have conditional least-trit
successes above the BLIND POPULATION bound's numerical value. This is not a
population violation: the readout uses full labels, and the comparison cohorts
are conditional. Computing these references enumerates every native word and
its fiber multiplicity. No efficient PGM compiler, fiber oracle or decoder is
provided. The information/implementation distinction is also central in
[Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0501044).

Reject or narrow this derivation if any nonkernel covariance appears outside
the residue/sign blocks, a positive effect violates the L4 variance bound,
the kernel replacement is undercharged, a valid prefix-only classifier
exceeds the mean weak bound, or a full-label gate/source filter is accidentally
admitted. A biased secret prior, odd native level, non-IID retained source or
additional oracle requires a separate argument. Finite favorable cohorts and
uncovered architectures are not evidence of a breakthrough.

```
python theorems/native_label_access_gate.py --write
node research/certificates/native_label_access_gate_crosscheck.js
python -m pytest -q tests/test_native_label_access_gate.py
```
