# Native bosonic parent: an exponential-gap counterfamily

2026-11-13. Independent analytic audit of `BOSONIC_NORMALIZATION_PARENT.md`.
Fresh STATE/TRAPS, TOOLBOX and targeted corpus queries were read. No API,
network, Git, numerical experiment or live paid report was used. The main
interpreter for file operations was `/opt/anaconda3/bin/python`.

**Disposition: the proposed uniform inverse-polynomial gap is FALSE.**
For every N divisible by four and N>=1024, an explicit rational complex
positive definite N-by-N matrix P_N has spectrum {1/2,1}, yet its parent
Hamiltonian on exactly N bosons satisfies

    gap(H_(P_N)) <= 2^22 N^5 exp(-3N/64).                 (1)

The unique-ground-state and polynomial operator-norm assertions are correct.
Equation (1) refutes the proposed uniform-global-gap certificate, not
efficient preparation or sampling, and not a
gap theorem for the narrower rank-one positive-entry family. No hardness,
novelty or general normalization no-go follows.

## 1. Parent algebra, with the column/row convention fixed

For an invertible one-particle matrix P, use

    b_j^dagger=sum_u P_(u,j) a_u^dagger,
    c_j=sum_v (P^-1)_(j,v) a_v,
    K_j=b_j^dagger c_j-1,
    H_P=sum_j K_j^dagger K_j.

Then [c_i,b_j^dagger]=delta_(i,j), and on the finite N-particle sector,

    K_j=Gamma(P)(n_j-1)Gamma(P)^-1.                       (2)

The row of P^-1 is essential; an adjoint column substituted without the
corresponding convention would not give (2). The common kernel of n_j-1
for j=1,...,N is the one-dimensional span of |Omega>=|1,...,1>.
Consequently H_P has exactly the claimed one-dimensional ground space,

    |psi>=Gamma(P)|Omega>/||Gamma(P)|Omega>||.             (3)

Writing K_j=dGamma(P|j><j|P^-1)-1, first quantization gives
    ||K_j||<=N ||P|| ||P^-1||+1<=2N+1,
    ||H_P||<=N(2N+1)^2.                                  (4)
The commuting non-Hermitian K_j are similar to integer-spectrum operators;
this does not lower-bound the singular-value gap of their joint map.

## 2. A legal rational rank-two matrix and its exact symmetry

Let N=4m. Index modes by j=(h,r), 1<=h<=m, r in {0,1,2,3}. Define orthogonal
unit vectors

    u_(h,r)=1/sqrt(N),  v_(h,r)=i^r/sqrt(N),
    Pi=uu^dagger+vv^dagger,
    P=(I+Pi)/2.                                         (5)

Although u and v use sqrt(N) in their notation, the actual matrix entries are

    P_((h,r),(h',s))=delta_((h,r),(h',s))/2
                         +(1+i^(r-s))/(2N).

Thus P has rational real and imaginary parts of O(log N) bits. It is
Hermitian positive definite, with eigenvalue 1 on span{u,v} and 1/2 on its
orthogonal complement. This is exactly N modes and N particles; no illicit
fixed-two-mode, growing-particle embedding is used.

Let n_u,n_v be the two mode number operators, M=n_u+n_v and D=n_u-n_v.
The scalar factor 2^-N in Gamma(P) cancels upon normalization, so

    |psi>=2^M|Omega>/sqrt(Z),
    Z=<Omega|4^M|Omega>=per(I+3Pi).                       (6)

For symmetry, let R permute r to -r modulo four, and let D_v be the
one-particle diagonal matrix with entries i^r. The unitary S=D_v R obeys
Su=v and Sv=u. It commutes with Pi and with P, and
Gamma(S)|Omega>=(-1)^m|Omega>. Hence

    Gamma(S)|psi>=(-1)^m|psi>,
    Gamma(S) D Gamma(S)^dagger=-D.                       (7)

The physical occupation law of D is therefore exactly symmetric.

## 3. An exact positive bridge from physical occupations to Gaussian radii

A saddle calculation alone is insufficient to bound physical Fock mass.
Here is the required exact probability coupling.

For indeterminates z_1,z_2, define

    Z(z_1,z_2)=per(I+z_1 uu^dagger+z_2 vv^dagger)
      =<Omega|(1+z_1)^(n_u)(1+z_2)^(n_v)|Omega>
      =sum_(r,s) c_(r,s) z_1^r z_2^s.                   (8)

