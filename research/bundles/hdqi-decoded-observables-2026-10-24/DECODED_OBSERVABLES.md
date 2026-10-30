# A Classical Attack On Actual Decoded Pauli Observables

Date: 2026-10-24. LOCAL, UNREVIEWED derivation and explicit classical
estimator. No general output sampler, classical hardness or novelty claim.

## 1. Same Quantum Output, Not A Substitute Task

Input consists of explicit Hermitian physical Paulis P_i on n qubits,
rational |J_i|<=1, 0<=beta<=1, and a total deterministic decoder Dec from
Pauli labels to m-bit strings. Its running time is charged and must be
polynomial for the conclusion below. Failed/out-of-image syndromes need
a defined output convention; their decoded value need not be correct.

Let B map a generator mask y to the binary label of the ordered product
P(y)=P_0^y_0 ... P_(m-1)^y_(m-1). Define the canonical pilot from the
anticommutation graph, with coefficients a_y and normalization Z_hat.
Coupling signs are already included in a_y. The EXACT output attacked is

    |Psi>=sum_y (a_y/sqrt(Z_hat)) |R(y)> |P(y)>,
    R(y)=y xor Dec(By), rho=Tr_R |Psi><Psi|,
    |P>=(P tensor I)|Bell_n>.                              (1)

This is the decoded output construction in Hastings--Schmidhuber, Section
II, equations (9)--(12), [primary source](https://arxiv.org/html/2610.03697v1).
It is well-defined even for a bad decoder. It is NOT automatically a Gibbs
state; any Gibbs approximation requires separate decoder-success and pilot
error guarantees. This attack does not import an average-sign promise.

The requested observable is a specified Hermitian Pauli Q on the physical
left register, or a polynomial list/samplable weighted sum of these. The
goal is additive expectation estimation, NOT full state simulation or exact
sampling of all physical output bits.

## 2. Decoder Pullback Is A Partial Signed Permutation

Let q be Q's binary Pauli label. A matrix element

    <P(y')|Q_left|P(y)>=tau(P(y')^dagger Q P(y))

vanishes unless By'=By xor q. Nonzero terms in (1) also require R(y')=R(y).
For supplied y, these conditions leave at most ONE possible partner:

    t(y)=y xor Dec(By) xor Dec(By xor q).                   (2)

Check B t(y)=By xor q. If this check fails, the row contributes zero.
If it holds, its coefficient is

    omega_y=tau(P(t(y))^dagger Q P(y)) in {1,-1,i,-i}.      (3)

Both the ordered product and its phase are computable by binary Pauli
arithmetic. On valid rows t is an involution: the second application swaps
the same two syndromes and cancels the decoder terms. Thus it is injective.
This proof does NOT assume B Dec(s)=s. Hermiticity gives conjugate phases
on paired rows. Taking the real part of each contribution recovers the real
expectation, including when individual phases are imaginary.

Represent Paulis as i^p X^x Z^z. Multiplication adds phases p+p'+2 z.dot(x')
modulo four; daggers add -p+2 x.dot(z). The implementation does not discard
Y phases or commute physical products without their signs.

## 3. Signed Words Supply The Missing Amplitude Information

Use the preceding classical sampler's identity

    a_y/sqrt(Z_commuting)=s_y sqrt(q_y) r_y,
    r_y=E[sigma|y], C=Z_commuting/Z_hat,
    D=E_(y~q)[r_y^2]=1/C.                                (4)

Here q is the explicit product envelope, not the requested observable label.
Draw y~q, two independent conditional signs sigma_1,sigma_2 at y, and a
third independent sign sigma_3 at t(y) when that label has positive proposal
probability. Define

    Y=sigma_1 sigma_2,
    X=Re(omega_y) s_y s_t sqrt(q_t/q_y) sigma_1 sigma_3,   (5)

with X=0 on invalid rows or q_t=0. Then

    E[Y]=D, E[X]=N, Tr(rho Q_left)=N/D.                  (6)

The two moments may share sigma_1; no independence between X and Y is needed
for separate concentration bounds and a union bound. The signs paired in
each product MUST be conditionally independent. Reusing one sign twice
would silently replace r_y^2 by one.

There is no amplitude oracle or exponentially expensive evaluation of r_y.
The word sampler uses local parity-conditioned count laws as before.

## 4. The Large Weight Does Not Imply Large Variance

Although sqrt(q_t/q_y) can be huge, its second moment satisfies

    E[X^2] <= sum_(valid y, q_y>0) q_y (q_t/q_y)
            =sum_(valid y, q_y>0) q_t <=1,                (7)

