# Monomial descent: bounded source and prior-art audit

7 November 2026. Source-scope review only; no implementation, network, or
novelty conclusion. Read STATE/TRAPS and CYCLIC_SUPPORT_MONOMIAL_DESCENT.md.
The latter's proposed real-log coordinate subsystem can be replaced by the
published exact multiplicative-relation interface below.

## Exact classical interface: Lenstra--Silverberg

Primary: `research/audits/sources/monomial_descent/lenstra_silverberg.txt`
(arXiv:1509.08843v2; matching PDF and source metadata in the same directory).
Lines33--38 specify a Q-algebra by rational multiplication structure constants,
elements by rational coordinate vectors, and homomorphisms by matrices.
Neither the degree nor the number of supplied elements is fixed.

Theorem1.11(i), lines230--235 (printed p5), states a DETERMINISTIC
POLYNOMIAL-TIME algorithm: given E and a finite system S of elements, test
S subset E*, then return generators for the FULL kernel
`Z^S -> E*, (m_s) -> product_s s^m_s`.
For a FIELD, Proposition8.2, lines810--817 (p15), explicitly returns a
Z-BASIS of that kernel. Its proof imports Ge's field algorithm; this review
checked this published statement, not the underlying scanned Ge proof.
The theorem has no GRH, integer-factoring oracle, supplied roots of unity,
integrality/S-unit promise, or independent-generator promise. In a field,
E* means nonzero elements. Polynomial time covers the whole explicit
structure-constant/coordinate input, including growing degree and tuple.

Algorithm8.3, lines819--852, and its correctness/time proof877--886 give the
general-algebra reduction. Algorithm8.4, lines854--873 (p15), computes
relations on the labelled tuple `(t,S)`, projects to the t-coordinate, tests
whether its generated ideal is Z, and uses Bezout coefficients to produce
exponents for t. Theorem1.11(ii) and proof887--892 establish exact subgroup
membership with exponent output. This is actual text, not merely a citation
to Algorithm8.4 from another paper.

Applicable reduction: flatten EVERY compact generator into its polynomial
list of expanded small field atoms, with binary exponents. Include the
expanded input cocycle coordinates, necessary automorphism images of atoms,
and complete source torsion generators. Apply Proposition8.2 once to this
labelled tuple B. It returns exactly
`Lambda = {v in Z^B : product_beta beta^v_beta = 1}`.
This is an integral relation lattice, NOT its saturation: torsion such as
`(-1)^2=1` is preserved. Integer HNF/SNF can turn any returned generators
into a basis if the general theorem rather than Proposition8.2 is used.

Express candidate x_i as integer powers of a COMPLETE compact S-unit
generating list. Every monomial descent equation becomes an atom-exponent
vector linear in these unknown exponents, required to belong to Lambda.
Introduce relation-basis coefficients and solve one integer linear system.
The same Lambda tests exact positive-witness equality without expansion.
Automorphisms act on each expanded atom by the supplied rational matrices;
polynomially many images still have polynomial coordinate bit size. Binary
compact exponents and binary A_g entries remain binary integer coefficients.
Do NOT submit an exponentially expanded compact generator to Theorem1.11.
No free S-unit coordinates, real-log inversion, or torsion discrete log is
needed in this reduction. Completeness of the source unit list, including
roots of unity, remains essential for NO; relations alone do not provide it.

## Biasse--Song complete-unit and compact interfaces

Primary PDF: `research/literature_cache/arxiv_2510_02280v2.pdf`.
Text locators below refer to `/tmp/qsearch-sunit-v2.txt`; durable selected
passages are in `research/audits/claude_inputs/2026-11-07-tensor-square-norm/bs_excerpt.md`.
Theorem1 lines103--106 states S-unit GROUP computation in compact form,
polynomial in degree, log discriminant, |S|, and max log prime-ideal norm.
It is not a theorem about merely independent units of unknown index.
Theorem5 lines1576--1594 has an adjustable failure parameter mu with
log(1/mu) cost; item3 is generation of the ENTIRE dual lattice, not validity
of individual vectors. Proposition2/Algorithm3 lines880--949 extract a
basis of the generated lattice at sufficient precision. Lines1525--1535
separate the free S-log lattice from its roots-of-unity kernel. Thus charge
the complete-generation event and separately include mu(E); an incomplete
list is inadequate for a negative answer. Complete generators suffice for
the atom-relation solve, so free-basis coordinate output is unnecessary.
Definition8 lines1654--1669 permits constant compact base (choose2), exact
polynomial-size atoms and polynomial length; lines1671--1683 restore the
rational correction for negative valuations. Proposition7 lines1769--1781
provides exact compact recovery in polynomial time. One field-E S-unit
computation suffices; growing torus rank adds polynomial integer bookkeeping,
not an extra hidden field extension. BS supplies number-field units, not
the new arbitrary-G-lattice support lemma.

## Prior-art scope

`research/audits/sources/monomial_descent/torsors_brauer.txt` is Duncan--Singh,
arXiv2505.10386v2. Theorems1.3/1.4 lines68--101 and Theorem6.1 lines702--727
give Brauer descriptions under RETRACT RATIONALITY of T. Lines875--880
explicitly warn that arbitrary Mackey resolutions do not connect to H^1(k,T)
without that hypothesis. This is substantial constructive cohomological
prior art, but those statements do not supply an arbitrary integer G-lattice
field-input polynomial-BIT cocycle witness algorithm or compact output.

Actual Kutas--Montessinos v3 primary:
`research/literature_cache/kutas_montessinos_2024_amitsur_v3.pdf`, extracted
`/tmp/qsearch-kutas-montessinos-v3.txt`. Theorem4.11 lines1070--1097 already
proves S-unit support for Amitsur 2-COBOUNDARIES. Algorithm2 lines1100--1132
uses full S-unit coordinate isomorphisms and an integer linear solve;
Theorem4.12 lines1135--1163 is a GRH quantum-polynomial trivialization
algorithm, factoring F, F tensor2, F tensor3. Line1155 expressly pays the
coordinate maps using Lenstra--Silverberg Algorithm8.4. Theorem4.13
lines1164--1173 applies this to promised split central simple algebras.
Hence S-unit cochain trivialization and its quantum arithmetic composition
are established prior art, not new here. The stated inputs are Amitsur
2-coboundaries/split CSA, not every arbitrary G-lattice monomial action;
an equivalence to the entire new endpoint has not been established.

Verdict: the coordinate/equality resource gate is paid by the existing LS
theorem on small atoms; completeness is paid by the complete BS event plus
torsion. The arbitrary-G-lattice cyclic-support proof remains a separate
new proof obligation. No novelty or quantum/classical separation follows
from these scoped checks. Magma S-unit cohomology is acknowledged prior art;
failed-download Preu and unread Ge scans are not treated as read sources.
