# Tensor-product norm tori: bounded actual-source comparison

2026-11-07. Read STATE and `TENSOR_SQUARE_RATIONAL_NORMS.md`; no Git,
network, API or implementation. Interpreter: `/opt/anaconda3/bin/python`.
This is a bounded applicability/prior-art check, not a full-paper audit or
novelty certificate.

## Florence--Hoshi--Yamasaki, actual local v3

Source: `research/audits/sources/non_galois_norm/florence_hoshi_yamasaki.txt`
and matching PDF, arXiv2605.17427v3, 21 June2026.

The relevant actual results concern rationality of tori and Hasse principles,
not the candidate's finite-prime support theorem:

- Lines147--172 distinguish the torus tensor product T_A tensor T_B from
  the norm-one torus of the algebra tensor product A tensor B. The stated
  constructive proofs manipulate flabby resolutions of finite G-lattices.
- Section7, Theorem7.3, lines3330--3527, gives explicit exact sequences and
  maps involving augmentation ideals and tensor products of G-lattices.
  Its splitting statements require the stated coprimality hypothesis.
- Theorem7.4, lines3540--3557, assumes A=product K_i and B=product E_j,
  gcd(all [K_i:k], all [E_j:k])=1, and stable/retract rationality of BOTH
  input norm-one tori. It concludes corresponding rationality statements
  for T_A tensor T_B and T_(A tensor B). The proof, lines3563--3617,
  constructs character-lattice/torus isomorphisms under these hypotheses.
- For fields A=B=L of degree n>1, the coprimality hypothesis is gcd(n,n)=1
  and FAILS. Thus this theorem cannot be invoked for arbitrary L tensor L.
  Example7.6, lines3674--3715, explicitly warns that dropping the
  coprimality condition is invalid in general.
- Theorem8.1, lines3814--3862, treats tensor products of fields with pairwise
  coprime degrees and stably/retract rational input norm-one tori. Its
  arithmetic conclusion is HNP: the norm hypersurface has a rational point
  iff it has points over every completion. The paper spells out this
  existential statement at lines3834--3860.

No SAME class-support theorem was found in these relevant statements/proofs:
they do not require ordinary class generators of the factors of L tensor L,
principalize outside-S divisors by paired relative norms, or bound support
using disc(O_L tensor O_L)=D_L^(2n). A targeted full-text search found the
discriminant term only in concrete field examples, not such a support bound.
References to algorithms concern group-lattice/GAP rationality computations;
the inspected passages do not give a polynomial-BIT compact norm-solution
algorithm on the candidate's explicit number-field/target-rational input.

There is real conceptual overlap: finite etale tensor products, norm-one
tori, explicit integral lattice maps, and arithmetic norm obstructions.
Do not describe the paper as unrelated or infer novelty from the preceding
bounded negative finding. Its word "constructive" is not itself a complexity
theorem for producing a compact x with N_L/Q(x)=a.

## Hoshi--Kanai--Yamasaki, exact Theorem1.10 scope

Source: `research/audits/sources/non_galois_norm/hoshi_kanai_yamasaki.txt`
and matching PDF, arXiv1910.01469v6, 31 January2022.

Actual lines526--531, Theorem1.10 (credited to Voskresenskii--Kunyavskii):
let k be a NUMBER FIELD, K/k a degree-n extension, and L/k its Galois
closure with Gal(L/k) isomorphic to S_n. For the norm-one torus T of K/k
and a smooth compactification X, H^1(S_n,Pic X_L)=0. Consequently T has
weak approximation and HNP HOLDS for K/k.

This statement is not restricted to the paper's later small-degree tables,
to prime/odd n, to unramified extensions, or to GRH. It is a genuine
all-degree S_n HNP baseline. It supplies neither the candidate's explicit
support cutoff nor a polynomial-height/compact-witness construction.
Do not use a generic S_n family as an HNP-failure example.

## HNP versus the candidate's endpoint

Florence et al. Definition4.4, lines1582--1600, defines HNP through the
idele/local norm quotient. The candidate instead proves that a target
ALREADY in the global norm image has an S-unit preimage for a specified
finite support, then computes that image and a compact witness. Those are
different obligations. HNP alone is not a paid local-test algorithm and
does not supply a global witness or its bit/output bounds.

For clarity, as a direct deduction, the global norm image of L tensor L
equals that of L: every tensor factor contains L, and the multiplication
map supplies a diagonal L factor. Thus self-tensor HNP would be equivalent
to original-field HNP, not an automatic new local-global principle.

VERDICT: these actual sources do not directly subsume the inspected
tensor-square class-support/GRH compact-witness composition. They provide
important rationality/HNP prior art and the all-degree S_n existence
baseline. Priority of the particular support argument remains UNKNOWN;
no classical hardness or separation follows.
