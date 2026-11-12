# Logarithmic-collision Merkl atlas

2026-11-12. Geometric lemma independently proved and parent-checked.
Precise proof: audits/reviews/2026-11-12-merkl-log-atlas.md. Arithmetic
transfer remains OPEN; analytic chart existence is not a BIT algorithm.
This directly targets the branch-height exponential in the surface classical
comparator, not a general-purpose geometry subsystem. Corpus query and primary
Javanpeykar1403.6404 Definition3.1.1/Theorem3.1.2 preceded this candidate.
The strongest existing bound uses a Belyi conversion with exponential dependence
on logarithmic branch height; Remark6.0.5 separately notes exponential degree
but logarithmic branch-height dependence in Bilu--Strambi. Neither is joint
polynomial. No full Faltings/coordinate-height or point-count claim follows yet.

Established geometric claim: fix r>=3. For EVERY finite holomorphic map
pi:Y->P1(C) of degree d, with Y compact connected genus>=1 and branch locus
contained in a set B of r distinct points, put delta=min pairwise chordal
separation and L=1+log(1/delta). There is a Merkl atlas for the CANONICAL
probability Arakelov measure with r1=3/4, chart count N<=C_r*d*(d+L),
c1<=C*d², and log M<=C*d. Consequently Theorem3.1.2 gives
sup gr_Y <= C_r*d³*(d+L). All constants uniform in the cover and branch positions.
No irreducibility, monodromy, real coordinates or supplied analytic charts
beyond the finite cover hypothesis are additional advice. This is a geometric
bound; implementing chart coordinates is not itself a claimed BIT algorithm.

## Proposed construction and exact risks

Use unitary Möbius coordinates on the sphere so local derivative ratios on
small spherical caps are universally controlled. For each branch point b,
choose a disjoint base disk |phi_b|<2h with h comparable to delta/100. A cover
component above that disk has a root coordinate w with phi_b(pi(w))=h*w^e,
1<=e<=d. Take the branch chart |w|<1; it extends to |w|<2^(1/e).
Its inner |w|<r1 contains all points over |phi_b|<h*r1^d.
There are at most r*d branch charts.

Cover the remaining base sphere by Whitney disks centered outside these tiny
inner holes, of radius a fixed small multiple of distance to B, capped by a
fixed spherical radius. Choose a maximal variable-radius net whose r1-inner
disks cover the complement. Their doubled disks avoid B. A dyadic packing
count gives at most C_r*(L+d) disks: at each distance scale the relevant area
is O_r(scale²), so only O_r(1) disks; the smallest required scale is comparable
to h*r1^d. Every disk lifts to d disjoint unramified charts. The lift extends
to a coordinate disk of radius at least3/2. Hence N<=C_r*d*(d+L).
CHECK the packing and coverage uniformly for clusters and hole boundaries;
no assertion based only on a picture is accepted.

Canonical density: write each globally L2-orthonormal holomorphic differential
in any enlarged chart. Mean-value bounds on a disk of radius R-1 around a
point of the unit chart give |f_nu|²<=C/(R-1)². Summing g such bounds and
normalizing the canonical measure by g cancels g. Unramified charts give
constant c1. Branch charts have R-1=2^(1/e)-1>=c/e, so c1<=C*d² on the
ENTIRE unit disk, not only its smaller inner disk. The larger branch disk is
essential; ordinary Bergman bounds on only the unit disk blow up at its boundary.

Transitions: overlapping unramified Whitney disks have comparable radii and
bounded unitary-Möbius factors, so derivatives and reciprocals are bounded.
Distinct branch disks/preimages do not overlap. On a branch/Whitney overlap,
the base Whitney radius is comparable to |phi_b|=h|w|^e. Thus derivative of
the normalized base coordinate with respect to w is comparable to e/|w|,
and its inverse to |w|/e. All Whitney centers lie outside |phi_b|<h*r1^d;
their small relative radius gives |w|>=c*r1^(d/e)>=c*r1^d throughout an
overlap. Hence M<=C*d*r1^(-d), and logM<=C*d. M itself need not be polynomial:
Merkl charges logM. CHECK transitions on ALL overlaps, not just inner overlaps.