by injectivity of t. Also E[Y^2]=1. Clipping rare large weights without a
bias budget is NOT valid. Bounded-second-moment estimation, such as median
of means, is the correct tool; bounded-range Hoeffding cannot simply be
applied to X with range [-1,1].

Thus additive estimation of N and D to O(eps/C_bar), for any established
polynomial C_bar>=C, takes polynomially many draws. Division must use a
certified lower bound on D, not an empirically positive tiny denominator.

## 5. Fully Priced Finite Version

For eps,delta in (0,1/4], choose the same rational truncation

    eta=eps^2/(16384 m C_bar^2).

Let q',r' be the finite proposal and conditional sign means. The preceding
coherent-sign proof, before its gate-error allowance, gives normalized
pilot trace distance <=eps/8. Applying the SAME decoder channel cannot
increase trace distance, so its observable expectation changes by <=eps/4.
Also D'=sum q'_y(r'_y)^2>=1/(2 C_bar). No quantum gate simulation is needed.

Compute w=sqrt(q'_t/q'_y) to a rational LOWER approximation w_tilde with
relative error <=nu. Scaling to its binary exponent and applying integer
square root gives this in polynomial input/precision bit cost, even when
w is extremely large or small. Use nu<=gamma/2 and

    gamma=eps/(16 C_bar).

The weight approximation changes E[X] by at most nu E[sqrt(q'_t/q'_y)]<=nu,
by Cauchy--Schwarz and (7). Its second moment remains <=1 because the
approximation is downward. All signs, phases, products and sums are exact
rational/integer calculations; no floating underflow is used.

Set b=ceil(16/gamma^2), r=ceil(log_2(4/delta)), g=8r+1, and make g blocks
of b independent draws. Each block mean deviates from its expectation by
more than gamma/2 with probability <=1/4 by Chebyshev. Hoeffding on the
independent bad-block indicators makes the median fail with probability
<=exp(-g/8)<=delta/4. Apply this separately to X and Y. With probability
at least 1-delta/2 their medians N_est,D_est satisfy

    |N_est-N'|<=gamma, |D_est-D'|<=gamma.

Since |N'|<=D', division then has error

    |N_est/D_est-N'/D'|
      <=2gamma/(D'-gamma) <=2eps/(8-eps) < eps/3.         (8)

Together with truncation the output error is less than eps. A denominator
below 1/(4 C_bar) is explicitly refused. Clipping only the final estimated
expectation to [-1,1] is harmless and never increases its error. An
insufficient draw budget returns no certified estimate. Worst-case work is
g*b draws, at most 3*g*b sampled words, with capped word lengths and charged
decoder/product arithmetic. The conservative constants are not advertised
as practical for all inputs. Small diagnostic runs are NOT certificates.
The concentration theorem assumes independent random bits. Seeded PRNG
receipts are reproducibility controls, not a proof of that randomness premise.

## 6. Consequence And Boundary

For polynomial C_bar, efficient classical decoding, and explicit physical
Paulis, the actual HDQI output's specified Pauli expectations admit a
polynomial-time classical additive estimator. Weighted sums cost polynomial
in their coefficient L1 norm divided by the desired absolute accuracy:
sample terms proportional to absolute coefficients, or allocate individual
accuracies and failure probabilities. Energy density and total energy have
different accuracy scales and must not be conflated.

This result is a direct matched classical comparator for energy/readout
claims in the newly preparable regime. It does not rely on the physical
Hamiltonian being redundancy-free or on the decoder being successful.

It does NOT give efficient exact output sampling. Tiny joint event
probabilities and conditioning on rare prefixes require a new error/cost
analysis; an additive expectation oracle does not supply that for free.
An arbitrary non-Pauli observable or extra quantum decoder is also outside
the claim. A decoder with superpolynomial runtime does not become efficient
merely by this reduction. The general degree-scale regime with no polynomial
bound on C remains open. Failure of this estimator is not a hardness proof.

## 7. Adversarial Controls

Controls compare the pullback with independently constructed physical Bell
states and the traced decoder register, including redundant physical Paulis,
bad decoders, Y phases, negative couplings and out-of-image observable labels.
Exact finite rational moments verify the expectation and second-moment bound.
A rare-label fixture has a weight greater than 10^50 while preserving that
bound; the code must not clip it. These are finite algebra falsifiers, not
new toy-oracle candidates. Large executions remain separately scoped.

