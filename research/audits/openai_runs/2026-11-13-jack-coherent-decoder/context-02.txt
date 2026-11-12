# New concrete full-transform proposal, not a proved algorithm

Assume A_d psi_(lambda,s)=J_(lambda+s), now independently derived via norm
saturation (parent review pending). Alpha3 fixed. Parent overlap deductions:
1. Poles a_i and zeros b_j of m_lambda(u)=prod(u-b)/prod(u-a) are strictly
interlacing INTEGERS in interval of length<=4d. Hence tau_i>=1/(16d^2),
for d>=1: on each side of a_i the residue product telescopes below by the
inverse distance to the extreme pole. d0 gives1.
2. For mu of size d+1, compressed spectral mass
kappa_i=-Res_(u=b_i) 1/m_mu(u)=prod_j |b_i-a_j|/prod_(j!=i)|b_i-b_j|
is >=(b_i-a_i)(a_(i+1)-b_i)>=1; all other interlacing ratios are>=1.
Sum kappa_i=3(d+1)=||A†Jmu||²/||Jmu||². Thus q_i=kappa_i/[3(d+1)]
>=1/[3(d+1)]. These derivations still require parent/paid review.

Native NONDEMOLITION label sampling, NO input lambda label:
UP: starting Jlambda at w0, measure L_d content c. Rewind to pi0 via
alternating pi0 and the observed-c projector; all paths stay Zlambda.
Record c, and return the original Jlambda. Both measurements native.
DOWN: starting Jmu, apply V=A†/sqrt(3(d+1)), measure L_d content c,
then alternate P_A and observed-c projector to return V Jmu; applyV†.
All paths should stay S_mu=span{psi_(mu-r,r)}. Record removable c.
Uniform overlap lower bounds give polynomial finite clocks without knowing
lambda or mu. Repeat polynomially many times to collect ALL up/down corners,
with uniform failure<=eta. No probability/weight estimation is required.

Given full sorted addable contents a1>...>a_(m+1) and removable contents
r1>...>rm, set bi=ri+2. Boundary block heights hi=ai-bi, width jumps
wi=(bi-a_(i+1))/3. Recover distinct row lengths Li=sum_(j>=i)wj,
repeating Li exactly hi times. All are positive integers and final sizeD.
Thus BOTH corner sets uniquely determine partition at alpha3.

Can this nondemolition decoder be made a clean coherent isometry
|Jlambda>|0> -> |Jlambda>|lambda> uniformly in superposition, with operator
norm error epsilon polynomial resources? Defer measurements into histories,
compute label into fresh register, reverse histories (compute-copy-uncompute).
Need a uniform operator norm bound, NOT merely basis-state success: dimension
p(D) is exponential. Exact successful histories are diagonal in the Jack
basis; this may bound failure operator by max_lambda p_fail instead of sum.
All caps and approximate spectral measurements need diamond/operator-norm
control, and success must not call reflection about Jlambda.

If such a decoder exists, controlled preparation |lambda>|0> ->
|lambda>|Jlambda> can erase lambda using the clean decoder (XOR output),
yielding a full unitary change of basis. Controlled preparation itself must
be coherent and clean: naive measured lambda-dependent histories leak lambda.
Possible compute-copy-uncompute for a fixed classical lambda works only if
one can coherently purify/remove lambda-dependent success histories; decide
whether amplitude amplification with known angles/native projectors does so
without recursive inverses. Do NOT assume state preparation implies a full
transform. This is the precise strengthened endpoint under investigation.
