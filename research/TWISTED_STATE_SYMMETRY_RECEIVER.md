# Character-Twisted State Symmetry Receiver

2026-10-22: REES_PROJECTIVE_STATE_SOURCE.md replaces the preferred
composition for explicit exponent-p FIXED c<p and LINEAR action. A public
zero-moment design over the positive Rees cover erases the unknown
character before central descent, with a prime-independent copy bound.
It removes this note's character-normalizer recursion and derived-class
restriction from the NEW WRITTEN ROUTE. Neither receiver is implemented
or independently verified. Preserve the distinctions and falsifiers below;
no generic projective-action or mixed-conjugation extension follows.

2026-10-21. CONSTRUCTIVE EXTENSION, UNDER REVIEW. The source identities,
public character-normalizer algebra and phase compiler have executable
controls. The complete recursive quantum algorithm is NOT implemented or
independently proved. No novelty, classical separation, practical speedup,
central-registry admission or Shor-level result is asserted.

## 1. Why This Is Worth Testing

The Bose-only source transfer in STATE_SYMMETRY_COSET_TRANSFER.md requires
R(h)rho=rho. Physical ray symmetries instead allow R(h)rho=chi(h)rho.
Tensor amplification does not remove chi, and unknown copies do not grant
conjugate copies. The newer full-jet receiver has a useful distinction:
its rank guarantee is independent of the central Fourier labels. It can
therefore potentially consume the AFFINE sectors of a character-twisted
source and erase the extra unknown linear phase.

The proposed contribution is a source-faithful extension of the repository's
nonabelian receiver, not a new abelian stabilizer learner. The core problem
is to learn nonnormal ray stabilizers of supplied states without a classical
hiding oracle or a conjugation resource. It remains an abstract quantum-input
problem until a useful state family and access-matched baseline are supplied.

## 2. Input And Boundaries

