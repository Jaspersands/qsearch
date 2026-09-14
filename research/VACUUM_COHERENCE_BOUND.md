# Empty-Subset Coherence Does Not Supply an Asymptotic Rescue

Status: derived, review pending. No independent proof review, formal
certificate, novelty determination, efficient algorithm or speedup claim.
This bounds an INCREMENT in information, not total distinguishability.

## Precisely Scoped Claim

Let G=S_n for even n>=8, D=n!, and let C be the class of fixed-point-free
involutions, of size M=(n-1)!!. Under the null input rho_0=I/D; under the
alternative rho_h=(I+R(h))/D for ONE shared h uniform in C. Take K identical
copies, averaging over h only AFTER tensor products. There is no additional
hidden-correlated side information or preprocessing transcript.

Fix a common group-algebra unitary U=sum_g a_g R(g), a partition of irreps
into classical source categories P_j, and a normalized pure selector mask,
all independently of the inputs and source outcomes. For subset S, apply
U_S=sum_g a_g R(g)^(tensor S) with identities elsewhere. Retain the selector
and all naturally weighted classical source records; discard physical inputs.
The final source/selector measurement is unrestricted. Write

    alpha = sqrt(w)|empty> + sqrt(1-w)|beta>,  <empty|beta>=0.

The phase convention on the first amplitude does not affect the conclusions.
Let f(alpha) be the class-decision trace distance of the two outputs. Let
f_pinched(alpha) be the same distance after pinching ONLY between the empty
subset and its nonempty complement. Then

    0 <= f(alpha)-f_pinched(alpha)
      <= sqrt(w(1-w))*max(B_low,B_high),                    (1)
    f_pinched(alpha) = w*T_source + (1-w)*f(beta).          (2)

For K<M, put Ebar=M/(M-K), L=n(n-1)/2, and t=min(K,n):

    B_low^2 = Ebar-1 + Ebar*(2^t-1)/M.                    (3)

If K>n, also use

    B_high = sqrt(Ebar-1) + sqrt(Ebar/M)
           + sqrt(D*Ebar)*(4/L)^((n+1)/2)
           + sqrt(D)*(1/L)^((n+1)/2).                    (4)

When K<=n only B_low is needed. At polynomial K(n), both relevant bounds
are superpolynomially small in n. They are uniform over the nonempty beta,
the vacuum probability, and the fixed common group-algebra unitary. No
radial-mask restriction is required for this statement.

Consequently adding vacuum cannot rescue an already obstructed nonempty
mask. This does NOT obstruct all beta: its nonempty/nonempty coherences
are not bounded by (1). It is not legitimate to set the unresolved f(beta)
in (2) to zero. Source outcomes still require the quantum coset-state front
end; this is not a classical dequantization.

## Source-Weighted Character Squares

For an irrep category j, let

    p_j(g)=Tr(P_j R(g))/D = sum_(lambda in j) d_lambda chi_lambda(g)/D,
    q0_j=p_j(e)>0,  qh_j=q0_j+p_j(h).

Characters of S_n are real. Within each category, Cauchy-Schwarz gives

    p_j(g)^2/q0_j <= sum_(lambda in j) chi_lambda(g)^2/D.

Column orthogonality, summed over categories, therefore gives

    sum_j p_j(g)^2/q0_j <= |C_G(g)|/D = 1/|class(g)|.     (5)

There is equality for the full irrep partition. This is a direct application
of standard character orthogonality, not a newly claimed representation
theorem. In particular the source chi-square is

    v=sum_j (qh_j-q0_j)^2/q0_j <= 1/M,                    (6)

without ANY category-count penalty. Since h stays in one class, qh_j is
independent of which h was drawn. For K source records, q_eta,J is their
product probability and

    sum_J qh_J^2/q0_J = (1+v)^K <= (1+1/M)^K <= Ebar.    (7)

The final inequality follows by binomial expansion, binom(K,i)<=K^i,
and the geometric series when K/M<1. Hence
T_source<=sqrt(Ebar-1)/2. Using Ebar avoids K-dependent giant integer powers.

