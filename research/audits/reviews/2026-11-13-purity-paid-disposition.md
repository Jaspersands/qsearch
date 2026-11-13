# Paid purity report: new visibility claims

2026-11-13. Independently read the complete 323-LF report
`research/audits/openai_runs/2026-11-13-rank-purity-construct/response.md`.
All new claims listed below check, with the stated scope. The general
polynomial rank–purity bound and proposed (V3) remain OPEN.

Let D=2^n, r_P=<psi|P|psi>, U=union_i L_i for the supplied k stabilizer
rays, V_U=D^(-1) sum_(P in U)|r_P|^2, and Pi=D^(-1) sum_P |r_P|^4.
Since |U|<=kD, Cauchy–Schwarz gives exactly

    Pi >= D V_U^2/|U| >= V_U^2/k.

This has no coefficient, conditioning, or independence hypothesis. U is
a mathematical witness; enumerating it is not a native polynomial operation.

## Sharp two-summand visibility

For distinct nonorthogonal stabilizers, the usual Clifford normal form is
|0^m>, |+^m>, with common stabilizer ancillas. Write q=2^(-m/2),
A+B=1, x=A-B, u=2 Re(conj(alpha) beta). The feasible region is x^2+u^2<=1.
The report's Pauli table gives

    V_U=q^2+(1-q^2)[(1+2qu)^2+x^2]/[2(1+qu)^2].

For fixed u it is minimized at x=0. For q<=1/2, the nonnegative ratio
(1+2qu)/(1+qu) increases with u, so the minimum is at u=-1:

    f(q)=(1-3q+2q^2+2q^3)/[2(1-q)].

For m=1 the square can instead vanish at u=-1/(2q), giving minimum 1/2.
For m=2 it gives 1/4; for m=3 it gives
nu=(29-12 sqrt(2))/56. On 0<q<=1/4,

    f'(q)=(-1+2q+2q^2-2q^3)/(1-q)^2 <0,

so all m>=4 have minimum >=f(1/4)=13/48>nu. The six-qubit minimum is
f(1/8)=169/448, as claimed.

For orthogonal stabilizers, every cross-dyad Pauli coefficient on U is zero.
The signed common-group sum is D*|<s_1|s_2>|^2=0, so V_U=A^2+B^2>=1/2.
Repeated rays or a zero coefficient cannot lower the minimum. Thus nu is
the exact all-dimension two-summand **visibility** minimum, attained by
the three-qubit balanced minus pair. It is not a claimed minimum of Pi.

For tensor-product lists, U_tensor is precisely the Cartesian product of
the factor unions, and both D and the squared Pauli expectations multiply.
Consequently the r-fold example has list length k=2^r and V_U=nu^r.
Since 4nu<1, V_U/k^(-2)=(4nu)^r tends to zero. Every fixed-prefactor
visibility bound V_U>=a k^(-2), a>0, is false. More generally the visibility
exponent must be >=log_2(1/nu). This refutes the indicated visibility route,
not every possible proof of a polynomial bound on Pi.

## Exact phase counterexample

For zeta=(-31+3i sqrt(7))/32, |zeta|=1 and the squared norm of
|0^6>+zeta|+^6> is 225/128. The rank-two table gives the nonidentity
magnitudes 97/225, 31/225, 3sqrt(7)/225 with multiplicities 126,1953,2016.
Exact rational arithmetic with `/opt/anaconda3/bin/python` verified

    [1+126*(97/225)^4+1953*(31/225)^4+2016*3969/225^4]/64
       = 8986816/94921875,
    65*94921875-686*8986816 = 4966099 > 0.

The magnitude 97/225 excludes a stabilizer state, so its rank is exactly two.
Tensor multiplicativity of Pi and chi<=2^r then exclude every fixed
c*k^(-C) bound with C<log_2(94921875/8986816). No assertion that tensor
rank equals 2^r is required. The example does not refute exponent four.

## What is and is not proved for larger lists

Let E_i be collision probability in the stabilizer eigenbasis for L_i.
Pauli/Fourier orthogonality gives E_i=D^(-1)sum_(P in L_i)|r_P|^2 and
V_U<=sum_i E_i<=k V_U. For an orthogonal supplied list, E_i>=|c_i|^4 and
sum_i |c_i|^4>=1/k, proving V_U>=k^(-2) only under that restriction.
Also E_i<=F_S, so the unproved (V3) would imply F_S>=k^(-4).

The report's homogeneous quartic inequality (8) is exactly (V3), including
arbitrary coefficients and singular Gram matrices; it supplies no proof of
that inequality. Its two-summand control and orthogonal-list theorem do not
pay the cancellation problem for growing k. There is no new constructive
operation here that closes the unrestricted endpoint. Park that route
pending such an operation or a decisive new theorem; retain no general
purity, extent, or tomography conclusion from this report.
