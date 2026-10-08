# Collective Frequency Receiver With Exact Character Feedforward

IMPLEMENTED / LOCAL DERIVATION REVIEW PENDING. This constructs and costs a
specific receiver, then falsifies its polynomial-time promise at growing
roots. It is NOT a lower bound against all collective measurements, a new
algorithm, a cryptographic attack, or a novelty claim.

## The Concrete Instrument

Take B independently sourced ridge-cancellation outputs, width d each,
root q=3^r and shared secret s in Z_q^n. Their joint flat state has words
x in F3^(dB), dimension D=3^(dB) and known frequency map

    F(x)=sum_j Q_j(x_j) modq,
    |psi_s>=D^(-1/2) sum_x chi_q(s.F(x))|x>.

Public frequency evaluation is reversible and inexpensive relative to its
local tables when d=O(log n). Append |F(x)>, Fourier-measure the WORD
register over F3, and Fourier-measure the frequency register over Z_q^n.
There is no inverse of an unknown-state preparation. Each input is used
once. These two Fourier transforms are DIFFERENT groups and must not be
silently identified. Frequency arithmetic costs polynomial in n, log q,
the charged number of programs and ridge dictionary.

For word outcome t=0, the unnormalized frequency state is

    sum_y (C_y/D)*chi_q(s.y)|y>, C_y=|F^(-1)(y)|.

Writing G=q^n and p0=sum_y C_y^2/D^2, its herald probability is p0.
The CORRECT group-Fourier outcome has joint probability EXACTLY1/G:
sum_y C_y/D=1. Its conditional probability is1/(G*p0). If
chi2=G*sum_y C_y^2/D^2-1, this is1/(1+chi2).

Thus a larger batch may make an accepted result reliable but does not
increase the unconditional correct yield of this branch. Direct restarting
requires G fresh batches per correct output on average. Failure consumes
the batch. This is a reciprocal correct-output yield, not a stopping rule:
there is no supplied flag identifying a correct guess. Amplitude amplification
about |psi_s> is not granted. A generic
balanced-frequency block encoding has singular value1/sqrt(G), not1:
greater density does not fix its normalization. This does not lower-bound
alternative block encodings or source-aware preconditioners.

For t!=0, direct uncorrected output s has probability ZERO, since the sum
of the nontrivial word character is zero. Discarding the erasure outcome
is not a way to promote the heralded success rate.

## A Real Feedforward Compiler, Not Free Postselection

An exact secret correction delta rescues t if and only if

    chi_q(delta.F(x))=chi_3(t.x) for EVERY word x.

Then the correct group-Fourier output is s-delta, and known addition of
delta recovers s. Every such t has herald probability p0 and joint correct
probability1/G. Let Lambda be the subgroup of deltas whose pullbacks are
word characters, K those with zero pullback, and T the resulting image.
The complete exact-character scheme has

    accepted_probability=|T|*p0,
    correct_and_accepted_probability=|T|/G.

T is an elementary abelian3-group. Every subgroup of Z_(3^r)^n has at most
n generators (e.g. Smith normal form over this finite principal ideal
ring), so its elementary quotient Lambda/K has rank<=n. Therefore

    |T|<=3^n,
    exact_character_feedforward_correct_yield<=3^(-n*(r-1)).

This ceiling is universal for this EXACT character-correction instrument;
it does not assume IID frequencies, full span, equal fiber sizes or small
sample counts. At r1 it becomes vacuous, correctly admitting ordinary
field-character Fourier decoding. At growing depth it is exponential even
with arbitrarily large batches. Approximate character matching, general
outcome-specific unitaries and noncommuting receivers are not covered.

The implementation checks a useful completeness certificate without
enumerating the joint cube. If all LOCAL frequency values span F3^n mod3,
they also span Z_q^n; hence 3*delta.F=0 implies delta=(q/3)*a for a in F3^n.
Each actual canceled Q_j mod3 is ordinary quadratic. Extract and check its
linear coefficients beta_j and quadratic monomial rows M_j. Then

    a in intersection_j ker(M_j),
    t_j=beta_j^T*a,
    delta=(q/3)*a.

The finite-field nullspace gives all exact corrections. Full frequency
span also makes the a->t map injective. If span is deficient, only the
order-three correction subgroup is implemented; completeness is explicitly
NOT certified. Reject a phase that fails the local quadratic check instead
of assuming its declared class. The O(B*3^d) LOCAL checks are polynomial at
d=O(log n); the O(3^(dB)) joint reference is calibration-only.

## Information Is Available; This Receiver Still Does Not Extract It Cheaply

