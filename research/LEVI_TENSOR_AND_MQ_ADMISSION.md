# Explicit Levi Tensor Source And Gaussian MQ Admission

2026-11-06. Two scoped analytical falsifiers, independently derived and
parent-checked, with independent actual-note review accepted. No quantum implementation, general hardness theorem,
novelty claim or rejection of other source/algorithm models.

## 1. Selection And Prior Work

The question after UNBALANCED_LEVI_COSET_RECOVERY.md is whether an
externally meaningful explicit object supplies its opaque coset oracle
without exposing the decomposition classically. A direct mixed tensor is
the concrete source tested here. An independent comparison tested Gaussian
Fourier linearization for explicit quadratic-system solving. Both fail
their cheapest analytical tests; neither warrants a subsystem or scan.

Corpus been-tried/baselines lookups were completed before extending either
proposal. The derivative filter in SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT.md
Section 3 is relevant prior work; this is a narrow application, not a
general polynomial-equivalence theorem. For MQ the catalogued competitors
are Groebner/XL and hybrid guessing. The separated-square falsifier below
is already solved by independent classical square roots, so no Groebner
benchmark is needed. Gaussian-sum Fourier identities are standard; the
calculation below is given directly and does not import a claimed MQ solver.

## 2. Explicit Tensor Contract And Intended Mechanism

Let V=Fp^n, p>=128n, and r>s>=1, r+s=n. Supply the coefficients of
T in a specified direct sum of mixed tensor spaces

    V^tensor(a) tensor (V*)^tensor(b),   a+b <= d < p-1.

Dense or explicit sparse coefficient lists are allowed; their actual
length is charged. Promise that the EXACT Fp-point stabilizer is
H=GL(U) x GL(W) in some unknown decomposition V=U direct-sum W of
dimensions r,s. The output is the ordered pair U,W. The orbit map
f(g)=g.T would give the earlier quantum algorithm its coset oracle.
The proposed advantage was polynomial work in this explicit description
and log p against decomposition search. It fails because the same input
allows the following classical polynomial algorithm.

No generators of H, idempotents or hidden basis are supplied. Equality of
finite and algebraic stabilizers is NOT an extra assumption.

## 3. Classical Recovery From The Actual Tensor

Compute, by linear equations in n^2 unknowns,

    L = { X in End(V) : d rho(X) T = 0 }.

On each mixed tensor, the derivative is the sum of X acting on vector
slots minus X^T acting on dual slots. Sparse input is sufficient: each
slot replacement expands the set of relevant coordinates by at most a
factor n, so the linear system remains polynomial in the explicit input.

Write A=End(U) direct-sum End(W), for analysis only. We prove L=A.

First A is contained in L. Within-block root groups I+tE fix T for every
t in Fp. Their action on T is polynomial in t of degree at most d<p:
the dual action uses (I+tE)^-T=I-tE^T. Interpolation therefore makes the
derivative zero. For within-block diagonal directions, the coordinate
torus acts with integer weights between -d and d. Finite-torus invariance
permits only weights divisible by p-1; the strict bound forces weight
zero. The root and diagonal directions span A.

Next L is H-conjugation invariant. If L is larger than A, a nonzero
off-diagonal component occurs. Conjugating by diag(c I_U,I_W), where
c^2 != 1, separates its two possible weights c and c^-1 from weight 1.
Polynomial projections in that conjugation operator isolate a nonzero
element of Hom(U,W) or Hom(W,U) in L. Its GL(U) x GL(W) orbit spans that
entire rectangular matrix space, so L contains a cross-block matrix
unit E. This can also be seen by elementary row/column operations.

But E^2=0 and d rho(E)T=0. The representation law gives

    d/dt [rho(I+tE)T] = rho(I+tE) d rho(E)T = 0.

Every coordinate has degree at most d<p, so zero derivative implies a
constant polynomial. Thus I+E fixes T, contradicting the exact finite
stabilizer promise. This proves L=A without a smoothness assumption.

Compute the commutant of L by a second linear system. It is precisely
Fp P_U direct-sum Fp P_W. Any nonscalar element has two distinct Fp
eigenvalues and its two eigenspaces are U,W. Their unequal dimensions
order them. Factoring the degree-two minimal polynomial is an ordinary
public finite-field task: a capped randomized nonsquare search and
Tonelli--Shanks suffice, with polynomial work and failure <=eta. All
other steps are exact linear algebra. Hence recovery costs polynomial
in the supplied description, n,d,log p,log(1/eta), exact on success.

The degree guard matters: scalar weight p-1 can be invariant on Fp* yet
have nonzero derivative, and degree-p Frobenius actions can have zero
derivative without being constant. This theorem makes no claim for high
degree, arbitrary rational actions, succinct unrestricted circuits or
opaque labels. A nonzero pure covariant/contravariant tensor of positive
order below p-1 cannot even have this stabilizer, since H contains all
global scalars. Mixed tensors are covered by the classical attack above.

## 4. Independent MQ Proposal And Exact Output Law

Input symmetric matrices A_1,...,A_m over odd Fp and b in Fp^m. Set
Q_i(x)=x^T A_i x. Output a publicly verified x with Q(x)=b. The proposed
goal was polynomial time in n,m,log p by Gaussian Fourier linearization.
Let

    A(z)=I+sum_i z_i A_i,   T={z:det A(z)!=0},   alpha=|T|/p^m.

The determinant polynomial is nonzero at z=0 and has degree <=n, so
alpha>=1-n/p. Constant-density preparation is paid only when this bound
is useful; elsewhere its actual probability must be retained.

Start with uniform z in T and x in Fp^n and phase
psi(x^T A(z)x+z.b). Fourier-transform x, change its frequency y to
u=(2A(z))^-1 y, remove the known quadratic Gauss factor
epsilon_p^n chi(det A(z)), and multiply by psi(u^T u).
Completing the square gives EXACTLY

    (|T| p^n)^(-1/2) sum_(z in T,u) psi[-z.(Q(u)-b)] |z,u>.

These are polynomial-cost public matrix operations and phases; there is
no hidden inverse or assumed state access. The operation reproduces
constraint evaluation with restricted Fourier support. Fourier-transform
z, require its zero frequency, and verify the measured u. Each solution
has joint probability |T|/p^(m+n), hence

    Pr[zero frequency AND verified solution | prepared T]
      = alpha * #{u:Q(u)=b}/p^n.

A single initial herald for T multiplies another alpha. Retrying that
herald when alpha is bounded below does not remove the solution density.
Amplitude amplification of this operation gives ordinary search scaling.

The cheapest exact family is m=n, Q_i(x)=x_i^2 and b_i=1. Here
alpha=(1-1/p)^n and the verified probability is
[2(p-1)/p^2]^n, although the classical solution x=(1,...,1) is immediate.
This refutes this proposed amplification mechanism. It does not bound
other MQ algorithms, general Fourier processing or quantum search beyond
this circuit. No finite numerical control is needed for the identity.

## 5. Decision

Do not extend either proposal. The Levi oracle theorem remains valid in
its opaque input model, but this explicit low-degree tensor source is
classical. The Gaussian MQ operation leaves the original density cost.
The next comparison is an explicit arithmetic output obtained from paid
compact units/class numbers; it must survive source, normalization and
matched classical checks before admission. No claim gates are promoted.
