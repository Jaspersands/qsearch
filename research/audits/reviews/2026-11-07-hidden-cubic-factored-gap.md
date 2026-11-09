# Independent review: gap for factored Bell events

7 November 2026. Reviewed the actual “Factored-event gap” section of
`HIDDEN_CUBIC_PHASE_LEARNING.md`. **Accepted with its stated restricted
scope.** The proof below supplies the phase and normalization details.
No general K5 gap, factor-extraction algorithm, or complete learner follows.

## Quantified statement

Let n be arbitrary, f:F2^n -> F2 have Boolean degree at most d, where d>=2,
and let psi=C 2^(-n/2) sum_x (-1)^f(x)|x> for any Clifford C. Measure two
fresh identical copies in the standard n-pair Bell basis, obtaining v in
F2^(2n). For any product P(v) of k affine Boolean forms, either

    Pr[P(v)=1]=0,

or

    Pr[P(v)=1] >= 2^(-2k-(d-1)(2^k-1)).

There is no bounded-occurrence assumption in this statement. The resource
consequence below fixes d=3 and k=5; it is not polynomial uniformly in k.

## Proof with phase conventions

An unknown Clifford induces an affine permutation of Bell labels, so it
suffices to prove the statement with C=I. Equivalently, conjugation by
C tensor C preserves the commuting Bell Pauli algebra: paired observables
W tensor W remain paired Paulis, with the required real signs. No inverse
of C is used by the measurement procedure.

The event P=1 is a system of affine parity equations. Constant or dependent
equations either make it inconsistent, giving probability zero immediately,
or reduce it to t independent constraints, t<=k. In the latter case their
signed joint projector on 2n qubits is

    Pi=2^(-t) sum_(s in F2^t) G_s,    G_0=I.

The G_s are products of signed X_j X'_j and Z_j Z'_j. These generators
commute and are real Hermitian matrices; hence all G_s are real signed
Paulis. Write G_s=(-1)^e_s X^u_s Z^v_s. With z=(x,y) and
F(z)=f(x)+f(y), the coefficient of |z> in Pi |phase_f>^tensor2 is exactly

    2^(-n-t) (-1)^F(z) S(z),
    S(z)=sum_s (-1)^r_s(z),
    r_s(z)=F(z+u_s)+F(z)+v_s dot (z+u_s)+e_s.

Here r_0=0. Translation differences lower Boolean degree by at least one,
and the remaining Pauli term is affine. Thus deg(r_s)<=d-1, including for
d=2 and for zero shifts. Negative real Pauli signs are retained in e_s;
there are no unaccounted imaginary amplitudes in S.

Define h(z)=1 when S(z) is nonzero and h(z)=0 otherwise. The sign for s=0
is fixed, so h is a Boolean function of at most 2^t-1 bits r_s(z). Every
Boolean function of that many bits has an ANF of degree at most 2^t-1.
After substitution and Boolean reduction,

    deg(h)<=(d-1)(2^t-1)=L.

Positive event probability means h is not the zero function. The Boolean
Reed--Muller minimum-weight bound then gives E_z h>=2^(-L). When L>2n,
the bound remains valid since a nonzero Boolean function on 2n variables
has weight at least 2^(-2n)>=2^(-L). For t=0 the event is the whole space
and the same formula gives one.

The amplitude normalization yields

    Pr[P=1]=||Pi |phase_f>^tensor2||^2
           =2^(-2t) E_z S(z)^2
           >=2^(-2t) E_z h(z)
           >=2^(-2t-(d-1)(2^t-1)).

The inequality S(z)^2>=h(z) uses only that S is an integer. Nonzero S is
actually even when t>=1, but the proof deliberately does not use that
improvement. The exponent increases with t, giving the stated k bound.

## Simultaneous finite-sample consequence and limits

There are at most 2^((2n+1)k) ordered products of k affine forms, including
zero and constant forms. Padding with the constant-one form includes all
shorter products. Any product not identically zero on the Bell support has
violation probability at least gamma=2^(-2k-(d-1)(2^k-1)). With M fresh IID
Bell samples, its probability of being falsely accepted as a vanishing
equation is at most exp(-gamma M). Therefore

    M >= gamma^(-1) ((2n+1)k ln(2)+ln(1/eta))

excludes all false products simultaneously with probability at least 1-eta.
This statement remains valid for products subsequently chosen adaptively
from the sample nullspace, because the union bound covers the entire fixed
finite family in advance. Each sample consumes two fresh source copies.

For d=3,k=5, gamma=2^(-72), and degree-at-most-five Boolean evaluation has
O(n^5) columns. This is a polynomial sample/time statement with an enormous
constant. It proves only that the empirical nullspace and exact vanishing
space have the same members among products of at most five affine forms.
It does not identify those members, show that they span the nullspace,
exclude false unfactored equations, or recover a phase frame. It assumes
the exact IID source; no noisy-source conclusion is proved here.
