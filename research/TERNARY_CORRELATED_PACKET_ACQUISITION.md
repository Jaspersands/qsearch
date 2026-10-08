# Original-Source Acquisition Of Correlated Carry Packets

LOCAL DERIVATION / REVIEW PENDING. This closes an acquisition debt in the
existing carry-packet track. It does NOT provide an efficient decoder, a
new sieve, an accepted algorithm, or a full-depth complexity improvement.

## Source And Instrument

The parent has dimension n, even native level2r>=4, integer secret
s in Z_(3^r)^n, and M=K*(n+1)^2 original samples, K>n. Each original register
has the actual two native frequency rows(a_i,c_i) at q=3^r. Their full pairs
are IID uniform only under the original native source promise. Public IDs
track ancestry; distinct IDs alone do not establish independence.

The [published CCP sieve](https://arxiv.org/html/2609.34996v1) supplies the
native sample model and known sieve baseline, but does not grant a
preparation unitary/inverse or unlimited approximate samples from LWE.
The [diagonal-equation method](https://arxiv.org/abs/1503.09016) underlies
the repo's existing F3 support finder. Neither construction is claimed new.
This adapter starts with PROVIDED original native samples; upstream DCP
conversion caps and joint input errors remain separate obligations.

1. Split the M samples into K fixed disjoint windows of W=(n+1)^2.
   In each window use ONLY B_i=(a_i+c_i) mod3 to find a nonempty support S_j
   with sum_(i in S_j) B_i=0. The support's first index is its pivot.
2. Apply inverse SUM from each pivot to its other active registers. Measure
   only those active complements, recording u. Leave the M-S inactive
   originals untouched, where S=sum_j |S_j|. All outcomes are accepted.
   There are P=S-K pointer trits, each joint pointer has probability3^-P.
3. Set pivot anchors to0, active complement anchors to u, and inactive
   placeholders to0. The remaining K pivots have the exact relative rows
   F(anchor+e_j*S_j)-F(anchor), F(anchor+2*e_j*S_j)-F(anchor), modulo q.
   These satisfy c'_j=2*a'_j mod3 and convert bijectively into the ACTUAL
   native odd level2r-1 labels. This is not a low-field phase substitution.
4. Compile the existing residue matrix of those odd labels into RREF C.
   For t in F3^K, implement the invertible coordinate map

       t -> (y=C*t, z=t_free).

   The pivot outputs use SUMs into distinct pivot wires. Measure y and
   keep every syndrome. If rho=rank(C), retain h=K-rho>=K-n joint registers.
   Conditional on u, each y has probability3^-rho. The combined raw branch
   probability is3^-(S-K+rho), NOT3^-(M-K+rho): inactive wires were not measured.

The public frame can depend on u and have variable rank. Outcome metadata
therefore specifies h and the logical wiring for each branch. This is a
valid adaptive instrument, not a single secretly chosen postselected frame.

## Original-Root Phase Identity

Let t_y(z) be the packet assignment obtained by solving the RREF pivots.
Lift it back to original active registers by

    x_i=u_i+t_y(z)_j mod3, i in S_j,

with each active pivot's u_i=0. Unused registers remain a tensor factor,
not measured zero values. For ANY fixed unused assignment w, define

    Q_y,u(z) = [F(lift(t_y(z),w))-F(lift(t_y(0),w)) mod q]/3.

The difference is divisible by3 because C*t is fixed. Contributions of w
cancel. Q equals BOTH the original carry packet's residual and the growing-
depth hierarchy's empty derivative. After the pointer and syndrome are
actually measured, the active output up to its branch global phase is

    3^(-h/2) sum_z exp(2*pi*i*<s,Q_y,u(z)>/(q/3)) |z>.

The inactive original factors are still present. If pointer or syndrome
registers remain coherent, their global phase cannot be dropped by this
argument. This implementation certifies the MEASURED instrument only.

## Label Law Is Not A Product-Payload Claim

Conditional on every original curvature B, the supports are fixed. At the
pivot of any support, vary its first frequency's low trit and the two high
frequency lifts, while all other original rows are fixed. The pivot anchor
is0. The allowed input pairs number q^2/3. Their contribution to the child
pair is injective; the zero-curvature support makes its output satisfy
c'=2*a' mod3, also a set of size q^2/3. Consequently the child is uniform
on the actual odd native pairs. This holds for every fixed curvature and
pointer stratum. Disjoint original windows give independent child rows.
The old cyclic extractor's exhaustive q=9 conditional census cross-checks
the one-coordinate premise; its two-support census checks the joint product.

This is an ensemble statement conditional on the IID original source law,
not a claim that repeated executions of a pinned public-label calibration
supply identical packets. Nor are the h logical registers independent native
samples: solving C*t=y couples their phase functions. The complete pinned
instrument has branches whose first-register purity is about0.368 at s=1;
at s=0 it is1. These are exact-source bounded controls, not a population
entanglement rate or a quantum advantage estimate.

The unused originals' curvature labels have been selected against. They
must not be relabelled as an unconditioned fresh IID source. Retaining them
is legitimate; applying another receiver must account for their actual law.

## What This Changes And What It Does Not

At K=2n, the original acquisition cap is2n*(n+1)^2, while at least n logical
registers remain after ONE root lowering. The retention ledger is analytic,
not a quantum-state simulation at large n. The full packet is represented
by K odd labels and an n-by-K field frame; public Q evaluation uses local
frequency sums and does not need a3^h table or an unknown phase oracle.
The existing hierarchy bounds additive degree by2r-1. Growing r is therefore
not automatically a fixed-degree stabilizer/cubic learning problem.

The standalone TernaryPacket's acquisition flag remains false: it still
starts with supplied odd inputs. The new composition explicitly charges all
M PROVIDED original samples, even though only S are active. Support finding
uses at most K*(n+2) Gaussian kernel calls; inner SUM cost is S-K, outer SUM
cost is the number of nonzero free-column frame entries. Classical label
arithmetic is polynomial in M,n,K,log q; hardware gate synthesis and total
error certification are not implemented.

The packet alone aliases s and s+(q/3)*e_l. Pointer/syndrome probabilities
are secret-independent and do not reveal this missing high digit. The
untouched original states can still depend on that digit. This is NOT a
claim that all information in the entire retained source is lost.

No legal recursion follows just from having h logical registers: Q is
coupled, not the original native product phase family. Reapplying an IID
native sieve or a tensor-matched cubic cancellation protocol requires a new
proof and genuinely supplied inputs. A weak decoder for this structured
joint phase family, or a costed useful multi-depth transducer, is still the
substantive missing result. Acquisition is now charged, not solved upstream.

## Falsifiers And Verification

Reject the composition if a selected mask has nonzero curvature; source
ancestry overlaps; a raw branch probability ignores active wires or measures
inactive ones; the original-root identity fails; the RREF map is noninvertible;
or correlated logical wires are promoted to fresh IID samples. Also reject
claims of supplied matched packet copies, preparation inverses, a full-depth
cost from multiplying this one-step ledger, or an efficient decoder.

The pinned n=1,r=3,K=4 control uses16 original inputs,5 active inputs and
11 untouched inputs. It replays ALL243 active words and ALL9 pointer/syndrome
branches, retaining3 logical wires per branch. The seed is a SELECTED
bounded instrument calibration, not a random-source population estimate.
Larger n=2,3 controls check bounded logical tables of27 and81 words through
their original ancestry; their original word cubes are NOT enumerated.
An independent JS checker reconstructs even and odd native charts, support
selection, RREF frames, branch phases, probability costs and logical purities.
Mutation tests attack phases, supply, branch omissions and false promotions.

A separate deterministic native-label TEST control checks pointer-dependent
rank:729 active words give three rank0 branches retaining4 wires and eighteen
rank1 branches retaining3 wires. Their exact raw masses sum to1. This control
is not included in the pinned JS report or a population experiment.

```
python theorems/ternary_correlated_packet_acquisition.py --write
node research/certificates/ternary_correlated_packet_acquisition_crosscheck.js
python -m pytest -q tests/test_ternary_correlated_packet_acquisition.py
```

Gemini/Antigravity owns CLI command `ternary-correlated-packet-acquisition`,
production registry/proof integration, full-project tests and Git backups.
The experimental result is acquisition correctness; it must not be registered
as an accepted breakthrough algorithm or a generic negative complexity result.
