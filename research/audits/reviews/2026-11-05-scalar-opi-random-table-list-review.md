# Independent review: native random-table OPI list sampler

5 November 2026. Mathematical and local-source review of
`research/SCALAR_OPI_RANDOM_TABLE_LIST_SAMPLER.md`. No numerical experiment,
quantum implementation, Git operation, or external-service action was used.

**Conclusion:** the stated source-specific composition is mathematically
supported. STATE may cite it as independently reviewed, incorporating the
Fourier-definition and global error-budget corrections below. No novelty,
classical hardness, runtime separation, or finite-instance advantage follows.
The conclusion is for fixed R in (0,1), q=2^t, m=q-1, k=floor(Rm), effective
public field arithmetic, and independent uniform q/2-element FULL input
tables. It is not a worst-case-table or compact-oracle theorem.

## Second moment and the instance quantifier

Equations (1)-(2) are exact/valid as stated. At one row, two distinct field
symbols receive equal signs with probability (q-2)/(2(q-1)), whereas equal
symbols agree certainly. For independent uniform codewords their difference
is uniform in C. Expanding the resulting product uses only the exact MDS
rank identity Pr[D_J=0]=q^(-min(|J|,k)); it does not assume independence of
all codeword coordinates. Subtraction of (r+a/q)^m=1 leaves exactly the
nonnegative j>k terms in (1).

The maximum-pattern failure implies chi2>delta^2/2^m, giving the stated
Markov bound 4^m/(delta^2 q^k). For the chosen delta_m, both delta_m and
the bad-instance probability decay exp(-Omega(m log m)) at fixed positive
R. This really is a simultaneous relative-count event for EVERY Boolean
pattern of the ONE supplied instance. It bounds Z and the total-variation
change for every nonnegative Boolean weight, including weights chosen after
the tables are known. It supplies no efficient conditional-count or inverse
sampling operation.

The explicit worst-case control is valid: take a full-support dual
codeword y (the nonzero GRS multipliers suffice), and set
S_i={x:Tr(y_i x)=0}. Each table has size q/2, but for all c in C,
product_i h_i(c_i)=(-1)^Tr(sum_i y_i c_i)=1. Every odd-parity pattern then
has count zero. Thus the IID source assumption cannot be dropped.

## Paid sampler and source checks

Use the explicit convention

    hat(h_i)(y)=q^(-1) sum_x h_i(x)(-1)^Tr(xy).

These are the Fourier coefficients of h_i, equivalently the quantum
Fourier amplitudes of the normalized phase state h_i/sqrt(q). They are
NOT the unitary Fourier transform of an unnormalized sign vector.
Balancedness gives hat(h_i)(0)=0 and sum_y |hat(h_i)(y)|^2=1. Consequently
the note's shell-normalized A_y have Z0=1 exactly. The trace pairing gives
H=B^T, F(h(Bz))=sum_y A_y (-1)^Tr(z dot Hy), and

    Z=sum_s |sum_(Hy=s) A_y|^2.

No field-size factor is missing. Characteristic two makes the two Fourier
sign conventions coincide. Its trace transform is implemented using
Hadamards and the computable, nonsingular trace-pairing basis change.

The local Jo source, Sections 3-5, explicitly supplies the Fourier grouping,
complete syndrome-list indexing, global padding, and projection identity.
Theorem 4.2 states a deterministic complete decoder for EVERY finite field;
Lemma 4.4 proves the bound J in (5), including J<=m^2, by selecting exactly
u agreement positions for each codeword. The dual GRS code has dimension
m-k and distance k+1, so (4) is the correct strict Johnson condition.
Rescaling GRS multipliers preserves Hamming distance. Shell filtering may
retain zero-amplitude elements, which is harmless; every nonzero-amplitude
element must be retained. One valid candidate is not a complete list.

The global padded L and match flag give precisely success Z/L. Empty
lists, invalid slots, phases, and reversible workspace are covered by the
construction. At the fixed margin, L is bounded independently of m.
Full-table circuit compilation, subset preparation, field arithmetic,
complete decoding, canonical sorting, and their reversals cost polynomial
time/space in the explicit input length. Even polynomial dependence on q
is legal here. This review checked the all-field decoder statement in Jo;
it does not constitute an implementation or an independent proof of the
underlying cited decoding theorem. Sun--Wootters's prime-field capacity
claims are not used as a decoder for this binary extension-field source.

## Score, bounded clock, and perfect witnesses

The Boolean-shell recurrence yields (6) with the displayed factor
1/(m(w+1)). Its limit is 1/2+sqrt(alpha(1-alpha)). The all-pattern event
transfers the score law with the stated total-variation error. Choosing a
fixed strict Johnson margin depending on a fixed 0<epsilon<1 proves (7)
for all sufficiently large m. Larger epsilon gives a trivial weaker claim.
The mean-to-success argument gives probability at least epsilon/2 per
successfully flagged draw once its mean is at least beta_J-epsilon/2.

The accepted GLOBAL budget removes any per-draw/total-error ambiguity.
On delta_m<=1/2, take

    S=ceil((2/epsilon) log(4/eta)),
    A=ceil(2L log(4S/eta))

attempts per requested draw. Each attempt succeeds with probability at
least 1/(2L). The union of all capped-draw aborts has probability <=eta/4;
failure of the score target has probability <=eta/4. Allocate total
unconditioned circuit error <=eta/4 across ALL S*A attempts. This controls
the final transcript without dividing errors by a selected branch's
probability. Including bad source instances adds delta_m^2. Fresh quantum
runs use the same fixed classical tables; no fresh IID table assumption is
introduced. The clock is polynomial even on bad source instances.

For fixed R>3/4, ell=floor(m/2) still has a fixed Johnson margin. Since
m=q-1 is odd and w=O(log m)=o(sqrt(m)), uniformly over the shell band,
binom(m,ell-j)=(1+o(1))binom(m,ell). Therefore

    2^(-m) F(1)^2 ~ (w+1) sqrt(2/(pi*m)).

The actual perfect-pattern probability differs multiplicatively by
(1+e_+)/Z=1+O(delta_m). Thus
O(sqrt(m)/(w+1) log(1/eta)) flagged draws find an exactly perfect witness.
Use the same capped-attempt construction with this number of draws and
allocate synthesis error globally. Ordinary native evaluation verifies
perfectness. This proves the strict R>3/4 corollary; it does not establish
a new perfect-search primitive or optimality of that threshold.

No substantive counterexample or missing algebraic dependency was found
inside the stated source and resource model. The unresolved comparison is
the performance of polynomial-time classical algorithms on these same full
random tables. The count theorem and the quantum construction do not bound
those classical algorithms.
