# Independent review: fixed corrupted-character reconstruction

2026-11-05. Read the current `research/STATE.md` and `research/TRAPS.md`.
This is a focused mathematical review of the proposed fixed-corruption
extension. No archives, network, Git, registry, or external-service action.
The reviewed construction builds on the independently reviewed squarefree
resultant receiver, not on a finite numerical inference.

## Verdict, source, and quantified theorem

ACCEPT the written extension under the following exact source promise.
Fix d>=2 and a public 0<=rho<1/4, and put kappa=1-4rho>0. The unknown
polynomial Q is monic squarefree of degree d over the odd prime field F_p.
There is ONE FIXED function F:F_p->{+1,-1} such that

    #{x:F(x)!=lambda(Q(x))} <=rho p,
    lambda(0)=+1, lambda(z)=chi_p(z) for z!=0.

The input consists of fresh exact pure tensor copies of

    |phi_F>=p^(-1/2)sum_x F(x)|x>.

A fixed corrupted BIT oracle or its uncontrolled unitary raw phase oracle
can produce these copies. This is not mixed-state noise, device noise,
independently resampled error tables, correlated copies, or a frozen bank
being silently reused. The error locations and their indicators are not
supplied. Source copies are never inverted or cloned.

A sufficient prime threshold is

    L_d=512*9^d*d!,
    p>=max{L_d,64d^2/kappa^2}.

The resulting written gate/copy bound is
C_d poly(log p,kappa^(-1),log(1/eta)), with the source model and fixed degree
as above. Constants in d are large and explicit below. No quantum execution,
novelty, classical hardness, asymptotic separation, growing-degree efficiency,
or exact finite-p decoding-radius optimality is established.

## 1. Exact signed-subset overlap

The d-copy distinct-root projection, sorting/permutation cleanup, coherent
scalar phase chi_p(a)^d, and clean coefficient encoding do not use Q or its
error positions. Because all F(x) are signs, the distinctness success remains
alpha=(p)_d/p^d, independently of the corruption pattern.

Let r<=d be the number of rational roots of Q and n=p-r. Let B be the number
of corrupted NONROOT inputs. The squarefree virtual norm-character state
vanishes on every split R sharing a root with Q. Thus root-position errors
make no contribution to the comparison overlap. On the good R, the extra
phase is the product of d error signs drawn uniformly WITHOUT replacement
from the n nonroot positions. Exactly B of these signs are negative.

Using the previous notation

    N0=(p-1)binom(p,d),
    Ngood=(p-1)binom(n,d),
    U=product_i(p^(d_i)-1),
    gamma_clean=Ngood/sqrt(N0*p*U),

the actual corrupted coefficient state S_F satisfies the EXACT identity

    |<N_Q|S_F>|=gamma_clean*|E_d|,
    E_d=sum_j (-1)^j binom(B,j)binom(n-B,d-j) / binom(n,d).

The scalar phase and resultant sign remain unchanged. The root error signs
are neither measured nor postselected away. The constant-modulus source
state on all split R is still the actual prepared state.

## 2. Controlled IID comparison and uniform escape

Put mu=1-2B/n. At p>=4d, B<=rho p<=p/4 and n>=p-d>=3p/4, so mu>=1/3.
For d IID draws from the n nonroot positions, the mean product is mu^d.
Conditioning those draws on distinctness gives exactly E_d. The probability
of a collision is at most binom(d,2)/n. Since each product lies in {+1,-1},

    |E_d-mu^d|<=2 Pr(collision)<=d(d-1)/n.

The factor 2 is necessary in this bounded-sign coupling argument. If
n>=2d(d-1)3^d, then

    E_d>=1/(2*3^d)>0.

At p>=4d^2, the squarefree proof gives gamma_clean>=1/(4sqrt(d!)), hence

    gamma_F=|<N_Q|S_F>|>=1/(8*3^d*sqrt(d!)).

The same virtual state is flat on U dual-unit labels in H=Q^perp. Every
proper W<H has virtual Fourier mass at most p^(d-1)/U<=2/p. Therefore

    Pr_{F S_F}[y in H\W]
      >=[gamma_F-sqrt(2/p)]_+^2.

At p>=L_d, the square-root term is at most
1/(16*3^d*sqrt(d!)), giving conditional escape at least
1/(256*9^d*d!). Including alpha>=1/2 gives at least 1/L_d per attempt.
A block of d fresh attempts has probability at least

    q0=L_d^(-d)

of giving d independent vectors spanning H; it consumes d^2 fresh copies.
The same degree-d squarefree nullspace filter produces Q on that event.

The stated L_d dominates all auxiliary thresholds. For d>=2,
d!>=d(d-1), L_d>=4d^2, and L_d>=2d. Hence n>=p-d>=p/2>=L_d/2,
and L_d/2=256*9^d*d!>=2d(d-1)3^d. These inequalities are intentionally
loose but uniform. No further asymptotic assumption is hidden in the
IID comparison or root count.

## 3. Verification against a fixed corrupted source

For the true candidate,

    <phi_Q|phi_F>=1-2E/p>=beta=1-2rho=(1+kappa)/2,

where E is the total error count. Its public-state projection therefore
accepts with probability at least beta^2. Unlike the clean-source proof,
true acceptance is not generally one and unanimity is not a valid verifier.

For any distinct monic squarefree degree-d candidate Q', the reviewed
shared-factor argument gives

    |<phi_Q'|phi_Q>|<=b,
    b=[(2d-1)sqrt(p)+2d]/p.

Changing at most rho p signs changes the normalized overlap by at most
2rho, so

    |<phi_Q'|phi_F>|<=2rho+b.

