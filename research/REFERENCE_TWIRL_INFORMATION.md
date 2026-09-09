# Reference Twirling and Lost Binary Information

Status: project derivation, independently tested at finite rank, **review
pending**. Not a machine-checked proof, new general entanglement lower bound,
or claim that efficient hidden-subgroup algorithms are impossible.

## Decision

Do not replace coherent encoded restriction with independent reference-type
measurements followed by carrier discard. Even an arbitrary entangled
measurement on all remaining multiplicity codes then has vanishing binary
advantage with polynomially many inputs. Noncommuting copy-space operators
do not recover erased correlations.

A single collective reference twirl on **all** inputs is different: it
preserves the uniform-prior binary mixture exactly. The encoded isometry
retaining all registers also escapes this particular obstruction.

Run `python qsearch.py coset-hidden-involution-reference-twirl-information`
or `python qsearch.py run EXP-COSET-HIDDEN-INVOLUTION-REFERENCE-TWIRL-INFORMATION`.
The artifact is
`research/representation/coset_hidden_involution_reference_twirl_information.json`.

## Physical Model

Let G=S_(2m), D=|G|, K=C2 wr S_m the centralizer of a known reference matching,
and C the M=(2m-1)!! fixed-point-free involutions. The hidden h is sampled
**once** uniformly from C. Every input has that same h:

    rho_h = (I + R_h)/D,       tau = I/D.

The binary alternatives are the uniform shared-h coset ensemble and the
trivial-subgroup state. T denotes HALF trace norm, so equal-prior success is
1/2+T/2. These are unpostselected physical states, not an aligned h-even
branch, a uniform distribution over representation labels, or independently
redrawn h in each input.

Within a block of b copies, average the simultaneous reference-conjugation
action. If O is the K-conjugacy orbit of h, of size s, the output is

    sigma_(O,b) = (1/s) sum_(g in O) rho_g^tensor(b).

Different blocks use independently forgotten conjugators. Their reference
subgroups may be different known conjugates of K, fixed or randomly chosen
independently of the input and measurement outcomes. Subsequent processing
of all block outputs may be fully quantum and collective.

For b=1, subgroup Schur decomposition identifies the twirl with dephasing
the K irrep type and replacing each carrier by its maximally mixed state:

    T_K(X) = direct_sum_mu [ I_(V_mu)/d_mu tensor
                            Tr_(V_mu)(P_mu X P_mu) ].

Keeping the type and multiplicity register after this discard is
statistically equivalent: the missing maximally mixed carrier can be added
back without input knowledge. Merely tracing a padded carrier register
while retaining intertype coherences is NOT asserted to implement this
channel. Nor is a unitary encoding with its environment retained a twirl.

## Derivation

Regular-representation orthogonality gives, for nonidentity involutions,

    D Tr(rho_g rho_h) = 1 + [g=h].

Consequently, including all physical row multiplicities,

    D^b Tr(sigma_(O,b)^2) = 1 + (2^b-1)/s.

For any density operator sigma in dimension d, Jensen's inequality applied
to its eigenvalues gives

    D_nats(sigma || I/d) <= log(d Tr(sigma^2)).

