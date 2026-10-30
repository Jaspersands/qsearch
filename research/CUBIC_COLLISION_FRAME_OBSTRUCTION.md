# Cubic Collision Frame Obstruction

30 October 2026. An exact, scoped algebraic obstruction with finite controls.
No general receiver bound, optimal SDE bound, or novelty claim.

## Fixed-Cell Reuse Model

Let p > 3 be prime with p = 1 mod 3. Let z_0,z_1,z_2 represent the
three distinct nonzero cube classes. A two-level collision scaffold has
disjoint cells I_ij, fixed nonzero internal weights b_a, and vector values

    V_ij = sum_(a in I_ij) ell_a*b_a^3,
    sum_i z_i*V_ij = 0,    sum_j z_j*V_ij = 0.

The labels ell_a lie in F_p^r. Reusing this FIXED scaffold means assigning
one scalar h_ij per cell and setting w(h)_a = b_a*h_ij on its support,
and zero outside. Consequently

    T(w(h),w(k),w(l)) = sum_ij V_ij*h_ij*k_ij*l_ij.

This is the collision structure in [power_sde.py](../theorems/power_sde.py)
and [the symmetric-contraction note](POWER_SDE_SYMMETRIC_CONTRACTION.md),
based on the [Ivanyos--Santha scaffold, Section 3.2](https://arxiv.org/html/1503.09016v2).
Different dependencies, partitions, or internal weights are NOT fixed-cell
reuse. Neither individual cubic witnesses nor independent root choices
automatically satisfy the mixed equations required by the Gram receiver.

## Annihilator And Universal Claim

Write U = ker(z^T), of dimension two. Each scalar component of V belongs
to U tensor U. With the entrywise pairing, its full annihilator is

    A = (U tensor U)^perp = {z*a^T + b*z^T : a,b in F_p^3}.

Containment follows from the two axis equations. The right-hand space has
dimension 6-1=5: its parameter kernel consists of a=c*z, b=-c*z.
The annihilator also has dimension 9-4=5, proving equality. Equivalently,
C belongs to A exactly when every rectangle satisfies

    C_ij/(z_i*z_j) - C_il/(z_i*z_l)
      - C_kj/(z_k*z_j) + C_kl/(z_k*z_l) = 0.                 (1)

Indeed, C_ij/(z_i*z_j) must be a sum of a row term and a column term;
the rectangle identities also imply that decomposition by fixing row and
column zero.

**Claim.** If S is a linear space of 3-by-3 matrices such that every
entrywise triple product h*k*l, for h,k,l in S, belongs to A, then dim S <= 1.
Equivalently, it is enough to require h^3 in A for every h in S: polarization
recovers the mixed products because 6 is invertible. This is universality
over tensors satisfying ONLY the two axis identities.

## Proof, Including Zeros

**Binary-form lemma.** Cubes of at most four nonzero, pairwise
nonproportional binary linear forms are linearly independent over F_p.
Normalize finite projective forms as X+t*Y. Their coefficient vectors are
(1,3t,3t^2,t^3); the first m coordinates form an invertible scaled
Vandermonde matrix for m <= 4 distinct t's. If Y is also present, there
are at most three finite forms. Their first m coordinates are independent,
whereas Y^3 has all these coordinates zero, and its final coordinate is
nonzero. This proves the lemma, including the projective point at infinity.

Restrict any proposed plane in S to h=X*h_0+Y*h_1. The four entries of
a rectangle are binary linear forms, and (1) applied to h^3 is an identity
between their cubes. It is a polynomial identity by the mixed conditions
(or by degree three being less than p).

Discard identically zero forms and group the others by proportionality.
All four rectangle multipliers are nonzero. The lemma says every surviving
direction must occur at least twice: a singleton cannot cancel. With at
most four entries, two independent directions therefore require exactly
four nonzero forms split into two cancelling pairs. If any entry is zero,
there can be at most one direction. This handles zeros without a
full-support assumption.

An adjacent cancelling pair would require z_i/z_k or z_j/z_l to be a
cube, contrary to distinct cube classes. The only remaining pairing is
the two diagonals. Put a=z_i/z_k and b=z_j/z_l. Those cancellations require
both a*b and a/b to be cubes; signs do not change the class since -1 is
a cube. Then a^2 is a cube. The cube-class quotient has order three, so
a itself is a cube, again a contradiction.

Thus every rectangle projection of S has dimension at most one: a
higher-dimensional image would contain the forbidden plane. Any two cell
positions share a rectangle, including positions in the same row or column.
Their coordinate functionals on S are therefore dependent. Choose any
nonzero coordinate functional; all the others are its multiples. Since
the nine coordinates distinguish matrices, dim S <= 1. QED.

## Rank-Four Actual Tensors And An Exact Example

Let L be the r-by-9 matrix with columns V_ij. Its row space lies in
U tensor U. If rank L = 4, that row space is all of U tensor U, so
ker L = A. The same obstruction then holds for this PARTICULAR tensor,
even for contractions chosen after inspecting its values. Rank four also
forces every V_ij to be nonzero, hence every cell to be nonempty and the
map h -> w(h) to be injective. The rank check costs O(r) field operations
because there are only nine columns.

Over F_7 take

    z = (1,2,4),
    q_0 = (1,0), q_1 = (0,1), q_2 = (5,3),
    ell_ij = q_i tensor q_j,  V_ij = ell_ij.

Since sum_i z_i*q_i=0, both axis identities hold. The first two q's
give all four standard tensor basis vectors, so the label matrix has
rank four. Each cell can be a singleton with weight one. With indices
starting at zero, set

    u = [[0,1,-1],[-1,0,1],[1,-1,0]],    v = u + E_01.

These are independent and have identical entrywise cubes, but

    T(u,u,u) = T(v,v,v) = (0,0,0,0),
    T(u,u,v) = (0,1,0,0),
    T(u,v,v) = (0,3,0,0).

Thus two valid SDE witnesses do not supply a singular plane. In fact the
nine-column bank has no singular plane at all, by the rank-four claim.

**Source-choice distinction.** These values are realizable by legal
two-level scaffold choices: for each j put ell_0j,ell_1j,ell_2j into a
first-level block, choose relation z, and then combine the three blocks
with relation z. At rank four, pad each block to width five and pad the
second level to nine blocks, giving 45 columns. Unused columns are zero;
the chosen active root weights are all one. The test reconstructs those
choices explicitly. It does NOT call or claim that a particular
deterministic `_relation` implementation selects them, and it does not
invoke the large-field symmetric sampler at p=7. Padding creates extra
trivial directions in the 45-column bank; the obstruction there applies
only to the fixed nine-cell image, not to the entire padded space.

## Scope, Comparators, And Replay

- The proof covers cubic fixed-cell reuse, including nonsymmetric
  contractions and zeros. It does not cover different scaffolds or
  within-cell weights, higher collision levels, or p=2 mod 3.
- Rank below four may provide additional relations; the universal claim
  does not exclude exploiting them. A rank-one positive control has two
  singular coordinate directions. No distribution of actual scaffold
  ranks is proved, even for genuinely IID uniform raw labels: adaptive
  dependence selection does not make the resulting cells IID.
- No general high-rank receiver or column lower bound follows. Separate
  comparator work must use the literature review's corrected ISS2012
  [Section 5, Claim 1](https://www.irif.fr/~santha/Papers/iss12.pdf)
  diagonal-quadratic arity (r+1)(r+2)/2, not (r+1)^2. At rank two this
  is six. Scalar cubic arity is two when p=2 mod 3 and at most three
  when p=1 mod 3, giving the matched sequential counts 12/18.
  For a scalar triple, a zero coefficient supplies a singleton, and
  two coefficients in the same cube class supply a pair. Otherwise,
  for coefficients (a,b,c), `ternary_cubic_scales(p,(a,(-b)%p,c))` returns
  (1,y,z), so a*z^3+b*y^3+c=0 and (z,y,1) is a witness. The three
  supplied representatives remain in distinct classes since -1 is a cube.
  The parent literature/Gram-geometry audit owns verification and
  integration of that comparison; this obstruction needs no such bound.
- A falsifier is an independent pair h,k with all four products
  h^3,h^2*k,h*k^2,k^3 in A under the stated cube-class promises, or
  their contractions zero on an axis tensor of rank four. Testing these
  four contractions costs O(r), without field enumeration or advice.

The tests use independent elementary modular arithmetic, not the production
solver. They check the annihilator dimensions, the binary-form lemma,
cube-class exclusions, all 2,850 RREF planes for EACH of nine F_7
rectangles (25,650 rectangle-plane checks), the 27-plane split-cubic
positive control, and the actual tensor and prescribed scaffold choices.
Finite enumeration is a small test only, not an algorithmic ingredient.

    PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -W error -m pytest -q -W error -p no:cacheprovider tests/test_cubic_collision_frame.py
