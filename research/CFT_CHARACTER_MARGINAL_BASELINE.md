# A classical marginal route to the character-state entropy estimator

2026-11-06. WRITTEN classical algorithm, independently reviewed with the
finite-window and precision clarifications below. Source scope separately
checked. No novelty, complete QCT simulation, joint sampling or exact
defect entropy claimed. Scoped finite classical controls are recorded below.

## Native question and strongest target

Given an explicit partition lambda of n, the inverse character transform
has row probabilities P_lambda(nu)=chi_lambda(nu)^2/z_nu. Section5.2 of
[Rathore--Zhou2610.05752v1](https://arxiv.org/html/2610.05752v1) estimates

    L_lambda=-E_nu log z_nu,
    Delta S_lambda=L_lambda+H(P_lambda),
    0<=Delta S_lambda-L_lambda<=log p(n)=O(sqrt(n)).

Here p(n) counts integer partitions. This is a POINTWISE explicit-lambda
application, not a uniform-random-lambda or Plancherel average. Finite
numerical or circuit error adds epsilon to the displayed bias bound.
The paper's column sampling/QCT tasks are different and stay untouched.

The proposed classical algorithm computes every single cycle-count
marginal P_lambda(m_s=m), then uses the ADDITIVE statistic

    log z_nu=sum_s [m_s log s+log(m_s!)].

It computes the SAME L_lambda to arbitrary additive epsilon
in polynomial(n,log(1/epsilon)) time. It would match the stated coarse
entropy estimator without a joint sampler. The decisive falsifiers are
finite-chain boson normalization, an unpaid infinite determinant, false
Taylor stabilization, or exponential coefficient/interpolation cost.

Corpus been-tried queries covered character marginals and defect entropy;
the nearby RECTANGULAR_CHARACTER_SAMPLER.md concerns COLUMNS, not this
row statistic. Scalar normalized-character Monte Carlo is also not the
same sampling task. Primary paper Sections2.3,5.2,6 were inspected; its
existing classical samplers are for uniform/almost-uniform cycle columns.
Baseline lookup was issued before building this classical control.

## 1. A formal displacement encodes one count marginal

Work first in the charge-zero infinite fermionic wedge, with occupied
Maya positions lambda_i-i and negative filled vacuum. Define

    b_s=sum_j c_(j-s)^dagger c_j,
    b_s^dagger=sum_j c_(j+s)^dagger c_j.

On finite-energy vectors these are well-defined; telescoping occupation
numbers gives [b_s,b_s^dagger]=s. This is NOT an identity of the paper's
finite 2n-mode operators on their whole Hilbert space.
The normalized bosonic occupation basis is |nu>; its amplitudes in
|lambda> are chi_lambda(nu)/sqrt(z_nu). Put M=floor(n/s). Only counts
0<=m_s<=M occur. The formal scalar matrix element is

    C_s(u)=<lambda|exp[u(b_s^dagger-b_s)]|lambda>
          =exp(-s*u^2/2) sum_(m=0)^M P_lambda(m_s=m) Laguerre_m(s*u^2).

This follows from the canonical single-mode displacement identity; other
mode occupation inner products remove off-diagonal terms, and FIXED TOTAL
energy n then forces the remaining s-mode indices to coincide. Therefore
R_s(u)=exp(s*u^2/2) C_s(u) is a polynomial in u^2 of degree <=M.
If r_k=[u^(2k)]R_s, then

    B_k=E binom(m_s,k)=(-1)^k k! r_k/s^k,
    P_lambda(m_s=m)=sum_(k=m)^M (-1)^(k-m) binom(k,m) B_k.

Only Taylor coefficients through degree2M are needed. No inversion of
noisy moment data is used: all arithmetic below is exact rational.

## 2. A polynomial finite determinant supplies those coefficients

Choose F=n+2Ms+1<=3n+1 and the 2F one-particle positions [-F,F-1].
The occupied set I consists of lambda_i-i, i=1,...,F, padding lambda
with zeros. Let J have entries J_(j+s,j)=1, J_(j,j+s)=-1 whenever both
indices lie in this window. Its second quantization is the finite
compression of b_s^dagger-b_s. The Slater determinant identity gives

    C_s^finite(u)=det( [exp(uJ)]_(I,I) ).

Every term in an operator word of length k<=2M changes the partition
energy by at most ks. Its intermediate partitions have size <=n+2Ms<F,
so no excited particle or hole can cross a window boundary. More explicitly,
before the final of at most2M hops the energy is at most
n+(2M-1)s=F-s-1: the bottom s sites remain filled and the top s sites empty,
so boundary-crossing terms vanish. The filled negative vacuum itself is
not claimed to have no particles at the lower boundary. Thus finite
and infinite matrix elements agree through degree2M. This pays the
infinite-sea replacement; a global finite-chain canonical commutator is
neither needed nor asserted.

Compute T(u)=sum_(k=0)^(2M) u^k J^k/k!, take its occupied minor's determinant
over Q[u], and retain degrees<=2M. Multiply the corresponding truncation
of exp(su^2/2), then use the preceding inversion formulas.

All matrices have O(n) rows, all entry degrees O(n). Even computing the
untruncated polynomial determinant has degree only O(n^2), not an
exponential number of monomials. With K=2M, entry coefficients have a
common denominator K! and O(K log K) bits; determinant denominators
divide (K!)^F and numerator bit lengths are polynomial in n. Standard
exact polynomial-matrix arithmetic therefore gives a polynomial bit
algorithm, with no optimized exponent asserted. Repeat for all s<=n.

## 3. Application and boundaries

The exact marginals give the rational linear combination

    L_lambda=-sum_(s=1)^n sum_(m=0)^floor(n/s)
                    P_lambda(m_s=m) log(s^m m!).

These probability coefficients sum to n and every integer argument is
at most(sm)!<=n!. Logarithms to precision epsilon/n suffice, at polynomial
cost in n and log(n/epsilon). The resulting approximation differs from
the actual defect entropy by at most log p(n)+epsilon, uniformly in lambda.
The actual-text core review accepted the formal displacement, stabilized
window, determinant coefficient costs, moment inversion and precision
ledger after the three explicit clarifications above. It did not rely on
finite controls or claim priority for this classical composition.

No joint law, joint entropy H(P_lambda), exact Delta S, general coherent
QCT, mixed-cycle column sampler, HSP solver or paper-error conclusion
follows. No interpretation of a finite numerical linear fit as an
asymptotic theorem is needed for this comparison.

Primary source cached as audits/sources/character_hamiltonian_2610_05752.pdf
and .txt. Source reviewer checked explicit lambda/Fock encoding at text
566--577, finite-current caution at585--588, row law at1821--1835, entropy
identity/bias at1837--1851, and separate column scope in Section6.
No single-count row-marginal routine was found in those actual sections;
this absence is not a novelty claim.

## 4. A uniform bound on the entropy scale

Let h_s(lambda) be the number of cells of hook length s. Removing one
s-rim hook gives a different smaller partition for each removal, with
coefficient +/-1. Therefore

    s E[m_s]=||b_s|lambda>||^2=h_s(lambda).

The last equality is the usual Maya particle/hole or hook/rim-hook
bijection. It also supplies a cheap first-moment falsifier for the decoder.
Equal-hook cells form an antichain: hook length is
(lambda_i-i)+(lambda'_j-j)+1, and each summand strictly decreases with
its index. If h cells have equal hooks, their positions force a staircase
of size h(h+1)/2 inside lambda. Consequently h_s<=sqrt(2n), for every s.

For every cycle type, m_s!<=m_s^m_s and s*m_s<=n imply
log z_nu<=log n*sum_s m_s. Using the source identity Delta S<=0 gives

    0<=-Delta S_lambda<=-L_lambda
      <=log n*sum_s h_s(lambda)/s
      <=sqrt(2n)*H_n*log n=o(n),

UNIFORMLY over every lambda of n. H_n is the harmonic number. This
corollary was independently checked. It excludes an asymptotic linear
growth rate for the maximum, Plancherel average or any other average.
The paper only reports finite fits through n=30; those data are not
contradicted, and are not silently promoted into a theorem to refute.

## 5. Scope of executable controls

The scoped producer and JSON are
classical_baselines/cft_character_marginal_control.py and .json.
The producer takes only public lambda,s and uses exact rational matrix
powers, the formal Jacobi identity C'/C=tr(A^-1 A'), and binomial inversion.
Partition enumeration and Sage characters occur ONLY in the validator.
The small controls do not establish the all-n theorem.

Five exact cases lambda=(2),s1; (2,1),s1; (3,2,1),s1 ands2; and(2,2),s2
give respectively [1/2,0,1/2], [1/3,0,0,2/3],
[2/9,1/5,0,2/9,0,0,16/45], [1,0,0,0], and[1/2,0,1/2]. All agree
with independent full-row character arithmetic, with exact nonnegativity
and normalization. A wrong bosonic scale for(3,2,1),s2 instead gives
[51/64,11/64,1/64,1/64], still positive and normalized but incorrect.
For(2,2),s2 it gives[13/16,-7/8,17/16]. A too-short window F=n for(2),s1
gives[7/12,1/3,1/12], also normalized and positive but wrong. Both kinds
of negative control fail the exact comparison. No scaling sweep or
quantum execution was performed.
