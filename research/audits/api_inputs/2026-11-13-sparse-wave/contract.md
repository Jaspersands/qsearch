# Native sparse-source damped lattice Helmholtz field sampling

13November2026. Selected after STATE/TRAPS, corpus been-tried and baseline
lookups, then actual primary2609.10282 Eq20,23-28,31,A18-A21. No close corpus
endpoint or catalog match was returned; that is NOT classical hardness.
Previous static Macdonald full-output question is parked after exact moment
classical samplers and a finite-time Poisson approximation. Do NOT extend it.
Independent comparison also considered qutrit partial-assignment gauge search
2611.01983: actual source has an easy classical XOR case and finite SAT tests,
not a newly paid general search route. General Selmer's global class/unit
bypass has no new operation; do not reopen it merely because it is open.

SINGLE scientific question: is there a completely paid quantum polynomial
algorithm for this physically motivated FULL spatial Born law, and does a
classical algorithm match it? No source normalizer, inverse, Green kernel,
annulus sampler, QRAM, eigenstate, or material oracle is supplied.

INPUT: n>=2, L=2^n; torus (Z/LZ)^2, fixed grid spacing1. Standard positive
nearest-neighbor Laplacian K=4I-Tx-Tx^-1-Ty-Ty^-1. Set eta=1/L and
A=I-K+i*eta*I (fixed squared wave number1, below the van Hove value4).
Explicit list of m DISTINCT sites x_j in the torus and nonzero rational
complex weights w_j of total bit length B; combine duplicates beforehand.
f=sum_j w_j |x_j>. Arbitrary phases/signs allowed, f!=0. Input epsilon>0.
OUTPUT: one lattice site x with TV<=epsilon from
P_f(x)=|u(x)|^2/||u||^2, u=A^-1 f.
Target BOTH total bit/gate work poly(n,m,B,1/epsilon) with a finite clock.
No general relative exponentially-small output precision is required.
The discrete Fourier symbol is lambda(k)=4-2cos(2pi*kx/L)-2cos(2pi*ky/L),
a(k)=1-lambda(k)+i/L, so |a|>=1/L. Generic QLSS pays kappa~L; explicit
full-grid FFT/solve costs L^2 poly(n,B,b). Geometric resonant prep is a
proposed route around that cost, not an admitted primitive or theorem.
We do not import the continuum-circle ring into this lattice symbol.

Expected advantage target: poly(log L) at polynomial m and fixed/error
inverse-polynomial n, versus full-grid work. A same-output sublinear
classical algorithm is the first falsifier; no classical lower bound,
novelty or speedup is asserted. State preparation only is not an advantage
for the requested classical sample. Any changed source/precision/geometry
promise must be labelled a RESTRICTED endpoint, never universal.

CHEAP parent attacks, exact but not yet an independent full proof:
1. Source-register LCU success is a Gram quadratic form. If G=A^-1 delta0,
Z0=||G||^2,Z=||sum w_j T_xj G||^2, then usual ell1-weight LCU succeeds
with Z/(||w||_1^2 Z0). It is NOT generally1/m; uncompute of the SAME
weighted source ket produces |alpha_j|^2 coefficients, not arbitrary w_j.
Use separate left/right preparations and phases if repairing that detail.
2. Matched classical mixture: if the SINGLE G spatial probability and
values are efficiently available, sample j proportional|w_j|^2 then
x from |G(x-x_j)|^2/Z0. Envelope is m*sum|w_j G(x-x_j)|^2. Rejection
success Z/(m*sum|w_j|^2*Z0). This is within a polynomial factor of LCU.
Do not grant the missing single-source sampler/evaluator or normalizers.
3. Five-source cancellation: f=(I-K)delta0 = -3delta0+delta_(1,0)
+delta_(-1,0)+delta_(0,1)+delta_(0,-1). Exactly u=delta0-i*eta*G.
FourierF=1-lambda vanishes ON the actual resonant curve. A shell with
|1-lambda|<=C/L may therefore lose almost all normalized full-field mass,
and source LCU may be exponentially small in n. Prove bounds or refute;
finite plots cannot establish asymptotics. This family is classically easy,
so it is a source-interface falsifier, not a difficult quantum application.

Resources/proof obligations: actual spectrum and lattice shell sampling,
normalization/conditioning for all allowed sources, all off-shell tails,
finite-bit trigonometry with n extra bits, coherent uncomputation, quantum
state-to-classical readout, cap success/failure and total clock. Standard
classical competitors: Fourier solve, Green superposition, sparse sampling
mixture, oscillatory quadrature/stationary phase, direct localized quotient
when f=A0 h, and exact small-grid controls. No implementation is requested.
Stop at the exact missing operation if blocked. Your report is advisory;
all material claims will be independently verified by parent.
