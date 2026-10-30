# Small-Bias Four-List Attack On Auxiliary Divisor Classes

Date: 2026-10-26. Parent derivation; independent review pending.

## Claim And Scope

Under the exact geometric, prime-sampling, class-label, pairing and rational
halving contract in `../auxiliary-construction-check-2026-10-26/REVIEW.md`,
the certified tower's auxiliary-divisor construction admits the conditional
bound

```text
T_pre + 2^ceil(r_2/3) poly(g, log q)
S_pre + 2^ceil(r_2/3) poly(g, log q)
```

for every existing dyadic level e>=64, q=100003, g=5e+1. Here
r_2=dim_F2 J(F_q)/2J(F_q)<=2g; it is not a measured small rank. Every
prime-sampling, divisor-representation and class-label operation is charged
per sample, not hidden as one-time preprocessing. The result remains
exponential when r_2 grows linearly. It is not an implemented native solver,
a hardness result, or a quantum advantage.

The four-list join is the known generalized-birthday mechanism. See
[Wagner's author page](https://people.eecs.berkeley.edu/~daw/papers/genbday.html),
which also identifies prior work by Camion and Patarin. The purpose here is
to justify this application to biased prime-class distributions, including
shared-index dependencies. No novelty claim is made. The related paper
[Lindo--Sagitov](https://arxiv.org/abs/1507.05490) studies solution-count
distributions for uniform cyclic-group inputs; that is not invoked as a
theorem about the nonuniform binary-group inputs below.

## Native Relation And Access

Original input remains the complete AG generator B over F_100003 and any
syndrome s. Output must satisfy Bz=s and z_i!=0 at every original coordinate.
Set d=2g+1=10e+3, m=22e, a=2e-9, C=K-G+D. With rational base point O,

```text
tau = [C-(2d+a)O] in Q=J(F_q)/2J(F_q).
```

Find an effective divisor A of degree a with [A-aO]=tau. Rationally halve
the class C-A-2dO to obtain degree-d class F. Charge moving F away from D,
RR spaces, differential residues and common-basis matroid intersection.
The reviewed auxiliary-code norm solve then gives an original native
witness for every s. Matching labels alone is NOT such a witness.

Choose four positive degrees n_i summing to a. Sample independent exact
uniform degree-n_i prime divisors with replacement, and compute their
correct labels [P-n_i O] in an actual basis of Q. Repeated prime divisors
are allowed. Approximate samplers need a separate error budget.

The previously reviewed prime-character estimate is

```text
C_n=(g+1)(n+6),
|mu_hat_n(chi)| <= epsilon_n=2 C_n q^(-n/2),  chi nontrivial,
```

provided q^(n/2)>=2C_n. It concerns degree-zero labels and geometric
O-split double covers, not Pic/2Pic with its forbidden degree coordinate.
We do not assume prime classes are uniform or enumerate quadratic covers.

## Abstract Four-List Lemma

Let Q=F_2^r, r>=3, t=floor(r/3), s=r-3t, delta=1 if s>0 else0,
L=2^(t+delta). There are four independent lists of L independent samples;
list i has any distribution mu_i such that every nontrivial Fourier
coefficient has absolute value at most epsilon<=1/(4L). The four laws
can differ. For an arbitrary fixed target tau:

1. Join lists1,2 on low-t-bit XOR zero.
2. Join lists3,4 on low-t-bit XOR low(tau).
3. Match full pair XORs whose XOR is tau.

Store one left pair per full XOR; it suffices because all tuples are
allowed and there is no disjointness constraint. Count every filtered
pair, even duplicate values, and abort after 40000L such pairs. Independent
fresh attempts succeed with probability greater than 1/8000 each. Space
is O(L poly(r)) and expected total time O(L poly(r)); constants are loose.
The r<=2 cases are constant-sized and are outside the implemented lemma.

### First Moment

Let Z count all filtered matching quadruples. For one tuple the constraints
have probability p_u=2^(-(r+t)) under uniform draws. For each low bit the
frequency row code is span{1100,0011}; for each high bit it is span{1111}.
The Fourier expansion of the indicator therefore gives

```text
|p/p_u-1| <= 2(2^t-1)epsilon^2
            + ((2^t-1)^2+(2^(r-t)-1)2^(2t))epsilon^4
          <= 2^(t+1)epsilon^2+2^(r+t)epsilon^4
          <= 1/16+1/256 <1/8.
```

For the last bound t>=1 and r+t-4(t+delta)=s-4delta<=0.
Thus p>=(7/8)p_u and E Z=L^4 p>=7/8, since 4delta-s>=0.
Target-dependent character phases can change signs but not this bound.

### Second Moment: No Independence Between Matches

Two tuples share the same sample index in exactly H subset{1,2,3,4};
h=|H|. There are L^4(L-1)^(4-h) ordered pairs of tuples of this type.
They involve v=8-h independent random variables. Equal sampled VALUES at
different indices do not merge independent variables.

Identify the eight tuple positions according to H. Let C_low be the
binary row span of the four pair constraints (12),(34),(1'2'),(3'4'),
and C_high that of the two all-four constraints. Write their ranks as
R_low,R_high. For a support A subset{1,...,v}, let

```text
D_low(A)  = R_low  - rank(C_low projected onto A-complement),
D_high(A) = R_high - rank(C_high projected onto A-complement).
```

The number of combined Fourier assignments with nonzero variable
frequencies confined to A is 2^(t D_low+(r-t)D_high). For assignments
with EXACT support A this is an upper bound. Independence of the v inputs
bounds their characteristic-function product by epsilon^|A|. Summing
over exact supports with this upper count is valid; it overcounts, rather
than replacing epsilon^|actual support| by an incorrect smaller number.

The constraint rank is t R_low+(r-t)R_high. Consistency affects the target
phases, not the upper bound. The following finite binary-rank inequality
holds for every H,A:

```text
8-h-R_low-2R_high+D_low(A)+2D_high(A)-|A| <=0.       (*)
```

`overlap_certificate()` checks all sum_H 2^(8-|H|)=1296 cases exactly,
using binary elimination; maximum is zero for every H. It is a finite
case lemma covering all r, not a numerical extrapolation. Rank patterns:

| H type | v | R_low | R_high |
| --- | ---: | ---: | ---: |
| empty | 8 | 4 | 2 |
| one shared index | 7 | 4 | 2 |
| two, one complete pair | 6 | 3 | 2 |
| two, crossing pairs | 6 | 4 | 2 |
| three | 5 | 3 | 2 |
| all four | 4 | 2 | 1 |

Combining the tuple count upper L^(8-h), the constraint normalization,
the support count and epsilon<=1/(4L), the coefficient of t in the base-2
exponent is exactly (*). The remaining factor is at most

```text
2^[delta(8-h-|A|)+s(D_high-R_high)] 4^(-|A|)
  <= 2^(8-h) (1/8)^|A|.
```

Here D_high<=R_high, 8-h-|A|>=0, and delta<=1. Therefore

```text
E Z^2 <= sum_H (9/4)^(8-|H|) = (117/16)^4,
Pr(Z>0) >= (E Z)^2/E Z^2
         >= (7/8)^2/(117/16)^4
         =50176/187388721 >1/4000.
```

This is deliberately conservative. No Bernoulli independence or Poisson
approximation for the L^4 tuple indicators is used.

### Bounded Storage And Aborts

For either two-list low-bit join, Fourier inversion gives pair-filter
probability <=2^-t(1+(2^t-1)epsilon^2). The expected total number M of
filtered pairs in both joins is <5L, including r not divisible by3.
Markov gives Pr(M>40000L)<1/8000. Aborting cannot remove more than this
probability, so Pr(success and no abort)>1/8000. Generation, bucketing,
sorting/hashing and a bounded pair scan cost O(L poly(r)) per attempt;
divisor sizes and arithmetic multiply this cost. The cap guarantees
storage even on highly atypical lists. A cap or failed attempt is UNKNOWN,
not evidence of infeasibility or hardness. Fresh independent attempts
eventually succeed with finite expected cost under the access premises.

## Degree Budget On The Actual Tower

For even e choose balanced degrees adding to a=2e-9:

```text
n_min=e/2-3, (n_1,n_2,n_3,n_4)=(n_min,n_min+1,n_min+1,n_min+1).
```

It suffices, for each n_i, that

```text
100003^n_i >=64 C_n_i^2 2^(2 ceil(r_2/3)).           (**)
```

This guarantees epsilon_n_i<=1/(4L), and implies the earlier prime-count
premise and nonempty sampling. At e64 and worst rank r_2=2g=642,
n_min=29, log2 L=214; the exact ratio of the two sides of (**) exceeds
1,776,281. At worst rank, this criterion fails for e8,16,32. Failure of
the criterion does not prove the attack fails at those levels.

For e->e+2, n_min increases by1, r_upper=10e+2 by20, and
ceil(r_upper/3) by at most7. Also
C_n_min=(5e+2)(e/2+3) has successive ratio <2 for e>=64. Thus the
ratio in (**) grows by more than 100003/(4*2^14)>1. Other degrees are
easier: increasing n by1 changes the ratio by
100003*((n+6)/(n+7))^2>1. This proves the bound for every even e>=64,
hence every existing dyadic level, without a typical-rank assumption.

The analytic length 2^214 at e64 was NOT allocated or run. Tests of the
binary join are verifier controls, not simulations of the native problem.

## Falsifiers And Remaining Debt

- Any violation of (*) or first/second-moment bounds breaks this proof.
- Sampling laws with biased characters larger than 1/(4L) are outside
  the theorem. This is not certified merely by list behavior.
- Correlated prime draws, incorrect labels or uncharged per-prime class
  computation invalidate the stated application/cost.
- A supplied coset match is not enough without rational halving, RR,
  moving, residues and final native verification.
- A large r_2 is not a hardness proof. Low-rank tower structure, effective
  divisor algorithms or other classical native attacks may be stronger.
- No eight-list or polynomial attack follows from this lemma. Nor does
  failure of a balanced eight-list sufficient budget imply an obstruction
  to other list distributions, sieves or divisor constructions.
- Independent mathematical review and the separate geometry-access
  review are required before treating this as a consolidated checkpoint.
