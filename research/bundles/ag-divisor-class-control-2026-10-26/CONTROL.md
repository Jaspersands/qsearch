# An Actual Divisor-Class Escape, Immediately Checked Classically

## Scientific Result

Constructed a complete AG evaluation code on the already certified degree-eight
prime-field cover with dimension43, length176, square126 and FULL cube176.
Unlike the near-canonical and one-point controls, its same-code cubic
annihilator is zero. This is an actual different divisor class, not a
parameter tuple or an unimplemented existence probability.

It is also classically easy. Exact uniform affine-fiber rejection sampling
succeeds with probability at least99827/100003 on EVERY syndrome, so its
expected raw-trial count is at most100003/99827. Four live original-relation
witnesses are retained. No advantage, candidate admission or hardness.

## Construction And Completeness

Use precisely the curve, prime100003, and176 evaluation points D from
prime-ag-tower-source-2026-10-26. Let I=pi^*(base infinity), degree8.
The extra x=51888 is outside D and all thirteen x-a are nonzero squares.
The16 points in its x-fiber are enumerated by independent signs of w1,w2,w3
and y, with w_j^2=x(x-j) and y^2=product_(a=0..12)(x-a).

Let E be the five DISTINCT rational points at indices(0,3,5,9,14) in the
documented product((1,-1),repeat=4) ordering, and take

    G = 11I-E,       deg G=88-5=83=2g+1,       g=41.

G has negative coefficients at these extra finite points. That is a valid
rational divisor, disjoint from D; effectiveness is not needed. The prior
character-decomposition proof gives a complete48-dimensional basis of
L(11I). Vanishing at E imposes five independent evaluation constraints.
Their nullspace is L(G), of dimension43, as also independently forced by
Riemann-Roch. Evaluating its full basis at D constructs B directly.

The previously established normal-generation theorem applies to this divisor
class too. Direct Schur computation yields dim(V^2)=126 and dim(V^3)=176.
Thus ell(K-3G+D)=0. Also G-K=I-E and L(I) consists only of constants;
vanishing on E forces that constant to be zero. Hence ell(G-K)=0 and this
class is not equivalent to K plus an effective degree-three divisor.
The93-section theorem from the earlier full Kummer cover does NOT apply
to every class on this smaller degree-eight cover.

The chosen points are a deterministic fixture, not a uniform Picard sample.
Four five-point selections were explored before retaining this one; all had
full cube. That bounded exploration says nothing about their distribution
in Picard space and is not a scaling experiment.

## Matched Classical Falsifier

The native problem remains Bz=s, all176 coordinates nonzero. Construct the
original affine fiber by RREF and a kernel basis. We verify directly from
the kernel that every coordinate functional is nonzero on that kernel.
Consequently every coordinate of an ideal uniform affine sample is uniform
on F_p, for every s. The union bound gives

    Pr(all coordinates nonzero) >= 1-m/p = 99827/100003.

No independence between different coordinates is needed for this bound.
With ideal independent field draws, rejection gives an exactly uniform
valid witness conditional on success. Seeded executions are reproducibility
controls, not evidence of a uniform PRNG distribution. Cap exhaustion is
UNKNOWN. Each retained witness is verified using the same original B and s.

The conditional quantum decoder bound remains small, but that is irrelevant
to an advantage at this finite size: m/p is tiny. Full cube rank defeats
one attack, not the elementary sampler, the auxiliary-code route, or all
other classical algorithms.

## Scaling Is Still An Open Obligation

Pulling G to a degree-r cover gives degree83r, genus40r+1 and length176r;
it is not the new level's degree-(2g+1) class used in the generic counting
note. A non-effective residual class can acquire sections after pullback.
Therefore full cube rank here must NOT be extrapolated to higher levels.
Selecting new suitable classes per level remains a separate construction
problem. The auxiliary-divisor review also proves eventual auxiliary
existence for every class in its stated parameters; same-code full rank
does not defeat that construction.

This control has no useful-problem reduction, hard asymptotic family,
efficient higher-level generator or implemented quantum circuit. Its value
is a concrete scope test and a native-input falsifier for future claims.

Run from /Users/jaspersands/Developer/qsearch-research-work:

```sh
/opt/anaconda3/bin/python -B ag-divisor-class-control-2026-10-26/divisor_control.py --check
```

Main repository integration remains deferred to a verified local checkout.
No Git, UI, main CLI or registry was changed.
