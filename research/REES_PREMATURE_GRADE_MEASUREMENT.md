# Premature Rees Grade Measurement: An Exact Instrument Obstruction

29 October 2026. Written derivation with a limited in-memory numerical
control, not a formal proof, implemented receiver, or general source bound.

## 1. Scope And Source Contract

The question is whether one common bank can replace the sequential product
of whole-grade arities in [the parameter bound](REES_FULL_GRADE_PARAMETER_BOUND.md).
This note rules out a specific interface: independently measure ALL grades
above one on every raw lifted coset source, retain every classical label
and the full conditional source, then perform arbitrary processing of that
measured bank. No further hiding-oracle access, retained oracle-label
purification, or additional unmeasured source is available to that processor.

The inputs are independent ideal mixed coset states. All accuracy and cost
guarantees concern complete trace-preserving instruments, INCLUDING ABORT.
They do not condition away a rare outcome or grant free source reuse.
The result is NOT a lower bound for arbitrary coherent collective receivers,
original-oracle algorithms, or the existing sequential arity product.

The [existing source theorem](REES_HSP_REDUCTION.md#4-central-descent-without-transversality)
uses a CENTRAL subgroup, whose projectors commute with the hidden coset
density. Its [measured composition](REES_MEASURED_RECEIVER_FORMALIZATION.md)
keeps all records and inactive-target masses. The premature measurement
here is a different instrument: its subgroup is abelian but noncentral.
Thus the obstruction below does not presuppose noncommuting joint labels.

## 2. An Actual Growing-Class Rees Family

For any prime p>c>=3, take the genuine filiform Lie algebra

    L = span(X,Y_1,...,Y_c),   [X,Y_j]=Y_(j+1) for j<c,
    [Y_i,Y_j]=0,              [X,Y_c]=0.

Its actual class is c, n=c+1, r=dim[L,L]=c-1, and
gamma_d(L)=span(Y_d,...,Y_c) for d>=2. Use the actual Rees algebra,
not an associated graded replacement or an artificial truncation:

    A = direct_sum_(d=1..c) t^d gamma_d(L),   G=exp(A),
    n_N = direct_sum_(d=2..c) A_d,           N=exp(n_N),
    R = dim(n_N)=c(c-1)/2,                  D=dim(A)=c+1+R.

The ideal n_N is abelian because all its coefficients lie in span(Y_j).
N is therefore an elementary abelian NORMAL subgroup of order p^R.
Choose original hidden subgroup exp(F_p X). Its exact Rees lift is
K=exp(F_p tX), since F_p X intersects every gamma_d(L), d>=2, trivially.
K has order p, K intersects N trivially, and every nonzero dilation
Delta_s preserves both K and N. Also consider the valid hidden subgroup 1.

Let T=ad(tX) restricted to n_N. On its displayed basis,

    T(t^d Y_j)=t^(d+1)Y_(j+1)  if d<c and j<c, else 0,
    kappa=rank(T)=sum_(d=2..c-1)(c-d)=(c-1)(c-2)/2.

The nonzero images are distinct basis elements, so this is an exact rank
calculation for every c, not an extrapolation from a small matrix.
For a!=0, Ad(exp(a tX))-I=exp(aT)-I=aT U_a(T), with U_a(0)=1.
The truncated exponential is valid since c<p; U_a(T) is invertible and
commutes with T. Hence image(exp(aT)-I)=image(T) for every a!=0.

## 3. The Actual Two-Sided Measurement

Use R_g|x>=|x g^-1>, so R_g R_h=R_(gh), and put omega=exp(2*pi*i/p).
For lambda in the dual of n_N, set chi_lambda(exp z)=omega^(lambda(z)).

    rho_J = |G|^-1 sum_(h in J) R_h,              J in {K,1},
    P_lambda = |N|^-1 sum_(n in N) conjugate(chi_lambda(n)) R_n.

Because N is abelian, these are a complete orthogonal family of genuine
projectors. A public right-N coordinate chart, abelian Fourier measurement,
and inverse Fourier restoration implement them on the full G register.
Measurement and restoration use 2R field Fourier transforms per source,
plus public chart arithmetic; M sources cost cM preparation queries and M such
measurements. Ideal arithmetic is polynomial in D,c,log p per source;
physical Fourier/gate approximation must be charged separately.

Define lambda^h=lambda composed with Ad(h^-1), so
R_h P_lambda R_h^-1=P_(lambda^h). Orthogonality gives

    P_lambda R_h P_lambda = R_h P_lambda if lambda^h=lambda, else 0.

Write K_lambda={h in K:lambda^h=lambda}. The actual branch, not a
one-sided surrogate, is therefore

    P_lambda rho_K P_lambda = |G|^-1 sum_(h in K_lambda) R_h P_lambda.

Only h=1,n=1 contributes to its trace, since K intersects N trivially.
Thus BOTH hidden instances have every label with probability 1/|N|=p^-R.
Let S=Ann(image T). Section 2 proves

    |S|=p^(R-kappa),   Pr(lambda in S)=p^-kappa,
    K_lambda=K for lambda in S, and K_lambda=1 otherwise.

For every bad label lambda outside S the normalized branches coincide:

    rho_(K,lambda) = (|N|/|G|) P_lambda = rho_(1,lambda).

This loses hidden-subgroup coherence even though all measured labels
commute. In particular, centrality cannot be replaced by abelianity in
the source theorem. The lost cross-character blocks cannot be restored
by later classical moment equations on these records.

## 4. Every Grade Moment Can Vanish And The Output Still Be Wrong

Choose any lambda outside S, the positive-probability two-source record
(lambda,-lambda), and scales (1,1). Writing lambda_d for its grade-d part,

    sum_(i=1..2) s_i^d lambda_(i,d)=0 for EVERY d=2,...,c.

Nevertheless each bad branch has correlation chi_lambda(g) for g in N
and zero otherwise. Consequently the literal controlled-action contraction
is

    F(g)=Tr(rho_(K,lambda) R_g) Tr(rho_(K,-lambda) R_g)=1_N(g).

The required function is 1_(KN)(g). On a public transversal of G/N the
output is I/|G/N|, hiding the trivial subgroup instead of KN/N. This is a
support failure, not a remaining scalar phase. Any active bad branch
also has support N after any nonzero dilation; moment cancellation cannot
repair its zero correlation on nonidentity elements of K.

## 5. Exact Distinguishability And Abort-Inclusive Cost

Let tau_J=sum_lambda p^-R |lambda><lambda| tensor rho_(J,lambda),
retaining the whole accessible measurement output, and use
Dtr(a,b)=||a-b||_1/2. Put m=|G|/|N|=p^(c+1).
For a good label, rho_(1,lambda)=P_lambda/m is uniform on rank m.
With P_K=p^-1 sum_(h in K) R_h, the other branch is
rho_(K,lambda)=p P_lambda P_K/m, uniform on a contained rank-m/p space.
Their distance is exactly 1-1/p. Bad branches coincide. Therefore

    delta := Dtr(tau_K,tau_1)=p^-kappa (1-1/p).

There is also an exact tensor formula, not just a hybrid upper bound:

    Dtr(tau_K^tensor M,tau_1^tensor M)=1-(1-delta)^M <= M delta.

Proof: labels have the same independent uniform law under both instances.
Conditional on b good labels, the K state is uniform on a subspace of
relative rank p^-b inside the trivial-instance support, giving distance
1-p^-b. Average over b~Binomial(M,p^-kappa).

Here M is a fixed bank size or worst-case cap, padding unused slots if needed.
Let Lambda be ANY instance-independent CPTP processing of this bank, with
an explicit OK/ABORT flag and every other outcome included. The ideal
outputs are sigma_J=|OK><OK| tensor rho_(G/N,JN/N). Their distance is
1-1/p. If Dtr(Lambda(tau_J^tensor M),sigma_J)<=epsilon_J for J=K,1,
contractivity and the triangle inequality imply, with e=epsilon_K+epsilon_1,

    1-(1-delta)^M >= 1-1/p-e,
    M >= log(1/(1/p+e)) / [-log(1-delta)]        if e<1-1/p,
    M >= p^kappa [1-e/(1-1/p)].

Round each applicable bound upward to an integer. Abort probability is
part of epsilon_J, not discarded by conditioning. If only success-branch
error e_J and abort probability a_J are given, a_J+(1-a_J)e_J is a
sufficient unconditional error bound. Arbitrarily rare accurate successes
alone do not satisfy the premise. Constant sufficiently small total error
requires Omega(p^kappa) measured lifted copies, hence Omega(c p^kappa)
original preparation queries IN THIS INTERFACE ONLY.

## 6. Actual Class-12 Profile And A Lawful One-Shot Boundary

At c=12 the family has actual profile (13,11,10,9,8,7,6,5,4,3,2,1),
r=11, D=79, R=66, kappa=55. The good-label fraction is exactly p^-55,
delta=(p-1)/p^56, and |S|=p^11. These hold for every prime p>12,
including supplied p=2^127-1; p^55 is not replaced by a rounded power of 2.

A valid one-shot alternative is Pi_N=|N|^-1 sum_(n in N) R_n.
Normality makes Pi_N central in the group algebra. For any subgroup J,
its success mass is |J intersect N|/|N| and its normalized output is
rho_(JN). Public quotient extraction gives the desired quotient source.
Uniform-N preparation, controlled right multiplication, unpreparation and
zero-outcome postselection implement this projector with polynomial public
arithmetic per attempt. Here success is p^-R, requiring p^R lifted copies
or c p^R original queries in expectation; capped-run abort is still charged.
For M fixed nonzero scales, set V_s(g)=tensor_i R_(Delta_si(g)). Then
Tr(rho_K^tensor M V_s(g))=1_K(g), so its invariant projector has the SAME
success mass, not a bank-size enhancement. Adaptive coherent instruments
that retain cross-character coherence are not excluded by either argument.

## 7. Seven-Coordinate Replay And Computations Actually Executed

For c=3 use second-kind coordinates (x,y,z,w,u,v,t), degrees
(1,1,1,1,2,2,3), and arithmetic modulo p>3. The actual Rees law is

    (x,y,z,w,u,v,t)*(X,Y,Z,W,U,V,T)
      =(x+X,y+Y,z+Z,w+W,u+U+xY,v+V+xZ,t+T+xU+x^2 Y/2).
    (x,y,z,w,u,v,t)^-1
      =(-x,-y,-z,-w,-u+xy,-v+xz,-t+xu-x^2 y/2).

Here N={(0,0,0,0,u,v,t)}, h(a)=(a,0,0,0,0,0,0) generates K, and
h(a)n(u,v,t)h(a)^-1=n(u,v,t+a u). For lambda=(alpha,beta,ell),
chi_lambda(n)=omega^(alpha*u+beta*v+ell*t); S is exactly ell=0.
Represent rho=|G|^-1 sum_g C(g)R_g and P_lambda by coefficients
p^-3 omega^(-alpha*u-beta*v-ell*t) on N. Multiply coefficient dictionaries
using the displayed group law TWICE to obtain B=P_lambda*C*P_lambda.
Branch mass is B(1), normalized coefficients are B/B(1), and correlation
at g is the normalized coefficient of g^-1.

Executed in the preceding read-only pass: one standard-library Python
in-memory convolution at p=5, with C_K(h(a))=1 versus C_1(1)=1.
Labels (0,0,1), (0,0,4), (1,2,0) each returned mass approximately
0.007999999999999985 (exact prediction 1/125). Both bad branches had
zero coefficient difference from the trivial-instance branch after the
script's 1e-10 cleanup, and zero h(1) correlation. The good branch returned
h(1) correlation approximately 1+7.2e-16 i. This used floating complex
phases, not exact cyclotomic arithmetic or a physical quantum execution.
The same command enumerated basis/image positions for c=3,4,8,12,20,
obtaining (R,kappa)=(3,1),(6,3),(28,21),(66,55),(190,171); it did NOT run
a large-group state simulation. No repository test suite or Lean build
was run. These controls support, but do not replace, the exact derivation.

No general source lower bound or necessity of the sequential arity product
is established. A source-saving collective instrument remains open.
