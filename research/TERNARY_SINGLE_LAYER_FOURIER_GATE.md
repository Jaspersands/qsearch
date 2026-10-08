# Label-Aware Diagonal Phases Followed By Word Fourier Readout

LOCAL DERIVATION / REVIEW PENDING. No novelty, generic quantum lower bound,
efficient decoder or accepted candidate is claimed. This gate is not the
label-independent product-POVM theorem: the initial diagonal may be collective,
depend on ALL full public labels and be arbitrarily difficult to compute.

## Receiver And Prior

Take M original native qutrits with two IID uniform full frequency rows per
register in Z_q^n, q=3^r. Write D=3^M, G=q^n and Q=q/3. The source is

    |psi_s>=D^(-1/2) sum_x chi_q(F(x).s)|x>, x in F3^M.

The target is s_j mod3, averaged over ALL uniform secrets. For every fixed
public label matrix, allow ANY initial public word-diagonal unitary

    U_phi |x>=exp(i*phi(x))|x>.

It may depend on the complete label matrix and independent public randomness.
Then apply inverse F3 on EVERY original word register, measure every word
output and perform ANY classical decision using all labels and all outputs.
There is no assumption that phi is polynomial, local or efficiently evaluable.
Partial-block quadratic chirps and top-digit phases are included here.

Do not replace this template with arbitrary label-dependent local POVMs,
multiple alternating phase/mixing layers, coherent subset selection, a new
source distribution or additional secret-bearing ancillas. They are outside
the statement. A public computational-basis permutation before the Fourier
readout can also change the offset multiplicities. The extension below covers
label-INDEPENDENT permutations and label-dependent AFFINE maps, not arbitrary
label-dependent nonlinear permutations.

## Exact Offset-Energy Bound For Each Label Matrix

For nonzero delta in F3^M and h=1,2 define

    N_(delta,h)=#{x: F(x+delta)-F(x)=Q*h*e_j modq}.
    C_(delta,h)=sum_(these x) exp(i*(phi(x)-phi(x+delta))).
    E=sum_(delta!=0,h=1,2) N_(delta,h)^2.

The uniform-secret trit ensemble has off-diagonal entries only when the full
frequency difference is0 or Q*h*e_j. The zero-difference terms are independent
of t and cancel when subtracting the mean output law p_bar. Thus

    p_t(z)-p_bar(z)=D^(-2) sum_(delta!=0) omega^(z.delta)
                          * sum_(h=1,2) C_(delta,h)*omega^(-t*h).

Finite Fourier orthogonality on BOTH the word cube and the logical trit gives

    sum_(z,t) |p_t(z)-p_bar(z)|^2
      =3*D^(-3) sum_(delta,h) |C_(delta,h)|^2
      <=3*D^(-3)*E.

For a real three-vector v with sum0, max(v)<=sqrt((2/3)*sum(v_t^2)). For the
best classical decoder, use this inequality and Cauchy-Schwarz across the D
outputs. The complete RAW success advantage therefore satisfies

    (P_correct-1/3)^2 <= min(4/9, 2*E/(9*D^2)).

This holds for EVERY fixed public label matrix and EVERY initial diagonal
phase. It does not require computing E as an algorithm. It already grants an
exponential optimal classical decoder, so efficient postprocessing cannot
evade it. Every failure/rejection must remain in the raw score; herald-only
conditional success is not the quantity bounded.

## Native Population Moment: No IID-Graph Assumption

Fix delta of support k. Its frequency difference depends only on k active
word coordinates. There are3^k active assignments, each repeated3^(M-k)
times by inactive coordinates. At one active coordinate, the transition
coefficient rows on the two native frequencies are

    delta=1: (1,0), (-1,1), (0,-1);
    delta=2: (0,1), (-1,0), (1,-1).

Every row has a unit coefficient. Any two DISTINCT rows in either list have
determinant +/-1. Two distinct active assignments differ at some coordinate,
which supplies a unit minor for their two COMPLETE difference equations.
Hence their frequency differences are jointly uniform, including over the
COMPOSITE ring Z_(3^r). No independence of all edges or all graph vertices is
assumed. For either h,

    E[N_(delta,h)^2]
      =D^2/(3^k*G) + D^2*(1-3^(-k))/G^2.

There are binomial(M,k)*2^k offsets of support k. With A=(5/3)^M,

    E[E]=2*D^2*((A-1)/G + (D-A)/G^2).
    E[P_correct-1/3]
      <=min(2/3, (2/3)*sqrt((A-1)/G + (D-A)/G^2)).

The latter uses Jensen AFTER the per-label bound; phase policies may depend
on their labels because the per-label envelope does not depend on phi.
Independent public coins are covered by conditioning on them, not by granting
independent conditional labels after secret-dependent selection.

At the current underfull batch M=n*r-2, G=9D. In particular,

    (mean advantage upper)^2
      <= (4/81)*((5/9)^M - 3^(-M))
         +(4/729)*(3^(-M) - (5/27)^M),

which decays exponentially in M. Retain the exact rational expression, not a
loose constant-floor approximation. Larger M is allowed by the general formula;
polynomial copy surplus can make this bound vacuous and is NOT excluded.

## Word-Permutation Extension

An invertible affine public word map x->A*x+b over F3 before word Fourier
readout only relabels outputs by A^T and supplies an irrelevant output phase.
This remains true when A,b depend on all public labels. Conjugating an initial
diagonal through the permutation still gives an arbitrary diagonal, so the
same bound covers these affine maps. Entangling linear SUM gates alone do not
escape this receiver class.

