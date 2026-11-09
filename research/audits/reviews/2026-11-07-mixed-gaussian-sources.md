# Mixed Gaussian pair: closed source/interface review

2026-11-07. Read-only primary-source audit followed by this requested record.
Interpreter: `/opt/anaconda3/bin/python`. No network/API/Git or new tests.
Main contract: `research/MIXED_GAUSSIAN_PAIR_LEARNING.md`; this review accepts
the source interfaces below, not the full growing-n reconstruction theorem.
Primary snapshots/hashes: `audits/sources/mixed_gaussian_pair/source.json`.
All line locators below refer to the retained extracted texts.

## Global trace bound: accepted, Gaussian endpoints only

`audits/sources/mixed_gaussian_pair/trace_bounds.txt` lines180–205,
Theorem1 Eq9, states for two possibly mixed free-fermionic states
`||rho-sigma||_1 <= (1/2)||Gamma(rho)-Gamma(sigma)||_1`.
These are raw Schatten trace norms; operational trace distance is half the
state norm. There is NO input covariance gap, full-rank, minimum occupation,
or purity promise. It does NOT apply directly to a nonGaussian mixture by
replacing that mixture with its mean covariance.

The proof is in lines1832–1994; derivative Lemma17 is1296–1301.
The mixed extension1950–1958 uses a convex decomposition into pure Gaussian
states and the derivative's linearity in the density operator. The physical
affine covariance path is1960–1994. Boundary states cause no hidden inverse:
Wick coefficients are polynomial in the covariance (derivation1303–1370).
Independent check of the displayed derivative: for antisymmetric
`X=sum_j lambda_j(u_j v_j^T-v_j u_j^T)`, a rank-two term is
`-i lambda_j/4 (gamma_u gamma_v rho + gamma_u rho gamma_v
 - gamma_v rho gamma_u + rho gamma_u gamma_v)`.
Each of the four terms has trace norm1, since unit-vector Majoranas are
unitary. Thus the derivative norm is at most
`sum_j |lambda_j| = ||X||_1/2`; integration proves the stated global bound.

## Channel/CJ conventions: accepted with the explicit corrections

`gaussian_channels.txt` lines90–128 gives an n-to-m Gaussian channel
`M -> A M A^T+B`, its Gaussian fermionic CJ covariance
`[[B,A],[-A^T,0]]`, and CP iff `I-AA^T-iB >= 0` (Eq4).
The conjugate `+iB` condition is equivalent for real A,B. This is a complete
channel, not merely a covariance prescription on Gaussian inputs:
`bravyi_maps.txt`586–589 explicitly permits nonGaussian input operators;
634–642 defines/proves parity preservation;666–704 gives CP and TP.

The signs must be translated. Bravyi's Majoranas are defined at91 as
`c_(2j-1)=a_j^dagger+a_j`, `c_(2j)=-i(a_j^dagger-a_j)`; in the fixed
occupation/Jordan–Wigner ordering they are `Zprefix X, -Zprefix Y`.
Bravyi's covariance uses `+i Tr(rho c_a c_b)` (245–247); the learner uses
`Gamma_ab=-i Tr(rho c_a c_b)`, matching the minus sign in
`trace_bounds.txt`135–138. Consequently a desired learner channel
`Gamma -> L Gamma L^T+Z` has source parameters `A=L,B=-Z`, source CJ
`[[-Z,L],[-L^T,0]]`, and learner CJ `[[Z,-L],[L^T,0]]`.

`bravyi_maps.txt`703–742 fixes the fermionic tensor isomorphism J;752–770
defines `rho_I=2^(-2r) product_a(I+i c_a c_(2r+a))` and the dual channel
state. This Gaussian maximally entangled state is NOT the ordinary qubit
Bell state. In output-then-reference occupation ordering J is conjugation
by `W=(-1)^(N_output N_reference)`, implemented by all output/reference
CZ gates. For r<=2 this costs O(n). Writing
`|Omega_r>=2^(-r/2) sum_x |x,x>`, one has
`J(rho_I)=(I tensor V_r)|Omega_r><Omega_r|(I tensor V_r^dagger)`, with
`V_1=X S`, `V_2=(X tensor X)(S^dagger tensor S) CZ`, `S=diag(1,i)`.
For example V2 sends `00->11, 01->i10, 10->-i01, 11->-00`.
Therefore apply W, then V_r^dagger on the reference, before ordinary Bell
postselection. Reference phases alone are insufficient. The main note now
uses this complete correction; it does not need the optional observation
that W cancels in the contraction for an even core.

The ordinary CJ identity then gives unnormalized output `E(sigma)/4^r`
for ANY input sigma, including an arbitrary even nonGaussian core, and
success exactly `4^(-r)>=1/16`. Ordinary qubit gates are explicitly allowed.
If physical parity-preserving gates alone were required, XS is an odd
correction and would need an ancillary parity partner; that stronger gate
model is not claimed. Here “even mixed” means commuting with parity, not
support exclusively in the even parity sector.

## Preparation/error costs and remaining scope

If the prepared physical Gaussian CJ has raw trace error e, the Bell CP
contraction has unnormalized error<=e and success>=`4^(-r)-e`.
Its normalized output raw trace error is <=`2*4^r*e`; this is constant
loss for r<=2. Exact TP reference marginal need not survive covariance
clipping, provided this success/error accounting is retained. Capped
retries consume freshly PREPARED resources and a fallback makes the
returned approximate preparation trace preserving; no source-copy
inverse or free success conditioning follows from the source.

Gaussian normal form/product preparation is `bravyi_maps.txt`263–289;
`trace_bounds.txt`775–790 states an O(q^2)-gate implementation for the
orthogonal Gaussian unitary. This is not itself a complete finite universal
gate BIT theorem. Charge approximation of all O(q^2) rotations and thermal
probabilities so their summed trace error is <=e, plus classical backward
error in the physical covariance decomposition. No eigenvector-gap promise
is supplied by the source or needed for an approximation in state norm.
The main note now explicitly charges these errors. Its reported exact
three-output/two-input CJ control is a finite convention check, not evidence
for an all-input theorem or the learner's quantitative inversion bounds.

## Alternative pure stabilizer-rank-two selection is already covered

`audits/sources/stabilizer_rank_priority/low_rank.txt`25–33 allows arbitrary
complex coefficients and nonorthogonal unknown stabilizer components;
Theorem1.1 at45–51 is copy-only and polynomial time/copies for rank2,
without component/frame advice. Independently, `extent.txt`223–227,
Corollary1.6, returns a classical pure-state description within trace
distance epsilon from copies of ANY normalized pure state of stabilizer
rank<=k, with the stated success guarantee and polynomial resources for
fixed k=2. This closes that alternative selection, not the distinct mixed
Gaussian-pair learning problem. No novelty, speedup, or full learner
acceptance follows from this source audit.
