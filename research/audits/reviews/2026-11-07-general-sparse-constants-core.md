# General sparse constants: independent core review

7 November2026. Read current STATE/TRAPS, Section1 and Section2 of
`GENERAL_SPARSE_CONSTANTS_ATTACK.md`, and the reused native contract and
minor/HNF estimate. No Git/network/API, implementation, or numerical sweep.

**ACCEPT the polynomial sparse-BIT Alg attack at its stated boundary.**
It recovers the FULL lattice of exponents whose products are algebraic
over Q. This is not full Rel, does not remove torsion/constants, and does
not pay the proposed small-number-field constant map. The Section2
specialization falsifier is also correct, with one scope clarification
about its norm sentence below. No substantive Section1 repair was found.

## Clearing, derivatives, and bounds

After clearing rational scalars within each pair, all numerator/denominator
polynomials are integral and nonzero denominators are promised. A single
product D of the denominator polynomials suffices for EVERY f/u coefficient.
The input product l1 bound H bounds D and each rewritten numerator
`P*(D/Q)`; no polynomial division or expansion is required. The stated
d0=(L+1)beta safely bounds their total degrees. Native unused variables are
dropped, and the numerical Y degree delta is charged, so matrix dimension,
number of derivatives, and tuple length are polynomial in native encoding.

For C=A/D, matrix powers have entry norm at most delta^(h-1) H^h.
The common powers of D for the five displayed multiplication matrices
are correct, including the extra denominator in FORMAL T derivatives.
Their numerators have degree at most e0=(delta+1)d0. The deliberately loose
U dominates coefficient derivatives, matrix-power sums, and integer Y
derivative factors. Determinant and adjugate entries are bounded by
V=delta! U^delta; adjugates have degree at most(delta-1)e0.

In particular, writing i,j subscripts as in the note,

    M(extended partial_j u_i)
      = (T_ji detJ - Y_i adjJ F_j)/(D^(delta+1) detJ),
    M(u_i)^(-1)=D^delta adjA_i/detA_i.

Their product is exactly the displayed logarithmic-derivative matrix.
It is NOT obtained by naively differentiating the multiplication matrix
in its moving power basis. The written order is valid even without an
informal exchange of factors; these are in fact commuting multiplication
operators in the field. The determinant scalings are
`detA_i=D^(delta^2) Norm(u_i)` and
`detJ=D^(delta*(delta-1)) Norm(f_Y)`. This does not insert those larger
norm powers into the matrix-inverse prefactors above. Irreducibility in
characteristic0 makes f_Y and all u_i invertible.

After multiplying by the other detA_l factors, the cleared numerator has
degree at most(k+1)delta e0 and entry norm at most
`delta*(1+delta^2)*U^2*V^(k+1) <= C0`.
Applying to the vector1 only selects a column. The common h has degree
at most Dstar and norm at most H V^(k+1)<=C0, and is nonzero.
All are formal bounds on polynomial-size evaluable expressions. Their
LOGARITHMS, not their numerical degrees, are polynomial in input bits.

The extended coordinate derivations span Der_Q(F) over F. In characteristic0
their common kernel is precisely the relative algebraic closure of Q in F.
Thus the implicit integer coefficient-matrix kernel is exactly Alg and is
saturated. This also includes s=0, when Alg=Z^k; k>=1 is native.

## Full kernel bound and modular/LLL recovery

The basis bound k! C0^k is justified without constructing coefficient rows.
Choose q independent rows and a nonsingular q-column minor B. With
d=abs(detB)<=q!C0^q, the projection of the integer kernel into the other
k-q coordinates contains d Z^(k-q). Its HNF basis has entries bounded by
d. Cramer's rule lifts each vector with pivot coordinates at most
(k-q)q!C0^q, hence the claimed bound. Rank0 and rankk are trivial endpoints.
The conservative Balg is larger and has polynomial bit length.

Every false box exponent has a nonzero coordinate polynomial whose
coefficients have magnitude at most kR C0. A PRIME p>2kR C0 preserves at
least one such coefficient, and preserves h. The stated union bound over
one witness per false exponent and h is valid; the box is proof-only.
Its size contributes k log(2R+1) bits to the prime bound. A polynomial-bit
prime can be found with the already paid capped prime-density routine.
The random-point bad probability is at most the claimed eta/8. Allocate
the remaining budget to capped prime/point sampling; no unbounded retry.

At h(t)!=0 all denominator and matrix-unit tests succeed. The full algebra
F_p[Y]/f_t retains delta basis coefficients; irreducibility is unnecessary.
Sparse evaluation/binary powering and finite-field matrix operations cost
polynomial time in log p, log beta, and charged dimensions. Its congruence
kernel M is full rank and contains Alg, including all unbounded true vectors.
On the good event no false vector has infinity norm<=R.

The first r LLL vectors have Euclidean norm at most
2^((k-1)/2)*sqrt(k)*Balg<R and span Alg's real space. Every later basis
vector has infinity norm>R. The note's Gram--Schmidt last-index argument
correctly proves FULL generation, not finite index. An even shorter proof:
a prefix of a Z-basis of M generates M intersect its real span; this
intersection contains Alg while the prefix lies in Alg. Thus equality
holds. Select the Euclidean-norm<=R prefix using squared integer norms.
Rankr=0 selects nothing; rankr=k selects the complete basis. There is no
saturation of full Rel or recovery of constants hidden in this step.

## Section2 falsifier and its exact limit

A=T^M+2 is Eisenstein at2. Modulo A, B/A is6, so the constant coefficient
of f divided by A is -6 and f is Eisenstein at prime polynomial A.
The sparse term count and coefficient bit lengths are polynomial in delta
and log M. At0, implicit-function expansion gives the written leading
coefficient `-2^(2-delta)/product_(l!=j)(j-l)` for u_j on branchj.
At infinity its exponent is M(4-delta), giving relative depth M(delta-3).
The height lower bound follows from h(a^M)<=h(a^M+2)+log4 and h(cA)>=h(A)-h(c).
For even M the only rational zeros of B are0,1,-1; localizing every u_j
at these points gives the zero algebra. Every other rational point forces
the stated expanded-monic coefficient-height cost. This blocks that direct
presentation shortcut, not every constant map or primitive-element change.

Clarify "Norm(u_j)=+/-B does repair this FAMILY" as repairing the displayed
naive-leading-term obstruction, not providing an injective constant test:
u_i/u_j has norm1 yet is nonconstant. Indeed the T=0 branchi valuations
are M for u_i and0 for the other units, so this tuple actually has Alg=0.
No general Puiseux/norm impossibility or fullRel algorithm follows.
