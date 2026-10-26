# Non-Split Class-Three Receiver

**Status: local constructive derivation, independent proof and novelty
review pending.** There is now an end-to-end finite generator-recovery
control, not only a successful quotient-state example. There is still no
compiled quantum circuit, demonstrated computational problem reduction,
or established new published-theorem-level result.

Follow-up: `AFFINE_PHASE_MIXED_CHANNEL_AUDIT.md` gives the independent
mixed-state/all-outcome audit and an all-`p>3` WRITTEN schedule using
published general SDE solvers. The implemented controller and the
restricted-prime copy schedule below are unchanged.

`NIL3_NORMAL_WORD_BRIDGE.md` now supplies explicit public coordinate
conversion from refined polycyclic normal words and identifies the
unimplemented trivial/normal/transverse dispatch. That bridge does not
turn this diagnostic into an executed all-case or recursive HSP solver.

## Scientific Question

Does the collective affine-support construction depend on a split
semidirect product, or does it also work for a genuinely non-split
class-three extension?

The answer in the written derivation below is that splitting is
unnecessary when the group is supplied in an explicit adapted
class-three Lie/BCH presentation. The extension cocycle must be retained.
Ignoring it makes the final graph-state reduction wrong.

This is a significant increase in mathematical scope, not evidence of
Shor-level significance. The next priority is independent review of this
proof and prior-art overlap, not a larger numerical campaign.

## Input And Proposed Statement

Public input:

- A prime `p>3`, with the implemented controller restricted to `p=11 mod12`.
- A finite-dimensional Lie algebra `L` over `Fp` of class at most three,
  explicitly given by structure constants.
- A public vector-space decomposition `L=V direct-sum N`, where
  `N=[L,L]`, with `dim(V)=m`, `dim(N)=n>0`.
- Standard independently prepared coset states of a cyclic order-`p`
  subgroup `H=<exp(X)>` in the corresponding BCH group.

For the main case, `X` has nonzero image in `V`. The proposed receiver
uses a number of copies and gates polynomial in `m,n,log p` to recover a
generator of `H`. It requires neither an unknown coset representative
nor a coherent oracle restricted to an unknown subgroup.

This is an explicit-presentation statement. It does NOT automatically
supply a black-box-group-to-Lie-algebra algorithm, arbitrary-hidden-subgroup
reduction, or a solver for every nilpotent group. The supplied-state model
also must not be replaced with classical basis samples.

An adapted basis can be obtained from explicit structure constants by
ordinary linear algebra. The implementation validates antisymmetry by its
storage convention, Jacobi, the derived subspace, `[N,N]=0`, and vanishing
fourfold nested brackets. It does not assume an unverified tensor is a
class-three Lie algebra.

## Exact Coordinates

Use `exp(n) exp(q)` as the group chart, for `q in V`, `n in N`. Since
`[N,N]=0` and `[L,[L,N]]=0`, conjugation on `N` is

```
Phi(q)n = n+[q,n].
```

In particular, `Phi(q+r)=Phi(q)Phi(r)` although the chosen section
`q -> exp(q)` is generally NOT a group homomorphism.

The class-three BCH formula is

```
BCH(a,b) = a+b+[a,b]/2
           +[a,[a,b]]/12 - [b,[a,b]]/12.
```

Factoring `exp(q)exp(r)` into normal-then-section order gives

```
C(q,r) = [q,r]/2 + [q,[q,r]]/3 + [r,[q,r]]/6,

(n,q)(n',r) = (n+Phi(q)n'+C(q,r), q+r).
```

For example, if `A=BCH(q,r)`, its chart normal coordinate is
`A_N+[q+r,A_N]/2`, yielding the coefficients `1/3` and `1/6`.
Confusing a logarithmic normal coordinate with this chart coordinate
would change those coefficients.

The cocycle identity is

```
C(q,r)+C(q+r,s) = Phi(q)C(r,s)+C(q,r+s).
```

