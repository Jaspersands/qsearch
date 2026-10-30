# Handoff: Full Measured-Output Classical Sampler

The new local proof directly samples the actual decoded circuit's joint
computational-basis output. It does not derive a sampler from additive
expectation queries. Coverage requires polynomial C_bar and
k=rank([X;Z])-rank(X)=O(log input size), with an efficient total decoder.
The sampler enumerates 2^k possible physical Z syndromes using forward
decoder calls. It never calls an amplitude oracle or inverse decoder.

An independent shortcut in commuting_linear.py covers the LEFT-register
output at arbitrary rank for commuting generators and an explicitly verified
linear right-inverse decoder. It samples independent rational biased coins,
forms diagonal subgroup constraints and draws a uniform affine solution.
No fiber is enumerated. This shortcut does not claim the joint two-half law.

## Bounded Gemini Work

1. After migration is resolved, expose the rank, fiber bound, C_bar, K,T,
   precision, word/letter and decoder-call costs in the classical baseline.
2. Supply a reproducible decoder with a stated complexity bound. Preserve
   the physical measurement basis and ordered Pauli phases in artifacts.
3. Keep explicit fiber/word-budget refusals and all-trial failure outcomes.
   A refused large-rank input is not a hardness result. Product Z inputs
   are a mandatory negative control for that mistake.
4. Record left, right and discarded decoder residue separately. Returning
   only left is legitimate marginalization, not a different temperature
   or hidden source promise. Gibbs accuracy needs its own proof.
5. Do not replace full output sampling with Bell-label pushforward; the
   one-Z test proves the difference. Do not replace complex sign averages
   with real-only scores or omit the first-stage envelope acceptance.
6. Prefer the commuting/linear shortcut when its exact input checks pass.
   Keep its left-only target explicit. Check BDB=B algebraically; never
   classify an arbitrary callback as linear from a few observed inputs.

## Scientific Next Step

Stop exploring low-rank examples for advantage. Compare a concrete useful
high-rank output task against stronger classical samplers, or return to
the genuinely broader degree-scale preparation problem. No generic
high-rank hardness, universal sampler or new quantum algorithm is established.

The implementation and local proofs have not had independent review.
Original source/staging, central registry, CLI/UI and Git remain untouched.
