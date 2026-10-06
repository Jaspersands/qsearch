# Native Ring-LWE: Sparse Inversion Does Not Supply The Witness

Date: 2026-10-04. LOCAL DERIVATION / REVIEW PENDING.

Follow-up to NATIVE_RLWE_ROTATIONAL_WITNESS_REDUCTION. No independent
verification, novelty, general lattice/quantum lower bound or security
estimate. This is an average-input existence bound for a SPECIFIC output
restriction in the ORIGINAL coefficient basis, not a runtime bound for
all witness finders. A better/reduced basis remains outside that restriction.

## 1. Decision

The one-witness target invites a tempting algebraic shortcut: set one
coefficient block to zero or sparse, and solve the other by modular
inversion while tuning the scalar label. On typical native labels this
does not produce a sufficiently short point. A union bound covers EVERY
allowed sparse vector and EVERY nonzero scalar, so adaptively choosing
them does not evade this particular obstruction.

This rules out a large original-coefficient sparse-output search class,
including unlimited computation within it, on all but a small fraction
of the stated label distribution. It does NOT rule out efficient dense
relation generation, ordinary/module lattice reduction, sparse coordinates
in a different basis, or every bounded-polynomial syndrome.

FURTHER FOLLOW-UP: NATIVE_RLWE_NONUNIT_WITNESS_AUDIT separately covers
ALL adaptive nonunit syndrome polynomials under the high-degree source
and THIS deterministic norm/box decoder. It does not reuse the invalid
unit-density lemma. Dense unit-syndrome and other-decoder routes remain open.

Do not substitute this negative result for actual-source classical primal
or lattice attacks. It only prevents promoting easy modular inverses,
sparse monomials, or scalar-rescaled native representatives to a finder.

## 2. Distribution And Exact Finite Bound

Let R_q=F_q[X]/(X^d+1), q an odd prime. Let a_1 be uniform among units
and a_2 be uniform in the whole ring, independently. Retain ORIGINAL
coefficient matrices

    F=[F_0,F_1], F_l=C_(a_l)^T.

The adjoint is a ring automorphism, so F_0 is also uniform among unit
multiplication matrices. Write

    v=F_0^(-1)*e_0, T=F_0^(-1)*F_1.

Then v is a uniform UNIT ring vector and T is a uniform ring multiplication
matrix INDEPENDENT of v. Proof: for each fixed unit F_0, multiplication
of the independent uniform a_2 by F_0^(-1) is a bijection of R_q. This
does not treat the dependent coefficients of T as iid matrix entries.

Define the exact cardinalities

    N_d(R)=#{x in Z^d: ||x||<=R},
    S_(d,k)(R)=#{y in Z^d: ||y||<=R, support(y)<=k},
    p_U=#R_q^*/q^d.

For every FIXED integer y and nonzero scalar t, a relation

    F_0*x+F_1*y=t*e_0 mod q

requires x=t*v-T*y mod q. Since t is a unit scalar, t*v is uniform on
R_q^*, with maximum point probability 1/(p_U*q^d). Subtracting independent
T*y is convolution of probability laws and cannot increase the maximum
point probability. This remains valid when y is a zero divisor: no full-
rank multiplication assumption about y is needed.

An integer ball has at most N_d(R) distinct residues. Union over ALL
allowed y and ALL q-1 nonzero t gives

    Pr[exists (x,y): ||(x,y)||<=R, support(y)<=k,
                    F*(x,y)=t*e_0, t!=0]
      <=beta=(q-1)*S_(d,k)(R)*N_d(R)/(p_U*q^d).           (1)

Cap the bound at one. Ignoring the joint-radius constraint when separately
counting x and y makes this only looser, never invalid. Integer lifts can
also collide modulo q; counting all lifts is another safe overcount.
Every valid spacing certificate from the rotational reduction has t!=0,
so (1) bounds its sparse subclass without using secret/error assumptions.

