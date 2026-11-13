# Community source independence — independent audit, 2026-11-13

**Two native proof gaps are confirmed.** The shared-mask sample split is not
independent conditional only on labels. The label-averaged covariance asserted
to vanish in Lemma 58 is nonzero for admissible collision-free native rows.
These findings invalidate the indicated independence/zero-covariance imports;
they do NOT show that the quantum algorithm or its final asymptotic conclusion
is false. A corrected source construction and overlap proof remain possible.

Source: Schmidhuber--Zlokapa, arXiv:2510.08494v1, retained as
`audits/sources/2026-11-13-community-selection/schmidhuber_zlokapa.{pdf,txt}`.
I read Definition 2, Definitions 8--10 and 27, the guiding-state definitions,
and the complete relevant C.3.1/C.3.3 proofs through (214). PDF pages 36--37
were also rendered and visually checked: neither “i.i.d.” nor “distinct” is
an extraction error. LF locators below count physical newlines in the text.
STATE/TRAPS were read. No network, API, Git, implementation or parameter sweep
was used. The parent's separate exact control/repair work is not assumed.

## 1. The native law and the shared-mask dependence

Definition 2, printed p5 / LF184--205, samples independent uniform vertex
labels x, then conditionally independent hyperedge indicators
  Y_S | x ~ Bern(q+epsilon*f(x_S)),
where 0<epsilon<q<1/2. Write
  A_S=(Y_S-q)/sqrt(q*(1-q)), beta=epsilon/sqrt(q*(1-q)).
For one fixed edge, conditional on x, set delta=epsilon*f(x_S), so
  E[A_S|x]=delta/sqrt(q*(1-q))=beta*f(x_S).

In C.3.1, LF2249--2279, M_S~Bern(zeta) is independent of (x,Y), and the SAME
mask allocates the guide coefficient M_S*A_S and the matrix coefficient
(1-M_S)*A_S. For X=M_S*A_S and Z=(1-M_S)*A_S,
  X*Z=0 identically,
  E[X|x]=zeta*delta/sqrt(q*(1-q)),
  E[Z|x]=(1-zeta)*delta/sqrt(q*(1-q)),
so
  Cov(X,Z|x)=-zeta*(1-zeta)*delta^2/(q*(1-q)).              (1)
For any edge with nonzero signal and 0<zeta<1 this is strictly negative.
This directly contradicts the conditional-independence assertion at the
start of printed p36, LF2278--2279. Absorbing mask randomness into P(x) does
not remove it. Even when delta=0, these variables are not independent:
A_S is never zero, each of X and Z has positive probability of being nonzero,
and they cannot both be nonzero. Zero covariance would not suffice.

The issue also survives taking the collision-free lambda-fold guide, rather
than only its one-edge precursor. For a row T of lambda disjoint edges
containing E, its block coefficient is
  U_T=product_(S in T) M_S*A_S.
The matrix coefficient Z_E=(1-M_E)*A_E satisfies U_T*Z_E=0. For the native
binary model below all conditional means are nonzero, so
  Cov(U_T,Z_E|x)
    =-zeta^lambda*(1-zeta)*beta^(lambda+1)
       *f(x_E)^2*product_(S in T, S!=E) f(x_S) !=0.         (2)
Such a matrix entry exists whenever the source's dimension constraints hold:
put half of E in the differing row positions, its other half in the column,
and fill the remaining positions with common distinct vertices outside E.
Thus this is a dependence of the source's actual guide/matrix data.

Conditional on BOTH x and the whole mask M, the remaining Y variables used
by the two objects are disjoint, so independence is restored. But the guide
mean in the block basis is then
  E[U_T | x,M]=beta^lambda*v_T*product_(S in T) M_S,         (3)
not (zeta*beta)^lambda*v_T. In particular a direction chosen from the
complementary matrix also depends on M. One cannot average the mask in (3)
while holding this random direction fixed. Therefore merely conditioning on
M does not establish Theorem 57's invocation in C.4. It creates a different
masked-certificate overlap obligation.

## 2. A native nonzero covariance with distinct hyperedges

