# Reciprocal elimination: exact degree and false boundary solutions

**Status: proved deductions with limited algorithmic scope.** Put
r=N-K and let C=ker(H), an [N,r] MDS code. On its all-nonzero stratum,
write y_i=1/x_i. The native trace conditions become linear over F_2,
but membership in the reciprocal image of C is the remaining constraint.
These observations do not give a classical complexity lower bound.

## Ordinary polynomial elimination starts at degree r

Over an algebraic closure of F_q, the minimum total degree of a nonzero
polynomial in y alone that vanishes identically on the reciprocal image
of C is exactly r. Here degree means ordinary field-polynomial degree,
not Boolean algebraic degree after Weil descent.

Proof of the lower bound: parametrize C by r field variables and denote
its coordinate linear forms by l_i. Any at most r of these are linearly
independent. Suppose F(y) is a nonzero relation of degree D<r. Choose a
nonzero monomial c_a y^a of maximum total degree D, and let S be its
support. There is a point p where l_i(p)=0 exactly for i in S: the
intersection has positive dimension, and no other coordinate hyperplane
contains it, by independence of every |S|+1 forms. Use the l_i, i in S,
as local parameters, fixing the other local coordinates at p.

In F(1/l_1,...,1/l_N), all denominators outside S are units and expand
with nonnegative powers of these local parameters. A term contributing
to the Laurent coefficient product_(i in S) l_i^(-a_i) must therefore
have exponents at least a_i on every i in S. Their sum already equals
the maximum degree D. Thus only the chosen monomial can contribute,
with coefficient c_a!=0. The rational function cannot vanish identically.

For attainment, take a minimum-weight dual word d in C^perp. Its support
S has size r+1. Clearing denominators in sum_(i in S) d_i/y_i=0 gives

    sum_(i in S) d_i product_(j in S, j!=i) y_j = 0,

a nonzero polynomial of degree r.

There is a finite-field qualification. A relation might vanish only on
the F_q points, without being a rational identity. For degree D<r, clear
denominators using the maximum exponent of each y_i appearing in F.
The resulting nonzero polynomial in the r parameters has degree at most
ND. The all-nonzero part of C has at least q^r-N*q^(r-1) points, while
the polynomial has at most ND*q^(r-1) zeros. Hence no such relation can
vanish on all these points when q>N(D+1). In particular q>Nr suffices
for the same minimum-degree statement over the finite native code.
This condition holds eventually at q=2^n, N=n².

This is consistent with established reciprocal-plane/circuit algebra,
not a claimed new algebraic-geometric theorem. See Fink--Speyer--Woo,
[A Groebner basis for the graph of the reciprocal plane](https://arxiv.org/html/1703.05967v1),
Theorem 1 and its initial setup over an arbitrary field. The elementary
argument above avoids importing a characteristic-zero hypothesis.

## Even the full reciprocal closure contains false native answers

Assume r>=2 and q>N-1. Fix an index j and c in F_q with Tr(c)=1.
The point y=c*e_j lies in the algebraic closure of the reciprocal image
of C, even though totalized inversion sends it to an invalid codeword.

To see this, choose v in C with v_j=0 and all other v_i nonzero. Such
a v exists: inside the (r-1)-dimensional space C intersect {x_j=0},
each other coordinate cuts a proper hyperplane, and q>N-1 permits
avoidance of their union. Choose w in C with w_j=1/c. For a formal
parameter T, take x(T)=T^(-1)*v+w. Its reciprocal has coordinates

    y_j(T)=c,
    y_i(T)=T/(v_i+T*w_i),  i!=j.

They are regular at T=0, with limit c*e_j. Thus every polynomial
identity of the reciprocal code vanishes at this point. It also
satisfies the desired trace vector b=e_j. Nevertheless inv0(y)=c^(-1)e_j
violates the first row of H, which is the all-one parity check.

Consequently solving even the full reciprocal-closure ideal together
with the trace equations is not an exact solver for the native relation.
This is stronger than a counterexample to a particular incomplete set
of cleared equations. Enforcing all y_i!=0 repairs this specific issue;
CONIC_REFORMULATION.md proves that an all-nonzero witness exists for
every sufficiently large native input. That open condition must still
be implemented in an attack.

## Self-attack and next obligation

The degree statement excludes only low-degree identities in reciprocal
coordinates before imposing the target trace equations. It says nothing
about the solving degree after adjoining trace/field equations, and
nothing about algorithms that retain x or use auxiliary variables.
Frobenius has high ordinary polynomial degree but is binary linear.
The existing quadratic lifted formulation is therefore fully compatible
with this result. Treating r as a classical hardness exponent would be
an error.

The strongest falsifiers are a failure of the MDS independence used in
the pole argument, or a finite-field relation below degree r outside
the stated size condition. Both are explicit hypotheses, not assumed
randomness. The boundary example is constructive over the supplied
field and uses the original first parity row.

The next useful attack must exploit the trace/Frobenius constraints or
coupled variables, and return a point in the required open stratum.
The residual affine system in CLASSICAL_RESTRICTION.md supplies a
concrete smaller target for such an algorithm; ordinary low-degree
elimination of the original reciprocal code alone cannot supply it.
