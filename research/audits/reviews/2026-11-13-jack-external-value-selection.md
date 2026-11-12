# 2026-11-13 — External target selection: a quantum Benjamin–Ono quench

SELECT one narrowly specified target for the next CLASSICAL attack: the work
law of a sudden dispersion quench, starting from an explicitly labelled
alpha=3 eigenstate of unrestricted shape. The closed Jack transform already
pays the quantum input preparation; ordinary sparse simulation pays the final
energy measurement. No new alpha extension, Macdonald construction, or quantum
subsystem is needed. This is a concrete algorithmic hypothesis to compare,
not a claim of advantage, novelty, or classical hardness.

STATE/TRAPS and the current classical down-set review were read. Corpus
`been-tried` and `baselines` were run for Jack/quench/Fourier-character topics;
they returned the current Jack notes and unrelated Fourier barriers, with no
matched catalog baseline. That absence is not evidence. Actual local primary
texts were then checked: Mickler–Moll (2.1), Theorem 2.2 and §5.1; Lapointe–Vinet
§§2.1–2.3; Stanley Proposition 2.2 and Cauchy/norm identities; Ben Dali–Dolega
§1.2 and Theorem 1.4. No network, API, Git, implementation, or sweep was used.

## 1. Native physical model and exact input/output

Work in the SAME canonical chiral boson Fock space for both Hamiltonians.
Let [a_k,a_l^dagger]=delta_kl, n_k=a_k^dagger a_k, and fix the exact finite
momentum sector sum k n_k=D. Define

    S=sum_(i,j>=1) sqrt(i*j*(i+j))
        (a_i^dagger a_j^dagger a_(i+j)+a_(i+j)^dagger a_i a_j),
    N2=sum_(k>=1) k^2 n_k,
    H_i=S+(2/sqrt(3)) N2,       H_f=S.

All sums restrict automatically to modes <=D. The sector is invariant, so
there is no uncharged continuum cutoff error. Mickler–Moll explicitly call
T3 in (2.1) the quantum Benjamin–Ono Hamiltonian (LF 296–307), and explain its
canonical Fourier-mode quantization in §5.1 (LF 681–737). Substituting
V_k=sqrt(alpha*k)a_k^dagger and V_-k=sqrt(alpha*k)a_k into that ACTUAL formula gives

    T3(alpha)=alpha^(3/2) S+alpha(alpha-1) N2.

Thus H_i=T3(3)/(3sqrt(3)) and H_f=T3(1) are a fixed sudden dispersion quench
in a common bosonic Hilbert space. The quench/work question is our proposed
observable of this sourced model; the retained paper does not itself assert
an algorithm or complexity separation for these statistics.

Native input: an explicit partition lambda of numerical size D and desired
TV error eta. Prepare the normalized alpha=3 Jack state supplied by the
reviewed transform. It is an H_i eigenstate with known energy

    E_i(lambda)=(2/sqrt(3)) [C3(lambda)+D],
    C3(lambda)=sum_(x,y in lambda)(3x-y).

The formula follows by expanding the source transfer eigenvalue through u^-4:
T3(3) has eigenvalue 6[C3(lambda)+D]. Quench to H_f and measure its energy.
Native output: an integer e sampled within TV eta of

    P_lambda(e)=||Pi_e(H_f) Jhat_lambda^(3)||^2.

The associated work is e-E_i(lambda), so outputting e already specifies the
exact work using the known quadratic-algebraic initial energy. There is no
promise of a rare branch, supplied eigenvector, or amplitude-loading oracle.
For D=0 the output is zero.

Final Schur eigenstates have energies

    e_nu=2 C1(nu)=sum_j nu_j(nu_j-2j+1),
    C1(nu)=sum_(x,y in nu)(x-y).

These are even integers in [-D(D-1),D(D-1)]. The target has only O(D^2)
energy bins. Hardness or difficulty of resolving the full final shape cannot
be transferred to this COARSER output.

## 2. Complete quantum route, with no new transform theorem

Initialize |lambda>, use the existing alpha=3 transform to prepare
Jhat_lambda^(3), and coherently phase-estimate H_f. Its occupation-basis rows
have O(D^2) split/join neighbors with polynomially bounded, polynomial-bit
computable square-root entries. Its norm is <=D(D-1), from the displayed
spectrum. The already retained sparse-simulation theorem therefore applies.
Choose a power-of-two QPE modulus >=8(D+1)^2: ideal integer energies are
recovered exactly with O(log D) phase bits and evolution times below 2pi.
Budget preparation and simulation errors in operator norm to O(eta).
The measured energy distribution then has TV error <=eta, in

    poly(D,1/eta)

BIT/gate cost. This uses neither a quantum alpha=1 Jack transform nor physical
particle-position loading. It is a direct reduction to the checked transform
and checked native simulation primitive.

Simple long-time evolution under the single fixed alpha=3 cubic Hamiltonian
is not the selected target: its eigenvalues are multiples of six, so time
can be reduced modulo pi/3 and ordinary sparse simulation already suffices.
The new resource in this quench is preparing an unrestricted specified
interacting eigenstate and measuring its response to a DIFFERENT Hamiltonian.

## 3. Exact matched classical target

Let H_lambda=||J_lambda^(3)||^2 and define the symmetric function

    F_lambda(p)=J_lambda^(3)(sqrt(3)p_1,sqrt(3)p_2,...)/sqrt(H_lambda).

