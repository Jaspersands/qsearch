# Native Known-Seed Group Workbench

Local constructive derivation / external review pending. Real native induced
actions on known noisy-linear preparations, not a new oracle problem or an
efficient quantum decoder. This pass tests coupling, normalization and the
classical counterpart before treating a conditional output as progress.

## Legal joint preparation

Use the actual known source preparation U_y from the coherent reflection
audit, on B indexed cohorts of M qutrits. Define the public representation

```
rho(g) = direct_sum_b tensor_product_j rho_(label_bj)(g)
A_y = (I tensor U_y^dagger) controlled_rho
      (uniform_work_preparation tensor U_y)
```

All phases in U_y are computed from original noisy values and the known
mask; rho uses only public labels and actual carried ring/group arithmetic.
The inverse is a genuine known original-data inverse, never an opaque HSP
input inverse or an exact secret-ideal inverse. The full A_y and its inverse
are legal on this source, so a rank-one reflection about A_y|0> is also
costable. This differs from the older copy-only RELATIVE orbit reflection.
The group register really couples to the source; it is not a decorative
pointer appended to a seed-only circuit.

For a uniform work domain X, source-zero amplitude at g is
m_y(g)/sqrt(|X|), with m_y(g)=<Phi_y,rho(g)Phi_y>. The other source outcomes
are not dropped for free. Literal controls apply the actual induced matrices,
then the entire known inverse, and retain both zero and nonzero branch mass.

Two domains are distinct experiments:

* FULL_NATIVE_GROUP: |G|=3*q^(2n), at even levelL=2r and q=3^r.
* INTEGER_SECRET_SLICE: g=((b_i,0)_i,1), b in (Z_q)^n, sizeN=q^n.

The second is a PUBLIC original-data promise, not hindsight knowledge of s.
The actual source constructor has a masked INTEGER-EMBEDDED secret. A returned
slice element yields candidate s=-b. Full-group elements with rotation0 do
not decode s. Rotation1 or2 allows a candidate via the known unit lambda_t;
only successful comparison to the fixture truth counts as full recovery.

Known work preparation uses nr trits on the slice, and2nr+1 on the full
group. The controlled action has M known cyclic permutations and at most
3*B*M diagonal character branches, with explicit index controls. Modular
arithmetic, angle compilation, source-zero test and physical gate errors
remain separately charged obligations. No QRAM or full group table is free.

## Central uncertainty, with its original-data falsifier

Let Z=pi^(L-1)*(F3)^n. Each product cohort belongs to one public central
character c_b. Even with arbitrary point phases, for any target g_t,

```
m(g_t z) = sum_c A_(c,t) chi_c(z)
sum_z |m(g_t z)|^2 = 3^n sum_c |A_(c,t)|^2
|m(g_t)|^2 <= C/3^n * sum_z |m(g_t z)|^2,
```

where C is the number of distinct occupied cohort characters, at most B.
This is Fourier orthogonality plus Cauchy, not a noise assumption. For full
uniform group input and source-zero followed by a rotation1/2 candidate,
correct-secret conditional probability is at most min(1,C/3^n). Both target
cosets are disjoint; no ideal H-fixed assumption is needed. More qutrits
inside one cohort do not increase C. The identity is NOT a decoded secret.

This does NOT exclude the real integer-embedded problem. At even level2r,
every nonzero center vector has nonzero zeta coordinate. A rotation1 hidden
generator for integer s has zero zeta coordinate. A public promised-slice
filter removes those central impostors. An initial slice preparation also
changes the uniform normalization from |G| to q^n. The full-group ceiling
cannot be carried across that filter. Exact ring tests, including the
contrasting odd-level case, already falsify that overbroad interpretation.

## Integer Fourier kernel and actual phase noise

For one original pair of public frequencies a,c, define

```
k_0=a, k_1=c-a, k_2=-c   (mod q)
eta_0=y_1, eta_1=y_2-y_1, eta_2=-y_2.
```

The actual native induced action on g=(b,1) gives

```
m_y(b) = (1/B) sum_cohort product_j
         [(sum_t omega^(k_jt.b+eta_jt))/3].
```

This is also a legal polynomial-work CLASSICAL scalar evaluator on the same
original records. For word x, let sigma(x)=sum_j k_j,xj and eta(x)=sum_j
eta_j,xj. With D=B*3^M, define the public pushforward p_sigma=count/D and
the actual complex coefficient z_sigma=sum_(x:sigma(x)=sigma) omega^eta(x)/D.
After the slice work Fourier transform, the UNNORMALIZED source-zero
amplitude is z_sigma, not sqrt(p_sigma). Exact Parseval gives

