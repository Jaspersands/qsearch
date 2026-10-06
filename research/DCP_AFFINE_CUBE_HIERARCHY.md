# Native Affine-Cube Hierarchy And The Clean-Tail Target Critique

LOCAL DERIVATION / REVIEW PENDING. No independent mathematical review, novelty,
accepted candidate, full decoder or speedup. These gates concern physical affine
blocks compressed into a secret-independent CLEAN tail. That restriction is
not necessary for a general DCP decoder; the countercontrol below proves it.

## Revised Research Decision

The preceding two-plane bound becoming vacuous at higher density does NOT
establish a viable clean-affine-tail architecture. Larger cubes close several
such escapes. For instance, n16,q=2^65,m1300 has clean rank-one terminal-tail
acceptance at most2^-62; at m2080 the bound is2^-14. At n32,density2 it is
2^-126, and at n64,density2 it is2^-511. These are mathematical source bounds,
not simulated decoder performance. All require independent proof review.

At every FIXED density rho>1, choosing a sufficiently large constant cube
dimension yields an asymptotic exp(-Omega(n^2)) clean-affine-tail bound in the
q=2^(4n+1) regime. Constants depend on rho; the finite gate can still be
vacuous. A separate deterministic rank gate handles large physical tails and
gives source bounds below2/3 even at polynomial-growing density in the recorded
profiles. It does NOT rule out rank-two targets or general decoding.

However, the most important correction is positive: a decoder needs a readable
residue register, NOT necessarily fixed clean junk. The next research task is
phase separation, not another round of clean-tail no-go calculations.

## Parity-Incidence Inverse

For an r-dimensional physical affine cube through an anchor, each coordinate
has an r-bit direction pattern. Let D be its distinct NONZERO patterns, h=|D|.
Independent directions imply h>=r. For each pattern p, the signed sum S_p of
native modular labels on that nonempty coordinate group is uniform modulo2^a.
Different groups and output rows are independent. Signs from the anchor are
units and preserve this IID law. Empty patterns are not assigned fresh sums.

Let P be the (2^r-1)-square integer matrix indexed by nonzero x,p with
P[x,p]=parity(x.p). Its row dot products give the exact identity

    P*(2P^T-J) = (2P^T-J)*P = 2^(r-1) I.

Flatness means P*S=0 modulo2^a, after putting unused pattern sums to0. Therefore
each active S_p must be divisible by2^max(a-r+1,0). The flatness probability
is at most2^(-n*h*max(a-r+1,0)). This is NECESSARY, not a sufficient condition.
It preserves the nonzero two-adic torsion solutions that naive rational rank
would lose. The explicit P is bounded calibration only, not the scaling code.

## Count Cubes Without Enumerating Patterns

For each h, there are at most binomial(2^r-1,h) pattern sets and(h+1)^m column
assignments. Actual groups must all be nonempty and span F2^r; overcounting their
NUMBER is allowed, but no claim is made about probabilities of the extra empty
assignments. Each cube has |GL_r(F2)| ordered bases, so divide by that count.

Use binomial(2^r-1,h)<=2^(r*h), |GL_r(F2)|>2^(r^2-2), and the decreasing ratio
log2(h+1)/h for h>=r. Let p=ceil(log2((r+1)^t)), with precision t=32, and put

    A = n*max(a-r+1,0) - r - ceil(m*p/(t*r)).

If A>=1, summing the geometric tail over h>=r gives a source-mean incident-point
bound <=2^(3-r*A-r^2). Uniform parity-kernel points and accepted-prefix
conditioning cost at most2^(n+2), exactly as in the preceding terminal note.
Thus the saved conditioned exponent is

    b = max(0,r*A+r^2-n-5), if A>=1; otherwise b=0.

There is no exponential pattern menu, cube vertex table, secret simulation,
floating logarithm or uncharged chart search in this evaluator. Passing to
full source data does NOT prove that a particular packet lacks global cubes.

For fixed rho choose constant r with rho*p/(t*r)<1. Then A=Omega(n^2) at
m=ceil(rho*n*(4n+1)), a=4n+1. The argument does not assert that the resulting
finite bound is useful at every n or at polynomial-growing rho.

## Cube-Free Fiber Caps And Quantum Compression

Let f_r(d) bound the largest subset of F2^d containing no affine r-cube. For
nonzero v, A intersect(A+v) consists of paired points. Quotienting by v gives
a subset of F2^(d-1) without an affine(r-1)-cube; otherwise its full inverse
image is an r-cube in A. Counting all ordered pair differences gives

    f_r(d)*(f_r(d)-1) <= 2*(2^d-1)*f_(r-1)(d-1),
    f_1(d)=1.

The implementation includes the integer-root recurrence for bounded controls.
For large d it uses the conservative proved induction

    f_r(d)/2^d <= min(1,2*2^(-(d-r+1)/2^(r-1))).

Indeed the root bound gives alpha_r(d)<=2^(-d-1)+sqrt(alpha_(r-1)(d-1)); the
claimed constant2 absorbs the additive term for d>=r>=2. The integer ledger
rounds this UP using max(0,floor((d-r+1)/2^(r-1))-1). r>d is inconclusive.

Outside the incident-point set, every residue fiber in a physical affine
d-bit block is cube-free. The uniform-secret averaged phase density has
eigenvalues equal to fiber multiplicities/2^d. A clean rank-R compression has
acceptance at most R*f_r(d)/2^d + incident_point_fraction. Known diagonal phases
and block-local unitaries cannot improve those eigenvalues. Entire ancillary
projector rank must be charged. Unrestricted CPTP reset can dump information
into trash and is NOT the rank-one operation bounded here.