Crucially, an algorithm may choose y,t AFTER seeing F and even b. The
union is over the entire finite admissible set, not just its nonadaptive
queries. That adaptivity is already covered. A label-dependent change of
basis or a label-dependent syndrome polynomial is NOT covered by this
same finite set and requires a different argument.

## 3. Sparse Either Block, And Fixed Unit Polynomial Syndromes

For h a FIXED unit of R_q independent of the sampled labels, replace
e_0 by h. F_0^(-1)*h is still uniform on units and independent of T,
so (1) holds without change for F*c=t*h. The h=2+X syndrome in the
rotational note is a unit at ALL THREE saved d^12 references, checked
exactly by 2^d+1!=0 mod q. Being a unit modulo q is needed for THIS
density argument, not for the earlier deterministic rational decoder.

For a fixed public catalogue H of unit polynomials, a union bound adds
|H|. Adaptively selecting among its entries is fine. It is NOT fine to
claim that a polynomial number of adaptive outputs restricts the total
number of possible h across all inputs to a polynomial-size catalogue.

Conditional on BOTH labels being units, the swapped-block argument also
holds. Now the ratio T is uniform on units rather than the whole ring,
but remains independent of v. The maximum-density convolution proof is
unchanged. Starting with only a_1 conditioned to be a unit, charge the
a_2 nonunit event explicitly:

    Pr[exists admissible relation with min(support(x),support(y))<=k]
      <=(1-p_U)+2*beta.                                   (2)

For a catalogue add |H| to the 2*beta term. Unit selection in the original
normal-form/source reduction remains separately charged. The reference
degree-d/2 two-factor family has

    p_U=(1-q^(-d/2))^2, p_U*q^d=(q^(d/2)-1)^2.

Do not reuse this formula for a split-modulus or different CRT family.

## 4. Entirely Integer Reference Certificates

For integer R, simple coordinate cubes give

    N_d(R)<=(2*R+1)^d,
    S_(d,k)(R)<=sum_(i=0)^k binom(d,i)*(2*R)^i.            (3)

The nonzero coordinate has at most 2R possible values. Combining (1)-(3)
at the saved two-factor references requires NO floating transcendental
arithmetic. The standalone probe checks exactly

    10^8*(q-1)*(2*R+1)^d*
        sum_(i=0)^k binom(d,i)*(2*R)^i
      <=(q^(d/2)-1)^2.                                    (4)

The largest k passing that conservative integer test are:

| d | R | k | one-block existence upper bound |
| ---: | ---: | ---: | ---: |
| 64 | 1099511627776 | 44 | <=1e-8 |
| 256 | 9007199254740992 | 193 | <=1e-8 |
| 1024 | 73786976294838206464 | 796 | <=1e-8 |

Thus with probability at least 1-(1-p_U)-2e-8 under the stated input
law, EVERY radius-R scalar-syndrome witness has MORE THAN k nonzero
coefficients in EACH original block. This does not say every longer vector
is dense. For the TWO-entry fixed catalogue {1,2+X}, charge 4e-8 instead
of 2e-8 and the same positive nonunit event.

These are exact counting/arithmetic certificates CONDITIONAL on the local
derivation and the reviewed source distribution. They are not independent
proof verification, attack costs or cryptographic security estimates.
The prime/CRT prerequisites come from the existing saved arithmetic chains.

## 5. Sharper Volume References And Asymptotic Meaning

Disjoint unit cubes centered on integer points yield

    B_i(R)=pi^(i/2)/Gamma(i/2+1)*(R+sqrt(i)/2)^i, B_0=1,
    N_d(R)<=B_d(R),
    S_(d,k)(R)<=sum_(i=0)^k binom(d,i)*B_i(R).             (5)

Using these in (1) gives sharper NUMERICAL, NOT INTERVAL-CERTIFIED values:

| d | k | log10 beta at k | log10 beta at k+1 |
| ---: | ---: | ---: | ---: |
| 64 | 50 | -11.368621 | -0.345687 |
| 256 | 220 | -6.290781 | 8.102122 |
| 1024 | 913 | -21.516009 | -3.645154 |

