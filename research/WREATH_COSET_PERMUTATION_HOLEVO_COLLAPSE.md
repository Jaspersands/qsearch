# Wreath Source Correction And Matched Classical Recovery

**2026-10-30: the historical factorial Holevo-collapse claim is withdrawn.**
The complete original negative is preserved by the hash-bound quarantine
mechanism, not rewritten into a different claim. The old input was not a
subgroup; its raw and compressed state formulas were mutually inconsistent.

A valid twisted-diagonal repair has substantial quantum Holevo information,
but the SAME full hiding-oracle access already permits polynomial classical
recovery. This is not general code equivalence, rigid graph isomorphism, a
quantum speedup, or a new hard problem. No new candidate is admitted.

The historical filenames and command remain only for provenance:

```sh
python qsearch.py wreath-coset-permutation-holevo-collapse
node research/certificates/wreath_coset_permutation_holevo_collapse_crosscheck.js
```

The command writes normalized-state controls and classical recovery results,
and quarantines the old record unless `--no-registry` is supplied. It cannot
re-register that record. Finite controls never substitute for the proofs below.

## 1. Fix The Source Before Evaluating It

Write permutations as image arrays with ab(i)=a(b(i)). Let
W=(S_n x S_n) semidirect C2, with the nontrivial bit swapping factors:

    (a,b,0)(c,d,t) = (ac,bd,t),
    (a,b,1)(c,d,t) = (ad,bc,1 xor t).

The old set was {(pi,pi,0)} union {(pi,pi*tau,1)}. Take n=3,
tau=(1 2), pi=(0 1), x=(e,tau,1), y=(pi,pi,0). Both factors are in the
set, but xy=(pi,tau*pi,1) is not: tau*pi differs from pi*tau. There is no
coset-state source for that purported subgroup for general noncentral tau.

A REAL subgroup is obtained by conjugating the diagonal-plus-swap subgroup
H_e by (e,tau,0):

    H_tau = {(pi,tau*pi*tau^-1,0): pi in S_n}
        union {(pi*tau^-1,tau*pi,1): pi in S_n}.

Its order is 2n! and its index in W is n!. Equivalently it stabilizes tau
under the action (a,b,0):x -> b*x*a^-1 and
(a,b,1):x -> b*x^-1*a^-1. This supplies a valid family; it does not prove
that an arbitrary coding or graph problem reduces to that family.

The access promise for the attack is an oracle f with f(x)=f(y) exactly
when xH_tau=yH_tau. Labels may be arbitrarily and opaquely relabeled; the
solver uses only equality and hashing, not their interpretation or evaluator
code. The oracle must accept all public W elements used below. Copy-only
access is a different model and does not automatically allow this attack.

## 2. Raw And Compressed States Are Different

For a genuine subgroup H<=W, the normalized regular mixed coset state is

    rho_H = (1/|W|) sum_(h in H) R_h,
    Tr(rho_H rho_K) = |H intersect K|/|W|.

Thus the raw state's purity is 1/n! for this repaired family, with rank
n! and entropy log2(n!). This purity is NOT its overlap with every other
state, nor does it imply a small Holevo information.

All irreducibles of S_n have real orthogonal models. For each partition
lambda, let d_lambda be its dimension. The plus extension of
U_lambda tensor U_lambda to W acts on the swap by tensor interchange.
Choose the factor convention D_lambda(a,b,s)=(U_lambda(b) tensor
U_lambda(a)) F^s. Its H_e invariant subspace is the one-dimensional span of
|Omega_lambda>=d_lambda^-1/2 sum_i |i,i>. The minus extension has no such
invariant, and unequal-factor irreps have none by Schur orthogonality.
Conjugating gives |psi_(lambda,tau)>=(U_lambda(tau) tensor I)|Omega_lambda>,
the row-vectorized U_lambda(tau)/sqrt(d_lambda) used in the finite control.
The other tensor convention differs by a fixed, secret-independent swap.

In group-Fourier coordinates the native raw state therefore has blocks

    rho_tau = direct_sum_lambda p_lambda
              [I_(d_lambda^2)/d_lambda^2 tensor |psi><psi|],
    p_lambda = d_lambda^2/n!.

The row register is maximally mixed independently of tau, conditional on
lambda. Discarding it leaves

    sigma_tau = direct_sum_lambda p_lambda |psi><psi|.

This is a mathematical channel description, not an implemented Fourier
transform or quantum receiver. The hidden-independent rows can also be
reattached, so they do not change the Holevo information of the ensemble.
The compressed state's purity is sum_lambda p_lambda^2, NOT 1/n!.

The conditional pure-state overlap is |chi_lambda(tau^-1 sigma)|^2/d_lambda^2.
When multiplying direct sums, the block probabilities are SQUARED:

    Tr(sigma_tau sigma_sigma)
      = (n!)^-2 sum_lambda d_lambda^2 |chi_lambda(tau^-1 sigma)|^2.

For the raw state there is an extra factor 1/d_lambda^2 from its mixed row:

    Tr(rho_tau rho_sigma)
      = (n!)^-2 sum_lambda |chi_lambda(tau^-1 sigma)|^2
      = |Z(tau^-1 sigma)|/(n!)^2.

