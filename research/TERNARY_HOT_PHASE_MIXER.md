# An Actual Hot Phase/Mixer Program, Not A Cold-Parent Extrapolation

LOCAL DERIVATION / REVIEW PENDING. No novelty, accepted algorithm or quantum
speedup. This tests ONE specific hot-stage architecture. General multi-layer
algorithms and label-adapted mixer shapes remain open.

## Circuit With Real Public Access

For native F(x)=sum_i(0,a_i,c_i)[x_i] at q=3^r and a known target y,
start from the KNOWN uniform word state u, not an unknown native state
or its inverse. Let E_y(x) count mismatched full-frequency coordinates.
One layer is

    U_beta exp(-i*gamma*E_y) u,
    U_beta=product_i exp[-i*beta*(I-|+><+|)_i].

Reversibly compute F and E_y, apply the known phase and uncompute scratch.
Then apply M explicit3-by-3 qutrit mixers. Evaluation uses polynomial
public arithmetic, not a phase/preparation/count oracle. Approximate rotations
need a charged whole-circuit error bound; hardware gate export is not supplied.
The finite statevector reference enumerates3^M words and declares that cost.

This is a fiber PREPARATION attempt. Its clean inverse would be a sufficient
decoder ingredient, but high target-fiber membership alone does not imply
uniform amplitudes, coherent phases or clean erasure. The implementation
records both membership and normalized uniform-fiber overlap.

