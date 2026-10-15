# Coarse-Only Disjoint-Kernel Pairing

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. No novelty or improved sieve
exponent. This is a concrete baseline realization of Gaussian dependence and
common-isotropic cancellation, not a groundbreaking quantum algorithm.

Run `python qsearch.py dcp-disjoint-kernel-pairing` and
`node research/certificates/dcp_disjoint_kernel_pairing_crosscheck.js`.

## Why Implement This

The preceding nonlinear frontier supplied an exponential lookup reference and
near-unit pairing existence at m>3n. Its coarse-only fresh-label theorem did
not supply a polynomial evaluator. Global affine rigidity blocks a shortcut,
but does NOT imply all nonlinear evaluators are hard. Here is an explicit
nonlinear involution with polynomial public preprocessing, coherent evaluation
and cleanup, at the much worse supply m>=(n+1)^2.

The existing `greedy_common_isotropic` in `theorems/dcp_carry_packets.py`
already supplies a related polynomial mod4 baseline. This implementation is
not an asymptotic advance over it. Its purpose is an executable ORIGINAL-wire
partner interface with coarse-only access and explicit reversible Gaussian
control, so future proposals must beat a real baseline rather than a table.

## Construction And Reciprocity

Let A be the full n-by-m public matrix modulo2^t, t>=3. Construction reads
ONLY A mod4. Partition (n+1)^2 columns into n+1 blocks of size n+1; any extra
columns are unused by this baseline. In each block find a nonempty binary
dependence u_j of A mod2 by Gaussian elimination. The supports u_j are disjoint.
For ORIGINAL assignment x define

```text
C_j(x) = [sum_{i in u_j} A_i (1-2*x_i)] / 2 mod2 in F2^n.
```

The numerator is even. This is an affine function of x depending only on
coarse labels. Find a canonical nonzero dependence d(x) among the n+1 columns
C_j(x). Set u(x)=XOR_{j:d_j(x)=1} u_j and F(x)=x XOR u(x).

Disjoint support makes u(x) nonzero. Dependence implies A(F(x)-x)=0 mod4.
Crucially, flipping any whole u_j negates its signed sum and leaves all other
block sums unchanged. Negation is identity AFTER division by2 modulo2. Hence

```text
C(F(x)) = C(x), d(F(x)) = d(x), F(F(x)) = x != F(x).
```

These identities hold on EVERY x and for EVERY A with sufficient supply.
There is no accepted-subset reciprocity assumption and no exponential search
over original assignments. A selected n6,m49 control has distinct nonzero low
signatures: global rigidity proves this involution cannot be globally affine.
That selected control is NOT an IID-native probability sample.

## Actual Reversible Evaluator

The evaluator exports static X/CX/CCX gate lists. Unknown assignment bits enter
only as quantum wires. Pivot occupancy, pivot columns, combination witnesses,
active branches and first-dependency selection are Boolean work wires. No
host-language Gaussian branch reads an unknown assignment during compilation.

Fresh-work-wire XOR/AND gates compute a canonical dependence; outputs are
copied into the arbitrary XOR target; ALL work gates are reversed. The map is

```text
|x>|z>|0_work> -> |x>|z XOR (valid=1,F(x))>|0_work>.
```

Every primitive is a full-space permutation, including on dirty work. Correct
XOR-F semantics require clean initial work; arbitrary dirty-work forward/inverse
round trips are tested, not confused with clean-work semantics.

The gate/work order is O(n*m+n^3+m), O(n^3) at this baseline's supply. Public
disjoint-support preprocessing is also polynomial and must be charged. Explicit
gate-list export has n<=8,m<=256 work caps; exceeding a cap returns UNKNOWN,
not an impossibility claim. This is elementary reversible gate IR, not a
hardware-transpiled, noise-calibrated or physically executed quantum circuit.

The existing six-XOR-F reciprocal compiler now dispatches this evaluator.
It consumes m input qubits on EVERY attempt, four F calls on failure and six
on success, plus reversible relation/ordering arithmetic. It rejects descended
label zero. Each accepted batch yields ONE phase qubit; outcome lists are not
parallel outputs. Finite tests compare exported gate semantics, actual original
phase densities, partner reciprocity and clean compiler workspace.

## Cheaper Measured Controller

There is no need to implement Gaussian selection coherently for this baseline.
Choose a pivot in each disjoint support and apply CNOTs from that pivot to all
other support coordinates. Then x=b XOR sum_j z_j u_j, and C(x)=C(b) is
independent of ALL z_j. Measure the nonpivot coordinates to obtain b. Gaussian
dependence selection is now classical. For its chosen d, CNOT from one selected
logical pivot to the other selected logical pivots; measure all but that output.

The module exports BOTH CNOT stages and ALL bounded branch records, including
actual oriented original endpoints, signed descended labels and Born masses.
Every physical attempt follows just ONE branch, uses O(m+n) CNOTs, measures
m-1 qubits and emits one phase qubit before the paid zero filter. Polynomial
classical preprocessing/control remains charged. No coherent solver, source
inverse or postselected syndrome is needed. Tests execute the basis permutations
on the full original mixed source and compare each conditional phase density.

This equivalence is an important self-critique: the globally nonlinear partner
does NOT escape existing adaptive affine/CNOT readout. It supplies an executable
baseline and a valid coarse-only source interface, not a new quantum mechanism.

## Source Law And Costs

