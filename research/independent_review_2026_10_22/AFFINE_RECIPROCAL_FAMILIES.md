# Exact scope of affine inverse-coordinate parametrizations

**Proved deduction for a specific attack family.** Making the inverse
coordinates affine in free field parameters would turn every trace target
into a binary linear equation. The parity identities severely constrain
such a parametrization: it is only disjoint-support codeword scaling in
disguise. This is not a lower bound on adaptive or nonlinear algorithms.

Let H be the native K-by-N Vandermonde matrix, C=ker H, and consider
nonzero affine polynomials in t=(t_1,...,t_d) over F_q,

    y_i(t)=a_i dot t+c_i,       x_i(t)=1/y_i(t).

Assume Hx(t)=0 as a rational identity. Coordinates fixed at x_i=0 can
instead be omitted; they force their target bits to zero. The other
coordinates are considered on the open set where every y_i is nonzero.

Partition the nonconstant y_i by proportionality over F_q. Write
y_i=s_i*L_g for i in group G_g, with s_i nonzero and L_g a representative
nonconstant affine polynomial. Distinct L_g are nonassociate irreducible
polynomials. Let v_g have entries 1/s_i on G_g and zero elsewhere, and
let v_0 contain the constant reciprocal coordinates. Then

    H v_0 + sum_g (H v_g)/L_g = 0.                  (1)

Multiply (1) by the product of the distinct L_g and reduce modulo one
L_h. The quotient polynomial ring is an integral domain; every other
L_g has nonzero residue. Therefore H v_h=0. Applying this separately to
each h, and then using (1), also gives H v_0=0.

Thus each varying group supports a nonzero native codeword. The MDS
distance of C is K+1, so |G_g|>=K+1. The groups are disjoint, giving

    g <= floor(N/(K+1)).                            (2)

At N=n^2 and K=floor(N/8), N<8(K+1), hence g<=7. This is true even
if the nominal number d of parameter variables is enormous: the output
depends on at most seven affine field values L_g(t).

## Finite-field identity qualification

One must not silently infer a rational identity merely from a finite
test. If, however, the proposed family is promised to satisfy Hx=0 for
EVERY t in F_q^d where the denominators are nonzero, the identity follows
when q>2N-1. Indeed, clearing the distinct nonconstant denominators yields
a polynomial of total degree at most N-1: with no constant coordinate
each term omits its denominator; with a constant coordinate there are
at most N-1 nonconstant denominators in total. A nonzero numerator has
at most (N-1)*q^(d-1) roots, whereas the open set has at least
(q-N)*q^(d-1) points. The displayed condition therefore forces the
identity. It holds for all sufficiently large native n. This argument
requires a whole-parameter-family guarantee, not a finite collection of
successful parameter choices.

## What this says about native targets

For a fixed family, each group's target bits have the form

    Tr(s_i*L_g(t)),       i in G_g.

They are determined by one field value. Consequently the entire fixed
family attains at most q^g<=2^(7n) target strings, including its fixed
constant-coordinate bits. A uniform N-bit target belongs to this set with
probability at most 2^(7n-N). Correlations between the L_g can only reduce
this count. This is an exact counting limitation on that fixed family,
not an assumption of independent target bits within a group.

The familiar single-codeword scaling construction is the one-group case.
Multiple groups do not give an unrestricted inverse-coordinate linear
solver; they require separate native codewords on disjoint supports.

## Self-attack and the next obligation

An algorithm may choose the partition, coefficients s_i, or entire family
AFTER seeing the target. Bound (2) still constrains each returned rational
identity, but the 2^(7n-N) probability statement does not apply to that
adaptive union. Choosing suitable codeword directions remains a genuine
search step and must be charged. The theorem also does not apply to
nonlinear denominators, relations valid only on a constrained parameter
variety, or parametrizations that satisfy Hx=0 only for the parameter
eventually found by another solver.

The strongest falsifier would be a claimed full affine inverse family
with more than seven genuinely varying groups at the native rate. Its
pole residues would explicitly contradict H v_g=0 or the MDS distance.
The next useful attack is therefore an adaptive method for choosing those
directions, or a nonlinear family with a paid search algorithm. This
deduction supplies neither classical hardness nor a novelty claim for
the elementary pole argument.