```
P_zero = sum_sigma |z_sigma|^2 <= sum_sigma p_sigma^2.
```

Every noisy term has unit modulus. In the ideal common-secret case,
z_sigma=p_sigma*omega^(sigma.s); therefore P_zero=sum p^2 and
P(correct AND zero)=1/N. The frequency-label Born law after zero is
p_sigma^2/sum p^2, independent of s; the useful phase survives only if that
register is retained coherently. Measuring a Fourier label is not decoding.

Noise need not destroy conditional correctness here. Let f be the fidelity
between the actual and secret-ideal indexed seed. Since the ideal seed is
fixed by the true h=(-s,1), decomposition along it gives

```
|m_y(h)|^2 >= max(0,1-4*(1-f)).
```

The cross terms vanish because rho(h) fixes that vector. Thus this target
bound is QUADRATIC in pure-state error, not a generic additive rare-branch
bound divided by P_zero. Combining it with |z|<=p supplies a source-specific
relative guarantee; it does not justify conditioning arbitrary trace errors.

For IID full-root original labels, any two distinct (cohort,word) frequency
images collide with probability1/N. In the same cohort a differing selector
has coefficient difference(2,-1),(1,1), or(-1,2); at least one is a unit
modulo3^r. Distinct cohorts have independent uniform images. Hence

```
E sum p^2 = 1/N + (1-1/N)/D.
```

If the original-source mean squared pure trace bound is e2, the ensemble
conditional correct probability (over source draws AND measured branches)
is at least

```
max(0,1-4*e2) / [1+(N-1)/D].
```

Mean zero acceptance is at most[1+(N-1)/D]/N, and mean correct-and-zero at
least max(0,1-4*e2)/N. No tiny event is discarded and no per-bank conditional
mean is mislabeled as this joint conditional law. The statement is for
exact native controlled characters and uniform-amplitude logical phase
preparations. Generic gate/measurement errors need a separate relative
certificate or precision sufficient for the rare event; none is inferred
from source moments.

## Preparation cost and classical baseline

If D is large enough to make the conditional state reliable, source-zero
acceptance is nevertheless about1/N. Ordinary two-reflection amplification
does not change its normalized good-state distribution and satisfies
P_j <=(2j+1)^2 P_zero. An expectation bound carries the same factor. Reaching
constant average zero acceptance requires order sqrt(N) iterations in this
specific family. That is Grover-scale search of the original secret space,
not an efficient receiver and not a lower bound on other algorithms.
The unchanged normalized good distribution is a PER-REALIZED-BANK statement.
Amplification changes how different source draws are weighted upon acceptance;
the unamplified ensemble conditional guarantee is not automatically an
amplified ensemble guarantee. The ledger explicitly leaves the latter unknown.

One-pass COMPUTATIONAL group readout has a stronger classical counterpart:
measure g early. This commutes with controlled rho and all subsequent
source-only operations. Sample g uniformly, build B known product terms,
apply the actual per-cohort inverse phases/F3 and index Hadamard, then use
the exact rational tensor sampler. No exponential group or source table is
needed. The program and shadow retain all raw shots, failures and finite
coin aborts. After group Fourier interference or whole-orbit amplification,
early measurement is NOT legal; no general entangled-work simulation is
claimed. Exhaustive scalar rejection is a baseline, not the best classical
lattice attack.

## Next Research Target

The useful missing operation is structural fibre/normalization processing,
not declaring a high-fidelity POSTSELECTED state to be an algorithm. Study
the weighted subset-sum map and multiplicity erasure on the retained work
register. Constant relative frame conditioning does not remove an
exponentially small absolute block-encoding scale. A classically compilable
short-preimage sampler is also a classical chosen-frequency attack and
must not be granted as a free quantum ingredient. Any candidate must supply
the actual quantum circuit, reductions, precision/noise accounting and a
matched SIS/preimage baseline.

Run `python theorems/native_known_seed_group_workbench.py --write`, its tests
and `node research/certificates/native_known_seed_group_crosscheck.js`.
Finite enumerations certify controls only. Scalable collision/moment/price
ledgers never enumerate q^n secrets, q^(2n) group elements or3^M words.
No efficient full decoder, hardware execution, source-hardness transfer or
new accepted speedup candidate is supplied.
