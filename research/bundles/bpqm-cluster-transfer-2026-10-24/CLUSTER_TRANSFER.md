# Quantum Decoding And Classical Cluster Mobility

Status: LOCAL UNREVIEWED derivation with an exact rational certificate and
finite implementation controls. No independent review, new quantum algorithm,
general classical lower bound, or mixing-time separation is claimed.

## Scientific Question

Does the rank-aware affine-cluster competitor actually make macroscopic
equilibrium moves on the SAME signed (3,6) socket ensemble used by the binary
BPQM hypothesis? Earlier nonstationary trajectories cannot answer this.
Nullity is also insufficient: a one-dimensional kernel can flip every spin.

This pass establishes a structural bound. At c=tanh(beta)=13/20, under the
planted equilibrium ensemble, a step changing at least n/50 spins has probability
at most

    u_n = min(1, (n+1)(6n+1)(99/100)^n).

This is a theorem of the stated local derivation, not a fitted decay rate. A
98-interval certificate checks the needed continuum inequality using rational
integer powers, not floating entropy evaluations. Conditional on average
quantum BLOCK decoding error at most delta_n, the same event under uniform
disorder has probability at most u_n+sqrt(delta_n). For ANY length-T equilibrium
history, the chance of at least one such step is at most T u_n+sqrt(delta_n).
The disorder-transfer penalty is paid once, not T times.

**This does not yet prove slow mixing.** Small steps can mix rapidly, and the
required separated Gibbs regions have not been established for this ensemble.
Nor is a useful finite-n delta_n available from the existing asymptotic BPQM
certificate. The live report therefore leaves every quenched numerical bound
UNKNOWN. A local bit-error density-evolution number is not delta_n.

## Prior Art And Scope Correction

