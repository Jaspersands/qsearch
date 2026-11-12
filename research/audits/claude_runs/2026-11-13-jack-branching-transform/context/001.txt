# Jack--Lax raising map: independent label proof

13 November 2026. Exact algebraic result. For every real alpha>0, every
D>=0, partition lambda of D, and addable box s,

    A_D psi_(lambda,s) = J_(lambda+s).

Here the source normalization is pi_0 psi_(lambda,s)=J_lambda and
A_D(sum_l f_l w^l)=sum_l V_(l+1) f_l. In particular the proposed alpha=3
identity is valid, including every global content degeneracy. This is not
inferred from the degree-three control. No sweep was run. The proof below
uses positive inner products, the source cyclic/compression theorem, and
the ordinary one-box Jack Pieri rule; no higher commuting charge or
generic-parameter limiting argument is required.

Scope: this proves the labels and exact normalization of the map. It does
not by itself prove a circuit, an efficient inverse to a rectangular map,
a quantum advantage, or the removal of a measurement/path register.
STATE/TRAPS were read; /opt/anaconda3/bin/python was the interpreter.
No network, API, or Git action was taken.

## 1. Conventions and actual source inputs

Set epsilon_1=alpha, epsilon_2=-1, epsilon=alpha-1, hbar=alpha. Write

    H_D = C[V_1,V_2,...,w]_D,       F_D = C[V_1,V_2,...]_D,
    c(x,y)=alpha*x-y,              N_lambda=||J_lambda||^2.

The monomials V_mu w^l are orthogonal and have squared norm
prod_k (alpha*k)^(m_k) m_k!. Thus w is an isometry between the appropriate
graded pieces, V_k^dagger=V_-k=alpha*k*partial_(V_k), and all N_lambda>0.

Actual Mickler--Moll source, mickler_moll.txt:

- Theorem 1.4, (1.14)--(1.18): H_D is the orthogonal sum of cyclic spaces
  Z_lambda; L_D has simple spectrum {c(s):s in A_lambda} WITHIN each
  Z_lambda; J_lambda=sum_s tau_(lambda,s) psi_(lambda,s).
- Lemmas 3.3--3.5 and Appendix A.5: pi_0 Z_lambda=C J_lambda and
  ||psi_(lambda,s)||^2=N_lambda/tau_(lambda,s). The weights are positive.
- Theorem 2.2(2.4), Appendix A.1/A.3/A.5: compressing L on Z_mu to the
  orthogonal complement of J_mu gives the simple spectrum of the zeros of
  its scalar transfer function, namely {c(r)+epsilon:r in R_mu}.
- Proposition 4.3(4.8): J_lambda(z,z,...)=prod_(b in lambda)(z+c(b)).
  Since J_lambda is weighted-homogeneous, this implies [V_1^D]J_lambda=1.

The ordinary, independently stated Pieri input is

    V_1 J_lambda = sum_(s in A_lambda) tau_(lambda,s) J_(lambda+s).   (P)

This is explicitly Lemma 2.8, (43)--(44), in the retained follow-up
mickler_lr.txt (physical lines 464--480), citing Kerov Theorem 6.7.
It precedes that paper's Shift Theorem. It is also the one-box case of
Stanley's Theorem 6.1, printed page 98, divided by the norm in Theorem 5.8.
There is no use of the conjectured A-map in (P).

For normalization checking, the one-box hook expression is

    tau_(lambda,s)
       = prod_(b in row_s(lambda)) hL_lambda(b)/hL_(lambda+s)(b)
         * prod_(b in col_s(lambda)) hU_lambda(b)/hU_(lambda+s)(b),

where hL=alpha*arm+leg+1 and hU=alpha*(arm+1)+leg. This is also follow-up
(66). Grouping the row factors by equal column heights, and the column
factors by equal row lengths, telescopes to

    prod_(t in R_lambda+(1,1)) (c(s)-c(t))
       / prod_(a in A_lambda, a!=s) (c(s)-c(a)),

exactly Mickler--Moll (1.18). Hence the Pieri and cyclic weights coincide
in the source's integral-Jack normalization.

## 2. The block matrix gives spectral support, not yet labels

With H_(D+1)=F_(D+1) direct-sum w H_D, direct calculation from (1.5) gives

    L_(D+1) = [[0, A_D], [A_D^dagger, L_D+epsilon I]],
    A_D^dagger f = sum_(k=1)^(D+1) w^(k-1) V_-k f,
    A_D A_D^dagger = sum_k V_k V_-k = alpha(D+1) I.                 (1)

Fix mu of size D+1 and set u_mu=A_D^dagger J_mu in H_D. The space
Z_mu perpendicular to J_mu equals pi_+ Z_mu and lies in w H_D, because
pi_0 Z_mu=C J_mu. Its compressed L action is L_D+epsilon under the
identification by w. Appendix A makes L J_mu=w u_mu cyclic for this
compression. Consequently

    u_mu has L_D spectral support only in {c(r):r in R_mu},
    ||u_mu||^2=alpha(D+1)N_mu.                                    (2)

This does NOT yet identify individual partitions inside a repeated
eigenspace. Let P_c denote the GLOBAL orthogonal spectral projector of L_D.
We keep these full projectors throughout the proof.

## 3. A corner-intersection lemma valid at alpha=3

If mu=lambda+s, then

    {c(a):a in A_lambda} intersection {c(r):r in R_mu}={c(s)}.      (3)

