# Copy-Only Mixed Conjugation: An Isospectral Obstruction

2026-10-23. Elementary proof and exact finite controls. This is a negative
access-model result, not a new quantum algorithm, a new hard application,
or an independently reviewed theorem. The property-testing mechanism is
standard; novelty is NOT claimed.

## Decision

Do not extend the Rees scalar-support source to arbitrary mixed-state
CONJUGATION symmetry using only copies and a trace-distance orbit gap.
Even the known cyclic group C3, acting on one qutrit, has an unconditional
exponential-in-register-size copy obstruction. The obstruction survives
equal spectra, equal rank, equal purity, and equal entropy in the two cases.
An explicit classical collision test matches the copy bound in order.

The current repository correctly excludes this task. This note explains
why that exclusion is essential, rather than an unimplemented convenience.
It does NOT refute clean HSP, pure-state Rees, scalar-support learning,
low-rank promises, or stronger charged input access.

## 1. Input And Exact Counterfamily

Fix p=3 (the formulas hold for every integer p>=2), M>=1, and 0<v<=1.
The known basis is |b,a,r>, with b in [M] and a,r in C_p. Dimension D=p^2 M.
The public representation shifts ONLY r:

    R_s |b,a,r> = |b,a,r+s>.

For M=2^n this uses n qubits and two constant-size qudits. The group is
abelian of class 1<p and its controlled action has constant cost apart
from register addressing. The algorithm receives IID copies of ONE fixed
unknown state, with no purification, preparation inverse, probability
evaluator, hidden orientation table, or basis-state conditioning oracle.

Put A=1+(p-1)v and B=1-v. For each fixed orientation theta in C_p^M define
two diagonal states by their probabilities:

    P^N_theta(b,a,r) = [B + p v 1_(a=theta_b)] / (p^2 M),
    P^S_theta(b,a,r) = [B + p v 1_(r=theta_b)] / (p^2 M).

N is symmetric under all C_p. S has trivial conjugation stabilizer. For
every s!=0, TD(rho^S,R_s rho^S R_s^dagger)=v, where TD=||.||_1/2.
Thus even constant trace-distance orbit separation is insufficient.

Both states have the SAME spectrum: A/D repeated pM times and B/D repeated
p(p-1)M times. They are full rank for v<1. In both cases:

    Tr(rho^2) = [1+(p-1)v^2]/D.

For S and s!=0:

    Tr(rho R_s rho R_s^dagger) = (1-v^2)/D,
    normalized HS overlap = (1-v^2)/[1+(p-1)v^2].

The normalized Hilbert-Schmidt orbit gap is constant for constant v, but
the ABSOLUTE Hilbert-Schmidt distance is O(D^-1/2). A result promised an
absolute inverse-polynomial HS gap is not contradicted. No known-spectrum
or known-purity side information distinguishes N from S.

At v=1 both states are normalized projectors of the same rank pM. For S,
R_s maps the support to an orthogonal support for every s!=0. The same
lower bound therefore also applies to copy access to maximally mixed
subspaces, even with the strongest orthogonal-orbit promise.

For both N and S, Tr(rho R_s)=0 for s!=0: a diagonal matrix times a
nonidentity shift has zero diagonal. Their scalar-support stabilizers are
both trivial. Applying the current Rees source would correctly learn that
DIFFERENT quantity; it would not learn conjugation symmetry.

## 2. Unconditional Copy Lower Bound

Choose theta uniformly once, independently for each bucket. Keep it FIXED
across all T copies. Let mu_N and mu_S denote the two T-copy averaged
states. Every state is diagonal in the same known basis. Hence their trace
distance is exactly the total variation distance of their classical sample
strings. All collective measurements, adaptive protocols capped at T
copies, public group gates, and ancillary computation are channels of this
input and cannot increase distinguishability.

Under either case the bucket labels b_i are IID uniform on [M]. Conditional
on no bucket repeating, averaging the independent hidden orientations
makes every (a_i,r_i) uniform. The two sample laws agree EXACTLY on this
event, and give it equal probability. Therefore

    TV(mu_N,mu_S) <= 1-(M)_T/M^T <= min(1,T(T-1)/(2M)).       (1)

