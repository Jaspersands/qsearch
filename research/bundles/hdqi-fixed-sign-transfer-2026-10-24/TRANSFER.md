# Fixed-Sign HDQI Transfer: A Missing Condition And A Constructive Test

Date: 2026-10-24. Status: LOCAL, UNREVIEWED derivations, exact rational
certificates, and capped dense controls. Not a new quantum algorithm,
independently reviewed theorem, or refutation of a published theorem.

## 1. Research Decision

Can a degree-scale pilot-preparation result be combined with a known
classically hard Gibbs family to obtain a useful end-to-end algorithm?
Not just by citing a small decoder failure probability. The coupling-sign
quantifier matters. This pass supplies a fixed-sign condition and an
explicit obstruction to omitting it. Preparing the pilot is a separate
unresolved cost, not a consequence of passing this transfer check.

The published robustness argument averages independent coefficient signs;
it does not certify every fixed sign choice. Its thermal inclusion bound
is the input to our sufficient criterion below.
[Hastings--Schmidhuber, Appendices A.2-A.3](https://arxiv.org/html/2610.03697v1).

Known constant-temperature sampling hardness uses circuit-parent families
with conditional complexity assumptions and already-efficient quantum
preparation. Their specified circuits also prepare the Gibbs states from
thermal product inputs. Reusing them is a benchmark, not a new algorithm.
[Bergamaschi--Chen--Liu, Lemma 6.1 and Section 9](https://arxiv.org/html/2404.14639v2).

## 2. Exact Fixed-Sign Error Identity

Input: explicit Hermitian n-qubit Paulis P_i, real rational J_i, beta>=0,
and a total deterministic decoder Dec. Define H=sum_i J_i P_i, the label
map B=[X;Z], ordered products P(y)=product_i P_i^y_i, and the canonical
independent coefficient pilot psi_y=a_y/sqrt(Zhat). Physical Pauli signs,
including phases in ordered products, are retained. Bell vectorization is
|P>=vec(P)/sqrt(2^n), so each Pauli vector has norm one.

The ACTUAL isometry, including its environment, is

    |Psi> = sum_y psi_y |R(y)> |P(y)>,  R(y)=y xor Dec(By).

Distinct y either have different B labels and orthogonal Bell vectors,
or equal B labels and different R. Thus this map is an isometry even for
an inaccurate decoder. No postselection on R=0 is being assumed.

Let E={y:R(y)!=0}, r=sum_E |psi_y|^2, and define physical vectors

    g=sum_{y notin E} psi_y |P(y)>, b=sum_{y in E} psi_y |P(y)>, w=||b||^2.

The coefficient identity gives g+b=|exp(-beta H/2)>/sqrt(Zhat), with
norm squared Zphys/Zhat. It generally is NOT a normalized target. Let T
be its normalized version, rho_pair=Tr_R |Psi><Psi|, and rho_left its
left reduction. Orthogonality of the nonzero-residue space to R=0 gives

    || |Psi> - |0>(g+b) ||^2 = r+w.                         (1)

Indeed the nonzero-residue part has squared norm r and the R=0
difference is -b. Project onto the complement of T in the physical pair;
the unnormalized comparison vector is annihilated. Therefore

    1-<T|rho_pair|T> <= r+w,
    D(rho_left, exp(-beta H)/Tr exp(-beta H))
        <= D(rho_pair, |T><T|) <= min(1,sqrt(r+w)).          (2)

D denotes one-half trace norm. If the actual pilot is within trace
distance delta_p of the ideal pilot, add delta_p to (2), by contractivity.
Coherent decoder/circuit approximation costs must likewise be charged.

If L_E is the largest number of bad words with one B label, Cauchy-Schwarz
within labels gives w<=L_E*r. In particular L_E<=2^dim(ker B). Small r
alone does not suffice when coherent bad-word multiplicities grow.

For independent uniform coupling signs, each coefficient acquires the
character v^y. Cross terms average to zero, giving E_v w_v=r and hence
E_v(r+w_v)=2r. This recovers, rather than contradicts, the cited theorem.

## 3. Constructive Fixed-Sign Certificate

Put b_i=min(1,beta|J_i|) and define the nonzero weighted kernel enumerator

    W_B(b) = sum_{0 != v in ker B} product_{i:v_i=1} b_i.

LOCAL CLAIM:

    w <= r+W_B(b),
    D(rho_left,Gibbs(H))^2 <= min(1,2r+W_B(b),(1+2^dim ker B)r).  (3)

Proof: in ||b||^2 only equal B labels survive. The diagonal is r. For
each nonzero v in ker B, the absolute off-diagonal contribution is at
most sum_y |psi_y psi_{y xor v}|, dropping restrictions to E. For any
U subset supp(v), partition y by y_U=A. Cauchy-Schwarz bounds that part
by sqrt(Pr[Y_U=A] Pr[Y_U=U\A]). The thermal inclusion inequality
Pr[S subset Y]<=product_{i in S}(beta J_i/2)^2 bounds each part by
product_{i in U}(beta|J_i|/2). Summing all 2^|U| parts and choosing
U={i in supp(v):beta|J_i|<1} gives product_{i in supp(v)} b_i.
No independent-error assumption or sign-ratio bound was used. Summing
over v proves (3). Phases can improve cancellation but cannot invalidate
this absolute upper bound. The bound is sufficient, not necessary.

The executable obtains a kernel basis by binary elimination and counts
all 2^k-1 nonzero words only within an explicit budget. Its decoder
certificate enumerates EVERY y of weight<=t, refuses if their syndromes
collide, and stores a unique inverse on those syndromes, with an exact
linear section elsewhere. Then r<=Pr[|Y|>t], bounded using the existing
exact factorial-moment bound. Injective B admits an exact linear decoder
with r=0 and no word enumeration. No estimated error frequency is accepted
as proof. Enumeration/budget refusal means UNKNOWN, not hardness.

Cost: polynomial bit elimination, plus O(m 2^k) rational kernel work and
O(m sum_{j<=t} binom(m,j)) low-weight checks/storage. Rational precision
and table/reversible lookup costs are not free. This is efficient only
in suitable parameter regimes; it is not a general code-distance solver.

Positive controls use independent X_j,Z_j and their all-coordinate Pauli
product, giving a single kernel word of weight 2n+1. At n=32, m=65,
beta=1/128, t=2, just 1 kernel word and 2,146 decoder words suffice for
a transfer error certificate below 10^-4. This is a certificate control,
not a hard native problem or an implemented 65-qubit preparation.

CRITICAL DISTINCTION: ker B controls scalar aliases and fixed-sign error.
The prior output-uniformity test instead studies ker X minus ker B,
namely nontrivial physical diagonal words. They are different objects.
A useful candidate needs controlled scalar aliases AND useful surviving
diagonal interference. A short kernel relation is not a useful observable.

## 4. Representation Dilution Cannot Manufacture A Useful Pilot

Fix H=sum_{j=1}^m J_j P_j. Replace each term with K copies J_j P_j/K.
Physical H is unchanged, while the canonical pilot has Km distinct
coefficient generators. Its squared coupling mass becomes M/K where
M=sum_j J_j^2. If the original anticommutation degree is d, the new degree
is Kd and beta^2 Jmax_new^2(d_new+1)=beta^2 Jmax^2(d/K+1/K^2).
Both preparation parameters can therefore shrink without changing H.

Nevertheless the inclusion union bound gives

    Pr[Y!=0] <= beta^2 M/(4K).

The pilot is within trace distance sqrt(Pr[Y!=0]) of vacuum. For ANY total
decoder, vacuum maps to a Bell identity vector (possibly with a nonzero
residue), whose left state is I/2^n. Consequently

    D(rho_actual,left,I/2^n) <= beta sqrt(M/(4K)).             (4)

If Gibbs(H) has distance Delta>0 from I/2^n, its actual preparation error
is at least Delta-beta sqrt(M/(4K)). Thus term splitting cannot turn a
cheap canonical pilot into a generic fixed-H Gibbs preparation. This
argument includes noncommuting H and does not assume a particular decoder.
K-dependent representation and circuit costs must still be paid.

Canonicalizing equal physical Paulis can flag this loophole. Do not merge
an intentionally random-sign ensemble while pretending its distribution
is unchanged: the fixed-target and ensemble problems are different.

## 5. All-Size Explicit Counterexample And Exact Certificate

Take H=sum_{i=1}^K Z/K=Z and 0<=beta<=1. The canonical independent pilot
is (a|0>-b|1>)^tensor K, where x=beta/(2K),

    a=cosh(x)/sqrt(cosh(2x)), b=sinh(x)/sqrt(cosh(2x)).

B reports parity. Use the legitimate minimum-weight section Dec(0)=0,
Dec(1)=e_1. Decoding succeeds exactly when all bits other than the first
are zero. Thus

    r=1-a^(2(K-1)) <= (K-1)beta^2/(4K^2) -> 0.

For each fixed suffix z on bits 2..K, the even- and odd-parity inputs
share a residue. Their physical matrix is proportional to
Z^parity(z)(a I-b Z). Squaring and summing suffix weights gives EXACTLY

    rho_actual,left=exp(-(beta/K)Z)/(2 cosh(beta/K)),
    D(rho_actual,left,Gibbs_beta(Z))
        = [tanh(beta)-tanh(beta/K)]/2 -> tanh(beta)/2.         (5)

Writing Zhat=cosh(beta/K)^K, the good coefficients are
g_I=cosh(x)^K/sqrt(Zhat), g_Z=-cosh(x)^(K-1)sinh(x)/sqrt(Zhat).
The full target coefficients are cosh(beta/2)/sqrt(Zhat) and
-sinh(beta/2)/sqrt(Zhat). Their difference gives w, which tends to
cosh(beta)-2cosh(beta/2)+1, NOT zero. The norm ratio tends to cosh(beta).

At beta=1 and K=65,536 the exact rational certificate establishes

    r <= (K-1)/(4K^2) < 1/250,000,
    D > 3/8-1/(2K) > 0.374,
    D^2 > 2r_upper.

Here tanh(1)>3/4 follows from e^2>7: its Taylor sum through degree four
is 7 and the next term is positive. Also tanh(1/K)<=1/K. No floating-point
transcendental estimate is needed for this strict countercertificate.
Canonical sign ratio is 1, beta^2 M=1/K, and degree parameter is 1/K^2.
The earlier small-mass pilot gap certificate applies for K>=64. This
is a transfer failure even with easy/gapped pilot preparation.

The one-qubit example is an adversarial algebra control, not a proposed
research candidate, oracle problem, or speedup. Generality comes from
the all-size identities (1)-(4), not the finite matrix tests.

## 6. Why Two Natural Sign Repairs Fail

Physical Pauli conjugations induce sign vectors in row(B). For v=B^T a,
the character on y is (-1)^(a.By). All words contributing to one B label
therefore acquire the same phase. Both r and w are invariant. Averaging
over these target-preserving Pauli gauges cannot suppress bad coherence.
Independent random signs additionally vary the dim(ker B) relation-sign
invariants, changing the physical target up to this gauge equivalence.

Alternatively introduce ancilla sign tags, H_tag=sum_i J_i P_i Z_tag,i.
Its Gibbs weight on sign sector v is Z_v/(2^m Zhat), not uniform; the
partition identity Zhat=2^-m sum_v Z_v follows by character orthogonality.
For the repeated-Z example, postselecting all-plus signs has probability
cosh(beta)/(2^K cosh(beta/K)^K). At beta=1 this is <=3*2^-K. Keeping this
postselection uncharged does not repair fixed-target preparation.

## 7. Correlated Circuit Parents Are Not Sign-Free Instances

A separate exact two-qubit identity illustrates the transfer issue.
Let U=exp(-i theta X1 X2), c=cos(2theta)=3/5, s=sin(2theta)=4/5. Then

    A=UZ1U^dagger=c Z1-s Y1X2,
    B=UZ2U^dagger=c Z2-s X1Y2.

The grouped terms commute and square to I. Flipping only the X1Y2
coefficient gives B'=c Z2+s X1Y2 and

    [A,B']=4 i c s Y1Y2 = -(48 i/25) X1X2Z1Z2 !=0.

Thus independent signs on a Pauli expansion do not in general preserve
the grouped commuting circuit-parent class. This is NOT an implementation
of a published hard instance and NOT a proof that every sign choice is
easy. A transfer proposal must verify its own hardness distribution,
encoding, decoding and coefficient correlations. Projector and Z-energy
temperature conventions must not be mixed.

## 8. Adversarial Reassessment And Next Decision

Objection: a good decoder should solve the dilution example. Equation (4)
applies to every decoder of the actual form, so changing only Dec cannot
remove the obstruction. A different source or postselection is a new,
separately charged algorithm.

Objection: tiny r should imply high fidelity by gentle measurement.
Gentleness compares the actual state with its correctly decoded part,
not that part with the normalized physical exponential. The omitted
coherent bad sum is exactly w. Its normalization cannot be discarded.

Objection: W_B is expensive and pessimistic. Correct. Refusal is not a
no-go theorem. A signed, decoder-specific cancellation proof or a tighter
code-family weight bound could improve it; the present certificate makes
no general efficiency or necessity claim.

Objection: these are already-classical controls. Correct. No algorithm
candidate is admitted. They prevent a false connection between a promising
pilot gap and an unrelated hard output problem.

NEXT SCIENTIFIC TEST: choose an explicit, sign-preserving native family;
verify the requested output remains nontrivial after the prior classical
fiber/sign and relative-distance tests; then certify fixed-sign transfer
by (3) or a stronger signed bound with a priced decoder. Reject a proposal
that merely imports known circuit-parent hardness, duplicates terms, or
randomizes the target. Do not add another preparation-only gap experiment
unless an end-to-end family survives these checks. A natural source for
the separately audited Rees mechanism remains an alternative priority.
