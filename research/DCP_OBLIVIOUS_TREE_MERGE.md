# Reversible Bounded-Output Join Without Quadratic Pair Materialization

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. No novelty, quantum speedup,
low-level gate export or complete-tree integration is claimed.

Run `python qsearch.py dcp-oblivious-tree-merge`. This supplies a tested
reversible join primitive for the native tree's next backend. It does not
silently replace the independently checked Cartesian baseline.

## Literature And Model

Oblivious equijoins without ORAM already have near-linear implementations;
see Krastnikov, Kerschbaum and Stebila,
[Efficient Oblivious Database Joins](https://arxiv.org/abs/2003.09481).
The contribution here is a local reversible bounded-output construction and
explicit cleanup/cost controls, not a new database algorithm or quantum speedup.

Left and right arrays have PUBLIC fixed lengths p,q. Each row is
(valid,key,payload), with fixed public key/payload wire widths. Payload may
contain the physical support ID and full componentwise signed sum. The key
is one tree chunk on the left and its group inverse on the right. All matching
ROW PAIRS must remain distinct, including duplicate keys or payloads.

Let N be the complete valid equal-key pair count. Capacity C is public.
If N<=C, output every pair in deterministic (key,left-index,right-index)
order, padded with invalid rows to E=min(C,p*q) slots. If N>C, output ONLY
invalid rows and set an overflow XOR wire. Copy into arbitrary target wires,
then reverse ALL work. The diagnostic N printed by the basis interpreter is
not an extra freely accessible coherent count register in the phase protocol.

## Four Fixed Sorting Networks

1. Sort the p+q input rows (with public power-of-two padding P) by key, side
   and original index. All equal-key left rows precede all matching right
   rows. A forward prefix scan records group left/right counts and starts.
   A second scan adds l*r ONCE at the end of each complete key group. Keep
   all prefix states. Do not stop at C or erase unmatched rows.
2. Give every positive-size group its pair-rank interval [s,s+l*r). Merge
   these descriptors with the fixed E requests j=0,...,E-1 by sorting on
   rank, with descriptors before requests at equal rank. A prefix scan
   broadcasts the latest descriptor. When s<=j<s+l*r, the requested pair
   has source indices

       left_start + floor((j-s)/r), right_start + (j-s) mod r.

   These indices are computed DATA FIELDS. They are NEVER Python array
   addresses in the interpreter. Invalid ranks use a dummy address and an
   explicit disabled flag; division by zero is never required. A bit-level
   implementation can mask the divisor to1 on a disabled branch.
3. Put all source records (keyed by their sorted index) and all lookup
   requests into a fixed fetch array. Sort by address, sources before
   requests. A prefix scan broadcasts the last source payload to every
   matching request, including repeated requests. This replaces RAM reads
   with a paid oblivious multi-lookup. A source payload is a computational
   function of the original input; copying it does not clone unknown phases.
4. Turn the fetched responses into rows keyed by output ID2j or2j+1 and
   sort again. Every real request has a unique output ID even when disabled,
   so fixed adjacent slots now supply the left/right payloads for output j.
   Overflow suppresses the whole output before XOR-copy. Reverse response
   sort/compute, fetch scan/sort/compute, requests, rank scan/sort/compute,
   descriptors, group-count scans and finally the input sort/compute.

Every pointer chase has therefore become a fixed sorting/scanning schedule.
All loops and buffer lengths depend only on public lengths/capacity, not on
keys, match counts or success. Conditional arithmetic computes bit fields;
it does not grant variable-address coherent memory or erase records.

## Correctness And Cost

The key sort partitions every valid row into exactly one equal-key group.
Each positive group owns a disjoint rank interval of length l*r. Euclidean
division by r is a bijection between its rank offsets and its Cartesian
row pairs. The rank scan chooses the unique containing interval. Address
sorting then supplies exactly the requested source payloads, and output-ID
sorting restores fixed output order. Thus there are no missing/duplicate
pairs on a nonoverflow input. On overflow the primitive rejects; it does not
claim a complete join or transfer a silent-truncation source bound.

Let P be the least power of two >=p+q, R>=P+E, F>=P+2R. Exactly four bitonic
sorts have sizes P,R,F,F, each reversed once. Forward scans use2P+R+F steps
and are reversed once. All buffers, prefix histories and compare flags are
charged in schedule(); no hidden input-dependent allocator or count oracle.
At fixed record widths, both time and retained coherent histories are
O((p+q+C)*log^2(p+q+C)), rather than quadratic Cartesian materialization.
The reported counts are record/comparator/scan operations, NOT physical gates;
bit-level comparison, division and arithmetic add polynomial wire/gate factors.

The actual native tree still uses the Cartesian reference. Once integrated,
this primitive would change the conservative large-b record exponent from
4n/(a+1) to2n/(a+1) at fixed a, modulo public cap factors and polynomial
overheads. That is a CONDITIONAL implementation target, not a measured
complete receiver exponent, a new known-best sieve or a breakthrough.

## What Could Invalidate Its Use

Passing a join test alone does not establish the native source moments or
the final quantum instrument. The tree wrapper must reject the entire attempt
on ANY node overflow, retain/correctly erase all node outputs and overflow
flags, and keep the reciprocal six-call check. Cap failure can differ across
partner endpoints. Capacity must meet the earlier source bound if that bound
is claimed. Actual noise remains v^(physical mask weight), and one-output
recursive supply remains unchanged.

The primitive's sorted output order differs from the Cartesian baseline's
support-ID compaction, but on nonoverflow inputs their full physical support
sets must agree. On overflow both wrappers must reject the whole attempt;
their partial contents must never receive acceptance credit.

## Gemini Integration Contract

Keep the Cartesian interpreter as an independent reference. Add an explicit
backend, not an invisible change to an old certificate. Encode each child
payload as support | (packed_full_sum << m); use componentwise-negated chunk
keys on the right. Keep returned left/right payload pairs until their combined
parent record can be erased. To reverse a node, erase that parent record then
call join_xor again with its previous target and overflow wire. Charge both
calls, live node payloads, input-key conversion buffers and transient join
histories. The whole-tree live workspace is NOT the sum of transient peaks
when work is reused, but is also NOT just the final root list.

Compare both backends against full native graphs on nonoverflow inputs,
asymmetric overflow, all-zero labels, padding, arbitrary XOR targets and
original unknown-phase densities. Only then update the complete-tree resource
frontier. No central candidate or negative-result promotion is authorized.
