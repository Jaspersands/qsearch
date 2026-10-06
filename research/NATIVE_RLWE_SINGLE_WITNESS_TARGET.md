# Native Ring-LWE: One Checkable Neutral Witness Per Coordinate

Date: 2026-10-04. LOCAL DERIVATION / REVIEW PENDING.

No new quantum algorithm, efficient witness generator, novelty, independent
verification or security estimate. This is a DISTINCT native q-near-d^12
source target. It is not a parameter update to the existing d^4 Gaussian
or d^6 norm-only families. Gemini owns routine implementation and baselines.

FOLLOW-UP: NATIVE_RLWE_ROTATIONAL_WITNESS_REDUCTION proves that ONE
coordinate-neutral witness supplies ALL coordinates by signed ring
rotation. It also permits short polynomial syndromes and gives an optimal
predetermined-label alternative. Read it before implementing d independent
finder calls. None of these reductions provides an efficient finder.

FINITE FALSIFIER: `NATIVE_RLWE_CLASSICAL_COVER_CERTIFICATE.md` saves an
exact classical all-coset cover for one native d64 kernel in both lanes.
The classical competitor need not match an internal R=sigma*sqrt(d) if
its longer witness still meets the ORIGINAL decoder spacing/noise gate.
`NATIVE_RLWE_BALANCED_NTRU_TARGET.md` makes single-relation classical
completion, ideal primitivity and finite-index alternatives explicit.
This is not an asymptotic source attack or an available quantum generator.

## 1. The Missing Output Can Be Finite And Directly Checkable

Earlier sufficient targets asked for a coherent inverse, chosen Gaussian
cosets, or centered homogeneous Gaussian samples. For the ACTUAL small
normal-form secret, a larger modulus permits a simpler finite output:

    For each j, find ONE integer c_j such that
    all other coordinates of F*c_j vanish, ||c_j||<=R,
    and its remaining label separates the permitted secret coordinates.

No sampling distribution, independent-call promise, Gaussian amplitudes,
phase consistency, covariance estimate or coherent erasure is required.
The output can be verified from public data by exact integer arithmetic.
Generation may be quantum or classical; a classical generator gives a
classical decoder. The hard part is GENERATION, not reading the certificate.
This is a version of neutral short-relation/dual-hybrid decoding, not a
claim to have invented a new cryptanalytic paradigm.

## 2. Exact Certificate And Decoder

Retain original native F=[C_(a_1)^T,C_(a_2)^T], actual b=F^T*s+e mod q,
and original secret coordinates. Let the prior contract give

    Pr[s not in [-R_s,R_s]^d mod q]<=delta_s, 2*R_s<q,
    Pr[||e||>E_max]<=delta_e.

The TWO original error records are concatenated in e. An integer error
lift is used in the proof, not provided to the algorithm. Choose integer
R and B=E_max*R. The certificate for coordinate j is

    ||c_j||^2<=R^2,
    F*c_j=t_j*e_j mod q,
    min_(1<=Delta<=2*R_s) ||Delta*t_j||_q>2*B,              (1)

where ||z||_q is centered torus distance. Every check is exact. Prime q
is not needed for this deterministic decoding lemma; primality matters
for the source, CRT and witness-existence arguments below.

Compute w_j=b dot c_j mod q. Test the allowed coordinate values r and
return the unique r with

    ||w_j-r*t_j||_q<=B.                                   (2)

