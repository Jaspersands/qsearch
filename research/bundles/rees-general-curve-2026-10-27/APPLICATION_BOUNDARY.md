# What The New Gap Does And Does Not Fix

2026-10-27. Local deductions about the existing logical-gate application,
not a new problem candidate. Depends on the general curve gap in RESULT.md.

Read the repository's `research/LOGICAL_GATE_STATE_HSP_APPLICATION.md` first.
The input remains a supplied encoder V and charged coherent linear actions
A and B. A forward encoder call prepares |J_V>; the action is
R(a,b)=A(a) tensor conjugate(B(b)). Its ray stabilizer is the SAME relation
A(a)V=phase*VB(b). Neither the relation nor the native input is replaced.

## A Phase-Spacing-Independent Sufficient Promise

For a nonrelation g of the exponent-p action, write its spectral resolution
R(g)=sum_r omega^r P_r, and w_r=||P_r J_V||^2. Then, with rho=|J_V><J_V|,

    Tr(rho*T_<g>(rho))=sum_r w_r^2.

Suppose every nonrelation satisfies max_r w_r<=1-alpha. Then

    1-Tr(rho*T_<g>(rho)) >= alpha,

since sum w_r^2<=max w_r. If K is not contained in H, choose g in K\H.
The K-invariant Hilbert-Schmidt subspace is contained in the <g>-invariant
subspace. Orthogonal-projection monotonicity gives

    1-Tr(rho*T_K(rho)) >= 1-Tr(rho*T_<g>(rho)) >= alpha.

Thus the proof can use this HS defect promise DIRECTLY: (6) becomes
E_t |overlap(t)|^2<=1-g_c*alpha and the packet overlap contraction is
g_c*alpha/2. There is no need to convert alpha to a trace-distance lower
bound and lose another power. This is an elementary corollary of the gap,
not a new spectral learning algorithm or a certified property of codes.

Crucially alpha concerns weight in eigenspaces, not angular distances
between eigenvalues. Equal weights on two adjacent eigenvalues give
sum w_r^2=1/2 independently of p, while a generator's overlap tends to one
as p grows. Random dilation can fix that phase-spacing problem.

## The Existing Population Obstruction Survives

The old marked-codeword control has weights 1-1/d and 1/d. Exactly,

    1-sum_r w_r^2 = 2(d-1)/d^2,
    TD(rho,T_<g>(rho)) = sqrt(d-1)/d.

So dilation removes the extra small-angle p dependence but still needs
order d copies in this bound, up to other factors. This agrees with the
existing independent Choi-copy lower bound Omega(d). It does not prove
a matching algorithm in all other parameters. A population promise with
inverse-polynomial alpha is still required when d is exponential in the
logical register size. Large code distance alone still does not imply it.

The control is an adversarial test already in the repository, not a new
toy-oracle candidate. No new search campaign or generator is added.

## Decision

The new all-fixed-class source result removes one mathematically real
restriction, but it does not yet raise this application to a serious
breakthrough candidate. We have no natural higher-class encoder/action
family with the required population promise and a task not already handled
by existing classical or quantum learners. The original application audit's
known stabilizer, tensor-network, explicit-matrix and sparse-Pauli baselines
remain binding.

STOP extending this branch solely by class, constants, or planted instances.
The next investment should either exhibit such an actual family with a
costed reduction, or pivot to another constructive lead. Keep the theorem
as a reusable source lemma, not an excuse for another workbench.