For T>M interpret the collision probability as 1. If an algorithm returns
the correct subgroup with error <=delta<1/2 on EVERY promised input, its
averaged decision probabilities differ by at least d=1-2delta. Thus

    T(T-1) >= 2M(1-2delta).                                 (2)

For constant error, Omega(sqrt(M)) copies are necessary. With M=2^n this
is exponential in n, despite a known group of order THREE. Computation
time, simulator sophistication, and group-theoretic receiver improvements
cannot remove this input-information obstruction.

This minimax proof does not redraw the hidden orientation after each copy.
Doing so would erase all information and define a different source.

## 3. Visibility Dependence And Exact Likelihood Check

Let U be the uniform distribution on the full basis. For one of the two
cases, independent hidden orientations theta,eta agree in K buckets, where
K~Binomial(M,1/p). Their one-sample likelihood cross moment is

    E_U L_theta L_eta = 1+v^2(pK/M-1).

Consequently the exact chi-square divergence of either T-copy mixture
from U^T is

    chi2 = E_K [1+v^2(pK/M-1)]^T - 1.                       (3)

For a null and a signal orientation, the cross moment is exactly 1:
their biases act on independent row and column coordinates. This remains
1 after taking T copies and averaging. Cauchy-Schwarz gives

    TV(mu_N,mu_S)^2 <= chi2/2.                              (4)

Using 1+x<=exp(x) and the bounded-variable moment-generating bound on the
M independent centered variables p*1_match-1, of range length p,

    chi2 <= exp(x)-1,  x=p^2 T^2 v^4/(8M).                  (5)

This proves Omega(sqrt(M)/v^2) copies for fixed p and constant error. The
code uses a conservative entirely rational consequence: exp(x)<=1/(1-x)
for 0<=x<1. Equations (4)-(5) imply the necessary condition

    T^2 >= 16M d^2 / [p^2 v^4 (1+2d^2)], d=1-2delta.        (6)

For x>=1 this necessary condition is automatic; no invalid exponential
estimate is used there. Exact integer ceilings give certified lower
bounds, NOT sufficient sampling budgets.

For finite verification, count observations n_bj on the biased coordinate
and k_b total samples in bucket b. The mixture likelihood is independently
computed as

    product_b [(1/p) sum_j A^(n_bj) B^(k_b-n_bj)].           (7)

Direct enumeration of hidden orientations checks (7); exhaustive joint
words check (3)-(4). In particular T=2 gives

    TV = v^2(p-1)/(pM),  chi2=(p-1)v^4/M.

These are finite checks of a general proof, not asymptotic extrapolation.

## 4. Matching Classical Baseline

Measure every copy in the known basis. Compute

    Z = sum_(i<j) 1_(b_i=b_j) [1_(a_i=a_j)-1_(r_i=r_j)].

Positive selects N; negative selects S; charge ties as errors. The score
can be computed by row/column hash counts in O(T) expected RAM operations
and O(T log D) bits, not by materializing every pair.

Set s2=[1+(p-1)v^2]/p, s3=[A^3+(p-1)B^3]/p^3, and

    u=v^2(p-1)/(pM),
    q=[s2(1-2/p)+1/p]/M,
    w=[s3-2s2/p+1/p^2]/M^2.

For N, E Z=binom(T,2)u; S has the negative mean. Both variances are

    Var Z=binom(T,2)(q-u^2)+6 binom(T,3)(w-u^2).            (8)

Disjoint pairs have zero covariance; overlapping pairs give w-u^2. These
formulas hold for EVERY fixed orientation, not only its prior average.
Since q<=1/M, w<=v^2/M^2 and u>=v^2/(2M), for T>=2,

    Pr[wrong sign or tie] <= Var Z/(E Z)^2
                         <=16M/(T^2 v^4)+64/(T v^2).

Thus T=ceil(256 sqrt(M)/v^2) suffices for error <1/3 for all M>=1. This
constant is deliberately loose. Together with (6), the family's classical
AND quantum copy complexities are Theta(sqrt(M)/v^2), for fixed p and
constant error. It supplies no quantum sample advantage. The upper bound
is a mathematical guarantee; a huge-state sampling campaign is not run.