The old inverse-conjugacy-class formula is not the raw or compressed
overlap. Its self-overlap of one already contradicted its claimed purity.

## 3. Correct One-Copy Information

Use a uniform prior on tau in S_n. Averaging each pure carrier over tau
gives I/d_lambda^2 by irreducibility. Hence the average compressed state
is I_(n!)/n!, whereas S(sigma_tau)=H(p), the Plancherel-label entropy.
For BOTH raw and compressed ensembles,

    Holevo_1 = log2(n!) - H(p) = 2 sum_lambda p_lambda log2(d_lambda).

This is large, not factorially vanishing. Since partitions are at most
the 2^(n-1) compositions, H(p)<=n-1. Thus

    max(0,log2(n!)-n+1) <= Holevo_1 <= log2(n!).

In particular Holevo_1=Theta(n log n). This does NOT say a measurement
extracts that much classical information or provide an efficient decoder.
For n=3, p=(1/6,1/6,2/3): compressed purity is 1/2, raw purity 1/6,
and both Holevo informations equal 4/3 bits. The producer builds all six
actual 72-dimensional native density matrices and checks positivity,
normalization, all36 overlaps, and both ensemble entropies numerically.

The old k^2/n Holevo bound and its claimed copy consequence are withdrawn.
Fano's inequality also does not identify guessing probability with
2^(-Shannon conditional entropy). These are distinct information measures.
No replacement general copy lower bound is asserted.

There is also a direct decision-theoretic falsifier, not just an entropy
calculation. Since sum_tau sigma_tau=I, the effects E_tau=sigma_tau form a
POVM with average success sum_lambda p_lambda^2. It is optimal: the dual
operator Y=direct_sum_lambda (p_lambda/n!)I_(d_lambda^2) dominates each
sigma_tau/n! and has that same trace. Thus optimal one-copy success is
at least 1/p(n)>=2^(-(n-1)), contradicting factorial suppression. This
mathematical POVM is NOT an efficient measurement implementation. Also
one-half of the trace norm of sigma_tau minus its ensemble average equals
1-p(n)/n!, as does the raw-state trace distance by the reversible channels.
The historical assertion that these distances collapse is therefore false.

## 4. Classical Recovery With The Same Oracle

For n>=3, let a=(0 i) be a public star transposition and let b range over
all binom(n,2) transpositions. The left-coset promise gives

    f((a,e,0)) = f((e,b,0))
      iff (a^-1,b,0) belongs to H_tau
      iff b=tau*a*tau^-1.

Cache f((e,b,0)) for every b. These labels are distinct: equality between
two such elements would put (e,b^-1*b',0) in H_tau, forcing b=b'. Query
the n-1 star elements and look up their image pairs {tau(0),tau(i)}.
The first two distinct pairs intersect exactly in tau(0). Their other
endpoints recover all remaining images, so tau is recovered exactly.

Finally compare f(e_W) and f((tau^-1,tau,1)), a required odd-branch
subgroup element. This is a consistency check against the original oracle,
not certification of its entire promise from finitely many observations.
All calls, including this check, total

    Q(n)=binom(n,2)+n+1.

The implementation `recover_twisted_diagonal(n,query)` receives only n and
the callback. It checks label uniqueness, star consistency, bijectivity and
the final relation; it never receives tau or enumerates S_n. Image-array
work is polynomial, with oracle evaluation, label length and comparison/
hashing costs charged. Even pairwise label comparisons without ideal hashing
remain polynomial. n=2 is explicitly outside this reconstruction contract.

The implementation also rejects an identity label merged with a cached
transposition label, an observable violation of this promise. The odd check
alone is NOT a unique-secret certificate: for a proposed rho it only requires
(tau^-1*rho)^2=e. Correctness relies on the transposition-image reconstruction
and the stated full coset promise, not on that last check alone.

The executable finite controls use lazy unique opaque tokens for the native
orbit action, not plaintext permutation labels or a factorial oracle table.
All secrets in S3 and S4 are checked, followed by n=8,32,64 controls. These
are regressions of the general proof, NOT new oracle problems admitted as
research candidates. This highly symmetric repaired source is classically
solved under full oracle access; the invalid old source was never a problem.

## 5. Scope And Next Decision

The corrected source is much more symmetric than the hard order-two
wreath-HSP instances. Its even subgroup is a whole twisted diagonal S_n,
which is precisely what exposes all public transposition images. General
graph/code-equivalence subgroups do not provide that promise. Published
[Fourier-sampling results for code equivalence](https://arxiv.org/abs/1111.4382)
must be applied to their actual subgroups and measurements, not to this
replacement or an arbitrary low-dimensional carrier ansatz.

Do not call increased Holevo information a quantum advantage. A proposed
source must survive the same transposition-image attack under its true
allowed queries. If a genuinely different input restricts those queries,
state that restriction and charge quantum preparation under the SAME
restriction. A useful next source must remove the classical recovery
mechanism without assuming free coherent access to the desired states.
No broad code-equivalence or nonabelian-HSP impossibility follows.
