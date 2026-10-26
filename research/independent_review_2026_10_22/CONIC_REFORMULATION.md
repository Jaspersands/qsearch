# A sharper algebraic attack formulation, with its zero-point trap

Status: proved reformulation and failed automatic-linearization argument.
No polynomial classical native solver is claimed.

Choose c in F_q with Tr(c)=1 by binary linear algebra. For each coordinate
introduce u_i and consider the SINGLE field-quadratic equation

    u_i² + x_i*u_i + c*b_i*x_i² = 1.                (1)

For x_i!=0, divide by x_i². The equation for v_i=u_i/x_i is

    v_i²+v_i = 1/x_i²+c*b_i.

It has two field roots exactly when Tr(1/x_i)=b_i. Thus the original native
relation is equivalent to Hx=0, equations (1), and x_i!=0 at every b_i=1.
For b_i=0, x_i=0 is legal and (1) has the unique root u_i=1. There is no
need to exclude that legitimate zero stratum.

**Specific falsifier of a naive MQ attack:** x=0 and u=(1,...,1) satisfy
all N quadrics and Hx=0 for EVERY b, including all ones. For any nonzero
b this output is not a native witness. A generic solver returning an
arbitrary zero of the quadratic system has therefore not solved the task.
Nonzero conditions can be enforced by x_i*r_i=1 at b_i=1, but those extra
variables/equations and their cost must be retained. They are not a free
promise about the answer returned by an MQ solver.

## Nonzero witnesses exist for every large native instance

**Proved deduction:** restricting the SEARCH to all-nonzero witnesses
does not require an extra input promise in the asymptotic native family.
Let eta_m bound all relative fiber errors at length m with the same K
checks, as in GIBBS_AUDIT.md. For any coordinate i with b_i=0, setting
x_i=0 leaves precisely the same problem on the other N-1 distinct points.
Its baseline count is (2/q) times the original baseline. Therefore

    Pr[x_i=0 | x uniform in A_b]
      <= (2/q)*(1+eta_(N-1))/(1-eta_N).

For b_i=1 this probability is zero. A union bound yields

    Pr[all x_i != 0 | x uniform in A_b]
      >= 1 - (2*#{i:b_i=0}/q)*(1+eta_(N-1))/(1-eta_N).

At N=n², K=floor(N/8), both errors vanish and N/q vanishes. Thus every
target has all-nonzero witnesses for sufficiently large n. This is a
counting proof, not a sampler: it does not tell a classical algorithm how
to locate one. It does mean that a correct efficient solver of the
nonzero stratum would solve the original native search problem. The
unsaturated all-zero counterexample remains invalid, and a method that
returns an arbitrary point of an algebraic closure has not enforced the
nonzero stratum. For the finite n=17 parameter size, the elementary
leading loss bound is 578/131072, with the displayed fiber-error factors
still retained; this is a bound, not a new experiment.

Self-attack: this argument uses the shorter-length fiber theorem, not an
assumption that conditioning preserves uniformity. If its error bound
were at least one, the conclusion would not follow. In the native regime
the same MDS/character-sum estimate explicitly handles N-1 and arbitrary
remaining target bits. No target or evaluation points are resampled.

After eliminating Hx=0, the unsaturated system has 2N-K field variables
and N quadratic equations. This constant-factor surplus is outside the
massively underdetermined polynomial-time regime of the general algorithms
reviewed in [Yasufumi Hashimoto, An improvement of algorithms to solve
under-defined systems of multivariate quadratic equations](https://eprint.iacr.org/2021/1045).
That observation is only a failure to import that theorem. The special
diagonal conic structure could be easier than general MQ and is a concrete
remaining attack target. General MQ hardness also cannot be imported here.

## Why the apparent oil-variable linearization is not already a solver

Over binary coordinates, squaring is linear. If x is fixed, (1) is a
binary linear equation in the u variables. For x_i!=0 the linear operator

    L_(x_i)(u)=u²+x_i*u

has kernel {0,x_i}, hence rank n-1. The missing compatibility equation is
exactly Tr(1/x_i²+c*b_i)=0. Over all coordinates the linear solve retains
the original inverse-trace compatibility tests; it has not eliminated
them. At x_i=0 the operator u->u² is invertible, which explains why the
spurious all-zero solution is so easy for the unsaturated system.

Fixing the other block does not give a useful random-vinegar solver
either. If u is fixed, squaring makes the equations binary linear in x,
together with Hx=0. But sample u uniformly from F_q^N and let X(u) count
the valid native x solutions of this linearized system, enforcing the
target-one nonzero condition. A native x with t nonzero coordinates has
exactly 2^t compatible u values. Hence

    E_u X(u) = q^(-N) sum_(x in A_b) 2^wt(x)
             <= 2^N |A_b|/q^N = lambda_b q^(-K).

Therefore Pr_u[X(u)>0]<=lambda_b q^(-K), even if the subsequent solve
could choose any valid solution without further cost. This is much worse
than the paid systematic-root probability lambda_b*2^-K. It is a precise
failure of independent uniform sampling of this block, not a lower bound
against target-dependent or correlated choices of u. Omitting the
nonzero condition instead counts the already exhibited false solutions.

One may instead seek large affine families in the lifted conic. This too
has a precise limit. For Q_b(x,u)=u²+xu+c*b*x², its polar form is

    B((x,u),(x',u'))=x*u'+x'*u.

If an affine binary space p+V lies entirely in Q_b=1, then B vanishes on
V x V. All nonzero directions in V are consequently collinear over F_q:
in a two-dimensional symplectic space, a vector's orthogonal space is its
own field line. Write V={a*v:a in T}. Constancy gives

    a² Q_b(v)+a B(p,v)=0   for every a in T.

This nonzero polynomial has at most two roots. If it were identically
zero, Q_b(v)=0 and B(p,v)=0 would force p onto the same isotropic field
line, contradicting Q_b(p)=1. Therefore dim_F2(V)<=1.

This does NOT bound the dimension of accepted flats in the x projection:
the choices of u above an accepted x-flat need not be affine. It rules out
one particular free-lift shortcut, not the accepted-flat attack itself.

## Next decisive algebraic question

The generic underdetermined-system literature does not make this step
free. [Gimenez--Matera--Perez--Privitelli](https://arxiv.org/pdf/2206.12516),
Algorithm 1.1 and Theorem 1.4, retain the cost of a zero-dimensional
solver in each vertical strip. Their average is over polynomial
coefficients, and the stated asymptotic setup fixes the numbers of
variables and equations. Neither premise is supplied by this structured
native family. A small expected number of restrictions is not a small
cost for solving each restriction.

Find a constructive algorithm for this particular product of conics cut
by the given Vandermonde equations, while avoiding x_i=0 where b_i=1.
Any useful solver must retain arbitrary target bits and the actual public
evaluation points. A proof that returns an arbitrary quadratic-system
solution, assumes a nonsingular oil matrix, or substitutes a supplied
nonzero solution fails at the explicit tests above.
