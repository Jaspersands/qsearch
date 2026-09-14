# A Typical-Mask Obstruction for One Common Group-Algebra Query

Status: derived, review pending. Finite checks and outward integer bounds
are implemented; there is no independent review, formal proof certificate,
novelty determination, or new quantum algorithm.

Subsequent extension: [arbitrary-mask tail fidelity](MASK_TAIL_FIDELITY_OBSTRUCTION.md)
removes the uniform-overlap penalty for high-occupation masks. The bound in
this note is still sharper for uniform masks; neither rules out all masks.

## Statement

Let n>=16 be even, G=S_n, D=n!, C the fixed-point-free involution class,
M=|C|=(n-1)!!, and L=n(n-1)/2. The inputs are either rho_0=I/D or
rho_h=(I+R_h)/D, with ONE unknown h drawn uniformly from C and shared by
all copies. There is no hidden-correlated side information.

Fix before the inputs, INDEPENDENTLY of the unknown h and any
hidden-correlated prior oracle transcript:

- Any partition of the irreps into r source categories, with central
  projectors P_j. All irreps may be retained separately.
- Any group-algebra unitary U=sum_g a_g R_g. Its irrep matrices need not
  be scalar, so U need not be central.
- A participating copy count k and the full uniform selector on {0,1}^k.

Apply one controlled common query

    sum_s |s><s| tensor U_s,
    U_s=sum_g a_g tensor_i R_g^(s_i).

Record source categories classically, discard ALL physical input registers,
and retain the whole quantum selector and all source records. Any subsequent
POVM or processing of this retained state is allowed. Regular unitarity of U
implies unitarity in every subset representation, including the empty mask.

Write Omega_0 and Omega_h for these outputs. With t=floor(k/4),

    E_h T(Omega_0,Omega_h) <=
        2k sqrt(r/M) + 2^(1-k/16)
        + D (6/sqrt(L))^t
        + 4 sqrt(D) 2^(k/2) (2/sqrt(L))^t.                 (1)

The decision distance T(Omega_0,E_h Omega_h) is no greater, and is also at
most (1/2)sqrt((2^k-1)/M). The raw-copy cap does NOT bound the average
individual distance. All h-averaging is AFTER tensor products.

For every polynomial budget K(n), the decision distance tends to zero
superpolynomially, uniformly over every pre-input choice 1<=k<=K(n).
This includes algorithms that ignore a preselected set of extra copies,
and independent classical randomization of the participating count.
It does not include source-dependent selection or regrouping of inputs.

The conclusion also holds for fixed diagonal mask contractions with a
common inverse-polynomial success lower bound on the uniform selector.
Central fixed-weight masks have p>=1/(k+1). Arbitrary mask states with
exponentially small overlap, retained physical data, source-adaptive
operations, and multiple queries are NOT ruled out.

## Local Kernels and the Positive Comparison

This proof uses the physical kernel rederived and checked in
[Before the Final Selector Measurement](SOURCE_SELECTOR_QUANTUM_BOUND.md).
For completeness, let

    p_j(g)=D^-1 sum_(lambda in j) d_lambda chi_lambda(g),
    p_j0(g)=p_j(g), p_jh(g)=p_j(g)+p_j(hg),
    q_jeta=p_jeta(e), H_0={e}, H_h={e,h}.

The source-j local selector kernel is

    K_jeta(u,v)=(1/2) [[q_jeta,       p_jeta(u^-1)],
                      [p_jeta(v),   p_jeta(u^-1 v)]].

The complete state is the direct sum over source tuples of
sum_(u,v) conjugate(a_u)a_v tensor_i K_(j_i,eta)(u,v).
Natural source masses are not conditioned away.

The coset diagonal u^-1 v in H_eta is the positive normalized comparison

    F_(eta,g)[j]=(q_jeta I+p_jeta(g)X)/2,
    Q_0=sum_g |a_g|^2 F_(0,g)^tensor k,
    Q_h=(1/2)sum_g |a_g+a_(gh)|^2 F_(h,g)^tensor k.

The coefficient translate is gh, not hg: centrality of a is unavailable.
Unitarity supplies sum_g conjugate(a_g)a_(gh)=0. The F states all commute
in a common source/Walsh basis.

