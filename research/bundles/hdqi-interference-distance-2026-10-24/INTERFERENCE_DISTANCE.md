# High Measurement Distance Can Erase The Sampling Signal

Date: 2026-10-24. LOCAL UNREVIEWED deduction and exact classical gate.
Not a new quantum algorithm, general dequantization, hardness theorem or
novelty claim. No candidate is admitted by the executable.

## Decision After Comparing Branches

The filtered-parent degree-scale gap remains an important constructive
problem, but the last two thermal comparison routes were disproved. Rees
has a completed scoped AI review and still needs a persuasive application
and broader verification. The scalar OPI reduction already transfers the
known guarantee; another custom source/backend would not establish a new
mechanism. None justifies adding more finite examples by inertia.

Before spending another pass on HDQI preparation, test a specific remaining
output premise: can high measurement-fiber rank and a nonlinear decoder
evade the existing classical comparators? The answer here is NO for a new
sufficient condition, independent of sign cost or decoder linearity.
Large relative code distance can make the requested physical output close
to uniform, instead of making it a hard sampling task.

This is a classical falsifier for that research direction, not a generic
algorithmic breakthrough. The underlying Pauli orthogonality and coding
ideas are standard; novelty has not been established.

## Same Input And Actual Output

Use the existing public Hermitian Pauli list P_1,...,P_m on n physical
qubits, real couplings J_i, and the exact canonical pilot

    |pi> = exp(-beta H_hat/2)|0>/sqrt(Z_hat) = sum_y psi_y |y>.

The canonical generators have the SAME anticommutation graph as the
physical list. Their independence is built into the canonical algebra;
the physical list need not be independent. Let B=[X;Z] be its binary
Pauli map, including all physical phases in the ordered product P(y).
For ANY total deterministic decoder Dec, the actual decoding isometry is

    |y> -> |R(y)> |P(y)>,
    R(y)=y xor Dec(By), |P>=2^(-n/2) sum_b P|b>|b>.

The output studied here is the PHYSICAL LEFT register measured in the
given computational basis, with the right half and residue discarded.
It is not the pilot-label law, Bell-label law, full joint law, a different
measurement basis or a coherent state-preparation task.

The map is an isometry even for a bad decoder. Distinct B labels give
orthogonal Bell vectors. If By=By', different y give different residues.
This fact is not a claim that an arbitrary decoder produces a Gibbs state.

## Relative Interference Distance

Define

    d_int = min{|v| : Xv=0, Zv!=0},

with infinity if no such vector exists. This is a RELATIVE distance:
words in ker B are excluded, even if the ordered product is -I. It is
not simply the minimum distance of ker X. The older fiber exponent is
k=rank(B)-rank(X); k and d_int answer different questions.

Let t be an integer with d_int>2t. For ANY normalized pilot supported on
|y|<=t, the left computational output is exactly uniform on n bits, for
every total deterministic decoder and every choice of complex amplitudes.

Proof: a diagonal output probability contains cross terms only when two
labels have the same residue and the same X syndrome. For y!=y', put
v=y xor y'. Its weight is <=2t. If Zv!=0, this contradicts the distance
condition. If Zv=0, then By=By'; equality of residues forces y=y', again
a contradiction. Only diagonal-in-y terms remain. Each Bell Pauli vector
has uniform left computational distribution, so their mixture does too.
No decoder inverse, decoder-success assumption or phase cancellation
approximation is used.

The condition is STRICT. At d_int=2t there can be full interference among
weight-t labels. The executable includes an exact two-Pauli counterexample.
Conversely, a short diagonal word need not cause bias for a particular
decoder: refusal is inconclusive, not a hardness or bias certificate.

## Full Thermal Pilot And A Rational Error Certificate

Let eta_t=Pr_pi[|Y|>t]. Normalize the pilot's projection onto |y|<=t.
Its pure-state trace distance from the original is sqrt(eta_t). Applying
the SAME decoding and measurement channel cannot increase that distance.
Thus

    TV(actual physical-left output, uniform n bits) <= sqrt(eta_t).

For eta_t=1 the bound is simply vacuous. The square root cannot generally
be replaced by eta_t: superposing Bell I and Bell Z with probabilities
1-eta and eta gives TV=sqrt(eta(1-eta)). This opposite control is retained.

The published redundancy-free inclusion bound is

    Pr[S subset supp(Y)] <= product_(i in S) rho_i,
    rho_i=(beta J_i/2)^2.