On the good-noise/prior event the true coordinate passes because
|e dot c_j|<=E_max*R=B. Two passing r,r' would imply
||(r-r')*t_j||_q<=2*B, contradicting (1). Thus the proof is deterministic
given the finite witnesses. It works with correlated/adaptive generation,
including reused witnesses; there is no artificial IID theorem obligation.

One global noise event and one global prior event cover all coordinates.
No extra factor d multiplies delta_e or delta_s. Failure to find a witness,
generation cost and original rounding/unit/anchor/verification losses remain
separate. After decoding, check an independent original held-out record.
Selecting only successful instances does not erase unconditional failures.

Do not normalize a_1 and keep the old secret box. Internal lattice solvers
may change coefficient bases, but (1)-(2) must be checked in ORIGINAL F,b
coordinates, or with a separately proved pushed-forward prior.

## 3. Exact Arithmetic References, Not Floating Security Parameters

Use sigma=2*d^6, R=sigma*sqrt(d). Construct a PRIME q>d^12 with q=3 mod 8
as q=2*k*r+1, where r is a certified prime near 2*d^6. This gives residue
degree d/2 and keeps the natural product coefficient metric. A separate
source-theorem applicability review is still required; original absolute
noise widths q*xi/q*alpha and prior laws are retained, not replaced by means.

See `research/certificates/native_rlwe_single_witness_d12_arithmetic.json`.
All large integers are decimal STRINGS to prevent JSON consumer rounding.

| d | q | R | E_max spherical | E_max elliptical |
| ---: | ---: | ---: | ---: | ---: |
| 64 | 4722366484553272393819 | 1099511627776 | 4351 | 4545 |
| 256 | 79228162514320210376421021211 | 9007199254740992 | 32788 | 32228 |
| 1024 | 1329227995784916208980425653176240211 | 73786976294838206464 | 231818 | 201205 |

The existing sharp prior-tail references use R_s=183,727,2699 in the
spherical lane and 197,734,2399 in the hidden-elliptical lane at
delta_s=.001; retain that existing proof obligation rather than infer
a prior cutoff from an observed histogram.

Noise bounds here use CONSERVATIVE RATIONAL energy certificates, avoiding
rounding a floating square root into a purported exact bound. Let

    L=log2(d)*(693148/1000000)>log d, pi>3,
    E_s<=d*(d*sqrt(d)+1)*L^2/6,
    E_e<=[d^2*L^2*(L^2+1/6)/2+d*L^2]/6.                  (3)

The original source notes give the formulas before these conservative
substitutions. A rational 12-term exponential Taylor sum proves
exp(693148/1000000)>2. Integer energy upper bounds E_U are respectively
94646/103284,5375101/5193019,268697635/202415653. The artifact checks
E_max^2>=200*E_U. Total expected training-error energy is <=2*E_U,
so Markov gives delta_e<=.01. Hidden covariance is not supplied; modular
centering never increases the norm used by this energy argument.

### Prime Certificates Do Not Depend On Probable-Prime Acceptance

The artifact contains 35 recursively verified prime nodes. Leaves below
100 use trial division. A nonleaf p has a factored F dividing p-1,
F^2>p, recursively proved prime factors ell, and integer witness a satisfying

    a^(p-1)=1 mod p,
    gcd(a^((p-1)/ell)-1,p)=1 for every ell dividing F.       (4)

Why it proves primality: for each prime divisor z of p, the order of a
mod z divides p-1 and must contain the required ell powers. Therefore
F divides z-1, implying z>sqrt(p); a composite p cannot have all prime
divisors that large. This is the classical factored-order/Pocklington
criterion, not a new theorem. Top-level F=2*r; their witnesses are a=2.
SymPy primality/factorization was only a CONSTRUCTION aid; a separate
integer-only checker verifies the saved chains without trusting those calls.

## 4. Admissible Witnesses Exist On The Existing Kind Of Flatness Event

Existence does not provide a finding algorithm. For the homogeneous
K_j={c: all other F coordinates vanish}, consider only for analysis the
centered probability law proportional to exp(-2*pi*||c||^2/sigma^2).
If the full syndrome law is eta-relatively flat, the t_j marginal has
density at most (1+eta)/[(1-eta)*q].

For prime q and 2*R_s<q, multiplication by each Delta=1,...,2*R_s is a
bijection. Thus a union bound gives

    Pr[separation in (1) fails]
      <=(1+eta)/(1-eta)*2*R_s*(4*B+1)/q.                 (5)

The discrete interval count is an upper bound; cap it at one if vacuous.
Centered Gaussian tilting gives, WITHOUT a coset assumption,

    Pr[||c||>R]<=2^d*exp(-pi*d).                           (6)

If (5)+(6)<1, at least one certified witness exists for EVERY j on the
same full-flatness event. There is no union factor d for this existence
claim. An implemented random finder would still charge its retries and
its probability of failing across all requested j.

At eta=.01 the separation-bad upper fractions, spherical/elliptical, are
.001513062/.001701439, .0000221175/.0000219491 and
.000000283470/.000000218688. Tail (6) is exponentially smaller.
Each is a probability under an UNSUPPLIED analytical Gaussian, not under
an implemented efficient generator or arbitrary short-vector routine.

The saved artifact checks the CRT B_2<=1e-8 statement by exact integers:
with f=d/2, n=(q^f-1)*10^d, D=(7*sigma)^d,

    (2*n*D+n^2)*10^8<=D^2.                                (7)

The bad-flatness-label fraction is therefore <=1e-6/p_U at eta=.01,
conditional on first-label unit. Charge that conditioning, prior and
normal-form reduction losses. These are distinct d^12-modulus references, not
evidence already produced by q^4 live experiments.

## 5. What Can And Cannot Be Claimed

- A checked witness immediately gives a conditional decoding result, not
  an efficient or quantum method for FINDING it.
- Finite d^12-modulus instances may be classically easy. Run original-data primal
  attacks, module/ordinary LLL/BKZ and neutral-relation generation before
  interpreting quantum behavior. Large modulus improves error tolerance;
  it is not itself a quantum advantage.
- A supplied short basis or trapdoor can make witness generation classical.
  Count obtaining it. Native Gaussian correction, frozen Gibbs parents
  and generic short-point Grover search do not supply a polynomial generator.
- Zero is short and valid but fails separation. A nonzero label also needs
  the full small-prior separation check; no uniform-label assumption is free.
- The guarantee fails outside the noise/prior contract. Held-out checks
  mitigate false reports but do not make an unsupported contract true.
- Enumerating the candidate secret COORDINATES is polynomial here; enumerating
  all coefficient vectors or q^d secrets is not. Do not hide the latter
  inside the finder. Generation must scale beyond exhaustive controls.

## 6. Checks Actually Run

- Seed 290950: 24 original native d=2 inputs at q=101,211,503. A 6,561-
  point exponential reference box supplied 48 checked coordinate witnesses.
  Exact syndrome, length, separation and unique-decoding checks passed.
  All 48 zero-label controls failed eligibility. Forty-eight out-of-noise-
  promise controls confidently decoded a DIFFERENT secret, preserving the
  requirement to charge the error contract. No scalable finder was tested.
- Constructed the three prime/energy/CRT reference rows, then verified
  the SAVED JSON with an integer-only recursive checker: 35 prime nodes,
  exact residue orders, energy/radius/separation arithmetic and (7).
- Four corrupted-certificate controls were rejected: witness 1, incorrect
  known factor, missing child certificate and composite trial-division leaf.

No production workflow, full suite, live registry candidate, commit or
proof promotion. Independent proof/source/prior review remains necessary.

## 7. Next Main-Model Task And Gemini Contract

This finite witness target should be a PRIMARY alternative to full DGS,
not an automatic claim that sampling was solved. Main-model work: construct
a high-upside quantum neutral-relation generator, or falsify a proposed
generator against classical lattice methods. Output needs useful label
spacing, not merely shortness or a circuit escaping an older simulator.
The rotational follow-up reduces the actual ring target to one witness,
not d separate searches, and specifies broader output certificates.

Gemini: implement the exact certificate checker and decoder, separate d^12-modulus
source ID, rational energy and recursive prime verification, with ORIGINAL
F/prior coordinates. Add a deliberately exponential reference backend and
strong classical LLL/BKZ/dual baselines with measured costs. Store witness
generation method, dimension, modulus, coefficient bits, norm, spacing,
failure/retry/preprocessing costs and held-out residuals. Keep the efficient-
generation obligation OPEN, even when every arithmetic check passes.

Compare d^4 distribution sampling, d^6 chosen short preimages and d^12-modulus
finite neutral witnesses as DIFFERENT sufficient routes. Neither expanding
modulus nor weakening the required interface justifies discarding the
classical baseline or promoting finite experiments to asymptotic speedups.
