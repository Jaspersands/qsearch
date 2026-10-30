# Black-Box Quotient Bridge: Paid Coordinates And Coherent Cleanup

2026-10-23. LOCAL DERIVATION; INDEPENDENT REVIEW PENDING.
This audits the normalizer reduction, not a new hard input or a speedup.
The new simulation is a bounded falsifier, not general quantum software.

## 1. What Changed

The large-prime log backend is not needed for the most general proposed
reduction. Existing p-group normalizer methods can be used if collection
is efficient. Nice cyclic-factor maps supply a proposed polynomial-time
QUANTUM collection procedure, even when ambient nilpotency class grows.
This removes the earlier small-prime rejection branch in the theoretical
reduction. The backend retains its p>a check and is still useful as an
independent exact arithmetic control.

The general theorem remains conditional on a reviewed terminal solver and
on this black-box composition. For k<=2 the published nil-2 terminal solver
suffices. For general fixed k the repository's Rees theorem remains an
unreviewed dependency. No all-prime uniform FPT estimate is asserted here.

## 2. Imported Interfaces, Not New Algorithms

- [IMS, Corollary5/Theorems6,8,10](https://arxiv.org/html/quant-ph/0102014)
  supply constructive membership with straight-line output, nice cyclic
  factor maps, normal HSP, and structure algorithms modulo a known solvable
  normal subgroup. Membership decisions alone would be insufficient.
- [ISS, Section3](https://arxiv.org/html/0707.1260) supplies the polynomial
  p-group normalizer statement with refined polycyclic presentation and
  efficient collection, citing Eick2002 and Luks1992. It does not justify
  dropping the collection premise for arbitrary-class classical inputs.
- [Luks1992, original report](https://www.cs.uoregon.edu/Reports/TR-1992-017.pdf)
  states dependence on the largest group-order prime OTHER than the field
  characteristic. Thus its use for p-subgroups in characteristic p does
  not itself impose a polynomial-in-p cost. This observation does not
  replace Eick's mixed-torsion interface or a complete runtime audit.

The applications and error bounds below are local derivations. None of
these papers is cited as having stated our bounded-index corollary.

## 3. Canonical Coordinates Without Classical Collection

Maintain B<=H<=S in the ORIGINAL uniquely encoded group G, with B normal
in S. Store each generator as an actual G-encoding. Q=S/B is the current
group. Apply the known-solvable-quotient preprocessing directly to S/B.
Never construct it by nesting all previous quotient oracle wrappers.

Conditional on valid classical preprocessing, fix a composition series

    Q=Q_1 > Q_2 > ... > Q_(m+1)=1

and maps pi_i:Q_i -> F_p with kernel Q_(i+1). Select original representatives
g_i whose image under pi_i is1 (power a nonzero image by its inverse).
For q represented by s in S, set r_1=s and repeat

    a_i=pi_i(r_i B),       r_(i+1)=g_i^(-a_i)*r_i.

Then r_(i+1)B lies in Q_(i+1). The tuple (a_1,...,a_m) is unique, independent
of the original representative s. Its section is g_1^a_1 ... g_m^a_m in G.
The maps may be evaluated by amplified bounded-error quantum routines;
they are not assumed to be classically easy or exact after preprocessing.

For multiplication, evaluate both sections in G, multiply, and compute
this tuple. The input length is O(N log p), there are at most N factor
calls, and exponentiation uses O(log p) original operations per factor.
Original encodings and direct S/B algorithms prevent a poly(N)^N wrapper
recursion. New subgroup generators are evaluated once and stored, not
expanded as exponentially large words in the original generators.

Run the known normalizer algorithm with these collection calls on classical
arguments. Cap its randomized control flow, amplify each call to the
predetermined global failure budget, and separately charge all original
group operations. A nonunique valid generating-set output need NOT be
coherently copied. Only deterministic mathematical functions, such as the
fixed normal-form coordinates, are compiled as coherent oracles.

For a section sigma:Q->S, f(sigma(q)) hides H/B: the lifted difference is
in H exactly when its quotient is in H/B. Normality of B in S and B<=H
are the needed properties; sigma need not be a homomorphism. Evaluate the
original f once, then uncompute the section. The label length is unchanged.

## 4. Two Different Coherent Error Bounds

Copy the computational-basis INPUT into scratch and leave its original
register untouched. This is not a claim that unknown quantum states can
be cloned into independent copies. Run a purified, capped computation V_x
on the scratch, with all measurements/randomness retained coherently. Its
answer is the unique function F(x), with worst-input error at most delta.
Classical preprocessing must already have fixed one valid representation.
All subgroup-state preparation, its inverse, and repeated fresh resources
are charged inside V_x. A copy-only supply of unknown states does not give
this circuit. Invalid strings may have arbitrary semantics, but every
branch must halt within the chosen cap; ideal queries stay in the domain.

Let P_x project onto workspace states whose answer equals F(x). Write
V_x|0>=good_x+bad_x with ||bad_x||^2=delta_x<=delta. Apply answer-XOR C to
target Y, then V_x^dagger. Compare to the ideal answer-XOR C_F.

For arbitrary target/reference state psi, before uncomputation,

    (C-C_F)(V_x|0> tensor psi)

vanishes on good_x. On each orthogonal bad-answer component, the difference
of two unitaries has norm at most2. Therefore the initialized-scratch
operator norm error is at most 2*sqrt(delta_x). Retained input blocks are
orthogonal, so the same maximum bound applies to superpositions of x and
arbitrary external references. The output register is NOT assumed zero.

For a fresh ZERO target, distinct classical answers are orthogonal and
the sharper EXACT squared vector error is 2*delta_x. This bound cannot be
used indiscriminately for later oracle calls. A one-bit wrong-answer branch
of weight delta and a target |-> saturate squared error4*delta.

For T compiled calls, a hybrid on ideal initialized-scratch states gives
operator error at most 2*T*sqrt(delta), hence channel diamond error at most
4*T*sqrt(delta). Setting delta<=epsilon_oracle^2/(16*T^2) suffices. Pay
logarithmic amplification in T/epsilon_oracle. Other errors, including
preprocessing, incomplete intersections, approximate transforms and the
terminal solver, receive separate budgets. No successful-branch conditioning.

To obtain the in-place group multiplication expected by a black-box routine,
first compute a product into fresh scratch, swap it into the destination,
and erase the old destination by computing the inverse product into it.
The latter XOR targets an existing register, so the arbitrary-target bound
is genuinely required. Count both evaluations and their cleanup.

## 5. Falsifier: Basis Accuracy Without A Retained Input

On d addresses take s=d^(-1/2)*sum_x |x> and U=I-2|s><s|. Used as an
in-place algorithm for the identity function, its computational-basis
failure probability is delta=4(d-1)/d^2, which tends to zero.

The naive compiler is W=(U^dagger tensor I)*COPY*U, where COPY copies the
modified address to a fresh output. Ideal copying is V=COPY. Directly,

    V^dagger W = (1-2/d)*U.

For v=(|0>-|1>)/sqrt(2), the input psi=(s+v)/sqrt(2) has <psi|U|psi>=0.
Thus W|psi> and V|psi> are exactly ORTHOGONAL: trace-norm distance2, despite
vanishing basis failure. This proves a physical channel discrepancy, not
just a vector-norm discrepancy caused by an unobservable global phase.

Indeed, uniform input s alone is a misleading witness: its vector error
approaches2 but its output trace distance is only 2*sqrt(delta), approaching
zero. The tests retain both facts to prevent that incorrect inference.
At d=2^40 the failure probability is below2^-37; the balanced witness still
has trace distance2. This last case uses exact symbolic formulas, not a
dense matrix allocation. The retained-input construction avoids this flaw.

## 6. Complete Bounded Reduction Control

Use the fixed free class-three BCH group over F_7 with basis X,Y,Z,U,V,
where [X,Y]=Z, [X,Z]=U, [Y,Z]=V. Set A=<Z,U,V>, and use the coset oracle
for the conjugate by exp(tY) of H=<X,Z,U>. The control covers t=0,1,3,6.

The numeric base label on coordinates (a,b,c,d,e) is

    (b, e-b*c/2-a*b^2/6).

It is constant exactly on left H-cosets. The simulator receives the label
evaluator, NOT the hidden intersection. Finite abelian Fourier sampling on
A learns K, then the public normalizer backend computes S, and another
abelian Fourier stage on S/K learns the terminal subgroup. Pulling back
the learned generators recovers H. K is noncentral in S and not normal in
G, so quotienting the ambient group directly would be invalid.

The quotient section is deliberately nonhomomorphic. Every pair of quotient
addresses is checked against the original oracle fiber relation. Tests also
check the action lift and BCH associativity. These checks can falsify the
composition, but are NOT proofs of its asymptotic runtime or input contract.

Enumeration of 343 and49 addresses makes this simulator exponential in
register dimension. The numeric labels have easy classical structure.
It is a bounded mechanism fixture, not a candidate or a hardness benchmark.
The implementation does not run black-box preprocessing, Eick/Luks, quantum
hardware, or the proposed Rees solver.

## 7. Remaining Kill Tests And Decision

1. Independently audit the known-normalizer interface with quantum collection.
   A hidden enumeration of field elements, subgroup orbits, or p-power
   digits with nonpolynomial bit cost would invalidate the claimed import.
2. Verify nice factor-map evaluation in S/B supplies fixed unique outputs
   and polynomial bounded-error runtimes. Construction of a composition
   series without these evaluation maps would not suffice.
3. Check whole-algorithm failure caps with original-group representatives.
   A state-only hiding source cannot be substituted for the ordinary oracle.
4. Independently review Rees for k>2. No fixed-k theorem implies a uniform
   FPT bound without checking its dependence on k and log p.
5. Find a useful native source that survives public-description classical
   attacks. This is still absent; more synthetic oracle examples do not help.

Recommendation: retain this tightened reduction as REVIEW PENDING, stop
expanding the normalizer backend, and prioritize independent scrutiny or
a genuinely useful source. No candidate admission or speedup flag changes.