For B_j(h)=sum_g |a_g|^2 p_j(hg)^2, projector orthogonality gives
sum_x p_j(x)^2=q_j and therefore E_h B_j(h)<=q_j/M. This uses a subset
sum over {hg:h in C} for each g, not pointwise centrality of |a_g|^2.
Cauchy-Schwarz, Jensen, the class-function identity p_j(gh)=p_j(hg),
and product-law Lipschitz continuity then give

    E_h T(Q_0,Q_h)<=2k sum_j sqrt(q_j/M)<=2k sqrt(r/M).      (2)

The detailed cross-weight cancellation is in the linked derivation. Neither
Q is claimed to be an efficient classical sampler or the exact output.

## Project Away Rare Selector Weights

Let P_t retain computational selector strings of Hamming weight at least t,
acting as identity on every source record. The diagonal of the selector
is uniform because EACH controlled U_s is unitary. This holds for each h
and each natural source block, independent of U's centrality. Hence

    Tr((I-P_t)Omega_eta)=pi,
    pi=Pr[Binomial(k,1/2)<t].

The unnormalized gentle-projection bound is
T(Omega_eta,P_t Omega_eta P_t)<=sqrt(pi). One can verify the constant by
purifying Omega: in the accepted/rejected two-dimensional span, the
difference from its unnormalized projection has trace norm
sqrt(4pi-3pi^2)<=2sqrt(pi); partial trace cannot increase it.
This is standard gentle-measurement reasoning, not a new lemma; see also
[Watrous, Chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.3.pdf).

Only the TWO actual states need the gentle bound. Keep the comparisons
projected and use trace-norm contractivity on their difference:

    T(Omega_0,Omega_h) <= 2sqrt(pi) + T(Q_0,Q_h)
        + (1/2)||P_t(Omega_0-Q_0)P_t||_1
        + (1/2)||P_t(Omega_h-Q_h)P_t||_1.                 (3)

There is no conditioning or physical postselection, and no division by
1-pi. P_t is a comparison tool, not an additional operation in the proposed
algorithm.

An elementary binomial estimate avoids floating-point tail probabilities.
Markov applied to 2^-W gives

    pi <= 2^(k/4)(3/4)^k <= 2^(-k/8).

The second inequality follows by raising its one-copy form to the eighth
power: 3^8=6561<=8192. Therefore 2sqrt(pi)<=2^(1-k/16).

## Why the Remainder Shrinks Faster

Fix an off-coset pair (u,v). Split K_j=B_j+E_j.

In the bulk, u,v not in H_eta,

    B_j=(q_jeta/2)|0><0|,
    sum_j ||B_j||_1=1/2,
    sum_j ||E_j||_1<=3/sqrt(L).

If u is in H_eta, instead take

    B_j=(q_jeta/2)|0>(<0|+<1|),
    E_j=(p_jeta(v)/2)|1>(<0|+<1|),
    sum_j ||B_j||_1=1/sqrt(2),
    sum_j ||E_j||_1<=sqrt(2)/sqrt(L).

If v is in H_eta, use the transposed orientation. Both endpoints cannot
be in H_eta for an off-coset pair. The character column envelope
sum_j |p_j(g)|<=1/sqrt(|class(g)|), and |class(g)|>=L for nonidentity g,
give the stated E bounds independently of the number of categories.

Expand tensor_i(B_(j_i)+E_(j_i)). A term with d<t E factors is killed by
P_t on both sides: every other factor pins a selector bit to zero on at
least one common side. The endpoint orientation is the same in every
position because (u,v) is shared. Using a projector on only one side
would NOT suffice for both endpoint orientations.

Summing all source tuples and using trace-norm multiplicativity yields

    ||P_t [direct-sum_j tensor_i K_(j_i)] P_t||_1
       <= sum_(d=t)^k C(k,d) b^(k-d) epsilon^d.           (4)

For epsilon<=b this is at most (2b)^k(epsilon/b)^t. Thus the bulk radius
becomes (6/sqrt(L))^t; the endpoint radius becomes
2^(k/2)(2/sqrt(L))^t. The old bound charged approximately 2^-k per pair
without recognizing that its dominant tensor terms lie on rare masks.