To prove it, first the contents of distinct addable corners of one diagram
are distinct for every alpha>0, as are the removable-corner contents.
For r in R_mu with r!=s, r belongs to lambda. If c(a)=c(r) for an addable
a of lambda, distinct a,r would have both coordinate differences strictly
of the same sign. If a is strictly northwest of r, the order-ideal
property of lambda would put a inside lambda, impossible. If a is strictly
southeast of r, then a-(0,1) belongs to lambda, since a is addable. The
box r+(1,0) is coordinatewise below a-(0,1), so it belongs to lambda and
hence to mu. That contradicts removability of r. The remaining r=s case
uses distinct contents within A_lambda. This proves (3).

This argument permits arbitrary rational content collisions elsewhere in
the whole space. It does not assert that different diagrams have disjoint
content sets.

## 4. The norm sum that eliminates every degenerate remainder

Taking adjoints in (P) gives

    V_-1 J_mu = sum_(r in R_mu)
        tau_(mu-r,r) N_mu/N_(mu-r) J_(mu-r).

Compare coefficients of V_1^D, using [V_1^k]J_nu=1 for |nu|=k and
V_-1=alpha*partial_(V_1). We obtain the exact sum rule

    sum_(r in R_mu) tau_(mu-r,r) N_mu/N_(mu-r)=alpha(D+1).          (4)

For each r in R_mu write lambda=mu-r and define

    e_r=P_(c(r)) J_lambda=tau_(lambda,r) psi_(lambda,r).

The e_r are mutually orthogonal: the removable contents of this fixed mu
are distinct. Their norms are ||e_r||^2=tau_(lambda,r)N_lambda.
By (2), (3), self-adjointness, and (P),

    <e_r,u_mu>=<J_lambda,u_mu>
              =<A_D J_lambda,J_mu>
              =<V_1 J_lambda,J_mu>=tau_(lambda,r)N_mu.             (5)

All coefficients are real in this positive-alpha convention. Thus the
orthogonal projection of u_mu onto C e_r is (N_mu/N_lambda)e_r. Its
squared norm is tau_(lambda,r)N_mu^2/N_lambda. Summing these squared
norms and applying (4) gives EXACTLY alpha(D+1)N_mu=||u_mu||^2.
Pythagoras therefore leaves zero orthogonal remainder, even inside any
degenerate global eigenspace. We have proved

    A_D^dagger J_mu = sum_(r in R_mu)
        tau_(mu-r,r) N_mu/N_(mu-r) psi_(mu-r,r).                    (6)

Now pair (6) with the full orthogonal basis psi_(lambda,s). The coefficient
of J_mu in A_D psi_(lambda,s) vanishes unless mu=lambda+s. In that case
the pairing equals

    tau_(lambda,s) N_mu/N_lambda * ||psi_(lambda,s)||^2=N_mu.

Since the J_mu form an orthogonal basis of F_(D+1), this proves

    A_D psi_(lambda,s)=J_(lambda+s).                               (7)

There is no missing rank, label, or generic-eigenvalue assumption in this
argument. It covers D=0 as well.

## 5. Shift theorem, sign correction, and the normalized isometry

The follow-up's Theorem 3.4 is already the relevant labelled Shift Theorem,
and Corollary 3.5(94) has the matching expansion. However its printed
compressed-eigenvector normalization contains a sign inconsistency.
Our independent argument did not use that theorem's proof or its down
residues.

Put mu=lambda+s and theta=c(s)+epsilon. Equation (7) and the block matrix
give

    (L_(D+1)-theta) w psi_(lambda,s)=J_mu.

Moreover (6) and cyclicity put w psi_(lambda,s) in Z_mu. Therefore the
precisely normalized identity is

    w psi_(lambda,s)=(L_(D+1)|Z_mu-theta)^(-1) J_mu
       =sum_(a in A_mu) tau_(mu,a)/(c(a)-theta) psi_(mu,a).          (8)

The inverse in (8) is on Z_mu. A full-space inverse can fail at a global
content collision. Within Z_mu, theta is a strictly interlacing compressed
eigenvalue, so none of these denominators vanishes.

The follow-up (52) instead prints (theta-L)^(-1)J_mu. With the
Mickler--Moll transfer m_mu(u)=u^(-1)T_mu(u), its (46) also defines the
down residue as Res 1/m_mu. These residues are NEGATIVE. To use positive
shifted vectors satisfying pi_0 L tilde-psi=J_mu, both signs must change:

    tilde-psi=(L|Z_mu-theta)^(-1)J_mu,
    positive down residue=-Res_(u=theta) 1/m_mu(u).

Exact degree-one diagnosis, not a numerical control: for mu=(1),
m_mu(u)=(u-epsilon)/((u-alpha)(u+1)). Its inverse has residue -alpha
at epsilon, and (epsilon-L_1)^(-1)J_1=-w. Thus printed (46)/(52)/(54)
are mutually compatible with NEGATIVE shifted vectors, whereas the base
case of Theorem 3.4 and Corollary 3.5 use +w. Formula (8) resolves the
normalization and agrees with Corollary 3.5's denominator.

Finally V=A_D^dagger/sqrt(alpha(D+1)) is an exact native linear isometry.
On normalized Jacks it has the completely labelled expansion

    V |J_mu> = sum_(r in R_mu) sqrt(d_(mu,r)) |psi_(mu-r,r)>,
    d_(mu,r)=tau_(mu-r,r) N_mu/[alpha(D+1)N_(mu-r)],
    sum_r d_(mu,r)=1.

All square roots use the positive convention; there is no unresolved
relative sign. A_D itself is a coisometry only after this normalization,
and maps several orthogonal parent eigenvectors to the same child ray.
Equation (7) must not be substituted for a deterministic unitary erasure
of those distinct inputs. Circuit and transition-resource conclusions
remain the separate obligations assigned by the parent.
