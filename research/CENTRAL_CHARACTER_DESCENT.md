# Complete Mixed Central-Character Descent

2026-10-22. **Written channel theorem plus partial Lean formalization and
bounded matrix controls. Not a new algorithm admission, independent proof
review, SDE implementation, or speedup claim.**

This resolves the next local interface in JET_ORACLE_HOMOGENIZATION.md:
an ordinary coset source for the homogenized group can be converted to
the required quotient coset source on EVERY ideal measurement branch.
It does not complete arbitrary-H recovery or establish novelty.

## 1. Exact Input Contract

Let G be a finite, explicitly encoded group; H an unknown subgroup; and
Z a PUBLIC central subgroup identified with F_p^r. Assume H intersect Z=1.
Require efficient public group multiplication/inversion, a public quotient
transversal, and uniform state preparation in that transversal. The source
is the ordinary mixed coset state, on a full G register:

```
R_g |x> = |x g^-1>,       R_g R_h = R_(g h),
rho_H[x,y] = 1/|G| [x^-1 y in H],
rho_H = (1/|G|) sum_(h in H) R_h.
```

For each s in F_p^*, require a PUBLIC efficiently controlled automorphism
Delta_s with Delta_s(H)=H and Delta_s(z)=s^d z on Z, for a fixed positive d.
An abstract grading does NOT imply preservation of an arbitrary H. The
jet graph construction proves preservation for its specific hidden group.
H, its generators, and its potential are never receiver inputs.

Receive M fresh conditional tensor copies of rho_H. A public diagonal-
equation routine, on ANY labels lambda_1,...,lambda_M in F_p^r, supplies
a nonzero vector s satisfying sum_i s_i^d lambda_i=0. This is a separately
charged algorithmic premise, not a brute-force field scan. Zero entries
are permitted, but the vector must not be identically zero.

## 2. The Full Measurement Instrument

Write chi_lambda(z)=exp(2 pi i <lambda,z>/p). Define

```
Pi_lambda = (1/|Z|) sum_(z in Z) chi_lambda(-z) R_z.
```

Finite character orthogonality gives Pi_lambda^*=Pi_lambda,
Pi_lambda Pi_mu=[lambda=mu]Pi_lambda, and sum_lambda Pi_lambda=I.
Since Z is central, every Pi_lambda commutes with rho_H. These facts
prove the COMPLETENESS of the instrument, not just a branch formula.

In a public right-central chart x=t(q)z, negative central Fourier,
copy/measurement of its computational label, then inverse Fourier on the
source implements Pi_lambda. The full projected source register remains
available. Alternatively, compress it but carry the exact induced twisted
action. Plain multiplication in G/Z on the compressed source is WRONG.

Regular traces satisfy Tr(R_g)=|G|[g=1]. Therefore

```
Pr(lambda) = Tr(Pi_lambda rho_H) = 1/|Z|,
rho_lambda = |Z| Pi_lambda rho_H Pi_lambda
           = (1/|G|) sum_(h in H,z in Z) chi_lambda(-z) R_(h z).
```

All labels, including zero, are retained. No inverse of a source-preparation
unitary and no postselection on a rare label is used. If K=H intersect Z
is nontrivial, the actual probability is |K|/|Z| for characters trivial
on K, and zero otherwise. Uniform labels cannot be assumed in that case.
The jet descent has the stronger transverse promise at each removed grade.

The regular trace now gives the complete normalized correlation:

```
Tr(rho_lambda R_g) = chi_lambda(z)  if g=h z in HZ,
                    0              if g not in HZ.
```

The central z in such a decomposition is unique by transversality. This
is derived from rho_H, not stipulated as a hypothetical source family.
The input matrix remains positive because it is a normalized projector
branch. A formal sum with the same diagonal alone would not prove that.

## 3. The Controlled Channel, Including All Scales

Given the observed labels and a validated SDE witness, set I={i:s_i!=0}.
Discard zero-scale inputs without reuse. Prepare a fresh uniform register
over Q=G/Z with public representative t(q). Controlled on q, apply

```
U_q = tensor_(i in I) R_(Delta_si(t(q)))
```

to the active projected targets, and trace all targets out. This is a
complete channel on arbitrary targets: controlled permutations, a fresh
uniform control, and partial trace. It is not a filter on an assumed kernel.
For one target its literal Kraus entries are

```
K_a[q,x] = |Q|^(-1/2) [x=a Delta_s(t(q))].
```

They satisfy sum_(a,q) conj(K_a[q,x]) K_a[q,y]=[x=y]. The two target sums
give output[q,r]=Tr(rho U_r^* U_q)/|Q|. On independent tensor sources this
becomes the product of the correlations above at
Delta_si(t(r)^-1 t(q)).

If g=t(r)^-1 t(q) is outside HZ, EVERY active factor vanishes: the
automorphism preserves HZ in both directions. At least one active factor
is necessary. If g=h z is in HZ, the product is

```
prod_(i in I) chi_lambda_i(s_i^d z)
  = exp(2 pi i <sum_i s_i^d lambda_i,z>/p) = 1.
```

Consequently the output is exactly

```
rho_out[q,r] = 1/|Q| [t(q)^-1 t(r) in HZ]
             = rho_(G/Z,HZ/Z)[q,r].
```

This conclusion holds for EACH label tuple and EACH valid nonzero SDE
witness, regardless of its active size. An all-zero witness instead
produces the pure uniform control state, erasing the support information.
Changing representatives only changes g by a central element; the cancelled
character makes the final output independent of that public choice.

## 4. Fresh Recursive Composition And Error Accounting

