# Native Full-Label Coherent-Edge Receiver

LOCAL DERIVATION / REVIEW PENDING. No novelty, polynomial-time learner,
accepted candidate or new quantum speedup is claimed. This is a constructive
alternative to the ordinary two-witness helper, with exponential search cost.
It changes a receiver interface, not the asymptotic algorithmic conclusion.

## Source And Public Predicate

At q=3^r, take M=n*r-2 original native qutrits, with two IID uniform full
frequency rows a_i,c_i in Z_q^n per register. Let D=3^M, G=q^n=9D, and

    F(x)=sum_i (0,a_i,c_i)[x_i] modq,
    |psi_s>=D^-1/2 sum_x chi_q(F(x).s)|x>.

For target coordinate j and Q=q/3, an offset d in F_3^M minus{0} is marked
at x iff F(x+d)-F(x)=+Q*e_j or -Q*e_j modq. There are A=D-1 offsets;
pad the public index register to P=2^ceil(log2(A)). Index l<A maps to the
base-three digits of l+1; padding never marks. Arithmetic evaluation and
unranking cost polynomially many operations on n,r-bit-size registers.
Full target-high labels ARE used. Therefore the low-only solver's
beta-to-4beta transfer theorem does NOT apply to this receiver.

Keep x coherent. Reflect ONLY the public offset register about its uniform
state, after a clean controlled phase predicate. One shared independently
sampled public Grover time is used for every x. Herald a marked edge at the
end. On rejection or schedule abort, return a uniform trit and charge all
consumed states and time. No degree oracle, source reflection, unique partner,
classical pair algorithm or explicit full table is granted.

## Native Orientation And Clean Workspace

Ternary translation has order THREE. Binary XOR orientation is not valid.
Choose the canonical sign of d by making its first nonzero trit1. For input
(x,d), copy e=1 iff that first trit is2. If e=1, translate x by the ORIGINAL
d, then negate d. The paired directed edges

    (x,d_canonical), (x+d_canonical,-d_canonical)

now share (representative=x, canonical offset=d_canonical) and have opposite
orientation bits. On the full basis this is a reversible sequence of a bit
XOR, controlled native translation and controlled index negation; padding is
fixed. The implementation supplies the inverse and exhausts bounded basis
controls. Arithmetic scratch MUST be uncomputed. Original offset tags differ
between endpoints; retaining them erases the useful interference.

The common representative/canonical index may be measured. Compute
delta=(F(rep+d)-F(rep))_j/Q in{1,2} from those COMMON data. Embed the orientation
bit in qutrit levels0,1 (level2 has amplitude0), apply inverse F_3, and return
delta^-1 times the outcome. No unknown secret enters this recipe.

## Unconditioned Born Score

Let q_x be the informative offset degree at x and theta_q=asin(sqrt(q/P)).
After t Grover iterations each marked offset amplitude is the REAL number

    g_t(q)=sin((2t+1)*theta_q)/sqrt(q), g_t(0)=0.

Endpoints can have different degrees and amplitudes, including opposite
signs. For an unordered informative edge, the correct trine probability is
(g_x^2+g_y^2+2*g_x*g_y)/(3D). Including uniform guesses on rejection gives,
for EVERY fixed full secret (including zero and nonprimitive secrets),

    raw_correct_probability = 1/3 + G_t/3,
    G_t = D^-1 sum_(x,d marked) g_t(q_x)*g_t(q_(x+d)).

This is NOT normalized by herald success. A fixed time can yield negative
interference. The same-time cross-endpoint kernel, not ordinary search
success, is the relevant quantity.

## Positive Shared-Time Kernel And Native Population

Reuse the exact kernel derived and tested in
[the DCP workbench](DCP_COHERENT_EDGE_READOUT.md). With h=ceil(log2(P)/2),
p=2^-h, rho=1-p, choose t with probability p*rho^t. Put u=q_x/P,v=q_y/P,
a=p^2, b=a+4*rho*(u+v-2uv). The infinite averaged cross kernel is

    K=(a/P)*(a+8rho-4rho*(u+v)) /
      (b^2-64*rho^2*u*v*(1-u)*(1-v)).

It is nonnegative for all positive degrees; for degrees<=C and P>=2C it is
at least1/(1+8C)^2. This reuses the kernel, NOT any DCP noise assumption.
Only the clean native source is covered here.

There is a direct algebraic positivity check, without subtractive floating
trigonometry: the denominator equals

    a^2+8*a*rho*(u*(1-v)+v*(1-u))+16*rho^2*(u-v)^2 >0.