At p>=64d^2/kappa^2, b<=kappa/2. For example the two terms are bounded by
kappa/4 and kappa^2/(32d), respectively, whose sum is <kappa/2. Thus every
wrong candidate's projection probability is at most 1/4, while the true
one is at least beta^2. Let

    Delta=beta^2-1/4=kappa/2+kappa^2/4>=kappa/2,
    tau=(beta^2+1/4)/2.

Use the empirical mean of K fresh-copy projections and accept when it is
at least tau. The projections use public candidate preparations and their
inverses, not an inverse of the unknown F source.

If each test's probability changes by at most Delta/8 due to approximation,
its mean remains at least 3Delta/8 away from tau on the correct side. The
conservative margin Delta/4 therefore suffices. Hoeffding gives either
false acceptance or true rejection probability at most

    exp(-K Delta^2/8).

The choice K=ceil((8/Delta^2)ln(8R/eta)) makes this <=eta/(8R). All tests
use fresh product copies of the SAME fixed F; conditional on the classically
chosen candidate and previous history, the same uniform probability bounds
hold. The candidate cannot be correlated with unconsumed input copies.

For a bit representation of the public rho, tau is explicitly computable.
If it is rounded, require threshold error <=Delta/8; together with the
per-test Delta/8 approximation this still leaves margin >=Delta/4.
The precision cost is polynomial in log(kappa^(-1)) and log K. A claimed
exact-real parameter oracle is neither needed nor supplied.

## 4. Bounded schedule and error accounting

Use the same shared public root-factorization seed and bounded sampler as
in the squarefree proof. On its one good event, all coefficient cleanup
works simultaneously for all supported labels and all blocks.

Take total public-circuit operator error <=q0/8 per block. The event error
is at most q0/4, leaving true-candidate probability >=3q0/4 and hence
>=q0/2. Set

    R=ceil((2/q0)ln(4/eta)).

The probability that no block produces Q is at most eta/4. A union bound
over at most R candidate verifications gives total verification error at
most eta/8, covering both rejection of a true candidate and acceptance of
a false one. One may analyze all R blocks in advance, then couple to the
actual algorithm that stops at its first acceptance; early stopping does
not invalidate this union bound.

Shared seed failure <=eta/16 and capped seed-sampler ABORT <=eta/8 bring
the displayed total to 9eta/16<eta. Approximate block/test circuits are
already included in the corresponding probability bounds, so their errors
are not counted again as a separate final hybrid budget.

Copy cap: R(d^2+K). The logarithmic block precision depends on fixed d;
verification sample count is polynomial in kappa^(-1), log R, and
log(1/eta). The public seed, reversible field/polynomial arithmetic,
coefficient maps, approximate abelian QFTs, linear algebra, and public
candidate circuits retain the previous polynomial gate accounting.
Independent device errors or mixed input-state errors are not covered.

## 5. Classical comparators and the quarter-distance boundary

Kopparty's proved Algorithm A has an error radius approximately 1/8, not
1/4. For fixed rho<1/8 it can be applied after charging at most d further
root-padding disagreements and respecting its actual degree bound
(epsilon/16)sqrt(p). Its theorem must not be extended to all rho<1/4 merely
because the present quantum proof treats that regime.

An elementary matched classical BIT-query comparator also exists throughout
the stated regime. Enumerate the at most p^d monic degree-d candidates,
filter squarefree, and compare their Hamming distance to F. Full-table
comparison takes p queries and O(p^(d+1)poly(d,log p)) time. Uniqueness follows
from the same Weil separation and the promise rho<1/4 with b<=kappa/2.

In fact the classical query cost need not be p. Draw

    T=ceil(128*kappa^(-2)*ln(2*p^d/eta))

IID uniform classical F queries and evaluate every public candidate on them.
Hoeffding plus a union bound makes all empirical Hamming fractions accurate
within kappa/16 with probability >=1-eta. The true distance is <=rho;
any wrong candidate's distance is at least (1-b)/2-rho. Their gap is at
least (kappa-b)/2>=kappa/4, so empirical minimization still separates them
by at least kappa/8. This uses polynomially many classical queries but
p^d*T*poly(d,log p) time. It is not a classical poly(log p) decoder or a
lower bound, and it underscores that query counts alone do not establish
a speedup. A fresh-phase-copy-only source retains its own access model;
these classical value-query comparators assume the BIT-oracle option.

For any distinct squarefree Q,Q' of fixed degree, their padded tables have
Hamming distance

    D=(p-sum_x lambda(Q(x))lambda(Q'(x)))/2
      =p/2+O_d(sqrt(p)).

A table that agrees with each on approximately half the disagreement set
is within ceil(D/2)=p/4+O_d(sqrt(p))+O(1) of both. Therefore every fixed
rho>1/4 admits nonunique target promises for sufficiently large primes;
no algorithm can always recover the intended Q there. This is an
information-theoretic ambiguity in one identical supplied F, not a claim
about an exact finite-p radius at rho=1/4 or the boundary approach rate.
The theorem's kappa-dependent prime threshold is consistent with this
asymptotic separation margin.

## 6. Decisive finite coupling falsifier

At p=7, Q=X(X^2+1) is squarefree with one rational root, so n=6. For d=3
and one corrupted nonroot value, B=1, the exact signed-subset mean is

    E_3=[binom(5,3)-binom(5,2)]/binom(6,3)=0,

whereas the IID expression is mu^3=(2/3)^3=8/27. This refutes an uncontrolled
substitution of the IID mean for the without-replacement source. It does
not refute the coupling inequality (whose bound is 1 here), the large-prime
theorem, or quantum reconstruction by all other measurements. The parent
may check this example with its scoped finite source control; no scan is
needed for the exact combinatorial identity.