Under the original physical IID frequency premise and LOW-only factory
selection, any two distinct words in a single output have independent
uniform vector frequency difference in Z_q^n: a selected full-rank physical
frame changes at least one trit by a unit(+/-1,+/-2), multiplying a remaining
independent alpha_i in Z_q. Injection words are uniform independently of
alpha. For independent original cohorts the same law holds for any distinct
JOINT words by conditioning on all other blocks. This is an ensemble law,
not randomness after conditioning on every public full label.

Consequently E[chi2]=(G-1)/D. For the uniform-secret abelian pure ensemble,
the ideal PGM is optimal and its exact success is

    P_opt=(sum_y sqrt(C_y))^2/(G*D).

This follows from orthogonal frequency fibers and the matching diagonal
dual, as in the previous conditional-digit derivation. If p=C/D and u=1/G,
P_opt is the squared classical fidelity F(p,u)^2. Since
2*(1-F)<=chi2 and1-F^2<=2*(1-F),

    E[1-P_opt]<=(G-1)/D.

D>=G/(epsilon*eta) therefore suffices for ideal failure<=epsilon on all
but eta source instances by Markov. Polynomially many width-O(log n)
outputs can satisfy this information condition. It is not an efficient
measurement compiler, computational lower bound, or external source-supply
theorem. The information-versus-implementation distinction is already
central in [Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0501044).
No new optimal-measurement principle is claimed here.

The lowest-digit joint reference averages ONE shared higher secret. It must
not tensor independently averaged single-output density matrices; joint
correlations can retain information absent from every individual marginal.

## Falsifiers And Next Positive Target

The actual native controls replay evaluation, word erasure and frequency
Fourier amplitudes at full secrets, including legal nonzero corrections
when present. They record all source ancestry and unused-program costs.
Physical IID supply is not certified by disjoint IDs or deterministic seeds.
Finite controls are not evidence for an asymptotic speedup.

## Self-Critique: Keep All Outcomes Before Rejecting The Broader Readout

The character ceiling bounds only exact translated-secret guesses on the
rescued branches. It does NOT bound the statistical information in every
measurement record. For a frequency-Fourier outcome y and word outcomes t_j,
the actual instrument has likelihood

    P(y,t|s)=G^(-1)*product_j L_j(t_j;s-y),
    L_j(t;u)=3^(-2d)*|sum_z chi_q(u.Q_j(z))*chi_3(-t.z)|^2.

The y marginal is uniform and independent of s. Keeping y is equivalent
to a known shared phase translation before independent local word Fourier
measurements. For a uniform secret prior, randomizing y does not change mean
optimal classical decoding success. The same value is attainable with plain
local word Fourier readout (y=0), not exponential postselection. Each fixed
secret's local likelihood is computable in polynomial time at d=O(log n).
The unresolved issue is finding a good secret without enumerating q^n of
them, and how many physically supplied outputs that decoder needs.

The [source-aware Fourier information audit](TERNARY_FOURIER_INFORMATION.md)
now answers part of the sample question: for certified selected physical
frames, mean information is at most approximately one bit per output, not
d trits. Fano requires Omega(n*log q) outputs for this fixed readout, even
with unlimited classical inference. This does not impose an inference-time
lower bound or invalidate nonproduct collective measurements.

The implementation evaluates the exact bounded all-record MAP baseline:

    P_MAP=G^(-1)*sum_t max_u product_j L_j(t_j;u).

It records maximizing secrets, checks normalization, and compares with the
optimal collective PGM. This costs exponential secret enumeration AND the
joint-outcome reference table. It is a classical attack/evaluation baseline,
not an efficient full-secret algorithm. Failed polynomial yield of the
character feedforward scheme therefore does not justify deleting the
all-record inference target. A tractable, source-aware classical optimizer
for these quantum-produced likelihoods remains an alternative positive
research direction, alongside noncharacter collective transforms.

Falsify a claimed exact correction by any word with a nonzero character
residual. Falsify an efficiency claim if it reports conditional success
without herald/source cost, erases unknown registers for free, or tensors
separately refreshed higher secrets. Retain failed full-span certification.

NEXT POSITIVE TARGET: a costed classical optimizer for the all-record
likelihood with rigorous sample/error scaling, or an outcome-specific,
SOURCE-AWARE NONCHARACTER transform exploiting the compact ridge structure,
or a different clean
global fiber action. Specify its unitary/inverse and a costed coverage/error
law before adding further infrastructure. Exact character feedforward is
now exhausted for growing-depth direct polynomial-yield decoding; repeatedly
optimizing its nullspace cannot remove the universal ceiling. Likewise,
the optional extra degree-drop stage does not by itself repair this cost.

```
python theorems/ternary_collective_character_receiver.py --write
node research/certificates/ternary_collective_character_receiver_crosscheck.js
python -m pytest -q tests/test_ternary_collective_character_receiver.py
```