## 5. Why Generic Canonical Purification Is Not A Free Fix

Suppose a copy-only channel outputs a state within TD eta of the canonical
pure state |sqrt(rho)>>, in the public basis, for EVERY N and S input.
Act on it with the known R_s tensor conjugate(R_s). For N the state is
invariant. For S each nonidentity overlap equals

    kappa_sqrt=[2 sqrt(A B)+(p-2)B]/p.

The projector onto nontrivial group characters clicks with probability

    g_sqrt=(p-1)(1-kappa_sqrt)/p > 0.

For constant v,p this is constant. On approximate outputs the difference
between the N and S click probabilities is at least g_sqrt-2eta. If
eta<g_sqrt/2 by a constant margin, data processing and (1) require
Omega(sqrt(M)) input copies. The same argument applies to a proposed
normalized density vector |rho>>/sqrt(Tr rho^2), replacing kappa_sqrt by
the normalized HS overlap in section 1. Both proposed outputs have a
constant orbit gap, yet cannot be generically made from few copies.

This proves a bound for a COMPLETE deterministic output channel. It does
not grant free conditioning on rare successful purification branches.
An alleged heralded workaround must pay success probability and retain
the full outcome instrument; no unproved heralded extension is asserted.

## 6. Attempts To Break The Argument / Scope

- Collective quantum processing: all input states commute in a known
  basis. Their trace distance is classical TV before any processing.
- Purity, rank, spectrum or entropy advice: identical in both cases.
- Large orbit gap or very easy group: constant trace gap; C3 already works.
- Subspace-only promise: v=1 gives equal-rank projector states and orthogonal
  off-stabilizer images, so it does not evade the high-rank obstruction.
- Changing norms: an absolute HS gap WOULD exclude the counterfamily at
  growing D. Normalizing overlaps silently changes the access cost.
- Low rank: this construction has rank proportional to D. It does not
  settle polynomial-rank or specially structured mixed states.
- Efficient hidden preparation: arbitrary orientation tables have length M.
  We do not prove exponential hardness for one fixed family of succinct
  polynomial-size preparation circuits, or pseudorandomness assumptions.
- Stronger access: a probability evaluator distinguishes row versus column
  structure with O(p) suitably chosen evaluations; a supplied canonical
  purification distinguishes with O(1) copies for constant v. Those are
  DIFFERENT resources, not consequences of IID density-operator copies.
- Runtime polynomial in D, rank or inverse purity is not ruled out. Only
  a generic poly(log D,1/v) copy guarantee is contradicted.
- Public orientation advice, state-conditioned sampling, or a changed
  verification target falls outside the theorem.

The decisive falsifier is explicit: a proposed copy-only generic learner
with fewer copies than (2) or (6), and the stated worst-case error, must
fail on some member of this family. An independent proof error or an
additional stated input promise excluding this family would change the
decision. Finite tests cannot establish the full quantum-channel proof.

## 7. Prior Art And Research Consequence

The collision/uniformity-testing mechanism is classical prior art; see
[Paninski, A coincidence-based test for uniformity](https://sites.stat.columbia.edu/liam/research/pubs/sparse-unif-test.pdf).
We give a self-contained adaptation to two isospectral symmetry classes.
No claim of first discovery, publication priority or literature completeness
is made.

[Holt and Subramanian, Learning quantum symmetries](https://arxiv.org/html/2609.38085),
section 10.4, separately defines copy-access conjugation and subspace
symmetry learning. The present argument addresses those access models for
trace norm; it does not refute their scalar-action algorithms or attribute
a polylog-dimension conjugation theorem to them.

Repository dependencies inspected: REES_PROJECTIVE_STATE_SOURCE.md,
STATE_SYMMETRY_COSET_TRANSFER.md, NOISY_COSET_LPN_BOUNDARY.md. The existing
LPN boundary concerns a different task and a computational assumption;
this result is unconditional and about conjugation information in copies.

Do not build a generic mixed-conjugation receiver on the assumption that
vectorization/purification is inexpensive. Return to a charged constructive
source with a natural problem reduction, or attack the SAME native MPI
problem classically. More small-state conjugation benchmarks would not
remove the obstruction. Integration is deferred while migration is live.