Every p_k is multiplied by sqrt(3), NOT by 3^(k/2). This is the bookkeeping
for the common normalized occupation basis; it is not a proposed nonunitary
state-preparation step. F_lambda has unit norm in the alpha=1 Hall product.
If a_(lambda,nu)=[s_nu]F_lambda, the work law is exactly

    P_lambda(e)=sum_(nu:2C1(nu)=e) a_(lambda,nu)^2.                 (1)

The existing down-set sampler samples POWER-SUM coefficient squares of one
Jack state. It does not supply these mixed-Jack/Schur interference sums or
sample their energy pushforward. Its bounded-Durfee theorem therefore does
NOT, by itself, settle bounded-Durfee quench laws. Nor does its unrestricted
cost prove a lower bound for (1).

The strongest immediate classical attack is to compute the generating
function G_lambda(z)=sum_e P_lambda(e) z^e through a mixed-parameter Cauchy,
Selberg, determinant, or positive growth representation. Only O(D^2) bins
need be recovered. Polynomial-time evaluations on a full root-of-unity grid
to additive O(eta/D^2), followed by inverse DFT and harmless clipping, would
already yield a polynomial classical TV sampler. Computing every final
shape overlap is unnecessary and may be the wrong comparison.

## 4. Decisive easy families: rows and columns are classically matched

Let h_n be the complete symmetric function, e_n the elementary function,
and (a)_D=a(a+1)...(a+D-1). Stanley Proposition 2.2(b), equivalently its Cauchy
specialization, gives J_(D)^(alpha)=D! alpha^D h_D[p/alpha]. Also
J_(1^D)=D! e_D. Combining with the actual hook norms gives:

* Row lambda=(D): sample nu from

      Z_D^z(nu)=D!/(z^2)_D * s_nu(1^z)^2,   z=1/sqrt(3),

  and output e=2C1(nu).
* Column lambda=(1^D): sample nu from the SAME formula with z=sqrt(3),
  transpose the sampled shape, and output e=-2C1(nu). Equivalently use
  z=-sqrt(3) without transposition. The energy sign must not be dropped.

Here s_nu(1^z)=product_(b in nu)(z+c1(b))/product_(b in nu)hook(b), by the
source principal specialization at alpha=1. Cauchy normalizes Z_D^z.
There is an elementary positive classical growth sampler. At a shape nu
of size n, use the Schur transition residue tau_(nu,s)^(1) and add s with
probability

    t_z(nu,s)=tau_(nu,s)^(1) * (z+c1(s))^2/(z^2+n).              (2)

The source transition moments are sum tau=1, sum tau*c1=0 and sum tau*c1^2=n,
so (2) sums to one. The hook/Pieri ratio gives detailed balance with
Z_(n+1)^z and the usual Schur down probabilities, proving that D steps give
Z_D^z. This matches the ENTIRE final-shape law in these two families, hence
also their work law.

Fixed irrational z is not an oracle. For z in {sqrt(3),sqrt(3)/3}, every
weight and cumulative probability lies in Q(sqrt(3)), with polynomial-bit
rational coefficients. Compute them exactly; comparing A+B sqrt(3) with a
rational threshold reduces, after checking signs, to an integer-square
comparison. There are O(D) corners per step and D steps. Individual residue
products have O(D log(D+1)) bits, and prefix sums have a conservative
O(D^2 log(D+1)) bound. Choose

    b=ceil(log2(4D(D+1)/eta))

fair bits per step and compare the resulting dyadic U with the exact CDF.
At most D+1 CDF boundaries can be affected by rounding a continuous U; the
whole-path TV error is <=D(D+1)/2^b<=eta/4. This is a fixed polynomial BIT
clock, with no exact-real sampling assumption or unresolved algebraic sign.

Do not use these row/column quenches as evidence of quantum advantage.
General growing-Durfee shapes are the correct remaining test class; no
claim about ALL bounded-Durfee quench laws is made.

## 5. Why this target, rather than the other immediate applications

* Finite-particle Calogero–Sutherland position quenches introduce a different
  physical inner product, a Jastrow ground-state factor, and position access.
  Lapointe–Vinet (2.17) versus (2.19) displays those distinct constructions.
  The present Hall transform does not pay that physical-position interface.
* Direct Jack-character Fourier sampling from a Fock occupation is a valid
  alternative, but the simplest inputs are classically easy: occupation
  1^D gives Jack–Plancherel growth, while a single D-cycle coefficient is
  product_(b!=0)c3(b). Its support excludes box (1,3), hence has fourth row
  <=1 and can be enumerated in polynomial time. Neither is a useful next
  separation example.
* The local Ben Dali–Dolega source motivates large Jack characters, but raw
  or relative character estimation is not supplied by additive estimation
  of a normalized transform entry, which may be exponentially small.
  A hidden-label learning claim would additionally need a native data source
  and a recovery theorem. Neither follows just from the transform.

Next action: attack (1) CLASSICALLY for general explicit lambda, with the
energy aggregation kept intact. A polynomial sampler/evaluator kills this
application without touching the valid transform theorem. Failure to find
one leaves an unmatched candidate, not hardness. No quantum implementation
or additional parameter-extension work should precede that attack.