The numerator factor a+4*rho*(2-u-v) is positive too. The independent checker
verifies this exact identity on every retained degree pair. The general
identity supplies the all-degree positivity argument; finite grids alone do not.

For any fixed x and nonzero d, a native simplex difference has a unit
coefficient, so its full frequency difference is uniform. For two distinct
offsets, the two pointed simplex difference rows have a determinant +/-1
minor (the existing native pointed-triple lemma). Hence the two differences
are jointly uniform even over the composite ring Z_(3^r). The events taking
either of the two useful values are pairwise independent. Consequently

    lambda=2A/G,
    E[q_x^2]=lambda^2+lambda*(1-2/G).

For every undirected graph, the oriented edges incident to a degree>C vertex
have normalized mass at most(2/C) times the second degree moment. At C=8,
the expected mass with BOTH degrees<=8 is therefore at least

    lambda - (1/4)*(lambda^2+lambda*(1-2/G))
    >=lambda*(3-lambda)/4 >=5/36, for n*r>=5.

The last bound uses1/5<=lambda<=2/9. No vertex selection/counting is performed;
nonnegative kernels allow all other edges to remain. Averaged over ALL IID
native labels and public schedule draws, the infinite interference is at
least1/30420, for every secret. This is not a pointwise guarantee for labels.

Abort at T=B_tail*2^h without resampling. Since |G_t|<=1 by Cauchy-Schwarz
and edge symmetry, clipping loses at most rho^T<=2^-B_tail. With B_tail=16,

    raw_trit_advantage >= (1/30420-1/65536)/3 >0.

This conservative constant says nothing about practical efficiency. Mean
predicate compute/uncompute calls<=2^(h+1)-1, worst-case<=2T-1, in addition
to public time-coin draws and polynomial arithmetic factors. Because
P is comparable to3^(n*r-2), time remains O(3^(n*r/2)*poly(n,r)). Space in
the reversible recipe is polynomial; dense finite calibration arrays are
NOT its implementation memory. Hardware gate export is not implemented.

## Interpretation And Attempted Refutation

Simply making THIS generic Grover template short cannot preserve constant
signal. For t<=T, |sin((2t+1)*theta)|<=(2t+1)*sin(theta), so every marked
amplitude has magnitude<=(2T+1)/sqrt(P). For every label instance this bounds
|G_t| by its oriented mean degree times(2T+1)^2/P. Averaging over ALL native
labels gives raw trit advantage at mostlambda*(2T+1)^2/(3P), capped at2/3.
This includes label-dependent shared time choices under the same hard cap.
At T=(nr)^2 and growing nr, the upper bound is exponentially small. It covers
only the unchanged clean public-index Grover predicate/reflection template,
not modified oracles, new preparation, walks or general quantum measurements.
The live scaling ledger records this restricted bound with explicit scope.

- Classical two-witness solving is not necessary for THIS alternative
  receiver. Its removal does not remove the exponential search.
- Full-label access is essential; do not apply low-only label-information
  bounds or low-only classical transfer factors to this operation.
- Endpoint-dependent time coins, dirty scratch or a retained source-word
  measurement invalidate the interference argument. Countercontrols retain
  an original-index tag and recover only chance-level raw trit correctness.
- Predicate pairwise independence is a native unit-minor argument, not an
  IID random graph assumption. Edge correlations beyond pairs are not erased.
- The population proof is for clean IID full native rows, not selected labels,
  noisy classical records, or arbitrary higher-root state preparation.
- The n*r>=5 bound does not supply the lower-root cases of full bootstrapping.
  Even completing them would yield an EXPONENTIAL decoder, not the missing
  polynomial-time weak learner.
- Native source acquisition, precision synthesis, noise tolerance, theorem
  review and novelty are independent unresolved obligations. No source
  reduction to vector DHSP is supplied here.

## Structure Worth Exploiting, Access Not Granted

The native graph is NOT a generic graph. Fix the nuisance syndrome S and
partition its original words by target-high value h=0,1,2. With class sizes
c_0,c_1,c_2 and C=sum(c_h), every different-class pair is an informative edge
and no same-class pair is. Thus each fiber is complete tripartite, with
degree C-c_h in class h. In its uniform-class basis the adjacency is only

    B_hk=sqrt(c_h*c_k) if h!=k, B_hh=0,
    det(zI-B)=z^3-(c_0*c_1+c_0*c_2+c_1*c_2)*z-2*c_0*c_1*c_2.

