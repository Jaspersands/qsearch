# Native metabelian HSP source and erasure: independent audit

2026-11-13. No network, API, Git, finite scan, or formal build was used.
Inspected CLASS_THREE_HSP_THEOREM_DRAFT.md (intersection/source and 375–485),
BOUNDED_CLASS_METABELIAN_HSP.md (245–405), AFFINE_PHASE_MIXED_CHANNEL_AUDIT.md,
and the actual statements/proofs in AffineSupportErasure.lean,
CosetSourceFourier.lean, and ClassThreePotential.lean.

**Finding.** No source or instrument counterexample in the stated model.
The global degree<=c potential and the complete mixed-input instrument
follow by the derivations below, for arbitrary hidden rank. This admits
these interfaces, not the full algorithm, published priority, practical
complexity, or a useful non-oracle quantum advantage.

## 1. Exact native model and the intersection step

Fix c and a prime p>c. The public input is a finite-dimensional metabelian
nilpotent Lie algebra L/F_p of class<=c, with explicit BCH arithmetic and
clean public group-coordinate encoding. G=exp(L), and the deterministic
quantum-query oracle f is constant and distinct on the cosets gH, for an
arbitrary subgroup H. No hidden generators, phase oracle, or coset origin
is supplied. Write N=[L,L], an abelian ideal, and V=L/N with a public linear
section s. Expressions exp(q) below mean exp(s(q)); s need not preserve
brackets. The bijection g(n,q)=exp(n)exp(q) and its inverse are public BCH
computations. They do not assume a semidirect-product splitting.

Uniform preparation followed by querying f and discarding its label gives

    rho_H(g,g')=|G|^-1 1[g^-1 g' in H].