Because F reads only A mod4, the preceding conditional fresh-label theorem
applies: writing A=B+4Z with independent uniform higher labels, each fixed
coarse-selected pair has uniform descended label in Z_(2^(t-2))^n. The zero
filter costs2^(-(t-2)*n), so native mean useful admission is exactly
1-2^(-(t-2)*n). This is a mean over higher lifts, not a statement for every A.
Preserve coarse lineage, discard the old HIGHER-label transcript at the output
interface, and use fresh independent batches. Pure zero-label injection remains
a theorem-level restoration, not an implemented backend.

Under independent balanced ORIGINAL-register visibilities, an outcome's
coherence is the product over the actual flipped support. Reuse that existing
law; marginal visibilities under arbitrary correlations do not suffice.
For n1,A mod4=(1,1,1,1), the width histogram is12 inputs of width2 and4 of
width4, giving mean unfiltered visibility(3*v^2+v^4)/4. Tests use actual mixed
phase matrices, not a merge-depth visibility surrogate.

The worst-width lower factor v^m is conservative. At v=1-1/n it decays with
this quadratic supply; that LOWER bound decaying does NOT prove the actual
algorithm's visibility decays. The constant-factor existential guarantee from
v=1-1/n^2 is also only a sufficient noise promise, not a natural-source proof.
No noise upper-bound/no-go is inferred from a weak lower bound.

## Exact Native Noise Law And A Genuine Upper Bound

The following stronger analysis is separate from those worst-width LOWER
factors. It uses independent second low bits, parity-only support selection,
and the actual Gaussian selector, and therefore supplies a legitimate UPPER
bound for THIS baseline under the independent balanced-source noise promise.

Condition on B=A mod2, its deterministic supports u_j, and any fixed original
x. The second bits of A make all C_j(x) independent uniform vectors in F2^n:
each nonempty disjoint support has a fresh higher-bit sum. Let w_j=|u_j|.
If J is the index of the first dependent column, then

```text
P[J=j] = product_{i=0}^{j-1}(1-2^(i-n)) * 2^(j-n),  0<=j<=n.
E[v^|u(x)| | J=j, B] = v^w_j * product_{i<j}(1+v^w_i)/2.
```

Before J the columns are independent; conditional on dependence, the new
column has a UNIFORM representation in their span. Thus its witness uses
the current block and IID fair choices of the previous blocks. Summing these
expressions is an exact mean, not a fitted exponent. It is conditioned on
parity B ONLY, not on an already fixed full A mod4. Complete column-table and
second-bit censuses test the distinction; A mod4=0 gives an explicit
counterexample to transferring this mean to a fixed coarse matrix.

For native IID B, let r=floor(n/16). The probability some block has ANY
nonempty kernel vector of weight<=r is at most

```text
b = min(1, (n+1) * sum_{w=1}^r binom(n+1,w) / 2^n).
```

On the complement all w_j>r. Set a=v^(r+1). Since P[J=j]<=2^(j-n),

```text
E[visibility | no short block] <= min(1, ((1+a)^(n+1)-1)/2^n) = g.
E_native[visibility] <= b + (1-b)*g.
```

The geometric sum cancels its leading factor a exactly, including v=0 by
continuity/direct substitution. The report stores exact dyadic arithmetic for
12 growing-parameter rows; an independent JS checker recomputes it.

Consequently constant v<1 is exponentially bad asymptotically for this
architecture. Even v=1-1/n is insufficient. For k=r+1>n/16, the binomial
inequality (1-1/n)^(-k)>=1+k/n gives a<16/17, hence
g<=2*(33/34)^(n+1). A direct generating-function estimate at z=1/15 gives
sum_{w<=r} binom(n+1,w)<=15^r*(16/15)^(n+1). The exact integer inequality
15^15>2^56 bounds its exponential factor by2^(n/2), so
b<=2*(n+1)*2^(-n/2). Thus both terms have explicit exponential bounds; no
floating entropy estimate or fitted noise exponent is needed.
The exact bound at n256,v255/256 is below1/1000; at n512,v511/512 below1/10^6.
By contrast v=1-1/n^2 has the earlier constant worst-width LOWER factor.
This exposes the quadratic noise scale of this baseline, without claiming a
noise threshold for arbitrary receivers or the actual natural-problem source.

Source lineage matters: accepting arbitrary disjoint kernel supports would
not prove that they were chosen independently of second bits. Program validation
reconstructs the deterministic parity-only block-kernel preprocessing. A
mathematically valid but noncanonical support list cannot inherit this record.

## Attempt To Kill The Apparent Progress

The supply is the main failure. Repeating this baseline until one phase bit
remains, with the usual final one-bit Gaussian stage if necessary, has ideal
original supply(n+1)^(t-1), BEFORE zero filters, source failures and physical
noise are paid. For growing t this is not polynomial and does not improve
known sieve exponents. The stored exact ledger records that failure rather
than advertising near-unit per-level admission as an efficient decoder.

This is therefore a useful implementation baseline, NOT discovery of a new
algorithmic mechanism. Fixed-depth polynomial descent does not solve growing-
depth DHSP, a natural lattice reduction, or final secret recovery. A genuine
advance must reduce supply, retain multiple useful outputs, establish valid
noise/supply composition, exploit structure without a matching classical
recovery attack, or avoid this single-pair architecture entirely.

The algebra would be falsified by any valid disjoint-kernel program for which
C changes under its own selected flip, F fails reciprocity, or the exported
gate evaluator differs from F with clean work. Those are direct executable
checks; complete scalar coarse tables and independent JS replay cover bounded
instances. External theorem review and the growing physical source remain open.

Related primary literature: Imran and Ivanyos,
[Zero sum subsequences and hidden subgroups](https://arxiv.org/abs/2304.08376).
Their nilpotent-HSP work also exploits zero-sum structure; it must not be
imported as a generic noisy-state source inverse. The existing repository
source-access audit retains that distinction.