The combined absolute bulk coefficient weight is at most D, including
the half-norm factors from both hypotheses. The combined endpoint weight
is at most (1+sqrt(2))sqrt(D), conservatively 4sqrt(D). Substitution into
(3), followed by (2), proves (1). The comparison is uniform in the choice
of the fixed common group-algebra unitary.

## Cover Every Polynomial Budget

For k<=5n use the monotone raw-copy bound at 5n. For k>5n use (1), charging
the mixture term at the maximum budget K and the other terms at the first
count in the interval. To remove floor-function oscillations, set
b=floor(sqrt(L)) and use k<=4t+3:

    4sqrt(D) 2^(k/2)(2/b)^t <= 4sqrt(8D)(8/b)^t.

This envelope is nonincreasing in k because b>8. The bulk term and
discarded-weight bound are also nonincreasing. No sweep through all K
values is required. The implementation rounds all bounds OUTWARD using
integers and exact rational squares.

For the asymptotics, b>=n/2, D<=n^n, M>=(n/2)!, and r<=2^(n-1).
The prefix bound and polynomial-budget mixture term are superpolynomially
small. At t>=5n/4-1 the bulk is at most
n^n(12/n)^(5n/4-1), and the endpoint envelope is at most a constant times
n^(n/2)(16/n)^(5n/4-1). Both decay as exp(-Omega(n log n)).
The gentle error decays as 2^-Omega(n). This proves the uniform
polynomial-budget statement, not a claim about exponential budgets.

A fixed diagonal mask contraction F with success at least p commutes
with the query. Its normalized output has decision distance at most the
uniform-mask bound divided by p. This is a comparison with direct mask
preparation, not a required physical postselection. In the prefix, the
raw-copy cap still applies WITHOUT division by p. For a family of copy
counts, the supplied p must be a lower bound UNIFORM over those counts.

## Numerical Certificates and Scope

- S4096, every 1<=k<=4096^2: decision T<=2^-571. The raw prefix ends at
  20480 and the typical-mask suffix starts at 20481. All source irreps are
  covered. Central fixed-weight masks keep the same overall bound with
  p>=1/(4096^2+1).
- S8192, every 1<=k<=8192^2: T<=2^-2557 for uniform masks and T<=2^-2530
  for the central-weight family using a single budget-wide p.
- S1024 k=8764: the formerly vacuous bound is now T<=2^-544.
  However, the conservative ALL-budget certificate at S1024 is still
  vacuous. This is not a finite-degree/all-count claim at S1024.

These are conditional numerical evaluations of a derived theorem, not
independent mathematical verification or experiments performed at S4096.
The finite physical controls remain small-degree calibration.

The strengthened theorem rules out the complete uniform-mask, one-common-
query, physical-discard architecture at polynomial resources, subject to
review. It does not rule out HSP algorithms, nonabelian Fourier methods,
graph isomorphism algorithms, or quantum advantage in general. It does not
provide a classical sampler for the quantum front end.

Independent review must particularly check the two-sided projection support,
the source-summed tensor norms, both endpoint orientations, the shared-h
average, the unnormalized gentle constant, the all-budget envelope and
the mask-overlap charge. Novelty review against prior coset-measurement
and information-loss theorems remains outstanding.

## Verification Record

Completed 2026-09-14: 166 integration tests passed, a final downstream and
focused run passed 129, and the final focused suite passed 74 after adding
the no-hidden-correlated-preprocessing guard. These overlap and are not
additive coverage. Python compilation, JS syntax and diff checks passed.
Twenty noncentral physical controls include 144 projected-remainder checks;
12 interval evaluations cover quadratic/quartic budgets and both mask families.

The live binary, synthesis, dequantize, proofs, conjectures, mutate and
progress workflows completed. The existing proof lemma remains
derived/review-pending, and the new evidence gates reject stale central-only
artifacts. Obsolete mutation recommendations inside this architecture were
removed; broader adaptive and multi-query proposals remain unproved.

The full-suite attempt stopped after 65 passes at the known missing
character-moment scaling-registry write in
`tests/test_character_moment_obstruction.py:73`. It is not a green full suite.
Maintenance and the next unverified mathematical direction are in
`research/AGENT_HANDOFF.md`.