More generally fix ANY word permutation pi INDEPENDENT of the random labels.
Let sigma be the complete original transition coefficient signature in the
2M native frequencies. At each active coordinate it is one of six directed
simplex differences, and inactive coordinates have signature0. A signature
of support k occurs r_sigma=3^(M-k) times among original ordered word pairs.
Let m_(delta,sigma) count the occurrences routed by pi into output difference
delta. Then sum_sigma m_(delta,sigma)=D for every nonzero delta, and
sum_delta m_(delta,sigma)=r_sigma. For sigma!=+/-tau a unit minor again gives
jointly uniform differences. If all local signatures are parallel but their
signs differ across coordinates, the minor can be+/-2 rather than+/-1;
it is still a UNIT at every ternary root. Opposite signatures cannot BOTH
equalQ*e_j. Do not discard this mixed-sign case.
Thus the exact positive-class energy expectation is

    sum_delta E[N_(delta,1)^2]
      =(D-1)*D^2/G^2
       +(1/G-1/G^2)*sum_(delta,sigma) m_(delta,sigma)^2
       -G^(-2)*sum_(delta,sigma) m_(delta,sigma)*m_(delta,-sigma).

The final sum is nonnegative. Splitting any signature across offsets cannot
increase its sum of squares, and

    sum_sigma r_sigma^2 = D^2*((5/3)^M-1).

This recovers the SAME population upper bound. Identity routing attains its
energy expectation. Public independent random permutations are covered by
conditioning. A permutation chosen from the random labels is not fixed for
this calculation; its routing can correlate with the marked-event indicators.
Only the affine label-dependent subclass has the separate exact output-
relabeling argument. Do not extend the claim to other label-sensitive maps.

## Necessary Target For A Surviving Nonlinear Routing

For any label-dependent nonlinear permutation pi, the per-label energy bound
still holds with offsets computed AFTER pi. Only the closed expectation can
change. Therefore mean raw advantage>=epsilon requires

    E[sum_(delta,h) |C_(delta,h)|^2] >= (9/2)*epsilon^2*D^2,
    E[E_pi] >= (9/2)*epsilon^2*D^2.

Concentrating edge counts is necessary, not sufficient: phases must align,
the receiver must be efficient and a costed decoder is still needed.
The total number K of useful directed edges is unchanged by ANY permutation,
and its exact native expectation is2D(D-1)/G. If a proposed map has a uniform
worst-case multiplicity bound N_(delta,h)<=L for every label instance, then
E_pi<=L*K pointwise. Its mean raw advantage is therefore at most

    sqrt(4*L*(D-1)/(9*D*G)).

Consequently a route promising epsilon needs

    L >= 9*epsilon^2*D*G/(4*(D-1)).

At G=9D even epsilon=1/poly(nr) requires L=D/poly(nr): nearly exponential
multiplicities in at least some instances. A polynomial-width packet or a few
found edges is not a constant or inverse-polynomial learner of this type.
This is a requirement on a claimed UNIFORM cap, not permission to replace
E[N_max*K] by E[N_max]*E[K]; those quantities may correlate.
The exact ledger records epsilon=1/(nr)^2 through r64. It supplies no map,
source inverse, witness solver, efficient decoder or generic quantum bound.

## Tight Native Control And Attempted Refutation

The selected legal q81,n1,M2 rows(1,2),(26,52) have E=50. With no chirp,
the exact uniform-prior Fourier MAP score is19/27. Its advantage10/27
saturates2E/(9D^2)=100/729. This is a selected-label control, not an IID
population algorithm. It shows the per-label bound is not merely a loose
phase-averaging estimate. Phase changes cannot beat this saturated control
within this receiver template.

Tests must also enumerate complete native frequency populations at prime and
composite roots, include inactive-coordinate multiplicities, replay ALL
uniform secrets physically for partial/cross/top-digit phases, and compare
the actual squared signal to both Parseval and the phase-independent envelope.
These exponential controls are calibration, not scalable receiver execution.

This result closes the SINGLE-phase-layer version of the surviving partial-
block idea. It does not close partial-block phases after a noncommuting mixer,
a label-dependent NONLINEAR reversible word map, a constructive frequency-fiber change
of basis, adaptive measurements or costed polynomial surplus samples.
Those are the next higher-upside targets. Do not add more single-chirp scans.
Alternatively charge a larger, still polynomial source batch and seek an
efficient decoder for its quantum-produced records. This gate can be vacuous
there; it does not prove entangling or multilayer measurements necessary.

Falsifiers: the coefficient unit minor fails; distinct active assignments are
not pairwise uniform under the stated IID source; inactive multiplicities are
omitted; Parseval loses a factor ofD or3; a complete raw score exceeds its
exact envelope; or the claim is extended to a circuit with an earlier mixer,
permutation, secret-dependent source selection or another source law.

## Relation To Literature

[Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0501044) analyze
optimal dihedral measurements and their implementation's subset-sum
connection. The derivation here is a separate native-qutrit, restricted
receiver calculation, NOT a corollary of their optimal-measurement theorem.
[Gupte, Ragavan and Zhandry](https://arxiv.org/abs/2609.40062) constrain a
different post-subset-sum label-loss template. All high labels are retained
here; their label-loss theorem is not imported as this proof. Novelty remains
unreviewed.

```
python theorems/ternary_single_layer_fourier_gate.py --write
node research/certificates/ternary_single_layer_fourier_gate_crosscheck.js
python -m pytest -q tests/test_ternary_single_layer_fourier_gate.py
```