The abrupt one-support change comes from the huge number of coefficient
values available, not a measured runtime transition. The probe uses 90
digits, but high precision alone is NOT an outward-rounded numerical
certificate. Only the more conservative integer table above is currently
claimed as an exact finite arithmetic check.

For q=Theta(d^a), fixed a>0, R=C*sqrt(d*q), fixed C, and p_U bounded
below, Stirling and (5) give for k<=alpha*d with fixed alpha<1

    log(beta)<=-(1-alpha)*d*log(q)/2+O(d+log(q)).           (6)

Hence the sparse-class existence fraction decays as exp(-Omega(d*log d)).
The O(d) includes the support-position entropy and radius constants;
dropping them at finite d would give falsely strong thresholds. A valid
finder near this radius must generate nearly dense ORIGINAL coefficient
blocks asymptotically, or use an output class outside the theorem.

This is compatible with many short witnesses existing globally. Their
coordinates need not be sparse. It also leaves classical LLL/BKZ alive:
a sparse combination of reduced-basis columns is usually a DENSE vector
in the original coefficient basis.

## 6. Deliberate Counterexamples And Scope Limits

- NONUNIT h invalidates the uniform-unit density step. At d=2,q=5,
  h=2+X, the 16 uniform units multiplied by h occupy only four residues.
  Point mass 1/4 exceeds the incorrectly reused 1/16 bound. This h is
  invertible over Q and is allowed by the rotational decoder. Its sparse
  subclass needs CRT-support analysis, not this blanket unit theorem.
- BIASED a_1 invalidates the native-label premise. If a_1=1, the sparse
  vector (e_0,0) is a length-one nonzero-label witness on EVERY a_2 input.
  The q=11,R=1,k=0 uniform-label bound is 5/12, so applying it to that
  point-mass label would be false. Tiny planted inputs are not typicality.
- A label-dependent h can absorb a long random public polynomial. Unless
  its bounded-prior/spacing and possible-output entropy are separately
  charged, that is not a useful escape or a covered unit catalogue.
- Different bases, dense vectors, larger radii and non-scalar syndrome
  subspaces are outside the sparse output class. This is not a barrier
  for all quantum algorithms, all low-depth circuits or all ideal methods.
- The bound does not establish hardness of FINDING an existent dense
  witness. It cannot support a Shor-level speedup claim by itself.

## 7. Checks And Handoff

Run the reproducible exact/numerical probe:

    python research/certificates/native_rlwe_sparse_witness_probe.py

- 104,064 exact d=2 native label-pair event checks across q=3,5,7,11,
  R=1,2 and k=0,1,2. All 24 event bounds passed; 22 are correctly marked
  vacuous. The two nonvacuous cases have actual probabilities 1/4 and
  1/6 versus upper bounds 5/8 and 5/12.
- All 32 exact fixed-(y,t) maximum-density checks passed, including a
  zero-divisor y at q=5. No iid ring-matrix model was used.
- Kept the nonunit-h counterexample and 121 biased-first-label inputs
  with always-present sparse witnesses. They explicitly defeat overbroad
  versions of the claim, rather than being dropped from reports.
- Exact integer inequalities (4) passed at k=44,193,796. Separate
  numerical volume references and exact h=2+X unit checks were computed.

Gemini: integrate only the scoped sparse-class exclusion and integer
certificate checker, preserving natural-label/unit/metric/support/radius
contracts and vacuous/counterexample controls. Do not mark full witness
generation impossible or resolved. Keep changed-basis and nonunit-h
backends distinct. Routine full suites/CLI/registry work is not done here.

Main-model next task: dense structural relation generation, nonunit-h
CRT-support analysis if it has a real costed construction, or a strong
original-data classical falsifier. Stop searching only single-block
inverses and fixed-support polynomials at this radius on these labels.