The second equality follows by second quantization in the orthogonal
u,v basis. In particular
    c_(r,s)=<Omega|binom(n_u,r)binom(n_v,s)|Omega>>=0,
and c_(r,s)=0 for r+s>N. The permanent identity is also directly obtained
by expanding the N creation operators of |Omega> and their annihilators.

Let (m_u,m_v) have the ACTUAL joint occupation law in the normalized state
(6). Given this pair, draw independent

    R_aux~Binomial(m_u,3/4),
    S_aux~Binomial(m_v,3/4).

Multiplying their probabilities by the physical filter weight 4^(m_u+m_v)
shows exactly that

    Pr(R_aux=r,S_aux=s)=c_(r,s)3^(r+s)/Z(3,3).            (9)

The same coefficients have a positive complex-Gaussian representation.
For independent standard circular complex Gaussians alpha,beta,

    Z(z_1,z_2)=E product_j
        [1+|sqrt(z_1)u_j alpha+sqrt(z_2)v_j beta|^2]      (10)

for nonnegative real z_1,z_2. To verify positivity and the coupling rather
than merely quote (10), expand the product by subsets I of [N]. For each
subset its term is the squared modulus of the homogeneous polynomial
product_(j in I)(sqrt(z_1)u_j alpha+sqrt(z_2)v_j beta).
Independent angular integration kills all cross terms with different
alpha/beta degrees, leaving nonnegative coefficients times
z_1^r z_2^s |alpha|^(2r)|beta|^(2s). Radial integration contributes r!s!,
which is precisely the coefficient c_(r,s) in (8).

Therefore under the normalized Gaussian measure with density proportional
to the product in (10) at z_1=z_2=3, its radial variables X=|alpha|^2 and
Y=|beta|^2 admit the following EXACT mixture:

    first draw (R_aux,S_aux) by (9);
    then X~Gamma(R_aux+1,rate 1),
         Y~Gamma(S_aux+1,rate 1), independently.          (11)

Equations (9)--(11) jointly couple the physical occupations to the positive
Gaussian integral, without assuming a classical coherent-state mixture
for the quantum state itself. Conditional on (m_u,m_v),

    E(X-Y)=3(m_u-m_v)/4,
    Var(X-Y)=15(m_u+m_v)/16+2<=N+2.                     (12)

The variance includes both the binomial and the Gamma layers.
When |m_u-m_v|<=2 and N>=256, Chebyshev and
N/6-3/2>=N/8 show

    Pr(|X-Y|<=N/6 | m_u,m_v)
       >=1-64(N+2)/N^2>=1/2.

Writing mu for the normalized Gaussian measure, this yields

    Pr_psi(|D|<=2) <= 2 mu(|X-Y|<=N/6).                 (13)

The bridge pays the actual occupation mass needed by the Hamiltonian
variational argument; auxiliary bimodality is not silently substituted.

## 4. Explicit Gaussian strip bound, uniformly over the relative phase

Set x=X/N, y=Y/N, t=x+y, and let phi be the relative Gaussian phase. Put
    A=1+3t, B=6sqrt(xy).
The four phase groups in (5) give the exact quartet product

    Q=(A^2-B^2 cos^2(phi))(A^2-B^2 sin^2(phi)).

With angular measure normalized to one, the full normalizing integral is

    Z=N^2 integral_(x,y>=0) integral_phi exp(N F(x,y,phi)) dx dy dphi,
    F=-t+(1/4)log Q.                                    (14)

Here A>B, so every logarithm is defined. Since cos^2(phi)sin^2(phi)<=1/4,

    F<=g(t)+(1/2)log(1-18xy/(1+3t)^2),
    g(t)=log(1+3t)-t,
    max_(t>=0) g(t)=f_*=log 3-2/3, at t=2/3.             (15)

On the central strip |x-y|<=1/6 there is a UNIFORM gap from this maximum.
If t<=1/3, then F<=g(1/3) and
    f_*-g(1/3)=log(3/2)-1/3>=1/15.
For the last inequality, convexity of 1/s on [1,3/2] gives log(3/2)>=2/5.
If t>=1/3, then |x-y|<=t/2 and xy>=3t^2/16. Consequently
    18xy/(1+3t)^2>=3/32,
and log(1-z)<=-z in (15) gives

    F<=f_*-kappa throughout the strip, kappa=3/64.       (16)

