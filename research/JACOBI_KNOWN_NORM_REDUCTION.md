# Known Relative Norm Removes The Prime-Conductor Quantum Opening

2026-10-17. Published classical theorem, local application REVIEW PENDING.
This supersedes the suggestion that growing-conductor LLL success is the
decisive unresolved question for this particular surface-counting proposal.
It does not assert that a Gentry-Szydlo implementation exists in the repo.

## Question And Decision

The [surface experiment](JACOBI_SURFACE_RECONSTRUCTION.md) proposed quantum
principal-ideal/unit recovery from public Jacobi carries. Generic principal
ideal problems can be hard. But this input also supplies the exact relative
norm, J*bar(J)=p^2. That additional information changes the computational
problem. Comparing only generic PIP or empirical LLL success misses the
appropriate classical competitor.

[Lenstra and Silverberg, Testing isomorphism of lattices over CM-orders,
1706.07373v3](https://arxiv.org/html/1706.07373), Theorem 1.3, gives a
deterministic classical polynomial-time decision AND recovery algorithm for
an ideal and prescribed relative norm in a CM-order, when the polarized
ideal identity holds. No GRH assumption is part of that theorem. Its
Algorithms 18.6/18.7 establish the recovery assertion, not merely a test of
the principal-ideal class. The factorization in Algorithm 18.1 is of a
constructed integer with bounded small prime factors, not a free generic
integer-factorization oracle.

**Decision:** for odd prime conductor and the stated public split-root
input, this published theorem plus the Jacobi identities and primary
congruence gives classical polynomial-time exact surface counting in
ell and log p. The proposed asymptotic quantum advantage is therefore not
a credible target under those premises. Do not continue this route by
searching for LLL failures or implementing known quantum PIP primitives.
This is a prior-art application, NOT a new classical algorithm claim.

## Direct Reduction To Theorem 1.3

Inputs: odd prime ell, prime p with ell|(p-1), explicit order-ell eta mod p,
and admissible nontrivial character exponents a,b,c with a+b+c nonzero mod ell.
Use A=Z[zeta_ell] and the POSITIVE embeddings zeta -> eta^t. All data are
explicit integers; no coherent oracle, true Jacobi value or field-sized
character table is an input.

1. A is a CM-order. In the basis 1,zeta,...,zeta^(ell-2), the multiplication
   table and conjugation matrix have polynomial size and integer entries.
2. Build I from the public split-prime powers P_t^e_t, with
   e_t=2-floor(((at mod ell)+(bt mod ell)+(ct mod ell))/ell).
   A basis follows from modular evaluation kernels at the lifted split roots.
3. Conjugation sends P_t to P_(-t). Since e_t+e_(-t)=2, we have
   I*bar(I)=product_t P_t^2=p^2*A. Set w=p^2, a totally positive scalar.
4. The Jacobi ideal identity gives I=(J); the Weil identity gives
   J*bar(J)=p^2. These establish the YES promise. IMPORTANT: the identity
   I*bar(I)=w*A by itself is NOT a proof that a normalized generator exists.
5. The published algorithm returns v with I=A*v and v*bar(v)=p^2.
   The ratio v/J is an algebraic unit with relative norm1. Every embedding
   has absolute value1; Kronecker's theorem makes it a root of unity.
6. For odd prime ell the root group is {+/-zeta^k}. The established primary
   condition J=1 mod(1-zeta)^2 identifies the correct one by testing
   A(1)=1, A'(1)=0 mod ell. This needs no quantum phase estimate.
7. Recover the at most (ell-1)^3 admissible sums, combine their explicit
   multiplicities and add p^2+p+1. No prime-square residue reconstruction or
   generic compact-output local division is needed on this classical route.

Each ideal contains p^2*A. Its canonical HNF basis has coefficient bit size
O(log p). The order has rank ell-1 and polynomial-size structure constants;
the whole theorem input has size polynomial in ell and log p. The output
also has polynomial size: writing J=sum_(j<ell-1) a_j*zeta^j, the known norm
implies ell*sum a_j^2-(sum a_j)^2=(ell-1)*p^2. The trace Gram's smallest
eigenvalue is1, so each |a_j|<=sqrt(ell-1)*p.

Thus enumeration of the character triples and root choices remains
polynomial in ell and log p. An explicit ell=poly(log p) promise suffices
for polynomial succinct-input time. Without it, neither the earlier quantum
proposal nor this reduction is claimed polynomial in log ell. This is a
complexity comparison, not an implementation/performance crossover claim.

## Independent Group-Ring Check

To avoid confusing the CM theorem with a generic-PIP solver, we also
construct an explicit input to the older Gentry-Szydlo setting.
[Lattices with Symmetry](https://arxiv.org/html/1501.00178), Remark 8.6,
explains the polynomial recovery of a generator from its ideal and cyclic
autocorrelation in R=Z[X]/(X^ell-1), ell odd prime.

Let J have canonical coefficients a_0,...,a_(ell-2), and pad a_(ell-1)=0.
Since sum a_j=1 mod ell and p=1 mod ell, the integer
c=(p-sum a_j)/ell exists. The lift v has coefficients a_j+c at all ell
positions. It projects to J and has augmentation v(1)=p.

The cyclic product v*bar(v)-p^2 vanishes in the cyclotomic quotient, so is
a multiple of Phi_ell in R. Its augmentation is0, hence that multiple is0.
Thus v has exactly known cyclic autocorrelation (p^2,0,...,0).

The public R-ideal imposes the SAME split-root carry constraints plus
augmentation divisible by p. Its index is p^(sum e_t+1)=p^ell. The principal
ideal (v) is contained in it and also has index
|v(1)*Norm_K(J)|=p^ell, proving equality. This proves the GS YES promise
without using v to construct the actual public basis.

For basis B, the normalized Gram B*B^T/p^2 is positive definite, integral
and unimodular. Cyclic shift has an explicit integral isometry matrix.
The cyclic order-2ell group is represented by -shift, whose ell-th power
is -I, matching the signed group-ring convention. Ordinary cyclotomic
trace Grams instead have determinant ell^(ell-2), NOT1; the two encodings
must not be silently interchanged. Group symmetry is supplied, not inferred
from an arbitrary unimodular lattice.

## Executed Evidence And Nonimplementation

Run:

```text
python theorems/jacobi_known_norm_reduction.py --write
python -m pytest -q tests/test_jacobi_known_norm_reduction.py tests/test_jacobi_surface_reconstruction.py
```

The producer builds both theorem inputs for six native controls and all51
distinct ideal profiles at p=2^61-1, ell11. It verifies exact product-ideal
HNF, normalized Gram positivity/determinants, module actions, signed cyclic
action, augmentation and index. The large inputs require no character
table, LLL, true Jacobi sum or phase estimate. The six small known-generator
lifts are separately charged CALIBRATIONS, not input constructors.
The reused reference source caps conductors at24 and primes below2^64;
these implementation caps are not assumptions of the symbolic reduction
or of the imported theorem, and exceeding them is not evidence of hardness.

Tests include an independent SymPy product-lattice HNF and matrix replay,
direct cyclic autocorrelations, all small admissible symmetric triples,
wrong norms, nonideal lattices with the right index, non-root unit
contamination and opposite-character conventions. A valid polarized input
is never labeled a solved instance just because those checks pass.

**Not executed:** the Lenstra-Silverberg auxiliary-ideal/tensor-power
generator-recovery algorithm. Existing actual surface reconstruction still
uses LLL plus exact primary normalization; its failure remains UNKNOWN for
that implementation. The asymptotic conclusion imports the published
classical theorem and depends on the stated local reduction proof, not on
finite success or a relabeling of LLL as GS. Local application has not had
independent human/formal review. No central candidate, proof or general
negative-result promotion is made automatically.

## Attempt To Falsify This Conclusion

- **Wrong theorem problem?** Theorem 1.3 requires the norm, not just the
  ideal. Here the norm is exactly the public scalar p^2. If the application
  supplied only an unknown positive unit times p^2, this reduction would
  fail. Native checks and the Jacobi Weil identity rule that out here.
- **Invalid ideal/involution?** Carry orientation matters. Every product
  ideal is checked exactly, and inverse-label inputs are retained as distinct
  valid inputs, not confused with the intended J. A carry or ideal-identity
  counterexample would invalidate the local application.
- **Norm identity implies existence?** It does not in general. This family
  has a concrete Jacobi witness analytically; arbitrary polarized ideals
  cannot inherit the YES conclusion. Native small witnesses independently
  check that premise but are not a proof for all inputs.
- **Uncharged number-theory oracle?** A verified eta is part of both input
  models; neither algorithm gets a hidden root for free. The imported
  theorem is unconditional deterministic polynomial time in its explicit
  input size, not a heuristic unit-group/PIP subroutine. Efficient public
  ideal construction and polynomial output size are shown above.
- **Root ambiguity still hard?** Prime-primary normalization removes it
  without evaluating J. This pass does NOT extend that step to all composite
  conductors. A counterexample to the prime-primary proof would reopen
  exact identification, not make generic normalized recovery quantum-hard.
- **Does this refute a recent quantum paper?** No. The repo's specific
  prime-conductor surface target is narrower than external claims and may
  have different output/input conventions. No author-error conclusion is
  inferred from a missing citation or this local reduction alone.

## Next Research Action

Retire this prime-conductor proposal as an asymptotic advantage target,
subject to independent review of the application. Keep its arithmetic
tests as reusable falsifiers. Do not spend main-model research budget
implementing a known GS algorithm solely to reproduce its theorem.

Before any broader arithmetic pivot, require a specific output NOT already
recoverable from a public ideal plus known relative norm. Otherwise compare
independent constructive mechanisms. Unknown norms or ambiguous composite
roots are not automatically hard tasks, and failure of LLL is not evidence
that a quantum algorithm is needed. A new candidate must have an explicit
end-to-end task and strongest known classical comparison first.
