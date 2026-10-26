# Parabolic Cut-List Correction

2026-10-23. The older October 11 investigations contain unsupported
dequantization and lower-bound claims. Their small tests did not validate
the asymptotic conclusions. Do not use their current negative-result labels
to exclude an entire research direction. This is a scoped correction, not
a complete audit of every claim or every downstream artifact.

## Confirmed Errors

1. **Field size is not its encoding length.** O(n q^k) is a valid symplectic
   transvection query upper bound, but is polynomial in n,log(q) only in a
   parameter regime where q^k is polynomial in those parameters. The
   sufficient condition k<=C log_q(n) was present in the body, then dropped
   from the summary and conclusions. Even k=1 costs exponentially many
   queries as log(q) grows with n fixed. The unitary q^(2k) statement has
   the same scope error. A polynomial classical upper bound would exclude
   a superpolynomial separation in that regime, not every quantum speedup.

2. **The orthogonal accepted-sample set can be empty.** In a split quadratic
   space of dimension 2m, for a maximal totally singular U, Uperp=U and
   every vector there is singular. A reflection sampler restricted to
   NONSINGULAR vectors therefore has acceptance probability ZERO, not
   Omega(q^-m). The displayed density formula was applied to a zero-
   dimensional quotient. The claimed universal reconstruction bound is
   false as stated; this does not prove that another classical algorithm
   is slow. Example: Q=x1*y1+x2*y2 and U={(x1,x2,0,0)} over F_3.

3. **The unitary accepted vectors need not span the asserted complement.**
   In odd Hermitian dimension 2m+1, a maximal isotropic U has a one-
   dimensional anisotropic quotient Uperp/U. Every isotropic vector in
   Uperp is then already in U. The proposed isotropic-vector sampler can
   never accumulate dim(Uperp)=m+1 independent accepted vectors. A revised
   algorithm might use their span U directly; that is not the stated proof.

4. **Counting observables is not a task-specific gate lower bound.** An
   exponentially large commutant does not force every informative
   measurement, or every hidden-subgroup learner, to implement a generic
   arbitrary element of that algebra. Likewise, an exponentially small
   bound for EACH Fourier outcome is not a bound for a union of useful
   outcomes. The old commutant/density statements do not exclude all
   efficient multi-copy or additive-Fourier algorithms. A specifically
   defined projection can still have a small acceptance probability.

5. **The bit-size conversion omitted log(q).** With matrix encoding length
   L=Theta(n^2 log q), q^n is 2^Theta(sqrt(L log q)), not uniformly
   2^O(sqrt L). The latter bound assumes bounded q. With fixed n and
   growing q it is exponential in L, not a uniform subexponential bound.

The algebraic symplectic membership criterion T_v in P_U iff v in Uperp
survives this correction. Nothing here restores the old fake field-level
Lie oracle or a classical birthday lower bound for unrestricted group queries.

## A Constructive Alternative, Not Just A Reopened Label

SYMPLECTIC_PRIME_SQUARE_REDUCTION.md gives a new proposed reduction for
Sp_(2n)(Z/p^2), odd prime p and n>=2, with a free Lagrangian stabilizer.
The socle really is additive, and legal elementary Levi probes give degree-
two hidden polynomial graphs for the remaining matrix coefficients. The
published HPGP algorithm supplies the quantum subroutine. This is a
different input from Sp(F_p); a field-only oracle cannot implement it.
There is no current classical lower bound or natural application admission.

## Validation And Mechanical Follow-Up

`tests/test_parabolic_cut_scope.py` contains exact controls for items 1--3.
The new symplectic reduction has independent actual-matrix/fiber tests.
Neither test suite proves a quantum runtime or a classical complexity bound;
the general statements above have the elementary proofs given here.

The historical notes now carry overriding correction banners. Do not
silently treat their untouched remaining sections as newly reviewed.
The referenced old theorem modules were not found at their stated paths;
their note's claim of four independent verifications is not current evidence.

Gemini follow-up, after files are resident: trace the old negative-result
and report dependencies, mark affected claims superseded or invalid with
the precise scope above, and regenerate only those reports. In particular
check NEG-ISOTROPIC-PARABOLIC-DEQUANTIZATION-BOUND and descendants. Do not
convert a withdrawn negative result into an accepted speedup. The central
negative-result file is now resident (metadata rechecked during this pass),
but was not opened or edited: report/registry wiring remains Gemini's task.
