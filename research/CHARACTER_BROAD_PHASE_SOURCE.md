# A restricted broad-character source falsifier

2026-11-12. Completed paid report
audits/openai_runs/2026-11-12-fast-character-build/response.md, independently
reviewed in audits/reviews/2026-11-12-character-broad-phase.md and parent-checked.
This is a source-model result; generic native reconstruction remains OPEN.

Input: coherent chosen BASE-FIELD BIT access to padded quadratic character
F_Q(x), unknown monic squarefree degree-d Q, odd p>=256d². A broad ideal
state with phase lambda(Res(Q,R)) on every squarefree exact-degree-(2d-1)
mask R has sufficient overlap with the already paid virtual norm-character
state for polynomial Fourier/Hankel decoding. This does not construct its
relative nonsplit phases from the actual BIT oracle.

For a clean unnormalized branch with coefficient amplitude
h_R(Q)=sum_A c_(R,A) product_(x in A)F_Q(x), public c and l1 norm <=L,
let J_Q be herald probability times conditional fidelity with that broad
target. The exact coherent expansion, averaged over irreducible monic Q,
gives

    E J_Q <= L² * [1/((1-1/p)*(2d-1)!)+2p^(1-d/2)].

Different nonsplit-factor classes retain an odd nonlinear factor even after
multiplication by ANY native parity; the Weil bound and full-degree-element
restriction give the second term. The largest same-class mass gives the
factorial term. This includes interference and padded zeros; it is not a
mixture argument or a pointwise all-Q bound. At polynomial-size p it defeats
uniform polynomial-L/resource constructions of this form. A uniform claimed
algorithm for all p above a polynomial threshold must include that subfamily.
Arbitrarily enormous logp requires using the displayed inequality itself.

Scope repairs: fixed-nonsplit-factor phase kickback requires root-free Q or
coprime supported masks; padding is not multiplicative at roots. A public
prepare/parity/project clean branch has L<=1. Multiple accepted branches
must be summed; an exponentially large accepted subspace is not free.
Arbitrary nonlinear BIT processing or intermediate label mixing is outside
this model. Classical chosen-query reconstruction uses O(dlogp+log1/eta)
queries but p^d candidate enumeration; fresh queries verify proposals. This
is not classical hardness, nor an efficient receiver from a query/POVM bound.

An explicit native escape proves the restriction matters. Choose2d distinct
public points, b_j=(1-F_Q(x_j))/2, and H(Q)=product_i(-1)^(b_(2i-1)b_(2i)).
Compute/AND-phase/uncompute uses4d BIT calls. On the actual irreducible-target
promise every parity expansion of H has l1 norm at least
2^d/(1+4^d*2p^(1-d/2)) >= (8/9)2^d for d>=4. Correlate H with each parity
and use the same Weil bound to prove this inequality. Applying H only to
labels with nonsquare leading coefficient makes it a relative phase; even
arbitrary Q-dependent global rephasing leaves some label norm at least
sqrt(8/9)*2^(d/2). This is NOT a construction of the desired resultant phase.

The restricted source route is closed. General native phase synthesis and
efficient full-law decoding are open; no general circuit/query impossibility,
hardness, novelty or speedup. The paired Claude decoder call was empty, with
no scientific finding. Park extensions while the compared surface route has
a concrete end-to-end classical test. A useful next construction must exhibit
relative nonsplit phases or another decodable law using permitted nonlinear
operations, with all probabilities and precision charged. No finite sweep.
