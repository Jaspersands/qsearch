# DCP Two-Copy Bell-Basis / Conjugate-Pair Phase Cancellation Obstruction

## 1. Exact Bell Measurement Law
For $\rho(a_1, s, \gamma_1) \otimes \rho(a_2, s, \gamma_2)$ measured in the Bell basis $\{|\Phi^\pm\rangle, |\Psi^\pm\rangle\}$:
$$P(\Phi^\pm \mid a_1, a_2, s) = \frac{1}{4}\left(1 \pm \gamma_1 \gamma_2 \cos\!\left(\frac{2\pi}{q}\langle a_1 + a_2, s \rangle\right)\right),$$
$$P(\Psi^\pm \mid a_1, a_2, s) = \frac{1}{4}\left(1 \pm \gamma_1 \gamma_2 \cos\!\left(\frac{2\pi}{q}\langle a_1 - a_2, s \rangle\right)\right).$$
All four probabilities are strictly invariant under $s \mapsto -s \pmod q$, and on matched headers $a_1 \equiv a_2 \pmod q$, $P(\Psi^+) = (1+\gamma^2)/4$ provides a secret-independent purity estimator.

## 2. Full Random-Header Transcript Reduction (Local, Review Pending)

The previous suggestion of a chosen combined-header coin did not specify a
legal random-sample implementation. V2 supplies one. Let $G=\mathbb Z_q^n$.
Given one ordinary sample $(h,b)$ with $h$ uniform and
$\mathbb E[(-1)^b\mid h]=\gamma_{src}\cos(2\pi\langle h,s\rangle/q)$:

1. Independently flip $b$ with probability $(1-\gamma_1\gamma_2/\gamma_{src})/2$.
   This requires known fixed coherences and $\gamma_1\gamma_2\le\gamma_{src}$.
   When both coherences are zero the target bit is independently fair.
2. Choose a fair branch and a uniform anchor $a_1\in G$.
3. In the Phi branch set $a_2=h-a_1$; in the Psi branch set $a_2=a_1-h$.
   Report the branch and the attenuated bit as the Bell outcome.

For either branch the map $(h,a_1)\mapsto(a_1,a_2)$ is bijective, including
even moduli; division by two is never required. Thus for every raw header
pair the joint mass is $|G|^{-2}(1\pm\gamma_1\gamma_2\cos\theta_{sum/diff})/4$,
exactly the native Bell transcript law. The simulator never receives $s$,
an evaluator or a chosen-query API. It uses one X observation, public random
bits and expected $O(n\log q)$ elementary bit work. Small full-joint controls
compare every raw header pair/outcome against native density matrices.

This is equivalence of a PARTICULAR receiver's classical transcript, NOT
classical simulation of quantum HSP oracle access or a DCP solver. Obtaining
the X observation can itself require a quantum state. The result applies to
independent uniform raw headers with fixed header-independent noise, without
additional correlated side information. It does NOT cover headers supplied
in advance, adaptive matching/selection of a pool, header-dependent noise,
or an unmeasured output qubit kept for a later sieve layer.

The fixed-header countercontrol is essential: at $q=4$, headers $e_1,e_2$
and secrets $(1,1)$ versus $(1,3)$, both individual X bits are fair, whereas
the Bell distributions have total-variation distance one. That does not
contradict the random-header transcript reduction. Do not erase this scope.

## 3. Research Decision

Unselected terminal Bell readout is not a constructive escape from the
single-copy X-observation model. Any next proposal must change a stated
premise and provide actual selection/preparation/readout costs, rather than
repeat this identity. No general negative result or speedup is admitted.
The broader optimal-measurement/subset-sum problem remains distinct; see
[Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0501044).
No novelty or formal/independent proof review is claimed here.