This is the explicit dependency from
[Hastings--Schmidhuber, Appendix A.2](https://arxiv.org/html/2610.03697v1).
It does NOT say the error bits are independent. For rho_i>1 one can replace
it by 1 by applying the bound to the remaining subset; the executable's
inherited input contract has beta<=1 and |J_i|<=1 anyway.

Let e_l(rho) be the elementary symmetric polynomial of order l. For
1<=l<=t+1,

    E binom(|Y|,l) <= e_l(rho),
    eta_t <= min(1, min_l e_l(rho)/binom(t+1,l)) = eta_bar.

Compute all these values by descending-order dynamic programming in
O(m(t+1)) rational operations. Bit lengths and the actual input precision
are charged. If d_int>2t is certified and eta_bar<=epsilon^2, the complete
classical sampler is just n independent random bits. It makes ZERO pilot
sample, amplitude, signed-word or decoder calls. No polynomial bound on
C=Z_commuting/Z_hat is required.

If the prepared pilot has trace error epsilon_p, add epsilon_p to the
output bound. If a SEPARATE result certifies that actual decoding is within
epsilon_d of the desired Gibbs state, add epsilon_d as well. No Gibbs
guarantee is inferred from the distance test itself, nor from average
decoding performance on unspecified coupling signs.

## Distance Verification Is Not Free

The executable enumerates every nonempty word of weight <=min(2t,m),
testing Xv=0 and Zv!=0. Its operation count is explicitly
sum_(j=1..min(2t,m)) binom(m,j), with an additional O(j) mask-XOR cost per
word. The allowed budget is checked BEFORE enumeration. If insufficient,
the outcome is UNKNOWN_BUDGET with no claimed certificate or samples.

At fixed t this is polynomial, but t growing with m can make it
exponential. A supplied lower bound on code distance is not automatically
trusted. Larger promised families require a separate structural proof or
independently checked certificate. The general distance problem is NOT
solved by this module. Once certification is done, each output costs O(n)
random bits and no renewed enumeration. A PRNG is used only for replayable
execution controls; the theorem assumes independent uniform random bits.

## Opposite Family: Large Rank And Exponential Sign Cost Still Easy

Start with n independent anticommuting pairs X_i,Z_i. There are m=2n
generators, matching anticommutation graph, and beta=1/32. Conjugate the
entire public list by a Clifford C and retain the requested computational
basis. This DEFINES a family of physical inputs; it is not permission to
rotate an existing task's output basis to pass a test.

B is invertible, so k=n and the older generic fiber bound is 2^n. The
canonical pilot's sign ratio is

    C_sign = [cosh(beta)^2 / cosh(sqrt(2)*beta)]^n.

The bracket is strictly greater than one for every beta>0: compare the
even series coefficients, equal at orders zero and two and strictly
larger for cosh(beta)^2 at every order >=4. Thus C_sign grows exponentially
at fixed beta. Pairwise pilot preparation itself is easy and the physical
Gibbs state is Clifford-conjugated product thermals. This is deliberately
an EASY family, not a new proposed hard instance.

For a UNIFORM random Clifford, every fixed nonzero Pauli label has
probability 1/(2^n+1) of becoming diagonal nonidentity. Therefore

    Pr[d_int<=2t] <= sum_(j=1..2t) binom(2n,j)/(2^n+1).

Uniform Clifford selection has a known polynomial construction:
[Koenig--Smolin](https://arxiv.org/abs/1406.2170). It is prior art, not
implemented here. At t=floor(m/32), the failure bound is exponentially
small because h_2(1/16)<1/2. The inclusion bound also gives a Poisson
Chernoff majorant with mu=m/4096. For K=t+1>=m/32,

    eta_t <= (e*mu/K)^K <= (e/128)^K,
    TV <= (e/128)^(K/2).

Hence there are, and uniform public Clifford selection supplies with high
probability, high-rank inputs with exponential sign cost but exponentially
near-uniform physical output. These probabilistic statements do not certify
the distance of an arbitrary individual Clifford circuit.

The live control instead uses a FIXED seeded sequence of symplectic
transvections and checks its distance exhaustively to a bounded radius.
It is NOT asserted to be a uniform Clifford draw. Its actual 32-qubit,
64-generator list is saved in receipt.json, with all phases, couplings and
beta. All words of weights 1 through 4 are checked. The exact rational tail
certificate is <10^-6, proving TV<10^-3. No 2^64 pilot vector or 2^32 fiber
is built. Changing Pauli signs does not change the graph or the distance.

## Falsifiers, Scope And Next Research Gate

The proof would fail if the actual output discarded residue coherence
incorrectly, if a short nontrivial diagonal product were missed, if a
different measurement basis were substituted, or if pilot inclusion tails
were assumed rather than established. Dense controls explicitly retain
residue, right register, ordered-product signs and physical Y phases.
They cover nonlinear valid decoders, invalid decoders, complex pilot
amplitudes, scalar redundancies, zero temperature parameter and nonzero
thermal tails. Neither finite controls nor the receipt constitute an
independent mathematical review.

The full joint distribution need not be uniform: even the vacuum pilot
gives perfectly correlated left/right computational strings. Coherent
pilot preparation and general high-temperature Gibbs sampling remain open.
Low distance, higher temperature, a different useful observable, or a
different native task may evade this sufficient comparator; none is
automatically hard.

Next candidate gate: specify the useful physical output BEFORE pursuing
another preparation theorem. For computational sampling, exhibit enough
actual diagonal interference to survive both the old fiber/sign comparator
and this distance/tail comparator, with a decoder whose Gibbs or search
guarantee is separately priced. Otherwise pivot to the Rees application
problem rather than strengthening a preparation primitive with no surviving
output-level advantage hypothesis.