For p=4,k=2, encode the two uniform labels as independent Rademacher signs
sigma_i. The source's actual Definition 2 function becomes exactly
  f(x_S)=(1/8)*chi_S, chi_S=product_(i in S) sigma_i.        (4)
Indeed the two summands in its definition are each (1/16)*chi_S. This is
within the stated k>=2,p even model, not a different planted distribution.

Take lambda=3, a=1, b=2 and n>=12. Define five distinct 4-sets
  E={9,10,11,12},
  A={1,2,3,4}, B={5,6,7,8},
  C={1,2,5,6}, D={3,4,7,8}.
The row block-tuples T=(E,A,B) and V=(E,C,D) are both in the collision-free
index set C_3 of Definition 27, LF879--894: blocks within EACH row are
pairwise vertex-disjoint. Their only common hyperedge is E. All four other
hyperedges are distinct, while
  A symmetric-difference B symmetric-difference C symmetric-difference D
      = empty,
and therefore chi_A*chi_B*chi_C*chi_D=1 identically. The rows are also valid
no-repeated-entry 12-tuples in T_n(12), using any ordering inside their blocks.
In the source's symmetrized p-set block basis, the guide coefficients are
exactly the products below. Expanding into ordered vertex tuples only adds
fixed positive normalization factors; it cannot make this covariance zero.

Let m_S=E[A_S|x]=beta*chi_S/8 and
  v_S=E[A_S^2|x]=1+epsilon*c*f(x_S),
  c=(1-2q)/(q*(1-q)).                                     (5)
This second-moment identity follows directly by expanding (Y_S-q)^2 for a
Bernoulli variable; it agrees with the source's moment dictionary.
The five observed edges are independent CONDITIONAL ON x. Consequently
  W(1,2)(x)=Cov(A_E*A_A*A_B, A_E*A_C*A_D | x)
            =m_A*m_B*m_C*m_D*(v_E-m_E^2)
            =(beta^4/8^4)*(1+epsilon*c*chi_E/8-beta^2/64).
Averaging over the independent labels of E yields
  E_x W(1,2)=(beta^4/8^4)*(1-beta^2/64)>0.                 (6)
Native 0<epsilon<q<1/2 implies 0<beta^2<q/(1-q)<1, so strict positivity
holds throughout the allowed nonzero-signal parameter range. No limiting
approximation or numerical evidence is needed.

This is not restricted to fixed lambda. For EVERY lambda>=3, keep A,B,C,D
and take a=lambda-2 shared 4-sets E_1,...,E_a, pairwise disjoint and disjoint
from {1,...,8}. Use rows (E_1,...,E_a,A,B) and (E_1,...,E_a,C,D).
For n>=4lambda both rows remain collision-free and
  E_x W(lambda-2,2)
       =(beta^4/8^4)*(1-(beta^2/64)^(lambda-2))>0.           (7)
Indeed the shared-edge labels are independent, E_x v_E=1, and m_E^2 is the
constant beta^2/64. Thus the omitted covariance type persists for growing
lambda with 4lambda=o(sqrt(n)); it cannot be dismissed solely because the
smallest explicit instance has lambda=3.

### Extension: every k>=2 and every even p>=2

The same defect occurs beyond binary communities. Let
  z_a(x)=1_(x=a)-1/k,
  C_ab=E_x[z_a(x)*z_b(x)]=delta_ab/k-1/k^2,
so the native function is f(x_S)=sum_a product_(i in S) z_a(x_i).
Take four disjoint vertex blocks X_1,...,X_4 of size r=p/2 and define
  A=X_1 union X_2, B=X_3 union X_4,
  C'=X_1 union X_3, D=X_2 union X_4.