Alternating cost and mixing layers are established ideas, not new:
[Farhi et al.](https://arxiv.org/abs/1411.4028). The following calculation
concerns this actual native source law and this one-layer template.

## Exact Fixed-Angle One-Layer Law

Put D=3^M, G=q^n, and first use a target y uniform over the FULL frequency
group, independent of labels. For any fixed output word z, its contribution
to success selects y=F(z) and has uniform-target weight1/G.

Condition on z as a word, NOT on its realized frequency. For x!=z,
F(x)-F(z) is uniform. For TWO distinct nonself words x,x', their differences
are jointly uniform by the existing pointed2-by-2 unit minor. Thus their
cost phases are PAIRWISE independent, including at composite roots.

Let

    eta=[(1+(q-1)*exp(-i*gamma))/q]^n,
    a=[(1+2*exp(-i*beta))/3]^M.

The mixer is label-independent, fixes u, and has diagonal a. Its row sums
are1 and squared row norms are1. Keeping the self-word cost phase1 gives

    E[uniform-target success]
      =[|eta+(1-eta)*a|^2+(1-|eta|^2)*(1-|a|^2)]/G.

The same argument bounds ANY fixed label-independent u-preserving unitary
after this fixed cost phase: use its own diagonal entry in each output row.
For v=|eta|<=1, triangle bounds give a numerator at most
(1+2*v)^2+(1-v^2)=2+4*v+3*v^2<=9. Therefore fixed-angle one-layer success
is at most9/G, regardless of batch enlargement. This is a population
statement, not an instance-by-instance upper bound.

At gamma=beta=pi every amplitude is rational apart from the known1/sqrt(D).
The producer and independent checker execute complete native populations:
n1/q3/M2 has81 label matrices and243 target cases; n1/q9/M1 has81 matrices
and729 target cases. Both exact mean probabilities agree with the formula.
These include empty fibers, repeated frequencies and zero rows.

## Even Label-Dependent Continuous Angle Tuning Is Not An Escape

Allow each public label matrix AND target y to choose its best gamma,beta.
Both angles have period2*pi. Their objective is Lipschitz: changing angles
by d_gamma,d_beta changes raw success by at most
2*n*|d_gamma|+2*M*|d_beta|, via the norms of the cost and mixer generators.

Use a mathematical net with m points per angle. The nearest point has each
angle error<=pi/m. Since max over a finite menu is at most the SUM of its
nonnegative probabilities, no independence among angle trials is required:

    E[best uniform-target one-layer success]
      <= min(1,9*m^2/G+2*pi*(n+M)/m)
      <= min(1,9*m^2/G+44*(n+M)/(7*m)).

Choose m=ceil(G^(1/3)). This net is EXPONENTIAL and is NOT executed as an
optimizer; it proves a uniform bound on arbitrary public angle tuning.
The resulting success ceiling is poly(n,M)*G^(-1/3), exponentially small
for growing n and polynomial M. Label-adapted mixer SHAPES, arbitrary new
cost functions or additional layers are outside the argument.

## Restore Original Born Weighting

Native fiber weight is p_y=C_y/D, not uniform over occupied fibers. For
ANY public success policy0<=P_y<=1, the pair law gives

    E_uniform(labels,y)[(G*p_y-1)^2]=(G-1)/D.

If its uniform-target mean success is at most s, Cauchy-Schwarz gives

    E_Born[P_y] <= min(1,s+sqrt((G-1)*s/D)).

This applies to the angle-optimized policy despite its dependence on labels
and y. For D>=G and polynomial M, the one-layer Born-weighted bound remains
exponentially small. It does not require frequency counts to be individually
flat or an uncharged target-selection rejection step. The large ledgers keep
exact integers and directed rational square-root bounds.

## Baselines And Positive Controls

Classical uniform-word rejection succeeds with p_y per draw. One Grover
iteration using the membership phase and the KNOWN uniform-state reflection
succeeds with p_y*(3-4*p_y)^2. Generic amplification can be implemented here,
but costs order1/sqrt(p_y); at density near1/G this remains exponential.
See [Grover's primary construction](https://arxiv.org/abs/quant-ph/9605043).
This is a baseline, not a new algorithm or a hardness assumption.

The live16-angle finite menu uses exact PUBLIC target membership to choose
its best simulated circuit. Its classical3^M score enumeration is charged,
not passed off as scalable training or secret-blind inference at large n.
It may produce constant-factor improvements on the small native instance;
the population bound prevents interpreting that as a breakthrough route.

An engineered but ACTUAL native field-root control has F(x)=x at n1/q3/M1.
Matched angles gamma=beta=2*pi/3 prepare its requested word perfectly.
This is a positive scope guard, not a candidate or IID scaling experiment.
A two-layer native control is also retained explicitly OUTSIDE the theorem.
Neither small control supplies a growing-root decoder.

## Decision And Failure Modes

Do not pursue one-layer global-angle residual QAOA as the missing polynomial
fiber compiler. Hot dynamics do not automatically imply useful interference;
their small apparent gains can be exactly bounded and compared with rejection.

The unresolved constructive question is whether MULTIPLE layers exploit
native algebraic dependencies beyond pointed-pair uniformity, or whether
an explicit label-sensitive mixer changes that law. Deeper phase products
involve four or more original words and can have nontrivial affine one-hot
dependencies. Pairwise independence must NOT be promoted to full independence
or a generic many-layer lower bound. A new proposal must identify the useful
dependency and charge its reversible access, not just tune more small circuits.

There is now a concrete nontrivial dependency to investigate, not merely that
warning. Take the five ORIGINAL words0000,0111,1011,1101,1110. The four
differences from0000 have first-row coefficient matrix J-I, determinant-3.
At q=3^r its frequency image has a three-character annihilator:
all four dual coordinates equal k*q/3 for k=0,1,2. For four residual phase
factors at angle pi, the per-frequency-coordinate joint moment is EXACTLY

    ((2-q)/q)^4+2*(2/q)^4,

not the independent prediction((2-q)/q)^4. Complete marginal native first-
row censuses check all81 assignments at q3 and all6,561 at q9; unused second
rows are integrated out, not fixed as a purported full IID source. Across
n independent frequency coordinates the moment is raised to n. A separate
mixed-sign phase calculation at gamma=pi/2 is also exactly checked, retaining
conjugate branch signs and its zero imaginary mean. These words
are native paths, not a new toy oracle, and this correlation does not by
itself yield a circuit advantage. See the next
[path-moment target](NATIVE_MULTILAYER_PATH_MOMENTS_TARGET.md).

Falsifiers: complete exact label census violates the stated mean; the self
word is omitted; a field shadow replaces full-root differences; probabilities
lose normalization; target membership is claimed to be clean erasure; an
adaptive policy inherits a fixed-angle claim without the net argument;
the implicit net is presented as an efficient optimizer; multi-layer or
label-adaptive mixer circuits receive a one-layer no-go flag.

Gemini/Antigravity owns routine CLI/registry wiring and full production
validation. No candidate or speedup is accepted from these controls.