This is an exact structural compression, not efficient coherent access to
the basis. The source already lies in this class-uniform span. IF its unitary
compression were supplied, an inverse F_3 readout would have raw correctness

    (1/(3D))*sum_S (sum_h sqrt(c_h))^2.

This agrees with the existing information-only least-trit optimum, not a
new measurement theorem. The finite audit reconstructs the original
adjacency from the uniform-class incidence factors and records exact cubic
coefficients, degrees and class lists. These exponential tables are NOT
passed to the actual edge receiver. The promising question is whether
native additive structure permits this compressed access without tables.

The tempting shortcut is explicitly costed. Compute full F reversibly,
then project every original word qutrit onto the PUBLIC uniform state.
Its Kraus map is K|x>=|F(x)>/sqrt(D); for a class-uniform input it has singular
value sqrt(c_h/D). On the original phase source its raw success is

    sum_(S,h) c_h^2 / D^2.

The FULL IID label-law mean, using Pr[F(x)=F(y)]=1/G for x!=y, is

    E[success]=1/D+(D-1)/(D*G), G=9D.

This is exponentially small, approximately10/(9D), despite tiny compressed
blocks. Normalizing this successful branch for free is invalid. Generic
singular-value amplification/inversion must address the native singleton
scale1/sqrt(D); a dimension-three block does not itself remove this burden.
No lower bound against structure-aware transformations follows. See the
[next research target](NATIVE_TERNARY_CLASS_ACCESS_TARGET.md).

The implementation also evolves the actual native word/full-label state
through inverse F_3 gates on EVERY original qutrit, then reads the all-zero
word outcome. The full output amplitudes match c_h*chi_q(F.s)/D and the raw
success above, with all other outcomes charged as failure. This is a finite
unitary calibration, not a coherent class-inverse compiler.

Source-weighted trimming does not cure this PARTICULAR normalization. If X
is a uniformly weighted original word, its class size c(F(X)) obeys

    E_labels,X[c(F(X))-1]=(D-1)/G <1/9.

Thus the mean source mass in singleton full-frequency classes is at least
1-(D-1)/G >8/9. For any K>=2, the mean mass in classes of size>=K is at most
(D-1)/(G*(K-1)), by Markov on c-1. Requiring erasure singular-value square
c/D>=tau keeps only K=ceil(D*tau) classes; at inverse-polynomial tau=1/(nr)^2
its retained source mass is exponentially small at growing roots. If all
discarded outputs are guessed uniformly, raw trit advantage is at most
two-thirds that mass, EVEN granting a class filter. The live scaling ledger
records this exact upper bound. This does not address alternative operator
normalizations, coherent reuse of discarded sectors, or general receivers.

Exact full-root translation controls separately check all per-wire cycle
increments a,c-a,-c. Ordinary F_3 word characters for EVERY secret require
c=2a and3a=0 modq, with IID probability3^(-n*M*(2r-1)). Scalable native
arithmetic controls reach r64 without enumerating native words. A simple
modulo-three match does not establish the full-root conditions. This is not
a no-go against nonlinear/coherent Fourier constructions or graph-specific
transforms; an empty graph may be translation invariant while F is not.

Known search with unknown solution count is established in
[BBHT](https://arxiv.org/abs/quant-ph/9605034). Existing DHSP benchmarks include
[Regev's polynomial-space subexponential algorithm](https://arxiv.org/abs/quant-ph/0406151)
and [Kuperberg's later subexponential algorithm](https://arxiv.org/abs/1112.3333).
This exponential construction is NOT asserted to improve either. These
references are context, not a literature novelty clearance for this adaptation.

## Live Controls And Next Decision

Run `python theorems/ternary_coherent_edge_receiver.py --write`.
The report contains exact population/cost certificates through n*r=64,
all ordered pointed triples at native width2, an exhaustive729-pair original
label census at n1/r3/M1, complete positive-degree kernel controls at P8,32,128,
and prespecified IID native physical cases. Actual oracle/reflection dynamics
are compared with the trine Born score and the exact averaged kernel.
Seeded cases are calibration, not an empirical population-performance theorem.

The next useful target is replacing generic edge search with a charged
structure-aware transformation that retains cross-endpoint coherence. A
polynomial classical degree table, free inverse state preparation, uncharged
QRAM, or fast-forwarded Grover oracle is not a solution. Prefer a provable
algebraic factorization of the native predicate, a multiscale coherent
collimation scheme, or a different collective measurement. Require fresh
native-source coverage and an end-to-end complexity ledger before promotion.