Thus its relative entropy is at most log(1+(2^b-1)/s), and hence at most
(2^b-1)/s. For a fixed h, relative entropy adds across the independent
blocks. Convexity bounds the entropy of the uniform-h mixture by the
average of these conditional entropies. For any predetermined reference,

    E_h[1/|O(h)|] = (# reference orbits)/M = p(m)/M.

Apply quantum Pinsker in nats, D_nats >= 2 T^2:

    T^2 <= min(1, p(m)/(2M) * sum_j (2^b_j - 1)).

The bound holds BEFORE the final measurement, so no joint processing of
the remaining block registers improves it. For t equal blocks and target
distance delta, a necessary condition is

    b >= ceil(log2(1 + 2 delta^2 M/(t p(m)))).

For t=poly(m), this is Omega(m log m). At m=128 and t=m^2 the necessary
block size for T>=1/3 is 792; this is **not sufficient**. For t=m^2
single-copy blocks at m=128, T is at most 2^-397.4079.

The reference orbit indexed by a partition nu of m has size
2^(m-length(nu)) m!/z_nu, where z_nu=product_i i^a_i a_i!.
Finite matching enumeration checks every orbit through m=4 independently.

## Counterchecks and Limits

1. **One global twirl is lossless for this binary task.** The uniform
   shared-h mixture is already invariant under simultaneous conjugation.
   S4 and S6 controls verify this identity. Thus diagonal K invariance of
   the whole effect does not imply the independent-discard obstruction.
2. **Information loss is directly visible, but finite numbers are not the
   theorem.** In S4 with two inputs, raw T=3/8, independent-discard T=1/3;
   for a single two-input block T remains 3/8. S6 supplies noncommuting
   group controls. Full S4 regular-basis matrices independently check the
   Fourier calculation and entropy constants.
3. **Rare-orbit second moments mislead.** For one fixed reference in every
   block the exact mixture chi-squared divergence is

       sum_O (s/M)^2 [ product_j(1+(2^b_j-1)/s) - 1 ].

   At m=8 with 64 single-copy blocks this is over one million, while
   T^2<=64/184275. A large chi-squared value is not a lower bound on T.
4. **Unknown alignment is not granted.** Picking K=C_G(h) after learning h
   would make s=1 and invalidate the uniform reference prior. A candidate
   must pay for such alignment; this workbench never supplies it.
5. **Adaptive references remain separate.** Conditioning on outcomes
   changes the hidden prior. The proof above does not license replacing
   posterior orbit averages by p(m)/M. The null-prefix hybrid below gives
   a weaker bound without that error. It permits quantum memory but requires
   a classical reference choice and twirling each fresh block before it
   interacts with memory. Quantum-controlled references are not covered.
6. **More input resources are outside scope.** Coherent oracle queries,
   known purifications, nonuniform promises, charged postselection, and
   fresh states after feedback are not automatically covered. Postselection
   cannot convert conditional advantage into unconditioned success for free.
7. **Not a classical simulation.** This is an information-loss boundary
   for a quantum channel, not a dequantization algorithm or hardness proof.

## Classical Adaptive References with Quantum Memory

Assume at most t rounds, with at most b_j fresh physical coset inputs in
round j. A reference can be chosen using all previous classical outcomes.
Quantum memory may persist. However, the new block must undergo its reference
twirl **before** interacting with that memory, and no other h-dependent
resource is available. The complete output includes failures/abort flags;
success is not conditioned on a rare transcript.

Use t+1 hybrids. Hybrid j supplies tau on the first j blocks and the real
shared-h, reference-twirled input thereafter. Adjacent hybrids differ only
at round j. Their identical null prefix has a classical history and a
conditional quantum memory state independent of h. Hence the chosen
reference is also independent of h at that point, even though it need not
be so in the actual run.

For fixed history and h, replacing the new block changes trace distance by
at most sqrt((2^b_j-1)/(2|O(h)|)), capped at one. Tensoring the same memory
does not change distance. The future protocol, including its h-dependent
fresh states, is a CPTP map for each fixed h and cannot increase it.
Average over h and null-prefix histories, then use Jensen/Cauchy-Schwarz:

    distance between adjacent hybrids
        <= sqrt((2^b_j-1) p(m)/(2M)).

Triangle inequality over hybrids and Cauchy-Schwarz over rounds give

    T <= min(1, sum_j sqrt((2^b_j-1) p(m)/(2M))),
    T^2 <= min(1, t p(m)/(2M) sum_j(2^b_j-1)).

For equal block sizes the squared bound is t^2(2^b-1)p(m)/(2M), not the
stronger predetermined-reference bound with t. For t=poly(m), a constant
advantage still requires b=Omega(m log m) within this architecture. At
m=128, t=m^2, the necessary block size for T>=1/3 is 778. Single-copy
blocks give T<=2^-390.4079, despite arbitrary subsequent quantum memory.

An exact two-round probe uses P_r=(I+R_r)/2, with known r. Its likelihood is
Pr(+|h)=(1+[h=r])/2. Repeating r after + and changing it after - gives a
source-normalized adaptive transcript checked at m=2,3,4. After an initial
+ outcome, the reciprocal reference-orbit mean changes from p(m)/M to
(p(m)+1)/(M+1). This explicitly falsifies the tempting posterior-uniformity
shortcut. These classical-transcript controls do not by themselves prove
the quantum-memory theorem; the hybrid argument is the uniform reduction.

This argument does NOT cover coupling a fresh input to memory before the
destructive twirl, nor maintaining a coherent superposition of references.
Those are genuine remaining architecture questions, not hidden assumptions
that can be inserted into the proven channel contract.

## Constructive Erasure Escape, Not a Decoder

The preinteraction condition is necessary, not just a cautionary phrase.
For any known unitary irrep rho_lambda of dimension d, coherently encode

    V|i> = (1/sqrt(|G|)) sum_g |g>_reference rho_lambda(g)^dagger |i>_carrier.

Irrep matrix-element orthogonality gives, in the stated Fourier convention,

    (QFT_G tensor I) V|i>
        = |lambda> |i>_row (1/sqrt(d)) sum_j |j>_column |j>_carrier.

Thus even total carrier erasure loses no input information: a reference QFT
and discarding its column recover the original input exactly. The carrier
is already maximally mixed and independent of the input. Conditional on
efficient uniform group preparation, controlled irrep action and the group
QFT, this is a normalized transport construction with no postselection.
Dense matrices here are finite checks, not an implementation at growing n.

All five S4 irreps are checked, including **every off-diagonal matrix unit**,
so the test verifies the full recovery channel, not just classical basis
labels. A subsequent K twirl on the carrier cannot destroy information
already transferred to the reference. This explicitly escapes the
preinteraction assumption; it does not refute the scoped bounds.

The construction uses ordinary orthogonality, not a new HSP algorithm.
Recovering the input returns the original hard quantum state. A reference
register that preserves the state does not supply a detector, a decoding
measurement, or a faster classical baseline. Do not open another research
track solely for this reversible change of encoding.

## Relation to Literature

[Watrous, Theorem 5.38](https://cs.uwaterloo.ca/~watrous/TQI/TQI.5.pdf)
gives quantum Pinsker; its base-two convention is converted here to nats.
[Diaconis and Simper](https://arxiv.org/abs/2102.04576) study the
hyperoctahedral double-coset/matching structure used for orbit counting.

The Omega(n log n) scale is **not new**:
[Hallgren, Roetteler and Sen](https://arxiv.org/abs/quant-ph/0511148) and
[Moore and Russell](https://arxiv.org/abs/quant-ph/0511149) already establish
general coset-measurement entanglement limitations. This module's
purpose is to audit a concrete destructive architecture, including arbitrary
later joint processing, explicit finite constants, and a register-discard
contract. The architecture restrictions differ, so no blanket strength or
novelty comparison is claimed. It does not replace those theorems.

## Next Research Obligation

Specify an actual source-weighted effect with charged resources that retains
the required cross-input information, not another multiplicity-basis
diagnostic. Record the block partition, discarded environments, reference
schedule, outcome law, and reduction from detection to the natural task.
Surviving this audit is only a necessary condition, not an algorithm.