In the homogenized K=J semidirect V, remove the top remaining grade
Z_d, for d=c,...,2. It is central, is contained in the image of J, and
is scaled by s^d. Since H_F intersects J trivially, its image stays
transverse after quotienting any subgroup of J. Dilation preservation
also passes to the quotient. The same theorem therefore applies again.
The final group is grade-one abelian of dimension m+r_1. Fourier recovery
there determines the subgroup image, whose projection to V is U. It does
NOT by itself recover the original subgroup generators or undo lost grades.

For an exact preparation tree, use disjoint fresh sources at every child.
Inductively, conditioned on all measured classical records, each completed
child has the same quotient density. Independent child preparations then
give the required conditional tensor product. The parent output is again
independent of its complete classical transcript. Discarded quantum
environments are never reused. The fixed hiding oracle is a function
unitary, not an unmodelled memory-bearing source.

Correct one-copy marginals and correct branch probabilities are NOT enough.
The new test constructs two sources with independent, exactly uniform
central labels and correct maximally mixed marginals, but an entangled
quotient pair. The parent gives a pure uniform quotient instead of the
required maximally mixed quotient, at trace distance 2/3. This falsifies
both weaker freshness arguments without changing their observed label law.

For approximate gates, keep the entire classical record and an explicit
abort outcome. Bound each COMPLETE adaptive instrument in diamond distance
(using the corresponding half-norm convention), not its normalized rare
branches. For conditional product children with errors e_i and local
instrument error eta, contractivity and a tensor hybrid give
e_parent <= sum_i e_i + eta. A probabilistic SDE implementation needs a
worst-case runtime cap and charged abort probability; always verify the
returned witness. Abort is not silently renormalized away.

If stage arities in execution order are b_1,...,b_k, one final sample
uses L=prod_j b_j original lifted sources. Stage j executes
N_j=prod_(t>j) b_t times. Thus

```
e_final <= L e_leaf + sum_j N_j eta_j.
```

Counts include consumed zero-scale inputs and failed capped solver calls.
For T final abelian samples, multiply these counts by T, and add their
decoding/rank failure bound. Gate precision must scale with the ENTIRE
tree, not merely its depth. For fixed c the tree size is polynomial in
input dimensions and log p under the published SDE contract; its degree
and constants are very large. No polynomial claim for growing c follows.
An actual elementary-gate count and all arbitrary-H recursion remain open.

## 5. What Is Checked, And What Is Not

`Formal/CentralCharacterDescent.lean` proves: the one-sided projected
matrix from the original coset matrix; normalized correlation and label
trace under transversality; literal controlled-action Kraus completeness
and output; independent tensor contraction; and the final quotient kernel
under EXPLICIT support-preservation and phase-cancellation premises.
The two-sided projector equality/completeness argument in Section 2,
concrete jet instantiation, character cancellation and trace-distance
composition are written proofs here, not claimed as fully formal Lean.

`theorems/central_character_descent.py` is a bounded falsifier harness.
Its exhaustive scale search is capped and is NOT an SDE backend. Twelve
tests check complete central projectors, restored Fourier implementation,
all 27 and 125 label tuples at p=3,5, a literal joint target trace,
zero scales, nontransversality, nonpreserved support, wrong compressed
action, shared-source corruption, and exact tree/error arithmetic.
Matrix comparisons use tolerances; they are not symbolic universal proofs.
The standalone `--write` workflow records both positive controls and the
nonpreserved-subgroup falsifier in a reduction artifact, not candidate admission.

## 6. Prior Art And Next Attempt To Falsify The Route

[Imran and Ivanyos, Section 4](https://arxiv.org/pdf/2304.08376) already
develop central-character subgroup-state conversion and recursive quotient
descent. This pass does NOT claim that mechanism as new. Here the
additional contract is an H-preserving public dilation that changes
central labels by s^d, permitting diagonal-equation cancellation in place
of a zero-sum subsequence. The known
[fixed-degree diagonal-equation algorithm](https://arxiv.org/pdf/1503.09016)
supplies the conditional solver premise, not new implementation evidence.

A fresh scope search also found
[Morales, arXiv2608.05321v2](https://arxiv.org/abs/2608.05321), whose
abstract treats scalar-action semidirect products under parameter bounds
and quasi-Hamiltonian groups under structured input. This is a further
comparison lead, not an exhaustive novelty verdict; its full proofs have
not been audited in this pass.

The likely failure points are now outside this local contraction: an
incorrect degree bound or hiding relation in homogenization; arbitrary-H
normalizer/quotient recursion that gives the wrong oracle; uncharged
coherent arithmetic; prior art subsuming the whole construction; or no
meaningful application surviving classical algorithms. The enormous
sufficient resource bound is also a practical limitation, not evidence
of advantage. Do not spend the next pass collecting more small examples.

NEXT: independently audit the arbitrary-H recursion, including quotient
representative cleanup, source access, termination and total resources.
An additional concurrently present finite recursion verifier is
`jet_tuple_oracle_central_descent_audit.py`; its callbacks must be checked
for hidden advice and must not be confused with an implemented receiver.

## Verification

167 connected Python tests pass (67.07s), including the 12 new controls
and the concurrent Milestone23 tests. RuntimeWarning was fatal. The full
cached `lake build --wfail` passes 3471 jobs with all five new axiom guards.
Python syntax, formal generated-value crosscheck, `qsearch.py validate`,
site JavaScript syntax/site checks and the live artifact workflow pass.
The full repository Python suite was not run. No central admission,
CLI/UI changes or Git commit/push was performed.
