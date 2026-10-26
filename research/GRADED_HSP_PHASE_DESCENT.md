# A Restricted Class-Three Central Conversion

2026-10-21. Constructive proposal with a written Gram identity and bounded
physical-state controls. Independent proof and novelty review pending.
No general nilpotent-HSP algorithm, new oracle separation, practical
application or Shor-level result is claimed.

## Why This Direction

The previous Hermite audit removed a credible time-only novelty claim.
Before choosing this pass, we compared three other routes:

- Original graph-coloring BPQM: the missing object is a finite-block
  whole-input receiver. More tree spectra would not supply it.
- Periodicity/rank-parameterized lattice BDD: the apparent opening in
  [Eldar--Hallgren](https://arxiv.org/abs/2201.13450) is met by the classical
  algorithm detailed in [Allen et al.](https://arxiv.org/abs/2203.05019).
  We did not implement another matched benchmark.
- Class-three central conversion: there is a precise missing operation,
  and public automorphisms might change its cost without inventing an
  amplitude oracle. This is the selected question.

[Imran--Ivanyos](https://arxiv.org/pdf/2304.08376), Section 4, already
construct quotient subgroup states using zero-sum central characters.
[Ivanyos--Sanselme--Santha](https://www.irif.fr/~santha/Papers/iss12.pdf),
Sections 4-5, already use automorphisms and simultaneous linear/quadratic
equations for nil-2 HSP. Our construction is a tightly specified
linear/cubic analogue, not a claim to have invented either technique.

## Problem And Promise

Let `p>3` be prime, `p=2 mod 3`, and

    G = UT_4(F_p)^r,     |G| = p^(6r).

The input is a standard quantum hiding-function oracle for a subgroup
`H=<exp(X)>` of order `p`, together with the public matrix-group encoding.
The logarithm has grades

    X = X_1 + X_3,       X_1 != 0.

Grade means distance above the diagonal, in each direct-product factor.
`X_3` is central and arbitrary. **The grade-two logarithmic component is
promised zero.** Matrix entries on the second superdiagonal generally
are not zero: exponentiation adds `X_1^2/2`.

The direct-product rank and prime both grow. This is not a constant-size
group table. But the promise is substantial, and no reduction from DCP,
lattice problems, graph isomorphism or another useful external task is
supplied. A standard HSP oracle is not a classical evaluator with hidden
implementation costs magically removed.

Our immediate target is to create subgroup states for `HZ/Z` in `G/Z`,
where `Z` is the top-grade center of dimension `r`. This removes the
class-three layer. It is a state-conversion problem, not a parameter fit.

## Public Moment Solver

Take `T=(r+1)^2` measured central labels `u_i in F_p^r`. Every batch is
allowed, including zero labels. The solver returns a nonzero vector `c`
with

    sum_i u_i*c_i = 0,
    sum_i u_i*c_i^3 = 0.                              (1)

Split the labels into `r+1` disjoint blocks of `r+1`. In each block,
find a nonzero linear dependence with coefficients `a_i`.
Cubing is bijective because `gcd(3,p-1)=1`; set
`b_i=a_i^(3^-1 mod (p-1))`. Then `sum u_i*b_i^3=0`.
Let `v_j=sum_(i in block j) u_i*b_i`. Find a nonzero linear dependence
`sum_j t_j*v_j=0`, and set `c_i=t_j*b_i` within that block.
Disjoint support makes the final vector nonzero. Scaling a block
preserves its cubic equation.

This is polynomial in `r,log p`, using field linear algebra and modular
exponentiation. It has no secret-dependent input, random-subset search
or large-field enumeration. Zero coefficients mean unused copies, not a
singular automorphism. All acquired copies are charged.

The disjoint-block idea also appears in the known nil-2 equation solver.
For other prime congruence classes, this specific cube-root construction
is not available; unsupported is not impossible.

## The Actual Quantum Interface

Write `R_g|x> = |x*g^-1>`. Start from independent ordinary coset states
`|a_i H>`. The representatives `a_i` are unknown and never used by the
receiver. Apply the central Fourier projector

    P_u = (1/|Z|) sum_(z in Z) omega^(-<u,z>) R_z.

Since `H cap Z` is trivial, every `u` has probability `1/|Z|`.
The normalized conditional state `|psi_i>` satisfies

    R_h |psi_i> = |psi_i>              for h in H,
    R_z |psi_i> = omega^(<u_i,z>) |psi_i>.

Its support is exactly `a_i HZ`. These are actual projected original
states, not ideal phases synthesized from unknown subgroup parameters.

The public graded dilation `delta_c` multiplies a grade-j matrix entry by
`c^j`. For `c!=0` it is a group automorphism. For the actual hidden
generator `h=exp(X_1+X_3)`,

    delta_c(h^t z)
      = h^(ct) * exp((c^3-c)*t*X_3) * delta_c(z).     (2)

Define the controlled output, for a public input group register `g`, as

    |F(g)> = tensor_(i:c_i!=0) R_(delta_ci(g)) |psi_i>.

No individual dilation must preserve H itself; equation (2) accounts
for the central discrepancy. Equation (1) cancels both that discrepancy
and the phase of every `z in Z`. Therefore

    <F(y)|F(x)> = 1[y^-1*x in HZ].                  (3)

For the zero case, note that `delta_c^-1(HZ)=HZ`, since the image of H
modulo Z is the homogeneous line generated by `X_1`. Thus outside HZ,
each active factor has disjoint support. Inside HZ, (1)-(2) give phase
exactly one, not just absolute overlap one.

Prepare a uniform register over an efficiently computable transversal
of `G/Z`, apply these controlled right actions, and discard the target
registers. Equation (3) makes the remaining density operator exactly the
ordinary subgroup-state mixture for `HZ/Z`. The zero-top-coordinate
transversal and all group operations are public polynomial-size circuits.
No list of cosets, support table, Gram inverse or subgroup generator
is needed by this physical recipe.

Although a particular measured label is unlikely, the algorithm accepts
every label batch. It does not pay or divide by the probability of a
preselected batch. Approximate QFT errors must be charged across the full
instrument; complete-channel trace-distance contractivity avoids an
artificial inverse-sector-probability penalty.

## Proposed End-To-End Completion Under The Promise

This is a written composition, NOT an executed full receiver:

1. Use (3) to obtain fresh subgroup states in `G/Z`, a class-two group.
2. Apply the established nil-2 automorphism/linear-quadratic construction
   to create states in its abelianization. Here the center has dimension
   `2r`, and the projected hidden subgroup remains a noncentral line.
3. Abelian Fourier sampling recovers `span(X_1)` in `F_p^(3r)`.
4. Choose a public nonzero representative `v` of that line. The group
   `K={exp(t*v+z): t in F_p, z in Z}` is explicitly abelian and contains H.
   Restrict the ORIGINAL hiding-function oracle to this known K and use
   abelian HSP to recover H, including its central displacement.

The final restriction is an oracle query on an explicitly encoded
subgroup, not postselection of a rare original coset. The supplied-state
conversion alone does not silently grant this extra oracle interface.

Using the published mixed quadratic solver gives `O(r^3)` first-quotient
copies per abelian sample, hence `O(r^5)` original coset copies per sample.
`O(r+log(1/eta))` samples suffice for the final subspace-learning error
budget eta. All operations have polynomial bit complexity. Fixed-degree
polynomial bounds are asymptotic, not practical gate-count estimates.
The nil-2 backend and final abelian receiver have not been compiled here.

## Decisive Negatives

**Only canceling cubes is insufficient.** It makes Z act trivially but
leaves a phase involving the unknown `X_3` on H. Its absolute overlap
can be one while the Gram entry is not one. Treating a ray as an identical
quantum hiding value would invalidate (3).

**Generic grade two defeats this construction.** If
`X=X_1+X_2+X_3` with `X_2!=0`, dilation changes the middle component by
`(c^2-c)X_2`. This displacement is noncentral. Scalar central-phase
equations cannot erase its orthogonal support change. The control below
produces the projector for Z alone, not HZ, so the quotient hides the
trivial subgroup. This is not a general HSP impossibility theorem.

### Why More Scalar Moments Do Not Repair This Product Construction

For nonzero `X_1` AND `X_2`, consider the supports after quotienting by Z.
The active factor with scale c has support governed by the line

    span(c^-1*X_1 + c^-2*X_2).

Two such lines agree only when their nonzero scales agree: compare their
grade-one components to fix the proportionality, then their grade-two
components. Distinct lines intersect only at zero. Consequently, two
unequal active scales already force the product-kernel support into Z.
Adding quadratic, quartic or any other scalar phase equation cannot
restore the lost support.

If every active scale equals a common c, the subgroup is only publicly
relabeled by `delta_c^-1`; this is NOT lost information and can be undone.
But central cancellation then requires `sum_(active i) u_i=0`.
Thus this direct-product/dilation ansatz, on a generic grade-two subgroup,
returns to the unweighted zero-sum-subsequence requirement even allowing
a common public relabeling. This statement is about this architecture,
not all central-state converters or all quantum algorithms.

An extra negative uses labels `(1,-1,2,-2)` and scales `(1,1,2,2)`.
Every scalar power moment vanishes, yet the kernel has support only Z.
A separate positive uses the first opposite-label pair and equal scales
`(2,2)`: it correctly produces the known rescaling of HZ. The latter
prevents an overbroad claim that every nonidentity dilation loses H.

**Knowing the promise is not learning it.** We do not test whether an
unknown subgroup satisfies it, learn a conjugator making it true, or
assume knowledge of the first-grade line while constructing (3).

## Executed Controls

The native bounded fixture uses `p=11,r=1`, ambient order `11^6`,
and `log h=(1,2,3,0,0,4)`. Four public labels `(1,2,3,4)` are used.
Unknown random coset representatives are used only by the fixture.
The implementation performs the public central projectors on original
coset states and obtains correlations from their complex amplitudes.
The active product kernel has all 121 entries of HZ and agrees with
its indicator numerically. The grade-two negative changes only the
fourth logarithmic coordinate to one.

Tests separately compare the kernel against direct controlled right
actions for EVERY element of `UT_4(F_5)`, verify independence from coset
representatives and complete Fourier branch probabilities, and check the
public moment solver up to prime `1,000,000,007` and label dimension eight.
Large-prime arithmetic is not a large quantum-state execution.
The two-factor `p=5` control uses ONE shared hidden subgroup parameter,
not independent hidden subgroups in the two factors; its target HZ has
125 elements. This checks the vector-center cancellation interface.

The sparse diagnostic enumerates up to `p^(r+1)` amplitudes and their
pairs. It is exponential in the succinct group input. The physical
construction is the separate circuit recipe above; do not advertise the
diagnostic runtime as its quantum cost.

## Assessment And Next Experiment

This is a constructive state-conversion component under a sharp promise.
Its ingredients are close to established nil-2 and quotient-state methods;
novelty is not established. Generic classical collision search is not
enough as a research baseline: before any advantage claim, test reductions
to known HSP/hidden-polynomial algorithms and identify a useful input task.

The substantive next target is the noncentral grade-two displacement.
Can a lawful collective representation operation preserve those
translations, rather than cancel only scalar phases? Alternatively, can
the promised case be reduced directly to known algorithms, removing even
the narrow novelty possibility? Neither question is answered by more
prime/rank fixtures, generic certificates, or simply setting another
moment to zero.

Reproduce:

    python -m theorems.graded_hsp_phase_descent --write
    python -m pytest -q tests/test_graded_hsp_phase_descent.py

Verification: 19 new tests and 289 connected tests pass with RuntimeWarnings
fatal. Python compilation, site JavaScript syntax, site checks and registry
validation pass. The full repository suite was not run. No existing
theorem producer, central claim, CLI/UI, commit or push was changed.
