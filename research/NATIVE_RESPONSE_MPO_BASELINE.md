# Fixed Public Fourier Calls: Paid Exact-Integer MPS Sampling

## Research Decision

Adding a third full cyclic QFT does NOT by itself escape classical approximate
simulation in the public product-response-phase model. The new baseline accepts
any fixed signed phase/Fourier schedule. For FIXED Fourier-call count Q at
inverse-polynomial accuracy, its structural and integer-bit costs are polynomial;
the polynomial degree grows with Q. No arbitrary-depth or unknown-copy quantum
simulation is claimed. This is a baseline, not a secret-recovery algorithm.

CLI: `python qsearch.py native-response-mpo-baseline`.
Artifact: `research/classical_baselines/native_response_mpo_baseline.json`.
Inputs are the SAME original classical observations and public mask used by
the quantum word-phase schedule. Private secrets/errors/preimages never enter.
Do NOT transfer this known phase access to unknown copy-only DCP/HSP states.

## Exact Operator And Physical Ordering

For M MSB-first sites, D=3^M and bandwidth b, the unreversed Fourier kernel is

    K_b(a,w) = D^(-1/2) product_j exp(2*pi*i [a_j*w_j/3
        + sum_(d=1..min(b-1,j)) a_(j-d)*w_j/3^(d+1)]).

An MPO carries the last min(b-1,j) OUTPUT digits before site j. The physical
input w_j and output a_j select the displayed root; the next memory appends a_j
and drops old digits. At the last site collapse memory to the scalar boundary.
Given full a,w exactly ONE virtual path contributes, proving the kernel identity.
Each bond has at most3^(b-1) states; no fitting or dense word table is involved.

F_b=P_reverse K_b: apply the MPO then reverse sites and transpose each MPS
matrix. F_b^dag=K_b^dag P_reverse: reverse FIRST, then conjugate MPO coefficients
and swap PHYSICAL input/output legs. Do NOT transpose virtual bond indices or
reverse after the adjoint. At b=M this is the full cyclic DFT. Product phases
leave bonds unchanged; each MPO multiplies them by its memory size; reversal
only reverses their order. After Q calls, chi<=3^(Q*(b-1)). The actual intermediate
bond lists and allocated tensor entries are preflighted, not inferred from a
headline bound. Stored bonds may be redundant, not minimal Schmidt ranks.

## Exact Paid Readout

Certified dyadic roots have denominator2^P. All denominators and Fourier/initial
normalizations are COMMON global scalars across amplitudes and cancel in normalized
measurements. MPS tensors are pairs of FLINT exact integer matrices. No floats,
SVD truncation, postselection or rare-prefix normalization is used.

Right environments satisfy E_M=1 and E_j=sum_x A_(j,x) E_(j+1) A_(j,x)^dag.
For a selected prefix row l, branch x has row l A_(j,x) and nonnegative integer
mass (l A_(j,x)) E_(j+1) (l A_(j,x))^dag. Children sum EXACTLY to the parent.
Cross-multiply their CDF against an independent K-bit uniform grid draw.

Environment construction uses6M complex matrix products; each sample uses9M
more. Each charges FOUR FLINT integer products plus shape-based scalar-term
upper bounds. Compiler block/scaling work, reversals, root entries, tensor and
environment storage, and observed/bounded integer sizes are separately recorded.
Readout costs O(M chi^3) preprocessing and O(M chi^2) per sample in scalar
arithmetic, with bit costs additional. No process-memory/CPU/hardware certificate
is inferred for every FLINT scratch allocation.

## Global Precision And Full Cyclic Target

Each root approximation has error epsilon<=4*2^-P. An MPO entry contains M
roots, so its error is <=2M epsilon/sqrt(D) when M epsilon is small. Bounding
operator norm by D times maximum entry error gives <=2 sqrt(D) M epsilon,
conservatively relaxed to eta=2D M epsilon. Product phase error<=2M epsilon.
All approximate operator norms are <=1+eta. For S scheduled operations and
S eta<=1/2, final unnormalized state error E<=2S eta. E<1 certifies nonzero
state, and ONE final normalization gives measurement TV<=2E. This is a global
bound, NOT a claim about precision of every rare conditional branch.

Choose P=f+ceil(log2(128 S M 3^M)) and K=f+ceil(log2(8M)). Phase TV and
random-grid TV are each <=2^(-f-2). The exponential3^M in the error estimate
costs O(M+f+log S+log M) BITS, not a dense array. Tensor numerator growth is
polynomial in M,S,P for fixed Q/bandwidth scaling; a conservative bound also
charges virtual summations. Ideal IID bits are required; PRNG fixtures do not
certify them. Root precision and complete-batch work caps fail closed.

For the FULL cyclic target charge EVERY transform, including adjoints:

    truncation TV <= Q*(176/7) sum_(d=b..M-1) (M-d)/3^(d+1)
                  <= Q*(88/7) M/3^b.

Set b=min(M,ceil(log3(64 max(1,Q) M 2^f))) by integer comparisons. Truncation
adds <=2^(-f-2), so total TV<=2^-f. At delta=2^-f, chi=O((QM/delta)^Q).
For FIXED Q and inverse-polynomial delta the tensor/bit costs are polynomial.
This is not practical dominance: degree and constants can be enormous; default
caps reject many full-cyclic profiles. Growing Q or exponential precision are
NOT polynomial under this bound. Cap failure is UNKNOWN, not hardness.

## Verification And Falsifiers

Independent full matrices at small M check all bandwidths, adjoints/reversal,
complete distributions and truncation bounds. Independent JS reconstructs rounded
dense kernels from Machin/Taylor-certified roots, verifies small integer MPS
calibration vectors/sample traces, and recomputes precision/bond/work ledgers.
The64-site product-width control is independently replayed using exact local
vectors and every recorded random draw, without a dense state. The16-site
nonproduct control's outcomes are NOT independently recomputed by JS; its
resource/precision ledger is checked. Large trace integers use hexadecimal
encoding above4096 bits to avoid Python's decimal conversion limit WITHOUT
disabling interpreter safety settings. This is not a formal proof of arbitrary code or
hardware. Falsifiers: wrong MPO kernel/ordering; non-normalizing prefix masses;
violated error/resource ledgers; missing root certificates; private-data leakage;
or a cap interpreted as a negative result.

The fixed-Q result removes a weak exponential-speedup route only in this PUBLIC
product-phase/Fourier family. Different entangling mixers, growing-depth schedules
and robust receivers from UNKNOWN noisy phase-state copies remain research targets.
No new active negative result, speedup candidate or novelty is admitted.