For n>=8 every nonidentity conjugacy class in S_n has size >=L. This is
the standard minimum-class fact, not inferred from our finite tables; see
[Elkies's group-theory notes](https://people.math.harvard.edu/~elkies/M155.15/notes.html)
in the discussion of automorphisms of S_n. Small S3 controls below instead
use their ACTUAL minimum class size and do not substitute n(n-1)/2 there.

## Bound One Empty-Subset Row

The naturally weighted source-J Schur coefficient is

    C_(eta,J)(S,T)=Tr(U_T^dagger U_S sigma_(eta,J)),
    A_J=E_h C_(h,J)-C_(0,J),
    V(S)=sum_J |A_J(S,empty)|^2/q0_J.

The empty query is zeta*I, zeta=sum_g a_g, with |zeta|=1 because the trivial
representation also sees a unitary. Regular-basis unitarity gives
sum_g |a_g|^2=1. These facts do not require a central U.

### Low Subset Weights

Fix a nonempty S with m=|S|. THIS matrix element depends on m active
physical copies and the remaining K-m classical source labels. Those
inactive source probabilities are independent of the conjugate h. Thus
the relevant compressed input hypotheses are

    tau_0=rho_0^tensor m tensor q0^tensor(K-m),
    tau_1=(E_h rho_h^tensor m) tensor qh^tensor(K-m).

This is NOT a simulation of the entire selector channel by m copies.
Each S can have a different active set; coherences between two nonempty
subsets have not been compressed by this argument.

To see the required bound, condition only on inactive source labels I,
and let Delta_I=qh_I E_h rho_h^tensor m-q0_I rho_0^tensor m. For an active
source projector P_A, Hilbert-Schmidt Cauchy gives

    |Tr(U_S P_A Delta_I)|^2 <= rank(P_A)*Tr(P_A Delta_I^2).

Here U_S commutes with the source projectors, so its restriction is unitary;
rank(P_A)=D^m q0_A. Sum over all A and I, retaining denominators q0_A q0_I:

    V(S) <= Tr((tau_1-tau_0) tau_0^-1 (tau_1-tau_0)).     (8)

The regular trace identity is
D*Tr(rho_h rho_h')=1+1_(h=h'). Consequently the active class-averaged
chi-square equals (2^m-1)/M. Factorizing the classical source component in
(8) yields

    V(S) <= [1+(2^m-1)/M]*(1+v)^(K-m)-1.                (9)

For every 1<=m<=min(K,n), (7) makes this at most (3).
There is no rare-source postselection or success renormalization.

### High Subset Weights

In the (S,empty) COLUMN, the expansion uses a_g times conjugate(zeta).
The transposed row has the conjugate coefficients. Dropping only that
common modulus-one phase, the class-averaged column is the sum of

    a_e*(qh_J-q0_J),
    (E_h a_h)*qh_J,
    E_h sum_(g not in {e,h}) a_g
        prod_(i in S)[p_ji(g)+p_ji(hg)] prod_(i not in S) qh_ji,
    -sum_(g != e) a_g prod_(i in S)p_ji(g) prod_(i not in S)q0_ji.

Give each source vector x the norm ||x||_(q0^-1)^2=sum_J |x_J|^2/q0_J.
The first two terms have norms at most sqrt(Ebar-1) and sqrt(Ebar/M),
respectively. The second uses |E_h a_h|<=1/sqrt(M), NOT a pointwise bound
on a particular a_h.

For g not in {e,h}, both g and hg are nonidentity. By (5),

    sum_j |p_j(g)+p_j(hg)|^2/q0_j <= 4/L.

For g!=e the null counterpart is <=1/L. The weighted norm of a product
factors over copies. Triangle inequality, sum_g |a_g|<=sqrt(D), and (7)
bound the third and fourth terms by

    sqrt(D*Ebar)*(4/L)^(m/2),  sqrt(D)*(1/L)^(m/2).

Since L>4, these decrease with m. Evaluating at m=n+1 bounds every remaining
weight through K, establishing (4). The low and high ranges have no gap.

## From Rows to an Information-Gain Bound

The off-diagonal vacuum/nonempty block in each source sector has rank at
most one. Its Hermitian completion has half trace norm

    sqrt(w(1-w))*sqrt(sum_(S != empty) |beta_S|^2 |A_J(S,empty)|^2).

Summing over J and applying Cauchy with the NATURAL q0_J, whose sum is one,
bounds this by

    sqrt(w(1-w))*sqrt(sum_S |beta_S|^2 V(S)).             (10)

The beta probabilities must be source independent to exchange these sums
as written. Equation (10), the row bounds and trace-norm triangle prove
the upper bound in (1). Pinching is a channel, proving its lower bound.
Additivity of the trace norm on the two pinched blocks proves (2).

For any fixed polynomial K(n), Ebar-1=K/(M-K) is negligible. Also
M>=(n/2)!, D<=n^n and L>=n^2/4. Thus 2^n/M is superpolynomially small,
and sqrt(D)*(4/L)^((n+1)/2)<=4^(n+1)*n^(-n/2-1) is as well.
This proves the claimed asymptotic rate, not a simulation at large n.

## Attempts to Falsify and Limits

- Exact S3/S4/S6 character checks cover every group element, all irrep
  labels, a sign coarsening and the fully merged source category. The
  full-label bound is saturated; the fully merged source chi-square is zero.
- Actual dense noncentral S3 group-algebra unitaries at K=2,3 reconstruct
  every empty-subset column for all ordered source tuples and all hidden
  members. All ten nonempty rows satisfy (9) and all four coefficient bounds.
- Twenty physical mask probes include positive finite coherence gains:
  maxima about 0.059125 and 0.019708 at K=2,3. Therefore this is NOT a
  pointwise zero-gain theorem. Pure vacuum has zero gain but nonzero
  source-only distance, falsifying the substitution of gain for total T.
- Conditional dyadic bounds for K=n^2, uniform over w, are 2^-3 at n=16,
  2^-115 at n=128, 2^-1679 at n=1024 and 2^-8763 at n=4096. These are
  outward-rounded integer evaluations of (1), not optimal bounds or
  large-degree experiments. K>=M gives a vacuous envelope, not an exception
  silently treated as a polynomial-budget certificate.
- Nonidentical/source-selected queries, arbitrary source measurements,
  hidden-correlated prior transcripts, source-adaptive masks, retained
  physical systems and multiple queries need new arguments. No boolean
  assumption contract verifies that an arbitrary program satisfies them.

The most plausible failure of this line as a useful research contribution
is scope rather than a finite numerical counterexample: it eliminates only
one type of coherence in an already restrictive architecture. Even a correct
and new bound could be of limited algorithmic importance. Stop extending
it mechanically if the remaining low-weight sector requires essentially
the same work as a more general retained-physical measurement architecture.

## Literature Boundary and Next Falsifier

[Moore and Russell, sections 3 and 5](https://arxiv.org/html/quant-ph/0504067)
give a useful contrasting target: a measurement on the span of missing-harmonic
subset subspaces, and an efficient measurement for an individual subset,
without a general efficient implementation of the span measurement. The
present physical-discard channel does not implement that span projector.
Our bound must not be used to declare their retained-physical construction
information-theoretically impossible. This is a scope comparison, not a
claim that their paper proves the bound here.

Next examine coherences BETWEEN nonempty low-occupation sectors. A tempting
but unproved move is to extend the one-row compression to the entire block;
the number of possible active subsets can defeat the resulting norm bound.
Require an actual bound on the full source-weighted operator, or a concrete
family that falsifies such a bound. An independent proof/prior-art review
of this note and the preceding mask-symmetry reduction remains necessary.

Implementation: `theorems/coset_vacuum_coherence.py`,
`source_selector_vacuum_coherence_contract` in `core/isotypic_instruments.py`,
and `tests/test_coset_vacuum_coherence.py`. Existing CLI:
`python qsearch.py coset-binary-carrier-instruments`. Registry evidence uses
`VACUUM-COHERENCE-NOT-ASYMPTOTIC-RESCUE`; its claim gate explicitly denies
a total-information or all-mask obstruction.