The code checks the chart law against direct BCH arithmetic. An independent
truncated free-associative-algebra calculation checks the BCH multiplication
against `exp(a)exp(b)` rather than comparing two copies of the same formula.
The standard BCH/Lie-group connection is background, not a contribution:
[Lazard, 1954](https://www.numdam.org/articles/10.24033/asens.1021/).

## A Shared Potential Still Exists

Write `h^t=(g(t),tv)`, with unknown `v!=0`. Then

```
g(s+t) = g(s)+Phi(sv)g(t)+C(sv,tv).
```

Choose an UNKNOWN proof-only functional `ell` with `ell(v)=1`.
For `tau=ell(q)` and `r=q-tau*v`, define

```
Q(q) = Phi(r)g(tau)+C(r,tau*v).
```

Applying the two cocycle identities gives exactly

```
Q(q+tv)-Q(q) = Phi(q)g(t)+C(q,tv).
```

Indeed the transverse coordinate `r` is unchanged, the change in `g`
contributes `Phi(r)Phi(tau*v)g(t)`, and the remaining three cocycle
terms combine to `C(q,tv)`. No coset-specific unknown polynomial is needed.

For a logarithmic generator `X=v+a`, `a in N`,

```
g(t) = t*a + t^2*[v,a]/2.
```

Consequently `Q` has total degree at most three. The action on the
quadratic term introduces no higher degree because `[v,a]` is central.
The remaining cocycle is cubic. This reasoning is valid without a grading
or a split extension and with an arbitrary public linear complement `V`.

An original coset `(n0,q0)H` has points

```
(n0+Phi(q0)g(t)+C(q0,tv), q0+tv).
```

Partial Fourier measurement on `N` therefore produces

```
p^(-1/2) sum_t omega^[lambda.Q(q0+tv)] |q0+tv>
```

up to one global phase. The actual public label `lambda` is uniform on
`Fp^n`. The receiver does not know or compute `ell`, `v`, or `Q` at this
stage. It uses exactly the public formal-coefficient controller already
defined in `UT4_AFFINE_PHASE_RECEIVER.md`; that producer was not changed.

## Copy And Gate Accounting

The previous all-outcome support lemma applies unchanged. The per-output
copy schedule is

```
S(m,n) = (n+1)*(n*(m+1)+1)^2*(n*binom(m+2,2)+1).
```

For `m,n<=d`, this is `O(d^8)` original cosets per phase-free quotient
sample. The public coefficient spaces and field-arithmetic operations
also have polynomial size. This is a copy bound, not a claim that the
full gate complexity has exponent eight or is practical.

Abelian Fourier samples learn `span(v)` with `O(m+log(1/epsilon))`
outputs. Zero or dependent frequencies are counted, not silently removed
from the source budget. They are standard uninformative outcomes.

All approximate operations must be budgeted as complete instruments.
The erasure retains every outcome; there is no inverse rare-branch
probability in the approximation error. The ideal description has
polynomial expected cost. A bounded-error implementation needs an
explicit polynomial stopping budget and an error allocation, not the
fixed diagnostic attempt limits in the Python simulator.

The simulator enumerates at least `p` amplitudes per line and `p^m`
Fourier outcomes. Its wall-clock runtime is NOT the proposed quantum
runtime and gives no classical HSP algorithm.

## Correct Completion After Learning The Line

Choose a KNOWN representative `v` of the learned line, and a KNOWN
functional `ell(v)=1`. On a fresh original coset, compute and measure
`r=q-ell(q)v`, retain `tau=ell(q)`, and send its normal coordinate to

```
n' = Phi(-r) (n-C(r,tau*v)).
```

The result is a full graph state

```
p^(-1/2) sum_tau |tau>|u+g_v(tau)>,
```

where `u` is a uniform unknown offset and `g_v` is the single fixed
normal orbit of the generator normalized to project to `v`.
This is the known univariate HPGP state format. Without the subtraction
of `C(r,tau*v)`, the polynomial depends on the coset; the negative
control exhibits that failure.

Here completion is simpler than generic cubic HPGP. If the unknown
normalized generator has chart coordinates `(w,v)`, then

```
D_v(w) = [v,w],
g_v(t) = t*w + (t^2-t)*D_v(w)/2.
```

`D_v` is now public and squares to zero. After Fourier-transforming the
normal register, the phase is

```
t * lambda.(I-D_v/2)w + t^2 * lambda.D_v w/2.
```

The implementation learns `w` by the established quadratic phase-learning
strategy. Maintain `w=w0+B*eta`, remove the known offset phase coherently,
cancel quadratic terms using public diagonal equations, and Fourier-read
one linear equation in `eta`. Update the affine solution space.
This final learning mechanism is prior art:
[Ivanyos and Santha, Section 5](https://arxiv.org/pdf/1503.09016).

Every source call and discarded uninformative outcome is counted.
At `k` remaining parameters, a uniformly drawn label has an identically
zero coefficient packet with probability at most `p^(-k)`, since
`Y1+Y2=lambda*B` and `B` has column rank `k`.
If a nonconstant packet is already linear, use it. Otherwise a merge of
quadratic packets has a nonzero affine-linear dependence on at least
one uniformly measured old coordinate, so its new coefficient vector
vanishes with probability at most `1/p`.
The expected additional source cost is bounded by
`sum_(k=1)^n (k+1)^2/(1-1/p)^2 = O(n^3)`.
All successful equations are exact in the ideal-state model.

The diagnostic has explicit attempt caps and reports failure if they
are exhausted; it never returns a secret-filled substitute.

## Strong Falsifiers And Controls

1. **Non-split extension.** In the free class-three algebra on `X,Y`,
   with `Z=[X,Y], U=[X,Z], W=[Y,Z]`, any lifts of the quotient basis
   still have bracket `Z` modulo the third lower-central term.
   No abelian complement to the derived ideal exists.
2. **Not a two-generator-product coincidence.** Tests also cover the free
   class-three Lie algebra on THREE generators, dimension 14, including
   genuinely three-way Jacobi identities. Its fixed potential is cubic
   and satisfies the source cocycle identity.
3. **Shared hidden parameter.** Product-rank-two tests use one common
   subgroup parameter, not independent hidden subgroups in the factors.
4. **Wrong chart.** Direct BCH multiplication and an independent
   free-associative model check the public coordinate formulas.
5. **Missing cocycle.** Removing it from graph relabeling produces
   nonconstant residual offsets; the known HPGP input promise then fails.
   Explicit `p=47`, hidden log `(1,2,3,4,5)`, coset representative
   `(0,1,0,0,0)`, learned direction `(1,2)`: at `tau=1`, the corrected
   normal coordinate is `(3,29,8)`; omission gives `(26,21,0)`.
6. **Hidden advice.** The erasure and learning entry points take public
   group data, a source callback and RNG. The actual generator and coset
   representatives exist only inside separate fixture code.
7. **Accidental easy sector.** Live erasure records zero Fourier labels
   and single-input merge shortcuts. Both counts are zero.
8. **Uncharged retries.** The live run's first quotient Fourier sample
   is zero. Its entire 7,600-copy batch remains charged.
9. **Wrong learned direction.** The actual graph support is no longer
   full; the completion rejects it instead of fitting a convenient phase.

The strongest classical statement inherited from the preceding note is
an opaque-oracle query bound. With uniform cyclic `H` outside `N`,
`M=(p^(m+n)-p^n)/(p-1)` possibilities, a `T`-query classical algorithm with
random opaque coset names succeeds with probability at most
`(binom(T,2)+1)/M`. This is not a lower bound for a structured explicit
evaluator. No such external reduction is supplied here.

## Live Result And Remaining Risks

At `p=47`, the group is the free two-generator class-three BCH group.
The hidden logarithmic generator fixture is `(1,2,3,4,5)`.
Separate source/receiver seeds are `20261022/20261023`.

The receiver spends 15,200 copies on quotient learning and 26 on known
quadratic HPGP, including the initial zero quotient Fourier sample.
It recovers `(24,1,25,2,26)`, exactly 24 times the original logarithm
modulo 47, hence a generator of the same subgroup.
The erasure uses 3,800 cubic, 38 quadratic and two linear merges.
There are no zero-character inputs or single-active-input shortcuts.
The final phase error is below `6.3e-14`.

This small fixed-prime instance was already within known tractable
classes. The putative contribution is the uniform growing-prime,
growing-dimension mechanism, not this finite instance.

Independent proof and novelty review are still missing. The source
[ISS reduction](https://arxiv.org/pdf/0707.1260) motivates studying cyclic
exponent-`p` subgroups, but it does not by itself validate this new
state conversion. Its group-presentation interfaces must be checked
separately before claiming a general nil-3 algorithm. The implemented
congruence class of primes is also a restriction; general SDE results
suggest a route beyond it, but that controller has not been implemented.

There is no established reduction from a lattice, coding, graph, tensor
isomorphism, or cryptographic problem to these instances. Novelty and
external relevance must not be inferred from passing tests or an empty
literature search.

Reproduce: `python -m theorems.nil3_cocycle_receiver --write`.
Tests: `tests/test_nil3_cocycle_receiver.py`.