These are four distinct p-sets with the same row-disjointness properties.
Write M_ab=C_ab^r, the ENTRYWISE power (not a matrix power). Independence of
the four vertex blocks, followed by expansion of the four f factors, gives
  E[f_A*f_B*f_C'*f_D]
    =sum_(a,b,c,d) M_ac*M_ad*M_bc*M_bd
    =sum_(a,b) (sum_c M_ac*M_bc)^2
    =Tr(M^4)>0.                                            (8)
M is a nonzero real symmetric matrix, so its fourth-power trace is strictly
positive even when r is odd and some of its entries/eigenvalues are negative.
Also mu=E[f_S^2]=sum_(a,b) C_ab^p=Tr(M^2).

Adding a=lambda-2>=1 disjoint shared p-sets outside the four blocks yields
  E_x W(a,2)=beta^4*Tr(M^4)*(1-(beta^2*mu)^a)>0.             (9)
The two groups of vertex labels are independent; each shared second moment
has label average 1, and each squared shared mean has average beta^2*mu.
The strict sign follows from beta^2<1 and mu<1. For example, Holder gives
|f|<=product_j ||z(x_j)||_p<1 since p>=2 and
||z(x_j)||_p<=||z(x_j)||_2=sqrt(1-1/k)<1.

For p=4, M has diagonal (k-1)^2/k^4 and off-diagonal 1/k^4. Its eigenvalues
are (k-1)/k^3 once and (k-2)/k^3 with multiplicity k-1. Thus at k=3,
  Tr(M^4)=2/59049, mu=2/243;
at k=2 they are 1/4096 and 1/64, agreeing with (6)--(7). This is an exact
symbolic derivation, not a numerical extrapolation. The construction applies
for every n>=lambda*p, including admissible growing-lambda sequences.

## 3. Exact source assumption and failed inference

Lemma 58, printed p36 / LF2326--2344, literally says the family (A_S) is
“i.i.d.” and requires the listed p-sets to be DISTINCT. Its covariance is
conditional under P(x), followed by averaging over x. These statements need
two careful distinctions.

* The native family is conditionally independent given x but generally has
  different conditional Bernoulli means. Its unconditional one-edge laws are
  identical, but the edges are not jointly independent. In our example,
  E[A_A*A_B*A_C*A_D]=beta^4/8^4, whereas each E[A_S]=0.
  Thus, if “i.i.d.” is read as a literal unconditional premise, the lemma is
  not a lemma applicable to the native observations. Equation (6) is not
  claimed to refute an unrelated theorem under an actually satisfied iid law.
* Under the intended native interpretation, the displayed claim (189) that
  E_x W(a,b)=0 for a<lambda is false by (6). Conditional observation
  independence proves the valid product formula (199). It does not justify
  the next sentence, LF2412, or equation (200): label averaging does not
  factorize across merely distinct p-sets. The four unique edges above share
  label variables and have a nonzero joint moment.

The proof's earlier word “disjoint” at LF2382 cannot fix the application by
itself. If it means genuinely vertex-disjoint supports across the ENTIRE
combined list, it is a stronger premise than the statement's “distinct”, and
it excludes legitimate pairs of collision-free rows such as T,V. A repaired
lemma confined to globally disjoint supports would not cover the sum of row
covariances in (210)--(211).

For completeness, the source's claimed transfer to masks by replacing beta
with zeta*beta “in all dictionary entries”, LF2471--2474, is also not an exact
moment identity. In particular
  E_x E[(M_S*A_S)^2|x]=zeta,
whereas dictionary entry (194) is 1 and has no beta to substitute. The first
moment does acquire zeta, but higher mask moments use M_S^j=M_S. A correct
masked variance bound might still follow with different bookkeeping; it is
not established by that substitution alone.

## 4. Disposition and remaining gate

The two exact failures enter the stated quantum overlap proof at different
places: (1) prevents the asserted conditional independence used to choose the
matrix-dependent direction; (6)--(7) invalidate the removal of all a<lambda
terms when deriving (211). Equations (212)--(214) then cite these steps in
Theorem 50's leading-eigenspace overlap argument.

This audit therefore does NOT import Theorem 50's native overlap guarantee,
or the claimed quantum cost as an already verified resource for a readout
upgrade. It does not refute the classical Kikuchi spectral argument, prove
that the missing covariance contribution is asymptotically fatal, or prove
that no alternative sample construction can succeed. Those require separate
analysis. No conclusion about all classical algorithms, statistical recovery,
algorithmic impossibility, novelty or a speedup follows from this proof gap.
The parent's constructive sample-law/covariance repair is deliberately outside
this review. A replacement must pay both the actual joint law and the full
matrix-dependent directional overlap, not merely a fixed-vector expectation.