This estimate includes the origin, all relative phases, and unbounded t.
To account for the infinite integration volume, note that g(t)<=-t/2
for t>=16: the inequality holds at 16 and its derivative remains favorable.
The part t<=16 has area 128. Thus the UNNORMALIZED strip integral is at most

    128 N^2 exp(N(f_*-kappa))+(32N+4)exp(-8N)
       <=164 N^2 exp(N(f_*-kappa)).                      (17)

A full-norm lower bound can be proved without a saddle approximation.
Integrate over
    2/3<=x<=2/3+1/N,  0<=y<=1/N,
and every relative phase. Since Q>=A^4(1-z), where
    z=36xy/(1+3t)^2<=3/N,
for N>=8 the inequality log(1-z)>=-2z applies. Also g(t)>=f_*-2/N
on this rectangle. It follows that F>=f_*-4/N there. Its area is 1/N^2,
cancelling the prefactor in (14), so

    Z>=exp(N f_*-4).                                    (18)

Combining (17)--(18), using 164e^4<2^14, gives

    mu(|X-Y|<=N/6)<=2^14 N^2 exp(-3N/64), N>=8.

The exact physical consequence of (13) is therefore

    p_boundary:=Pr_psi(|D|<=2)
       <=2^15 N^2 exp(-3N/64), N>=256.                   (19)

In particular p_boundary<=1/2 for N>=1024. To check this last explicit
threshold, the right side is decreasing there and at 1024 it is
2^35 exp(-48)<exp(-13)<1/2. No fitted finite-size constant is used.

## 5. The orthogonal low-energy vector and the spectral gap

Define the bounded spectral function F_D=sign(D), with sign(0)=0, and
    |phi>=F_D|psi>.
By (7), <psi|phi>=0 exactly, while
    ||phi||^2=1-Pr_psi(D=0)>=1-p_boundary.                (20)

In the orthonormal mode basis containing u and v, K_j is a scalar plus a
one-body number-preserving operator. Each a_mu^dagger a_nu changes D by
one of -2,-1,0,1,2. Thus its WHOLE commutator with sign(D) vanishes on every
input D-sector outside [-2,2]:

    [K_j,F_D]=[K_j,F_D] Pi_(|D|<=2).                     (21)

No bound on separate shift components is needed. From K_j|psi>=0, (4),
||F_D||<=1 and (21),

    ||K_j phi||=||[K_j,F_D]Pi_(|D|<=2)psi||
                <=2(2N+1)sqrt(p_boundary).

The variational principle above the UNIQUE zero state, followed by (19),
now gives, for N>=1024 divisible by four,

    gap(H_P)<=<phi,H_P phi>/||phi||^2
       <=8N(2N+1)^2 p_boundary
       <=72*2^15 N^5 exp(-3N/64)
       <=2^22 N^5 exp(-3N/64),

which is (1). Every Hamiltonian and probability here is on the full legal
N-particle, N-mode space. The two enhanced modes are merely an analysis
basis; the remaining N-2 modes and their particle occupations were retained
throughout the positive-coefficient and Gamma-mixture argument.

## 6. Consequence for the proposed operation

The exact rank-one norm sum in the parent note can indicate a continuous
collective transition but does not by itself bound a parent gap. The
rank-two construction above is a distinct, fully quantified obstruction:
two symmetry-related occupation regions have exponentially little central
mass, and the quartic parent's one-body constraints cannot cross that
central region without the small commutator cost in (21).

The path P(s)=(1-s)I+sP includes the counterexample endpoint s=1. Thus the
claim that EVERY matrix on EVERY such path has inverse-polynomial gap is
refuted, even with O(log N)-bit matrix entries and condition number two.
The parent norm bound and unique-ground-state statement remain correct.

There is an important symmetry qualification: sign(D)|psi> lies in the
OPPOSITE S-symmetry sector from |psi>. Both P(s)=(1-s)I+sP and its parent
H_(P(s)) preserve that symmetry, so the exponentially small GLOBAL gap does
not by itself prove slow adiabatic execution on this family. The gap to
excited states in the initial state's own symmetry sector could be inverse
polynomial; that question is unproved here. This counterexample falsifies
the proposed uniform GLOBAL-gap certificate only.

This does not prove that every interpolation, parent Hamiltonian or direct
state-preparation method is inefficient. In particular no classical hardness
of this highly symmetric bounded-rank counterfamily is asserted. The false
global-gap conjecture cannot certify the proposed full-input adiabatic
compiler; no new sector-gap analysis or alternative variant is selected here.
