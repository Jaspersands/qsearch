# DCP Overlapping CNOT DAG Carry Fanout Obstruction

## Correction: Termwise Necessity Retracted (2026-10-17)

V1's claimed necessary condition is false. At modulus4, take
`A=[[1,1,3,5]]` and `V=[[1,1],[1,1],[1,0],[0,1]]`. V has full column rank.
The two shared rows have odd coefficients, yet their cross-terms sum to
`-2*((1-2*x0[0])+(1-2*x0[1]))*u0*u1`, zero modulo4 for EVERY anchor.
The old termwise condition remains sufficient, not necessary.

## Exact Multilinear Expansion
For $x(u; x_0) = x_0 \oplus V u \in \{0,1\}^K$ with row fanout sets $S_r = \{j : V_{r,j} = 1\}$:
$$A x(u; x_0) \equiv A x_0 + \sum_{j=1}^m \tilde{A}_j(x_0) u_j + \sum_{r : |S_r| \ge 2} (1 - 2(x_0)_r) A_{\cdot, r} \sum_{J \subseteq S_r, |J| \ge 2} (-2)^{|J|-1} \prod_{j \in J} u_j \pmod{2^t}.$$
## Corrected All-Anchor Criterion

The cross-terms vanish for all anchors and all u if and only if BOTH hold:

- `4*A[:,r] == 0 mod 2^t` for every shared row r.
- `2*sum(A[:,r] for r containing wire pair j,k) == 0 mod 2^t` for every pair.

Necessity: multilinear coefficients of a zero function on the Boolean cube
vanish by integer Mobius inversion, also over Z/(2^t). The quadratic pair
coefficient at anchor zero gives the second condition. Toggling one shared
anchor bit changes that coefficient by4*A[:,r], giving the first.
Sufficiency: the quadratic coefficients stay zero under every anchor toggle;
degree>=3 coefficients contain a factor divisible by4, and vanish termwise.
This argument also covers t=1, when both conditions are automatic.

The analytic checker is polynomial in matrix size; exhaustive controls are
small references only. Tests enumerate every two-row/two-wire binary V and
every coefficient vector at moduli2,4,8, include full-rank cancellation,
three-wire cubic cancellation, and an anchor-zero-only cancellation failure.
JS independently evaluates direct XOR versus the linear prediction, rather
than reusing a mistyped quadratic coefficient as v1 did.

The general derivation is REVIEW PENDING. This is label linearity for all
anchors, not a fixed-anchor criterion, all-secret entanglement assertion,
efficient quantum decoder, new negative result, or general DCP no-go.
