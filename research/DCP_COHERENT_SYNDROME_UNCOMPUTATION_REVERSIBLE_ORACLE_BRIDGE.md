# DCP Coherent Syndrome Uncomputation and Reversible Oracle Bridge

## Correction: Coherent Upper Bound Retracted (2026-10-17)

V1 applied a classical-quantum block-diagonal formula to a coherent pure state.
For theta=(0,0), theta'=(0,pi), with zero relative branch-amplitude phases,
the coherent inner product is1/2 and trace distance is sqrt(3)/2. The
branch-average distance is only1/2. It is NOT a coherent upper bound.

## Three Different States

All distances here mean half the trace norm, twice equal-prior success bias.
Write `Psi = sum_d exp(i*alpha_d)|d>|psi(theta_d)>/sqrt(B)`.

- Coherent: `D=sqrt(1-|inner|^2)`, where
  `inner=mean_d exp(i*(alpha'_d-alpha_d))*(1+exp(i*(theta'_d-theta_d)))/2`.
- Dephased syndrome: `D=mean_d |sin((theta_d-theta'_d)/2)|`.
- Discarded syndrome: `D=|mean_d(exp(i*theta_d)-exp(i*theta'_d))|/2`.

Data processing gives `D_coherent >= D_dephased >= D_discarded`.
A secret-independent unitary preserves the COHERENT distance; that does
not supply efficient measurement synthesis, and dephasing need not be harmless.

## Native CNOT Accounting

From product phases theta_j, use target u=x_0 and syndromes d_j=x_j XOR x_0.
The actual branch-amplitude phase is `alpha_d=sum_{j>0} theta_j*d_j`; the
conditional target phase is `theta_0+sum_{j>0}(1-2*d_j)*theta_j`.
Both depend on the secret. Dropping alpha_d changes relative coherent phases,
not just a global gauge. The new control explicitly permutes native product
amplitudes and verifies the complex product-state inner product.

## Constructive Control And Limits

When alpha_d=0 and theta_d=theta_0+delta_d for publicly known, secret-independent
delta_d, controlled phase correction followed by syndrome Hadamards erases
the syndrome deterministically. Actual gates are now applied to the whole
finite reference vector. Generic DCP does NOT provide that phase access.

Tests independently diagonalize coherent, dephased and discarded density
differences, apply unrelated random unitaries, retain native branch phases,
and check invalid models. Dense references grow exponentially and are not a
scalable decoder. No candidate, negative result or proof status is promoted.
