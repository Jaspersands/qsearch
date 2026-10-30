# What Would Actually Be New?

2026-10-26. This is a selected primary-source comparison, not a novelty
certificate. The mathematical proposal remains unreviewed.

## Existing Result And Its Input

Chen--Petit, *Computing the endomorphism ring of a supersingular elliptic
curve from a full rank suborder*, EUROCRYPT 2025, already gives a heuristic
quantum-polynomial algorithm for this endpoint. The retained accepted
manuscript was read at PDF pages 4, 8-9, 12 and 17-18. Theorem 1 assumes
efficiently represented rank-four basis maps and labels the result heuristic.
Remark 2 charges basis heights. Its route uses a reference order and weak
isogeny. Lemmas 8/10 use GRH for the general small reference parameter;
Remark 17 discusses the quaternion dictionary and quantum factorization.
Proposition 26 and Remark 27 identify norm-solving/strong-approximation
heuristics. These are distinct dependencies, not one interchangeable
"heuristic" switch.

The author's [official slides](https://iacr.org/submit/files/slides/2025/eurocrypt/eurocrypt2025/563/563_slides.pdf),
PDF pages 15-20 and 27-29, independently distinguish lattice-membership
search, their heuristic main theorem, and the reference/weak-isogeny route.
The [publication record](https://research.birmingham.ac.uk/en/publications/computing-the-endomorphism-ring-of-a-supersingular-elliptic-curve/)
alone is not sufficient for inspecting those assumptions.

## Proposed Difference, Not Yet An Established Improvement

The new proposal stays in the supplied native alpha coordinates. Its query
group is the ADDITIVE R/dR, not a quaternion-unit or nonabelian matrix group.
It builds a framed principal polarization for each rational gamma, seeking
equality exactly modulo End(E). If the full source proof holds, ordinary
abelian Fourier sampling recovers d*End(E)/dR. This does not require a
reference curve, full source maximal order, global quaternion dictionary,
powersmooth quaternion lift, connecting hidden isogeny or nonabelian HSP.

That is a possible change in mechanism and assumptions, not a first
quantum-polynomial solution. The same native rank-four input remains a
substantial restriction. A direct theorem with a prohibitively large fixed
dimension may still be mathematically useful, but no cryptographic runtime
claim follows. A complete comparison against subsequent literature and
compositions of known reductions has not been performed.

## Imported Algorithms Still Have To Be Charged

The [2026 represented-PPAV framework](https://eprint.iacr.org/2026/1142)
supplies operations on already represented polarized varieties. The new
argument must construct such models through its explicit smooth quotient
sequence; representability alone is not conversion. It also must preserve
fixed field embeddings, exact point signs and a common automorphism across
all marked relations.

[Isogeny division](https://arxiv.org/html/2309.11912v4#S4) is an existing
dependency for certifying recovered output maps, not an invention here.
Its availability as an integrality test does not by itself construct
separating coset labels. The existing local membership-interface barrier
already addresses that distinction.

The initial four-square witness and subsequent converter norm witnesses
must use an unconditional expected-polynomial algorithm, such as the
variants in [Pollack--Trevino](https://math.colgate.edu/~integers/sjs15/sjs15.pdf).
The local SymPy arithmetic fixtures do not implement that asymptotic claim.
Source uniformity, reversible compilation and output-map recovery remain
unexecuted. A green receipt is not evidence that these imports compose
correctly, that no classical counterpart exists, or that the construction
is novel.