Let K=log(H intersect exp(N)), a linear subspace of N. Measure the quotient
coordinate q. Its outcome is uniform, and its conditional normal kernel is

    |N|^-1 1[n'-n in Phi(q)K],   Phi(q)=exp(ad(s(q)))|_N.

Indeed g(n,q)exp(k)=g(n+Phi(q)k,q). Applying the known inverse Phi(-q)
therefore gives the ordinary abelian K-source for EVERY measured q.
The full finite exponential is needed; 1+ad(q) alone is a class-three
shortcut. A fixed batch t>=dim(N)+ceil(log_p(1/delta)) of exact Fourier
samples has rank failure <=delta. Its annihilator Khat always contains K.
Checking f(exp(k_i))=f(1) on a basis of Khat certifies equality in this exact
sampling model, because N is abelian. Approximate Fourier sampling requires
a separate global error allowance; these checks alone do not certify that
an approximately sampled Khat contains K.

On successful recovery, H<=M=N_G(exp(K)), since this intersection is normal
in H. The Lie normalizer is exactly

    log(M)={x in L : [x,K] subset K}.

One implication follows from exp(ad x). Conversely, if exp(ad x) preserves
K, its finite logarithm preserves K and equals ad x. Nilpotence and p>c
justify these inverse polynomials. Thus the normalizer is computable by
public linear equations; it contains N. K is an ideal in log(M), so M/K
is a legitimate public Lie quotient. A linear section implements its
oracle f'(mK)=f(m), well-defined because K<=H. Coherent section computation
and uncomputation use no hidden membership query beyond the original f.
The quotient stays metabelian and H/K is transverse to N/K, hence to its
new derived ideal. Recompute that ideal and a section; finish directly if
it is zero. Below rename the quotient objects L,N,V,H.

## 2. One bounded-degree potential, fixed for all source copies

Now H intersect exp(N)=1. Every commutator of H belongs to that intersection,
so H is abelian. Its logarithms commute: exp(ad x)y=y implies [x,y]=0 by
the same finite-logarithm argument. Hence log(H) is additive, and powers
give F_p scalar closure. Its quotient image is a linear U<=V, and

    h(u)=exp(s(u)+a(u)),   a:U->N linear,
    h(u)h(v)=h(u+v).

Choose ONE proof-only linear projection pi:V->U, with pi|_U=id. For all
q in V, set u=pi(q), r=q-u and

    Q(q)=log(exp(s(r)) exp(s(u)+a(u)) exp(-s(q))).

The word projects to zero in V, so Q(q) lies in N. Every input logarithm
is linear in q. Multi-BCH is a sum of bracket words of total length<=c;
all longer words vanish in L. Thus every coordinate of Q is a polynomial
of total degree<=c. Nesting two truncated BCH expressions does NOT create
a surviving degree c^2 term. The given p>c BCH hypothesis pays denominators.
No coefficients of pi, a, or Q have to be computed by the controller.

By definition exp(Q(q))exp(s(q))=exp(s(r))h(u). For v in U, the residual
r is unchanged at q+v. The homomorphism law for h therefore gives

    exp(s(q))h(v)=exp(-Q(q))exp(Q(q+v))exp(s(q+v))
                  =exp(Q(q+v)-Q(q))exp(s(q+v)).

The second equality uses precisely the abelianness of N. Multiplying by
exp(n) proves the exact public-chart action

    g(n,q)h(v)=g(n+Q(q+v)-Q(q), q+v).

This holds simultaneously for every q,v, with the SAME Q. Different choices
of pi give potentials differing by a function constant on each U-coset,
which does not change any source kernel. U=0 is included (H trivial, Q=0).

## 3. The actual Fourier source, including normalization and signs

Put D=|V|, B=|N|. Transversality and the action identity give

    g(n,q)^-1 g(n',q') in H
      iff q'-q in U and n'-n=Q(q')-Q(q).

Apply the positive-sign normal QFT |n> -> B^-1/2 sum_lambda chi_lambda(n)
|lambda>. For a connected pair q,q' exactly B pairs n,n' contribute, so

    sigma_lambda(q,q')=(BD)^-1 1[q'-q in U]
                       chi_lambda(Q(q)-Q(q')).

Its trace is 1/B. Thus every lambda, including zero, is uniform and the
normalized block is rho(U,lambda.Q), where

    rho(U,P)(x,x')=D^-1 1[x-x' in U] omega^(P(x)-P(x')).

This is the uniform mixture of phase-decorated U-coset states, hence positive
with trace one. Fresh original-oracle preparations give independent mixed
blocks conditional on the fixed subgroup and their observed labels.
The discarded oracle register is never reused as correlated advice.

## 4. Complete public instrument and its exact scope

For k product inputs rho(U,P_i), public scales c_i with some c_i!=0, append
a fresh uniform ambient register x, subtract c_i x from input register i,
and measure the old registers, retaining the complete outcome y. Its Kraus
operator is

    K_y=D^-1/2 sum_x |x><y_1+c_1 x,...,y_k+c_k x|.

For fixed input tuples a,b, output orthogonality makes (sum_y K_y^*K_y)_(a,b)
zero unless a=b; for each x there is exactly one y=a-cx. Thus the diagonal
sum is D/D=1. This is a complete physical instrument, not postselection.
Direct substitution into the product kernel gives

    K_y (tensor_i rho(U,P_i)) K_y^*
       =D^-k rho(U, sum_i P_i(y_i+c_i x)).

Indeed its indicator is all c_i(x-x') in U, equivalent to x-x' in U since
some scale is nonzero. Every outcome has probability D^-k. Zero-scale
inputs may be measured and their outcomes forgotten; discarding those
unused inputs implements the same active channel, with all copies charged.

Conditioning on the entire earlier CLASSICAL transcript fixes public scales
and packet choices. Disjoint packets remain a product under local merges
and fresh oracle preparation, by induction using this branch identity.
This is not a claim of decoupling from an arbitrary external purification.
For fixed c the unknown coefficient vector of Q has at most
dim(N)*(binom(dim(V)+c,c)-1) entries. Symbolic public maps on these formal
coefficients update under translation/scaling without evaluating Q or pi.
The cancellation solver and its bit clock remain separately charged.

Two exact falsifiers delimit this admission. Before removing K, H=exp(N)
with N!=0 has only the zero normal character, contradicting a uniform-label
claim. Also, take U=0 and two correlated inputs D^-1 sum_a |a,a><a,a|,
each marginal rho(0,0). With c_1=c_2=1 only outcomes y_1=y_2 occur, each
with probability 1/D; the product-input law would give all D^2 outcomes
probability 1/D^2. Finally all-zero scales produce the pure ambient uniform
state, not rho(U,0) when U is proper. The native construction avoids all
three failures; no extension to correlated suppliers is admitted.

## 5. Formal and algorithmic boundary

AffineSupportErasure explicitly assumes product kernels and a nonzero scale;
its branch, completeness, and trace proofs match the calculation above.
CosetSourceFourier explicitly assumes a coordinate equivalence and the
right-action law; Section 2 supplies those hypotheses in the native model.
ClassThreePotential treats c=3 with proof-only linear maps and commuting
hidden lifts; it is not a formal proof of the general-c construction.
No Lean acceptance label was used to infer these source premises.

The admitted result is the ideal native source/instrument interface for
every fixed c, p>c, and arbitrary H after the charged intersection step.
Public-presentation acquisition outside this input model, general-degree
diagonal solvers, finite-gate error accounting, class-descent completion,
the full bounded-error time bound, and literature priority are not newly
certified here. No growing-class or nonmetabelian conclusion follows.
