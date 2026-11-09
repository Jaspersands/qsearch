# Superlattice conditional records: paid source audit

2026-11-06. Parent derivation checked against the primary paper and an
independent local source review. This is a scoped consequence of the paper's
stated lemmas; its full 144-page algorithm has not been independently proved.

## Source and question

Hhan, Kim, Kim and Laarhoven, *Superlattice methods for the shortest vector
problem and discrete Gaussian sampling*, ePrint2026/2761, 4 November2026.
Primary https://eprint.iacr.org/2026/2761.pdf returned403; the public mirror
https://eprint.iacr.asia/2026/2761.pdf supplied the full PDF (1846425 bytes),
SHA256 893806e7308fdae41175a29bf2b47aa2b2370f83823e04331da03f92f25a024a.
The actual intro, DGS construction, record definition and Lemma4.7 were read.
Durable selected text: audits/sources/superlattice_2026_2761_excerpts.txt.
Corpus been-tried and baseline lookups preceded the source audit.

Native candidate: given a rational n-dimensional lattice basis and width s,
prepare a pure discrete-Gaussian state with all lattice, precision, memory and
success costs charged. The proposed mechanism was to use the paper's forced
output construction as the conditional inverse needed to erase a classical
sampler's record. A polynomial-time construction at useful narrow widths
would remove a significant lattice-algorithm blocker. No such clock or
coherent inverse is presently available from this construction.

## What the paper actually supplies

Theorem1.4 states classical arbitrary-width approximate DGS with
T=(3/2)^(n/2+o(n))*poly(kappa) and
S=(4/3)^(n/2+o(n))*poly(kappa), for total variation error2^-kappa.
Its quantum SVP bound2^(0.2469n+o(n)) uses coherent indexed access to stored
classical arrays. These are source claims, not independently verified bounds
or polynomial algorithms. Lists, pair enumeration, dictionaries and caps are
explicit. Random shifts regularize expected occurrence counts, not actual
counts in each list. A preparation trial itself costs2^O(n/log n).

Fix a legal bin j and U>=rho_s(L), and let P be the ordinary run's record
law, including preparation. Write ell(z) for expected uncapped occurrence
count and Q_z for Algorithm8's forced occurrence record and marked position.
Lemma4.7, with the cap indicator included, states the measure identity

 P(d omega) sum_{i in Occ_z(omega)} delta_i
   = ell(z) Q_z(d omega,di) 1_success.

The ordinary Candidate picks a uniform position in its nonempty root list.
Consequently its joint record/position law conditional on output z is
proportional to the left-hand side divided by |list(omega)|. Running Q_z
and accepting with probability1/|list(omega)| produces EXACTLY that
conditional law in the ideal mathematical model. Lemma4.1 says its success
probability varpi_z lies in[1/2,1]; at most two complete test runs are needed
in expectation. O(log(1/epsilon)) independent repetitions cap the failure.

The forced record alone is occurrence-size-biased. It is neither an ordinary
record conditioned merely on containing z nor a uniform preimage. The
normalization factor ell(z) cancels only after conditioning on acceptance.
The source's finite-precision approximation must also be charged in an
implementation; the identity above uses its ideal sampling laws.

## Decisive admission boundary

This is a real classical conditional-record sampler, so saying that none
exists would be wrong. However its tests retain the same exponential list
work/space. Moreover the record definition on printedp44 explicitly omits
scalar random numbers discarded by execution. It is NOT a full-random-tape
conditional sampler, and it is not a clean coherent inverse.

Reversibly executing a randomized conditional sampler leaves its random
coins and workspace. Even a correct classical conditional output law does
not automatically provide a pure superposition with its square-root
amplitudes or the inverse needed for garbage erasure. A clean circuit,
complete coin law, success amplitude and total clock are separate obligations.
This is a missing construction, not a no-go theorem about coherification.

Strongest matched classical baseline here is the paper's own explicit-list
DGS algorithm; the previous Klein/Babai pair-cooling baseline also remains
in STRUCTURED_EDCP_KLEIN_DUALITY_AUDIT.md. No quantum implementation, source
sweep or new infrastructure is warranted by this source audit. False gates:
polynomial DGS, coherent erasure, full-random-tape inversion, new quantum
algorithm, classical hardness, novelty and speedup.

Actual text locators (newline-split pdftotext -layout): printedp31,
lines1692--1699; pp34--36,1856--2009; p43,2360--2415; p44,2419--2438;
p48,2703--2742; p49,2780--2790. Use split("\n"), never splitlines(),
for those locators. Independent source reviewer: superlattice_source_scope.

## Selection

The new paper supplies no admitted polynomial coherent primitive. A chosen-
line multivariate character extension was compared next: the corpus already
records the quadratic composition in AFFINE_QUADRATIC_CHARACTER_SLICE_READOUT
Section7, and fixed-degree interpolation inherits the univariate decoder.
It does not remove growing-degree cost. The next higher-value question is
whether native character reconstruction admits a measurement/decoder beyond
the proved split-support factorial boundary. No extension-field or arbitrary-
resultant oracle may be supplied to answer it.