The actual terminal tail is d=m-n*log2(q), not a fixed16 bits when packet
density increases. At fixed rho>1, d=Omega(n^2), so both cap and source terms
decay exp(-Omega(n^2)). This is a clean-reference architecture result only.

## Dense Half-Width Rank Gate

For actual independent binary parity rows B, let z count zero columns. Take
ANY physical d-dimensional W inside a parity kernel/coset. The first carry bit
is quadratic on W, with scalar polar matrices

    M_l[u,v] = sum_i B_li*u_i*v_i mod2.

These matrices are alternating because B*u=0 for every direction u. No higher
labels or linear terms can remove their ranks. On active coordinates the formal
weights h_i(T)=sum_l T^l B_li are nonzero. Over F2(T), diag(h_i) is nondegenerate.
The active projection of W has dimension at least d-z, so restriction rank is
at least g=2d-m-z. But the restriction equals sum_l T^l M_l, whose rank is at
most sum_l rank(M_l). Constant binary-matrix ranks are unchanged by extension.
Thus SOME actual scalar row has even rank at least

    2*max(0,ceil(g/(2n))).

This field extension is a rank PROOF, not an imported physical oracle. There
need not be a full-support binary row: column types10/01/11 provide an explicit
counterexample to that unjustified assumption. Generic nondegeneracy is enough.

A scalar quadratic with alternating polar rank2h has any value mass at most
1/2+2^(-h-1). One derivation squares its character bias and sums over the polar
radical; the bias is either0 or2^-h. Every full-modulus fiber is contained in
such a scalar carry fiber. This bounds clean rank-one acceptance for EVERY
physical affine block of the given dimension, on this PARTICULAR B. It is
still a uniform-secret mean, not a pointwise-secret success bound.

For native accepted-prefix packets, tail zero-column count has mean(m-n)/2^n.
Allow z<=floor((2d-m)/2), and charge its failure by Markov rather than filtering
away all zeros. The live n8/16/32/64 density3, n64 density4 and n64 density64
profiles all have conservative source-mean acceptance below2/3. Adaptive
original-pool selection cannot borrow this IID zero-count law; scan its actual
B with the deterministic gate or derive the selected source law.

## Prove The Target Assumption Wrong

The actual packet A=(1,1,2,4,2,4),q8 has a public permutation with

    F(P(t,j))=t+c(j) mod4,
    c(j)=j0+j1+2*j2 mod4.

The state FACTORS into a correct Fourier phase register on t and unknown
secret-dependent junk phase on j. The t QFT succeeds for EVERY secret with
probability1. Yet uniform-secret mean projection onto flat junk is only1/4.
All128 independent-target/reference/junk witness controls also succeed, as
predicted by the existing exact two-forward-call arithmetic baseline.

This is not a scalable native algorithm: the literal label table conditional
on prefix acceptance has probability2^-17 at this bounded size. It exists to
falsify our own unnecessary clean-junk target, NOT to add a toy candidate.
It shows why the negative geometry gates cannot reject phase separation.

Revised positive target: construct polynomial reversible P with F(P(t,j))-t
independent of t, or sufficiently concentrated offset buckets, while allowing
unknown junk. The existing offset-collision certificate directly measures the
actual mean readout success. An efficient CLASSICAL implementation would also
solve independent arithmetic challenges: that is a legitimate potential DCP
contribution through known reductions, not a classical simulation of the input.
Quantum-only evaluators retain quantum rather than classical access accounting.

## Falsifiers And Next Work

- Incorrect incidence inverse, a forgotten active pattern, undercounted bases,
  or invalid parity/prefix conditioning would invalidate the cube source bound.
- A cube-free set exceeding the recurrence, or a false quotient argument,
  invalidates the cap/compression bound. Small subsets are exhaustively checked.
- A physical parity block violating the actual polar-rank floor would invalidate
  the half-width gate. The tests cover4,371 small kernel subspaces and zero cases.
- Clean-tail gates do NOT cover unknown junk, nonlinear physical blocks,
  interblock mixing, or branch-conditioned operations after secret-informative
  measurements. Those require actual decoder/source proofs, not rejection here.
- Completed-packet menus and original-state regrouping must be charged. The
  n32 density2 menu of n^4 completed packets retains2^-531; regrouping a pool
  of n^4 original states makes the recorded cube bound inconclusive.

Do not continue accumulating clean-tail no-go reports. The current evidence is
enough to redirect effort toward compact additive phase separation, independent
target arithmetic, and genuinely quantum operations that avoid its classical
evaluator requirement. A proof of a native conditional higher-carry invariant
or an efficient phase-separating inverse is still missing.

## Evidence And Literature Scope

Module/test/report stem: `dcp_affine_cube_hierarchy`.
Independent checker: `research/certificates/dcp_affine_cube_crosscheck.js`.
It checks1,245 integer inverse entries,16,896 complete modular pattern tables,
8 scaling ledgers,702 cap recurrences,3 physical polar profiles,6 dense-source
ledgers,4 fixed-secret QFT controls,128 witnesses,2 selection ledgers and5 hashes.
These are implementation checks, NOT independent mathematical review.
All124 focused cube/terminal/Schur/source/pivot/carry/normalizer/dense regression
cases pass in27.66s, including24 new cases. Python/JS syntax, JSON parsing and
whitespace checks pass. Full production/qsearch validation is not claimed.

[Kurz's Divisible Codes text](https://arxiv.org/pdf/2112.11763) supplies relevant
Hamming-weight divisibility context. Its ordinary weight hypotheses do not
automatically apply to native signed modular labels. In particular A=(1,q-1)
has a zero weighted sum of Hamming weight2; no unweighted minimum-support bound
is imported here. The rank, counting and compression arguments above are local
derivations, not attributed to that text or claimed novel.
Routine registry/CLI/UI wiring and full production regressions remain Gemini work.
