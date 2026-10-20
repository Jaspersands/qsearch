# Draft: a classical sampler for the uniform-sign polar Gibbs source

Status: DRAFT, not sent. Recipients: [authors of the polar-code quantum message-passing
papers, of the DQI Gibbs-sampling paper the project cites, and of arXiv:2610.03566
(Piveteau, Quek, Franco Garrido); confirm before sending].

---

Subject: Classical successive-cancellation sampling for the uniform-sign polar Gibbs task

Dear [names],

We run a small project that proposes quantum mechanisms and then looks for the matching
classical method. One proposal combined a polar receiver with quantum messages and the
DQI reduction from decoding to Gibbs sampling. The goal was to sample the signed
parity-Ising Gibbs law on the kernel of a polar parity-check matrix faster than
classical methods. For the uniform-sign average we found a classical route that matches
it, with a certified finite design. We would value your view on whether this is already
known, and whether the adversarial-sign case is the one that matters.

**Setting.** E has N independent Bernoulli(p) bits with p = (1 − c)/2. U = G(E) is the
polar transform. A public frozen set F defines checks H_F with U_F = H_F E. For clause
signs J, let s = H_F J and draw E conditioned on U_F = s. Then y = E ⊕ J follows the
signed Gibbs law ∏_j (1 + c(−1)^{y_j + J_j}) on ker H_F. Uniform signs give a uniform
syndrome s.

**What we found.**

- **Hybrid bound.** Successive-cancellation source shaping forces frozen coordinates and
  samples the rest from the exact unrestricted conditionals. Averaged over uniform signs,
  its total-variation error is at most Σ_{i∈F} m_i, where m_i = E|P(U_i=0|U_{<i}) −
  P(U_i=1|U_{<i})|. Korada and Urbanke (2010) put the joint law with uniform frozen
  values within total variation ½ Σ_{i∈F} m_i of the source law; passing to the
  conditional law given the syndrome at most doubles this on average. Each m_i is the
  root fidelity of the reversed synthesized classical-quantum bit channel. We claim no
  new duality theorem here: this is an instance of known channel/code duality (Renes;
  the BSC/PSC treatment of Rengaswamy and Pfister). Our local derivation of the identity
  for this setting is checked numerically only at the smallest lengths and is marked
  review pending. If it holds, a polar Gibbs proposal justified by a vanishing sum of
  these fidelities also gives this classical average-sign sampler.
- **A certified design without a source table, conditional on review-pending steps.**
  Upper bounds on every m_i come from exact integer channel combination on a nonuniform
  overlap mesh with 96-bit dyadic herald masses, with every rounding chosen to degrade.
  That the computed means are upper bounds rests on two local derivations in our source
  note, both marked review pending: that the posterior-magnitude recursion is a
  combination of flagged pure-state channels, and that each rounding is a physical
  degradation of such a channel, under which root fidelity cannot decrease. Given those
  and the hybrid bound above (also review pending), at N = 32768, rate 1/2, c = 13/20
  (p = 7/40), the design has E_J TV ≤ 0.010221. The report stores this bound as an exact
  rational. Setting it up took 65,534 channel combinations and about 10^9 support-pair
  visits, and we count that cost; it is not free advice.
- **The average is essential.** On a length-2 calibration with p = 1/10, the
  uniform-syndrome average error is 2/5, but the worst syndrome has error 18/25.

**What we do not claim.** The guarantee is an average over uniform signs, not a
worst-case or adversarial-sign sampler. It covers polar codes only, not random LDPC
codes, so it does not refute random-hypergraph results. It proves no fixed-mesh
asymptotic convergence. It is not a quantum advantage or a no-go, and no Gibbs draw at
the largest length has been run. Our source notes mark the degradation and hybrid
derivations as review pending; none has had independent review.

**Reproducing it.**

```bash
pip install python-flint sympy numpy scipy cvxpy
docs/papers/classical-competitors/reproduce.sh OUT
```

The N = 32768 design takes minutes. The script runs the solver source vendored in the
repository (it puts `packages/qsearch_classical/src` on `PYTHONPATH`) and stops if one of
the five packages is missing; the installable package
(`pip install -e packages/qsearch_classical`) is not what it exercises. Repository: [link].

Two questions, if you have time:

1. Is the identity between the SC source-shaping error terms and the reversed bit-channel
   root fidelities already stated somewhere we should cite? We know the joint-law step
   from Korada and Urbanke.
2. Piveteau, Quek and Franco Garrido (arXiv:2610.03566) dequantize the
   unambiguous-discrimination decoder for uniform signs and report a BPQM threshold
   beyond the classical Shannon limit on dilute spin glasses. Their claim concerns
   classical decoders inside the reduction, not every classical sampler. For the polar
   family, where SC source shaping already matches the uniform average, do you expect a
   quantum receiver to have an edge only for adversarial signs?

Thank you for considering this.

[signature]
