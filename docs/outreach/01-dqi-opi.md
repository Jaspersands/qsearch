# Draft: classical attacks on explicit prime-character OPI instances

Status: DRAFT, not sent. Recipients: [authors of the DQI and prime-field OPI papers the
project cites; confirm before sending].

---

Subject: Classical attacks on explicit quadratic-character OPI instances

Dear [names],

We run a small project that proposes quantum mechanisms and then attacks each one with
the strongest classical method we can find. One target was optimal polynomial
intersection (OPI) with explicit power-character constraints. These are instances where
membership is decided by modular exponentiation, so there is no random acceptance table
and no oracle. We wanted to know whether such explicit predicates keep perfect high-rate
intersection out of classical reach. We have a finite answer for one family and would
value your view on whether it is of interest, or already known to you.

**Setting.** p = 2^61 − 1, N = 127 points, quadratic characters (r = 2), public shifts
and seeded orientations. Position i accepts Q when Q(i) − t_i lies in a prescribed coset of
the squares, optionally also allowing zero.

**What we found.**

- **High rate (K = 77).** Classical attacks find perfect 127/127 witnesses on every saved
  input. Common-coset inputs fall to power completion, a formal square root at infinity.
  Mixed-orientation inputs fall to a norm search from F_{p^2}: write the residual target
  as R² − νZ² and read Q off R. This works in both the zero-allowing and the strict modes.
- **We have no fixed-input guarantee for the N = 127 inputs in the original field.** A
  Morse-progression argument with twist and exterior-power trace bounds lower-bounds the
  success rate for a fixed input. For the saved N = 127 inputs over the original 61-bit
  prime both bounds are zero, because their error
  terms exceed p. That says only that these conservative bounds do not apply; it is not
  evidence of hardness. For one input (strict, seed 29) re-posed over a declared 192-bit
  prime, the exterior bound is positive and a perfect strict witness is found. A lift
  changes the problem, so this does not solve the original input.
- **Low rate (K = 39) is open.** On the mixed inputs the best classical witness is
  109/127, from adaptive local repair. That is a witnessed score, not an optimum. Among
  the radii evaluated, a finite certificate for a known DQI route beats it only at
  radius ℓ = 32, with a certified mean of at least 0.9028 of the positions. The
  certificate assumes an exact source and an exact unique decoder beyond half the
  minimum distance. No such decoder circuit has been built.

**What we do not claim.** This is not an all-rate or all-field dequantization of OPI. It
does not touch the asymptotic guarantee or the random-oracle separation: a finite
near-perfect classical word does not disprove asymptotic perfect quantum search. There
is no hardness claim and no matched runtime comparison. Our source notes mark the local
derivations as review pending; none has had independent review.

**Reproducing it.** The classical solvers are packaged separately:

```bash
pip install -e packages/qsearch_classical
docs/papers/classical-competitors/reproduce.sh OUT
```

The script regenerates every report and compares each number with the committed value.
Repository: [link]. A short write-up is attached [if sending the draft].

Two questions, if you have time:

1. Is the explicit quadratic-character family already known to be classically easy at
   high rate, for example through the norm-form argument?
2. Is the low-rate regime, roughly K/N below 1/3 with explicit characters, one where you
   would expect the quantum route to beat every classical method?

Thank you for considering this.

[signature]
