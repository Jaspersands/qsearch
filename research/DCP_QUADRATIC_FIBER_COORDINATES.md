# Actual Mod4 Fibers As Structured Quadratic Systems

LOCAL DERIVATION / REVIEW PENDING. This compiler changes coordinates, NOT
information or the source law. It is not a new hidden-shift algorithm, a
quadratic-system solver, a fresh-product-source reduction or a full fiber
inverse. Run `python theorems/dcp_quadratic_fiber_coordinates.py --write`.

## A Useful Exact Representation

Write the coarse labels A mod4=B+2C, with binary matrices B,C. For Boolean x,
the measured equation A*x=y mod4 is EXACTLY

    B_l*x = y_l mod2,
    C_l*x + sum_(i<j) B_li B_lj x_i x_j = floor(y_l/2) mod2.

The carry identity is floor(w/2)=binomial(w,2) mod2 for the integer count
w=sum_i B_li x_i. This is a coupled linear/quadratic system over F2, not an
arbitrary collection of random polynomials. Higher original label bits remain
essential to the quantum phase and are never thrown away by this representation.

RREF of B supplies a particular solution x0 and kernel directions V_j, with
k=m-r variables, r=rank(B). Every low-syndrome solution is uniquely

    x(u)=x0 XOR XOR_j u_j V_j,

where u_j is the ORIGINAL free-coordinate bit. The high syndrome becomes
n explicit degree-at-most-two equations in u. If q_l(x) is the original
high-bit polynomial, its reduced coefficients are

    constant: q_l(x0) XOR floor(y_l/2),
    linear_j: q_l(x0 XOR V_j) XOR q_l(x0),
    quadratic_ij: popcount(B_l AND V_i AND V_j) mod2, i<j.

For the last formula, the original carry Hessian is
B_l^T B_l+diag(B_l) over F2. Since B_l*V_j=0, the outer-product contribution
vanishes on the kernel. Its restricted diagonal entries also vanish. Thus
the remaining Hessians are all restrictions of diagonal coordinate forms
through the SAME kernel basis. This is a potential algebraic handle, not
evidence that the system is easy or hard. Do not invoke generic MQ hardness
or generic random-quadratic heuristics without proving they apply here.

## Actual Clifford Compression, Not Abstract Reindexing

For pivot p with RREF equation x_p XOR sum_j R_pj x_free_j=b_p, apply
CNOT(free_j -> p) for each nonzero R_pj, followed by X(p) when b_p=1.
Every observed-fiber basis vector then has pivot p=0. Free wires are untouched.
All controls are free wires, all targets pivot wires; this is a reversible
affine map on the WHOLE Hilbert space, not a postselected inverse oracle.
At most r*k CNOT and r X gates, no extra work qubits. The measured syndrome
was already charged by the original block circuit. Pivot zeros can be
discarded; there is no new success/postselection penalty for compression.

For native width m=3n, a uniform binary B has full row rank except probability
<2^(n-m)=2^(-2n), by a union bound over nonzero left-kernel vectors. If full
rank, the compiler retains2n original free wires and removes n fixed wires,
with at most2n^2 CNOT gates and n X gates. Rank-deficient cases are handled
with their actual r, not discarded. The remaining n quadratic constraints
are NOT solved; most free-coordinate strings are still outside the full fiber.

The lift u->x(u) inverts the LOW LINEAR affine coset. It does not index only
valid full-fiber states, prepare a uniform quadratic solution, count those
solutions, or certify a new independent phase source. Enumerating all u is
exponential and occurs only in explicitly bounded calibration.

## Preserve Higher Phases And Correlated Noise

The actual retained state on allowed free coordinates has entries

    rho_s(u,u') = D^-1 * exp(2*pi*i*<s,A[x(u)-x(u')]>/q)
                         * v^popcount(V*(u XOR u')),

with D the full-fiber cardinality. The exponent uses ORIGINAL integer labels;
x(u) uses XOR, so the phase need not be linear in the free bits. We do not
substitute A*V as a fresh independent label matrix.

An original independent Z fault vector e transforms to free fault bits
eta_j=<e,V_j> mod2. These are generally correlated. Their marginal visibility
is v^weight(V_j), but a joint parity uses v^weight(XOR_j V_j), NOT the product
of the marginal visibilities. For a concrete same-source counterexample,
A=(1,5,9),y=1 gives x0=001, V_0=011,V_1=101, and quadratic constraint
u0*u1=0. Both directions have weight2, but their XOR also has weight2:
the actual off-diagonal factor between free words01 and10 is v^2, not v^4.
The compiler and tests keep that discrepancy rather than silently dephasing
or multiplying marginal noise laws.

## Research Use And Kill Criteria

This is an exact common representation for receiver synthesis, native-fiber
weighted-moment analysis and classical attacks. It reduces avoidable Hilbert
space size without claiming an entropy gain. Next investigate whether the
simultaneously restricted Hessians admit a useful normal form, sampler,
uniform-state compiler or contraction, and charge all remaining source,
phase, sampling and inverse costs. A polynomial classical representation
alone is not an efficient solver.

Falsifiers: any disagreement with original mod4 constraints; a compiler
requiring full-fiber enumeration; nonzero cleared pivot support on a valid
branch; a lost phase or independent-noise substitution; or a claimed fresh
phase-state reduction that ignores the residual quadratic constraints.
Finite density controls replay the original noisy state. Gate tests include
arbitrary outside-fiber inputs and the complete inverse, not just truth tables
restricted to the desired syndrome.
