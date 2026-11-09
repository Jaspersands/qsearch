# Determinant characters: reject the direct Fourier receiver

2026-11-06. A short admission test after the independent Kloosterman pass.
No implementation, novelty, separation or general learning lower bound.

## Candidate and prior-work check

The proposed structured growing-degree family was

    F_L(x)=det(mat(Lx)),  L in GL(n^2,F_p),  n>=2, p odd.

The input would be fresh exact global copies of

    |psi_L> = p^(-n^2/2) sum_x lambda(F_L(x)) |x>,
    lambda(0)=1, lambda(a)=quadratic_character(a) for a!=0.

The output would be a determinant representation up to common nonzero
polynomial scale (not the unique original L, which is unidentifiable).
The hoped-for mechanism was additive Fourier sampling followed by learning
the transformed determinant variety, with poly(n,logp) copies, arithmetic,
storage and classical decoding. This would test whether a structured
growing-degree family escapes the factorial univariate receiver cost.

Polynomial equivalence has external algebraic-complexity motivation, but
that alone does NOT establish a natural source application for this
weakened character-only input. An end-to-end source application remains
an admission obligation. We do not manufacture one from an open residual.

Corpus first: `been-tried "hidden determinant quadratic character matrix
equivalence Fourier rank"`, then `baselines --no-refresh -k 3 "determinant
polynomial equivalence sign oracle matrix Gauss sums"`. No matching
catalog baseline was returned; this is not evidence of hardness.
The literature supplies the decisive formulas below, so no quantum
subsystem, sweep or finite experiment was built.

## Classical comparison and exact input boundary

[Garg--Gupta--Kayal--Saha, ICALP2019, Theorem1](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2019.62)
already gives randomized poly(n,log|F|) determinant equivalence with
FULL polynomial-evaluation black-box access, for |F|>=10n^4 and
char(F) not dividing n(n-1). Its footnote2 defines evaluations in F,
not Legendre signs or quantum copies. We inspected the actual theorem
and definition. Supplying this stronger oracle would remove the proposed
opening; it is not a classical solution of the character-only problem.
The imported full-value routine was not executed.

For the SPECIFIC measured Fourier output, uniform classical field vectors
give an approximate sampler with the rigorous bound below. It uses no
oracle, hidden L, inverse source, learned determinant or quantum copies.
This is the matching classical attack on the proposed receiver, not a
classical learner for the native input problem.

## Paid source calculation, including the padded zeros

Let N=p^(n^2), alpha=|GL_n(F_p)|/N=prod_(j=1)^n(1-p^-j), and s=1-alpha.
Use the standard dot pairing on the n^2 matrix entries. Under the
additive QFT, the hidden change of coordinates sends y to

    Y=mat(L^(-T)y).

Let chi_0(det X) be zero on singular matrices and the quadratic character
on invertible ones. The ACTUAL source is the normalized sum of two
unnormalized vectors chi_0(det X)/sqrt(N) and 1_singular(X)/sqrt(N).
Their squared norms are alpha and s; no postselection is supplied.
Call their QFT vectors f and h. Li--Hu Theorem2.1 gives

    f(Y)=c*chi(det Y)/sqrt(N) for invertible Y, |c|=1;
    f(Y)=0 for singular Y;
    h(Y)=(-1)^(n+1)*p^(-n(n+1)/2) for invertible Y.

Here c=G(chi,psi)^n/p^(n/2). The theorem states the nonzero-label cases;
at Y=0, f(0)=0 follows by multiplying matrices by a fixed determinant-
nonsquare invertible matrix and cancelling the character sum.
The h formula uses sum_X psi(Y dot X)=0 for invertible Y and the
TRIVIAL-character branch of the same matrix Gauss formula. Parseval gives
sum|h|^2=s. We retain the singular-label probabilities, including Y=0.

Write P_L(y)=|f(Y)+h(Y)|^2 and U(y)=1/N. Then

    sum_y ||f(Y)|^2-U(y)| = s,
    sum_y |h(Y)|^2 = s,
    sum_y 2|f(Y)h(Y)| = 2*alpha*p^(-n/2).

The first identity holds because |f|^2 equals 1/N on the invertible
labels and zero elsewhere. The last holds because f is supported there,
there are alpha*N such labels, and both displayed magnitudes are exact.
Triangle inequality therefore proves, for EVERY hidden invertible L,

    TV(P_L,U) <= s+alpha*p^(-n/2)
              <= 1/(p-1)+p^(-n/2).                         (1)

The final inequality uses 1-prod(1-p^-j)<=sum_j p^-j<1/(p-1).
It is uniform in n>=2 and retains the actual zero padding.

For t independent copies measured in this SAME way, tensorization gives
TV(P_L^tensor(t),U^tensor(t))<=t times the bound in (1). Two hidden-label
laws have mutual TV at most twice that. Thus when t=o(p), this receiver
cannot distinguish two projectively distinct determinant polynomials with
constant advantage over 1/2, even with arbitrary classical processing of
the measured labels. In particular, p superpolynomial in the relevant
input parameters defeats polynomially many such measured samples.
More explicitly, the bound in (1) is at most 5/(2p) for n>=2,p>=3.
Binary success at least2/3 requires t>=p/15. This is a measured-label
lower bound for this receiver only; it is not a general copy lower bound.

Projectively distinct instances do exist: compare L=I with the invertible
coordinate shear replacing X11 by X11+X12 and leaving all other entries
fixed. The determinants agree at I, but are respectively 0 and 1 at the
upper-triangular matrix with X11=0,X12=X22=1 and all remaining diagonal
entries1. They cannot be constant multiples. This is a binary testing
obstruction for this receiver, not a statement about inequivalence under
general linear coordinate changes (all candidates are so equivalent).

## Decision, review and limits

Reject the direct-Fourier variety-learning mechanism before implementation.
The family does not transfer the odd-dimensional quadratic dual-cone
readout. Known finite-field matrix Gauss sums already determine this fact.
This does not rule out coherent use of Fourier phases, collective
measurements, chosen-query algorithms, measured slices, or a different
paid source. It also does not assert classical hardness or a native
poly(n,logp) classical learner. No new determinant program is admitted.

The independent core review checked the exact normalization, transpose,
zero-frequency cancellation, padding interference, TV/tensorization bound
and full-value classical theorem scope. It corrected the conclusion to
"no constant advantage over 1/2" and "projectively distinct". Parent
derivation agrees. No numerical or quantum execution is claimed.

Source PDFs/texts: audits/sources/legendre_prf/matrix_gauss_1105_4513.*
([Li--Hu](https://arxiv.org/abs/1105.4513), Theorem2.1), and
determinant_equivalence_2019.* (Theorem1 and footnote2). The matrix-Gauss
identities are prior art, not a repository discovery.

Next high-value question remains a genuinely paid poly(d,logp) native
polynomial-character reconstruction mechanism, compared with independent
externally motivated directions. Neither a formal Frobenius unitary nor
direct determinant Fourier labels remove its blocker. Do not expand this
admission test into another nearby barrier/sweep. All general-algorithm,
novelty, separation, hardness and quantum-execution gates remain false.