Public exponent-p Lazard group G=exp(L), fixed class c, class(L')<=3,
unique public Lie coordinates, and p>max(c,3(c-2),3). The conservative
large-prime condition is inherited from the current nonabelian compiler,
not a claimed necessary threshold. An efficient controlled LINEAR
representation R(g) acts on a supplied quantum workspace. Fresh IID
copies of density operator rho are available with charged acquisition cost.

Promise, with a supplied and charged inverse gap 1/gamma:

```
H = {g : |Tr(rho R(g))|=1},
R(h)rho = chi(h)rho                    for h in H,
|Tr(rho R(g))| <= 1-gamma               for g outside H.
```

Unit-modulus expectation forces a unitary to be scalar on the support of
rho; therefore H is a subgroup and chi is a character. In this exponent-p
setting chi(exp(v))=omega^ell(v), with ell linear on log H and zero on
[log H,log H]. This is scalar LEFT-action symmetry. It is not general
mixed-state conjugation symmetry R(g)rho R(g)^dag=rho. For pure states
it is the usual ray stabilizer. Arbitrary projective representations need
a separately supplied, costed linear central extension meeting our group
conditions; no such extension is automatic here.

No state-preparation inverse, purification, conjugate copies, Fourier-label
postselection, supplied hidden projection or hidden polynomial evaluator
is assumed. Controlled group action is a real quantum-access requirement,
not an uncharged classical evaluator. Correlated copies and merely local
overlap gaps do not meet the promise.

## 3. Actual Twisted Sources And Error

For public address map r:D->G, prepare uniform D, apply R(r(a)) to k fresh
copies controlled by address a, and discard those copies. Exactly:

```
sigma_k[a,b] = Tr(rho R(r(b))^dag R(r(a)))^k / |D|.
tau_k[a,b] = [r(a)^(-1)r(b) in H]
             * conjugate(chi(r(a)^(-1)r(b)))^k / |D|.
```

Tau is positive and normalized: on each coset fiber choose a representative
g and write r(a)=g h_a; its block is the rank-one Gram matrix
chi(h_a)^k conjugate(chi(h_b))^k/|D|. Representatives are proof witnesses,
never constructed. On all off-fiber entries the error modulus is at most
(1-gamma)^k/|D|. Consequently

```
TD(sigma_k,tau_k) <= sqrt(|D|)*(1-gamma)^k/2.
```

The existing exact arithmetic planner plan_orbit_state_transfer may bound
this error with projective_pair=False, BUT ONLY by this new twisted-source
lemma. That flag does not convert an arbitrary projective source to an
ordinary coset state. Its conservative schedule gives

```
k = O((log |G| + log B + log(1/delta))/gamma),
total fresh copies and controlled actions <= B*k,
```

where B caps every source packet, including discarded/rejected batches,
all restrictions, quotients and recursive calls. Sequential hybrids use
the entire classical-quantum instrument, including ABORT. Do not divide
the source error by a small Fourier-sector probability. The comparison
works on any public map even on a bad adaptive history; algorithmic
correctness on such histories is not assumed.

Forcing chi^k=1 with k=p is NOT allowed as an efficient phase-removal
argument. Conversely an accidentally zero k mod p is harmless to this
source; the original character must still be learned from ORIGINAL copies.

## 4. Learn The Character Of A Known Subgroup

If K<=H has been correctly learned, choose its public Lie basis v_j.
Prepare uniform t in F_p, apply R(exp(t v_j)) to one original fresh copy,
and Fourier-transform t. Since every occupied state has eigenvalue
omega^(t ell(v_j)), this returns ell(v_j) with probability one in the
ideal Fourier model. Approximate Fourier and controlled-action errors
must be charged. This is one source copy and one full controlled-action
call per basis vector; generator-only access instead needs a separately
costed power construction. Polynomial log-p Fourier precision suffices.

The values must vanish on [K,K]; that is a public consistency check, NOT
certification that K was correctly learned. First-error accounting applies
when an earlier subgroup estimate was wrong. Learning only chi^k loses
information when k=0 mod p. Filtering individually zero-phase generators
is also wrong: compute the linear character kernel.

## 5. The Correct Normalizer

Write K0=ker chi_K in Lie coordinates and define

```
M_chi = {x in L : [x,K] subset K0}.
```

This is the normalizer of K preserving its character. The group/Lie
equivalence follows from exp(ad x) and its logarithm: a character-preserving
normalizer fixes ell under exp(ad x); since log is a polynomial in
exp(ad x)-I for nilpotency class <p, it also kills ell ad x. Conversely,
[x,K]<=K0 implies all higher iterates remain in K0. Jacobi shows M_chi
is a Lie subalgebra and K0 an ideal in it. Also K<=M_chi because chi
kills [K,K]. All these spaces are computed by public linear equations.

If K=H intersect N for N normal, H<=M_chi: conjugation by H preserves
both K and its restricted character. On the M_chi orbit span of supp rho,
K0 acts identically. Thus R factors through

```
S=M_chi/K0,       Z_new=K/K0.
```

Z_new is central, dimension zero or one; when nonzero its induced character
is faithful. Public sections in the original group implement quotient
actions. They need form a representation only on the preserved occupied
orbit span, not on unused ambient Hilbert space. The original gap descends:
every representative outside the quotient stabilizer was outside H.

**Negative control.** In the Heisenberg algebra [x,y]=z, K=<y,z> is an
ideal. Let ell(y)=a, ell(z)=1. The ordinary normalizer is all L, but
M_chi=K and K0=<y-a*z>. Conjugation by exp(x) changes the character.
Quotienting by K0 inside the ordinary normalizer is invalid. The new module
checks this at small and 127-bit primes and rejects noncharacters.

## 6. Relative Recursion With A Known Scalar Center

Maintain (G,Z), where Z is central, known, dimension zero or one, contained
in H, and has a known faithful character if nonzero. Initially Z=1.
Let Q=G/Z and measure progress by the nilpotency class r of Q, not only
by that of G. Each underlying group is a subquotient of the original G;
its class and derived-class bounds are inherited. Source maps and actions
compose through public sections into the original representation.

If Q=1, return H=G. If Q is abelian, use the relative scalar primitive
below. Otherwise:

1. Set N=G' Z. Recursively learn K=H intersect N on (N,Z), whose relative
   quotient is Q'. It has class at most floor(r/2), and the underlying N
   has class at most three. This is a strictly smaller recursive call.
2. Learn chi_K with original copies. Form S=M_chi/K0 and Z_new=K/K0.
   In S the new H obeys H intersect (S' Z_new)=Z_new. Indeed M_chi'<=G',
   and any lift in H of S' Z_new lies in H intersect G'K=K.
3. Use the twisted image primitive to learn U, the image of H in
   S/(S' Z_new). Restrict S to the inverse image T=H(S' Z_new) of U.
4. Repeat image/restriction until the relative quotient T/Z_new is abelian;
   use the scalar base, then lift and adjoin K0. No fresh intersection
   learner is needed inside this loop.

For the class drop, pass to Q=S/Z_new. The target H/Z_new intersects Q'
trivially, so it is abelian. For the inverse-image subgroup T_bar=H_bar Q',
[T_bar,T_bar] lies in gamma_3(Q): both [H_bar,Q'] and [Q',Q'] do, the
latter even lying in gamma_4(Q). Hence gamma_r(T_bar)<=gamma_(r+1)(Q)=1.
Transversality persists under restriction. This is the same class-drop
argument as the ordinary receiver, now applied to the RELATIVE quotient.

For r=1, G is a central extension of an abelian group by Z. Thus class G<=2
and H is abelian: [H,H]<=Z and chi_H kills [H,H], while chi_Z is faithful.
The scalar image primitive uses N=Z; it learns H/Z and lifts with Z.
Do NOT run ordinary abelian HSP on Q with an unexamined projective action.
Its source can have a quadratic phase from the central extension, plus
the unknown linear character. If Z=1 this reduces to the abelian case.

This proves the intended recursion's descent and conditional interfaces,
not correctness of an unimplemented image solver. Malformed answers must
be rejected or capped, and all group/chart costs and failure allocations
must be included in a complete implementation.

## 7. Twisted Image Source And Full-Jet Compatibility

At an image call N=G' Z and H intersect N=Z. H is abelian by faithfulness
of chi_Z and the commutator argument above (also when Z=1). Choose a
proof-only subgroup complement h:U->H to Z. Write chi(h(u))=omega^ell(u)
and extend ell linearly to V=G/N. Neither h nor ell is supplied.

The ordinary common-potential construction still applies to h(U), which
intersects N trivially. It gives g:V->N and the same degree bounds for
Q=log g. Adding central Z to G' does not alter the bounds: noncentral
coefficients modulo C=Z(N) have degree <=D=c-2 and central coefficients
degree <=c. C MUST be the full center of N, not an arbitrary central span.

Write z=dim C, t=dim Z. Negative central Fourier gives, for the IDEAL
k-copy twisted source,

```
lambda|Z = k*chi_Z,
Pr(lambda) = p^(t-z) on this affine set, zero elsewhere.
```

This follows by summing over the central right translations z0 in Z:
sum_z0 omega^(lambda(z0)-k chi_Z(z0)). The allowed set can be a singleton;
it need not contain zero. No nonzero-label filtering or inverse sector
probability is permitted. Actual approximate sources are compared as
whole instruments, not claimed to have exactly uniform allowed labels.

Using the class-three monomial gauge W'_lambda, the conditional source is

```
rho[(q,t0),(q',t1)] = p^-(m+r_A+s_B) [q'-q in U]
   * omega^(k ell(q)-k ell(q'))
   * (W'_lambda(g(q))^dag W'_lambda(g(q')))[t0,t1].
```

The carrier dimension and normalized kernel are otherwise unchanged.
For the class-three case, B-Fourier frequency mu remains QUANTUM. Full
Taylor-jet alignment uses the identity block of each displacement map,
so its feature-rank bound holds for any labels, including affine/fixed
ones. All labels and spectator outcomes are retained.

After the independent shears q_i=Y_i+s_i*q and the verified public GL
alignment, the scalar phase is

```
P_twisted(q,t0) = P_ordinary(q,t0) + sum_i k_i*ell(Y_i+s_i*q).
```

The compiler wrapper appends m UNKNOWN linear coefficients to the common
parameter schema. It does not evaluate ell. The extra term has weight one,
so e=max(c,3D) and the quadratic parameter lift still suffice; the fixed
schema is kept even when every k_i=0 mod p. Weighted erasure e,...,1 then
jet Fourier and ordinary erasure D,...,1 are unchanged. The residual jet
polynomial uses no new character coefficients.

For N abelian use the scalar phase branch with the same added linear
term. In the relative abelian base N=Z, the central section potential is
degree <=2 and the character phase degree <=1. No noncentral carrier or
full-jet compiler with a fictitious A register should be introduced.

## 8. Resources And What Is Still Missing

Let I(r) count image/scalar-image calls, including the relative abelian
finish, but not character-learning batches. Safe bounds are

```
I(0)=0, I(1)=1,
I(r) <= I(min(3,floor(r/2))) + r,        r>=2.
```

Thus I(2)<=3, I(3)<=4 and I(c)<=c+4 for c>=4. There are at most two
nonabelian recursion nodes, hence at most two known-K character-learning
batches, each using at most dim L original copies. Optionally recovering
the final Bose kernel requires one more character-learning batch on H.
These bounds concern a correct history; public caps must control bad ones.
They do not cap the much larger erasure trees inside each image call.

If B is a bound on the sum of those complete image-source budgets, the
new copy cost is B*k+O(dim L), not p copies per packet. Quantum gates,
memory, generic diagonal-equation/SDE solvers, action precision and the
overlap gap remain charged. The existing SDE polynomial bounds have large
degree-dependent exponents and do not imply a usable implementation.

Unresolved: independent validation of the full monomial/source/erasure
proof; complete bounded controller and uniform-source implementation;
generic efficient SDE backend; formal proofs of the new Fourier and
character-normalizer interface; exhaustive access-matched novelty review;
and, most importantly, a natural state family outside existing classical
reconstruction/tomography and known quantum symmetry-learning algorithms.

## 9. Literature, Baselines, And Falsifiers

[Holt--Subramanian, Learning quantum symmetries, Sections 8--9](https://arxiv.org/html/2609.38085v2)
already studies phase symmetries and projective actions, including abelian
linearizations and stabilizer learning. Compare exact group and access
conditions; this proposal is not a claim that phase symmetries are new.
The phase-graph strict-gap trap is documented in our prior transfer note;
the present construction keeps the character instead of invoking that
gap assertion. This is a local dependency audit, not a rejection of all
results in that paper.

[Liu--Carrasco--Eisert--Bellante, The power of oracle access](https://arxiv.org/abs/2609.35656)
distinguishes sample and preparation-unitary/inverse models for abelian
StateHSP. We use original copies plus controlled group action, not their
stronger preparation-query access. No improved inverse-gap dependence or
new abelian sample-complexity claim is made here.

Strongest immediate classical filters: an explicit polynomial-size state
vector/density matrix must be tested against tomography and direct linear
algebra, although efficient stabilizer recovery is not automatic for an
arbitrary group encoding. A stabilizer/tableau description supplies
structure absent in opaque-copy access; low-degree
succinct object actions may be classically reconstructible, as previous
repository audits show. A general classical algorithm on quantum copies
must specify allowed measurements. Comparing this algorithm to a classical
routine denied its supplied object or group action is not a separation.

Decisive falsifiers and limits:

- If the actual source has non-character phases or correlated copies,
  Sections 3--4 fail. Mixed conjugation symmetry is outside the contract.
- If M_chi cannot be computed under the real group encoding, the supplied
  Lie-coordinate model has not been implemented, not solved generically.
- If a source section does not preserve the occupied quotient orbit span,
  the representation/gap inheritance must be withdrawn.
- If full-jet erasure needs uniform free Fourier labels, this extension
  fails. Fixed-label algebra controls are included precisely to test this.
- If the extra character survives either erasure or requires exponential
  samples, no efficient receiver follows from finite source identities.
- If existing algorithms solve the same nonnormal/growing-prime problem
  with the same access, the novelty claim disappears even if our proof works.
- If every succinct state application is classically reconstructible, this
  remains an abstract structural result, not a path to a major useful speedup.

The next research decision is to validate this as one algorithm and seek
an access-matched application, not to generate another small oracle family.

Application follow-up: LOGICAL_GATE_STATE_HSP_APPLICATION.md gives a
conditional encoder-to-logical-relation reduction and rejects an automatic
code-distance/transversality gap claim. Exact symmetry learning can hide
a marked logical word; even an error-correcting subcode can retain the
exponentially small Choi gap. Require a separately proved population gap.

## 10. Implemented Versus Proposed

theorems/twisted_state_source.py implements public character normalizers,
affine central-character constraints and the symbolic linear-phase wrapper.
It does not infer hidden subgroups or characters from state data.
tests/test_twisted_state_source.py checks actual mixed-copy Gram kernels,
positive twisted states, a sparse regular state with the asserted character,
direct transformed class-three regular-kernel entries and normalization,
fixed-label coefficient compilation, 127-bit arithmetic and bad shortcuts.
These are structural falsifiers, not algorithm-performance benchmarks.
An independent Heisenberg/Schrodinger action on a chirp state checks the
relative abelian base: naive quotient Fourier sampling puts 1-1/p mass
outside the true annihilator. Its quadratic section phase is therefore
essential. Original-copy character Fourier readout is checked separately.

No new production command, UI, registry candidate, quantum backend or Lean
theorem was added. The existing generic source budget is reused only at
the level of its proved arithmetic bound.
