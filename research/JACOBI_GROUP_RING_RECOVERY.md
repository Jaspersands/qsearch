# Repeated Jacobi sums from a public group-ring ideal and norm

2026-11-06. Independently reviewed WRITTEN group-ring reduction. No
novelty, external-paper-error, implemented-generator recovery, or matched
factorial-exponent claim. The native task is already classically solved by
September 2026 prior art; the planned control subsystem is CANCELLED.

**Priority-changing source refresh:** Tal's September follow-up,
[Computing Modular Factorials Below the Square-Root Barrier, ECCC TR26-211](https://eccc.weizmann.ac.il/report/2026/211/),
Theorem1.5 and Section3.1, already gives deterministic polynomial(q,logp)
exact repeated-Jacobi reconstruction for EVERY q|p-1 and 1<=a<q, with a
compatible character/prime, including residues modp and modp². Composite,
even and noncoprime parameters are included. Its known-norm recovery and
van Wamelen root selection resolve the complete input problem. The July
quantum paper is not the strongest current comparator. The derivation below
is retained as a reviewed explanation; its specific priority is unverified.
No further arithmetic subsystem is justified by an alleged unresolved
composite root-of-unity phase. The September source was read in full at
the relevant theorem/procedure/complexity sections, not inferred from its
abstract. Source PDF/text: audits/sources/jacobi_classical_eccc_2026_211.*.

## Native target and sources

Given prime p, q|p-1, an order-q eta in F_p, and 1<=a<q, let K=(p-1)/q.
Define chi:F_p^*->mu_q by eta^e=x^(-K) iff chi(x)=zeta_q^e, with chi(0)=0.
The target is the repeated a-fold Jacobi sum J_a(chi), exactly, and its
residues at zeta_q->eta_h modulo p^h for h=1,2. Desired classical cost is
polynomial in q,logp, NOT in logq. q may grow and may be composite/even.

This is the exact input/output in Tal2607.29453, Sections2.1/2.2 and
Theorem1.3, with a character and compatible prime. For modular factorials
the character may be chosen, so an order-q eta suffices; a generator of
F_p^* and factorization of p-1 need not be supplied. Factoring q by trial
division and sampling h^K with an exact order test cost polynomial in q,
logp. A given compatible character/prime is retained, not relabeled.

Corpus lookup `composite conductor Jacobi root of unity primary
normalization quantum modular factorial` leads to JACOBI_KNOWN_NORM_REDUCTION.md.
That note covers prime-conductor three-character sums. The baseline lookup
returns only a noisy LLL match; the stronger appropriate comparator is
Lenstra--Silverberg Theorem1.3, read directly below. No LLL failure is needed
to motivate a quantum routine. Watkins2018's practical/fixed-motive
Grossencharacter identification is not imported as uniform growing-q time.

Primary sources, stored under audits/sources/:

- [Tal, 2607.29453](https://arxiv.org/abs/2607.29453), definitions,
  Propositions2.1/2.2, Theorems1.1--1.3 and AppendixB/C.
- [Lenstra--Silverberg, 1706.07373](https://arxiv.org/abs/1706.07373),
  Definition1.1, Example1.2(ii), Theorem1.3, Algorithms18.6/18.7.
- [Watkins, Jacobi sums and Grossencharacters](https://www.numdam.org/article/PMB_2018____111_0.pdf),
  Section6, used only to check the boundary of the classical comparison.

## 1. Retain all characters in an integral group ring

For a=1 return1. Below a>=2. Let R=Z[X]/(X^q-1), with bar(X)=X^-1, and
write every element in the q-coefficient basis. This is a reduced CM-order;
the cited source explicitly includes integral group rings of finite abelian
groups. It is not a domain. No rational idempotent is silently made integral.

Define an ANALYTIC witness, not data used by the constructor:

    V = sum_(x1+...+xa=1, all xi!=0) X^(e(x1)+...+e(xa) modq).

Its component at X=zeta_q^j is J_a(chi^j), including imprimitive characters.
The augmentation is the explicit positive integer

    M=V(1)=((p-1)^a-(-1)^a)/p.

For j!=0, the component has squared complex magnitude p^(a-1) if q does
not divide aj, and p^(a-2) if q divides aj. The latter follows from
J_a(psi)=-G(psi)^a/p when psi!=1 and psi^a=1; the usual quotient by
G(psi^a) is NOT valid in this case. All components, including M, are nonzero.

## 2. Construct the full principal ideal without knowing V

Lift eta to a root eta_A of X^q-1 modulo p^A, A>=a. For j=1,...,q-1 put

    E_j=ceil(aj/q)-1.

These are nonnegative integers. Here is an explicit valuation proof,
including nonprimitive characters; Tal's primitive-character proposition
alone does not cover all j. In the local embedding X->eta_A^j, write
psi=omega^(-k), k=jK in[1,p-2], for the Teichmuller character omega. Put
pi=zeta_p-1. Expanding the additive character gives

    G(psi)=sum_(t=0)^(p-1) c_t*pi^t,
    c_t=sum_(x=1)^(p-1) omega(x)^(-k)*binom(x,t).

Modulo p, finite-field power sums show c_t=0 for t<k and c_k=-1/k!.
Since v_pi(p)=p-1>k, the k term has uniquely least valuation, so
v_p(G(psi))=k/(p-1)=j/q. If psi^a!=1, divide G(psi)^a by G(psi^a),
whose valuation is (aj modq)/q. If psi^a=1, group tuples by their sum:
S(s)=J_a(psi) for s!=0 and sum_s S(s)=0, so S(0)=-(p-1)J_a and
G(psi)^a=S(0)-J_a=-pJ_a. The valuation then subtracts1 instead.
Both cases give E_j=ceil(aj/q)-1.
In particular this is floor(aj/q), EXCEPT at q|aj where it is one less.

Define the public full-rank ideal

    I={v in R: v(eta_A^j)=0 mod p^E_j for 1<=j<q,
                  v(1)=0 mod M}.

No factorization of M is required: these are modular linear constraints
on q integer coefficients. Evaluation is a ring map at every modulus,
so their kernels and intersection are ideals. Their index is

    [R:I]=M*p^(sum_j E_j).                                  (1)

Indeed M=a*(-1)^(a-1) modp is nonzero since a<q<p. The p-constraints are
independent by the distinct-root Vandermonde determinant, a p-adic unit;
the augmentation constraint is coprime to them. CRT proves (1).

The analytic witness satisfies all constraints, so RV is contained in I.
Let m=gcd(a,q). Pairing j with q-j gives

    sum_j E_j=((q-1)(a-1)-(m-1))/2.

The complex component norms therefore give

    |det(multiplication by V)|=M*p^(sum_j E_j)=[R:I].

All components are nonzero, so this determinant really is the index of RV.
The inclusion and equal index prove I=RV, including the integral gluing
at conductor primes. We do NOT merely recover its rational components.

## 3. The relative norm is explicit and integral

Use the following RATIONAL idempotents only to state the formula:

    e0=(1/q)*sum_(k=0)^(q-1) X^k,
    eH=(m/q)*sum_(t=0)^(q/m-1) X^(m*t).

eH evaluates to1 precisely at characters with aj=0 modq. Set

    w=p^(a-1)*(1-eH)+p^(a-2)*(eH-e0)+M^2*e0.                (2)

Then V*bar(V)=w by every complex evaluation. w is IN R: the coefficient
of eH is p^(a-2)*(1-p), and q|p-1; the remaining denominator q divides
M^2-p^(a-2), since M=(-1)^(a-1) modq and p=1 modq. All character values
of w are positive, so it is a totally positive unit of R_Q.
The analytically established I=RV implies I*bar(I)=Rw and supplies the
YES witness. The polarized identity by itself is not used to infer one.

Lenstra--Silverberg Theorem1.3 now returns an actual v in R_Q satisfying
I=Rv and v*bar(v)=w, deterministically in polynomial explicit input size.
Since v belongs to I, it is integral in this R, not merely in its maximal
order. This imported algorithm is NOT implemented by the proposed controls.

## 4. Two public integer moments remove every remaining ambiguity

Because Rv=RV and V is invertible in R_Q, u=v/V lies in R^* and
u*bar(u)=1. If u=sum u_i X^i, the coefficient of1 in u*bar(u) is
sum u_i^2=1. Hence u is EXACTLY +/-X^k. No unproved torsion-unit
classification or independent root choices in the cyclotomic factors
are needed; integrality in the full group ring is essential.

First choose the sign so v(1)=M. Define D(v)=sum_i i*v_i modq; this is
well-defined on R because the derivative of X^q-1 at1 is q. Put

    C=((p-1)^(a-1)-(-1)^(a-1))/p,
    D0=a*C*K*q*(q-1)/2 modq.                               (3)

Then D(V)=D0: for one fixed coordinate x!=1, the number of choices of
the remaining nonzero coordinates with their required nonzero sum is C.
The exception x=1 has e(1)=0. Each character exponent e in0,...,q-1 occurs
K times, so summing all a positions proves (3), also for EVEN q.

Since M=(-1)^(a-1) modq, it is invertible modulo q. If v=X^k V, then
D(v)=k*M+D0 modq. Compute

    k=(D(v)-D0)*M^-1 modq,  and output X^-k*v.

This is V itself. Projection to Z[zeta_q] gives the requested exact sum;
evaluation at the Hensel lift eta_h gives its residue modulo p^h.
The nonprimitive components are used to fix integral phase, not supplied
as extra advice or discarded during norm recovery.

## 5. Resource ledger, payoff and falsifiers

R has rank q with explicit cyclic multiplication and conjugation.
E_j<a, M has O(a logp) bits, and (2) has polynomial coefficient bit length.
HNF/intersections of q modular linear constraints give I in polynomial
q,logp time, without factoring M. Its index has O(q*a logp) bits. The
ordinary coefficient output is also polynomial-size: the witness counts
are at most M, and any recovered v is a signed cyclic shift of it.
Thus compact-output evaluation is not a hidden additional problem here.

The reviewed written reduction gives classical polynomial
q,logp exact repeated-Jacobi recovery for ALL q, including residues modp².
Using Tal's stated modular-factorial congruence and ordinary interval
products would give SOME classical bound q^C*polylogp plus
sqrt(p/q)*polylogp for an unspecified absolute C. This does not prove
that C equals or improves the quantum paper's exponent c, does not
give polylogp arbitrary factorials, and does not yet audit the modp²
factorial composition. The imported norm-recovery routine is unexecuted.

Decisive falsifiers: wrong trivial-product valuation or norm; wrong
integral index/gluing; inapplicability of the CM-order theorem; uncharged
factorization; nonmonomial integral norm-one ambiguity; incorrect even-q
moment; or superpolynomial coefficient sizes. Exact controls must build
I,w from public p,q,a,eta BEFORE any true character-table computation.
The true sum may subsequently check the input, not enter its constructor.

## 6. Closed reviews, prior art and execution boundary

The core independent review accepted the all-q valuations, full integral
index/gluing, positive integral norm, unit argument, even-q derivative and
bit complexity. A separate source/resource review checked that the CM
source explicitly includes Z[C_q], returns ordinary integral coordinates,
and requires no factorization of M. Both were checked against the actual
source by the parent. R_Q decomposes; R is a non-domain, not a disconnected
integral order. The text above avoids the latter erroneous description.

After this derivation, the targeted literature refresh found the September
classical paper. A separate actual-source audit confirmed its theorem,
all-conductor procedure, even-conductor criterion and uniform cost. With
supplied p,q, construction of a compatible pair is Las Vegas expected
polynomial(q,logp): factor q within polynomial(q) work and test random
h^K for exact order q. The deterministic theorem assumes that pair as
input. Selecting a suitable divisor q from p alone is a separate task;
no free factorization of p-1 or deterministic polylog setup is inferred.

The relevant September locations are Theorem1.5, Lemma2.8, Section3.1 /
Theorem3.1, and Section3.3. Its factorial improvements are published work.
We do not independently validate the entire 69-page paper, its density-
of-primes statements, or all higher-prime-power factorial constructions.

No new finite control, normalized-generator implementation, quantum
algorithm, or modular-factorial execution was performed in this pass.
The four proposed controls were cancelled before implementation because
prior art already supplies the intended classical algorithmic conclusion.
Do not execute that retired queue or infer an execution result from the
reviewed proof. No new asymptotic quantum opening remains in this task.

Next research selection must compare genuinely different paid mechanisms
and their strongest CURRENT classical comparators. Native polynomial-
character reconstruction still has a query/time gap; this arithmetic
candidate cannot supply an independent unaccounted-for quantum advantage.