The cluster mechanism is not novel: [Hangleiter, Ju and Vazirani,
Code Swendsen-Wang Dynamics](https://arxiv.org/html/2510.08446v1) study the
homogeneous code version and prove rapid mixing for specified approximately
graphic/cographic code Hamiltonians. The repository's signed affine update
is its frustrated extension. Their positive stabilizer-Hamiltonian theorem
does not automatically cover uniform independent frustrated signs. A verified
gauge J=Bx0 removes frustration; an arbitrary J cannot be so removed. Do not
call the existing sampler a newly discovered algorithm or import that mixing
theorem without its hypotheses.

The pure-state decoding/Bhattacharyya identity below is established channel
duality, not a new claim: [Rengaswamy and Pfister, Theorem 15](https://arxiv.org/html/2103.09225v1).
[Piveteau, Quek and Franco Garrido, Section 4.2](https://arxiv.org/pdf/2610.03566)
also connect the Gram spectrum to normalized Gibbs partition functions. The
local work here combines those identities with the exact socket first moment
to attack a particular classical competitor. No novelty search establishes
priority for that combination.

## Exact Native Problem

There are n spins and m=2n clauses. Match six distinguishable sockets at each
spin uniformly to three sockets at each clause. Reduce parallel incidences
modulo two, producing B in F2^(m by n). Do not condition on rank, girth, simple
edges or successful decoding. J is uniform in F2^m. The target is

    pi_J(x) = q(J+Bx)/Z_J,
    q(e) = ((1-c)/2)^|e| ((1+c)/2)^(m-|e|),
    Z_J = sum_x q(J+Bx).

This is the Gibbs distribution proportional to
exp(beta sum_i (-1)^(J_i+(Bx)_i)); the q normalization is convenient bookkeeping.
Zero/duplicate rows and rank-deficient matrices are allowed in all identities.

Given x, retain every satisfied row independently with probability
p=2c/(1+c), and no unsatisfied row. Draw y uniformly from B_S y=J_S using
Gaussian elimination. Equivalently, y=x+d for uniform d in ker B_S. The joint
weight (2c/(1-c))^|S| 1[B_S x=J_S] proves detailed balance. Dependence between
retained equations is not a rejection event.

## Disorder Transfer, With All Conditioning Visible

For a fixed B of rank r, let V=im B and let p_A=sum_(e in A) q(e) for each
coset A of V. There are M=2^(m-r) cosets. Each x image has 2^(n-r) preimages,
so Z_J=2^(n-r) p_[J]. Define two joint laws:

    Q(J,x)=2^-m pi_J(x)                 [quenched: uniform supplied disorder]
    A(J,x)=2^-n q(J+Bx)                 [annealed/planted: generate disorder]

Both have x|J=pi_J, but their J marginals differ. Direct summation gives

    TV(A,Q) = TV(p, Uniform(M)) =: eta_B.

For C=ker B^T, the pure-state channel codewords have Gram entries
G_(a,b)=c^|a+b|. Character diagonalization gives eigenvalues M p_A. The known
optimal square-root measurement formula consequently reads

    P_opt = (sum_A sqrt(p_A/M))^2.

The classical fidelity/TV inequality yields eta_B <= sqrt(1-P_opt). Thus ANY
decoder with block error delta_B gives eta_B<=sqrt(delta_B), whether or not
it is optimal. Averaging B and applying Cauchy-Schwarz gives
E_B eta_B <= sqrt(E_B delta_B). This is an information-theoretic transfer;
an efficient decoder is not needed to prove it, but is needed for the quantum
algorithm under comparison. An unproved decoder error estimate is not enough.

One can sample A exactly: choose x uniform, choose e with independent
Pr[e_i=1]=(1-c)/2, set J=Bx+e. Then x is an exact stationary start conditional
on this GENERATED J. Run the usual cluster chain keeping that J fixed.
For every history length, A and Q have the SAME conditional history law given
J. Their full-history TV is therefore still eta_B. Appending or omitting
observed history cannot increase that distance. No accumulation in T occurs.

Under A, satisfaction indicators at any single stationary time are independent
with probability (1+c)/2. Retention therefore gives independent S~Ber(c), and
d is uniform in ker B_S. Across times the S sets are NOT generally independent;
the history bound uses a union bound and stationarity only.

Important countercontrols:

* Fixed x independent of uniform J gives S~Ber(c/(1+c)), not Ber(c). The
  equilibrium mobility bound is not a uniform worst-start transition bound.
* Planting NEW J is not sampling the Gibbs law of a requested fixed J. Even
  perfect disorder flatness does not solve conditional inversion. Gauge repair
  preserves J+im B; at flatness, rejection to a requested coset costs M=2^(m-r)
  trials. This is a limitation of that repair route, not general hardness.
* Replanting J each step changes the process. It cannot test fixed-instance
  mixing or produce its equilibrium histories.

## Exact Socket First Moment

Fix a displacement d of Hamming weight h. Exactly 6h of the 6n spin sockets
are marked. Uniform matching makes their clause-socket positions a uniform
6h-subset. A clause hit by an odd number of marked sockets must be unretained
for B_S d=0. An even-hit clause imposes no restriction. Hence, with

    F_c(z)=1+3(1-c)z+3z^2+(1-c)z^3,

the expected number N_h of weight-h words in ker B_S is EXACTLY

    E N_h = binom(n,h) [z^(6h)] F_c(z)^(2n) / binom(6n,6h).

This counts the actual regular socket model including cancellations; replacing
it with independent sparse rows would be a different ensemble. The finite
test enumerates all marked positions for n=2 and checks this identity directly.

For any z>0, positive coefficients give
[z^(6h)]F_c(z)^(2n) <= F_c(z)^(2n)/z^(6h). Writing rho=h/n and H for binary
entropy with natural logs, the elementary type-count bounds

    binom(n,h) <= exp(n H(rho)),
    binom(6n,6h) >= exp(6n H(rho))/(6n+1)

imply

    E N_h <= (6n+1) exp(n f(rho,z)),
    f(rho,z)=2 log F_c(z)-6rho log z-5H(rho).

The lower type-count bound follows because the binomial probability at its
integer mean 6h is a mode and is at least 1/(6n+1). It includes endpoints.

At c=13/20, the certificate covers [1/50,1] by 98 contiguous intervals with
rational endpoints. Each interval supplies a positive rational z. For fixed
z, f(rho,z) is convex in rho (minus entropy plus an affine function), so it
is at most the larger endpoint value. Each endpoint rho=a/b is checked by
the purely rational inequality

    F_c(z)^(2b) z^(-6a) (a/b)^(5a) (1-a/b)^(5(b-a)) <= (99/100)^b.

Use 0^0=1 at the boundary. Thus f<=log(99/100) everywhere in that interval.
The numerical root finder only proposes z; it has no proof authority. The
standalone verifier rejects missing coverage, bad witnesses and false bounds.

Summing over at most n+1 possible h and applying Markov's inequality gives

    Pr_B,S[exists d in ker B_S, |d|>=n/50] <= u_n.

This controls EVERY possible displacement on a good retained matrix, not just
a randomly drawn kernel word. It also implies fewer than n/25 active coordinates
there, since a uniform kernel word has expected weight half the number of
active coordinates. That observation is not required for the probability bound.
The bound also holds for c>=13/20 by monotone retention coupling, without any
assertion that a quantum decoder succeeds at those higher overlaps.

At n=2048, u_n is about 0.02897; at n=4096 it is below 1.333e-10, and at n=8192
below 7.056e-28. These are analytical ensemble bounds, not observed frequencies
or certificates for a chosen matrix. They are deliberately capped at one.

## What Would Actually Prove Slow Mixing?

For a SAME fixed (B,J), suppose A and its complement outside a separator S
are separated by at least n/50 in Hamming distance, pi(A)=a in (0,1/2],
pi(S)<=s, and the stationary long-step probability is at most ell. Then

    Q_flow(A,A^c) <= s+ell,    Phi(A)<=min(1,(s+ell)/a).

Start at pi conditioned on A. The chance of an exit by time t is at most
t Phi(A), so the distance from stationarity is at least 1-a-t Phi(A).
Consequently t<1/(4 Phi(A)) rules out worst-start TV mixing to tolerance 1/4.
This is a conditional cut argument, NOT a first-witness hitting-time claim.

Missing obligations are material:

1. Prove such regions and small separator mass for the regular signed native
   ensemble at this overlap. Existing Erdos-Renyi shattering results cannot be
   imported by relabeling degrees. First/second moments alone do not prove it.
2. Transfer averaged bounds to typical fixed instances with explicit failure
   budgets, e.g. Markov costs. An ensemble average is not a universal instance
   guarantee. The decoder error rate must be strong enough for the claimed
   mixing lower bound; merely delta_n=o(1) does not imply exponential slowing.
3. Keep alternative classical samplers live: tempering, nonlocal moves,
   factor contraction, and code-specific algorithms are not ruled out.
4. Keep finite quantum compilation and accuracy costs visible. The prior BPQM
   tree certificate's huge depth constants are not fixed by this result.

Falsifiers: a correct entropy-verifier failure invalidates the local bound;
an ensemble mismatch invalidates its application; fast polynomial mixing via
many short steps defeats the bottleneck conjecture; or a different efficient
classical sampler removes the proposed sampling comparison altogether.

## Next High-Reasoning Task

Do not add more random trajectories. Resolve the missing GEOMETRY for the
actual (3,6), c=13/20 regular signed model: either construct a balanced
low-boundary Gibbs cut with explicit rates or identify a short-step coupling/
conductance mechanism consistent with rapid mixing. A comparison against the
overlap gap must account for entropy and quenched normalization. The exact
mobility certificate now supplies one input to that question, not its answer.