These give precisely the four hypotheses of the actual Merkl definition,
with fixed r1>1/2. If any extension, density, overlap or counting assertion
fails, exhibit the offending finite cover/degeneration and correct the bound.
No finite numerical scan can establish this uniform claim.

## Arithmetic use stays separate

For algebraic B with bounded total Galois orbit, averaged log chordal collision
is bounded by C_r*(1+h_B) via projective height/product-formula inequalities.
Thus the proposed analytic bound would avoid exponential h_B in this Green
quantity. It does NOT alone prove stable Faltings height, finite-place
intersection estimates, bounded supplied-coordinate divisor heights, or
uniform CRT reconstruction. The known twist family y²=a*x(x-1)(x-2) still
forces charging model height. A separate source-proof audit identifies exactly
which steps of the source can use this bound and what remains. No quantum
algorithm, speedup, novelty or full classical matching is asserted.

## Final geometric disposition

The independent proof uses angular a(s)=min(1/4,dist(s,B)), radii a(s)/100,
centers outside holes theta0=(delta/100)*(3/4)^d and separation at least
min(rho_s,rho_t)/4. Balls of radius rho_s/16 are disjoint. Each distance
layer lies in r caps of proportional area; hence O_r(1) centers per layer
and O(L+d) layers. Inner coverage follows from maximality, including hole
boundaries. On a branch/Whitney overlap the center distance t<3h makes the
branch uniquely nearest; h|w|^e>=(49/100)h(3/4)^d. Both full-overlap
derivatives are bounded by M=500d(4/3)^d, while the enlarged embedded
disks give full-unit density c1<=d². This establishes all actual Merkl
hypotheses without delicate decimal constants or spectral assumptions.

The primary theorem AND appendix were checked. Its local two-sided
regularization bound is also available in these coordinates; globally only
sup gr is bounded, since gr diverges at the diagonal. The fixed-radius
asymptotic follows from the appendix before its final numerical optimization.

Completed Fable proof estimateUSD2.168550 is substantively correct; replace
its compressed nearest-branch step by the direct distance proof above. Its
reference to the separate false surface Theorem4.1 as part of this source
is rejected as a source mix-up. Opus transfer estimateUSD0.787048 is
TRUNCATED/PARTIAL, not a completed arithmetic proof. It correctly warns
that sup gr alone is insufficient; its Faltings headline is unproved here.
Six closure obligations include a new, fully sourced general-branch
arithmetic proof task. No whole surface algorithm or coordinate-height
claim follows from this geometric lemma.

## Global lower bound away from equal base images

Parent deduction independently checked: for pi(b)!=pi(x), including infinity,

    gr_Y(b,x) >= log dist_ch(pi(b),pi(x))-log(C*d)-C_r*d³*(d+L).

Apply actual Merkl on the SAME atlas with inner radius7/8; coverage and the
other hypotheses persist, with the same asymptotic local bound. Choose b
in a3/4-inner chart. Its centered circle of coordinate radius1/8 lies strictly
in the7/8-inner disk, where gr>=-log8-Lambda'. Outside that disk the source
Green function is superharmonic, so the boundary minimum principle gives
the same lower bound. Inside, the coordinate straight segment remains in
the unit disk; the spherical derivative of pi is <=C*d on branch charts
and <=C on Whitney charts. Thus coordinate distance >=dist_ch(pi b,pi x)/(Cd),
and the local regularization bound proves the claim. No global bound on
absolute gr near the diagonal, or arithmetic model conclusion, is inferred.

Uniform stable Faltings transfer is now established separately in
SURFACE_UNIFORM_ARITHMETIC_HEIGHT.md and its source-checked review. It uses
the FULL atlas rather than sup gr alone; torsion coordinate heights remain open.
