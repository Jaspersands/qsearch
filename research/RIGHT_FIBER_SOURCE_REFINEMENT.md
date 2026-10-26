# Right-Fiber Source Refinement

This pass audits one obstruction in the metabelian-derived HSP proposal:
whether the ordinary hiding oracle supplies the exact monomial mixed
source used by the higher-degree compiler. It does not propose a new
oracle problem or claim a quantum separation.

## General Source Identity

Let N be a finite group, I a finite abelian group and T a transversal.
The public data are a group embedding of I, a section r:T->N and a
bijection satisfying n=r(x)i. Neither centrality nor normality of I is
needed for this source identity. Define

```
(T_g(x), kappa(g,x)) = coordinates(g*r(x)).
g*r(x)*i = r(T_g(x))*(kappa(g,x)+i).
```

Only associativity and the abelian fiber law are used. In particular,
centrality must not be silently substituted for the RIGHT-fiber convention.
The cocycle composition is

```
kappa(gh,x) = kappa(h,x) + kappa(g,T_h(x)).
```

After normal-coordinate inversion the public Fourier amplitudes are

```
K_chi[x,n] = |I|^(-1/2) [x=pr_T(n^-1)] chi(pr_I(n^-1)).
```

Summing K_chi^dag K_chi over every character, including the trivial one,
gives the identity. Direct contraction of the right-regular kernel gives

```
W_chi(g)|x> = chi(kappa(g,x)) |T_g(x)>.
```

This need not be irreducible. The regular-sector source is not normalized
by an irreducible dimension or by the image of one character.

For a transverse ordinary HSP source with projected hidden subspace U,
the original hiding-output trace and normal-first ambient chart give

```
rho_chi[(q,x),(r,y)] = |I|^-1 [r-q in U] / (|V|*|T|)
                      * (W_chi(g(q))^dag W_chi(g(r)))[x,y].
```

Every character has mass 1/|I| under these hypotheses. A nontrivial
hidden intersection with the normal subgroup invalidates the transverse
parametrization; no uniform-label conclusion is made in that case.
The hidden potential is a proof witness, not a source-preparation input.

## Additive Quotient And Phase Sign

For the proposed receiver, I is normal and contains N'. A public quotient
homomorphism to additive A=N/I identifies T=A. It follows that
T_g(x)=a(g)+x. No homomorphic section is required. This is exactly the
translation model required by the new compiler.

If a public GL alignment satisfies

```
L a(g(q)) = (a0+F(q), b0),
```

then measuring the spectator zeta produces

```
|I|^-1 |Z|^-1 curveRho_U,F(P),
P(q,t) = chi(-kappa(g(q), L^-1(t,zeta))).
```

The minus sign comes from W(g(q))^dag, not from changing the Fourier
convention. The corresponding conditional curve state is normalized,
but the displayed expression keeps the physical branch mass. In the
batch receiver kappa is summed over independent source factors.

## Implementation And Evidence

`formal/Formal/CentralRegularSource.lean` is generalized at its chart
boundary. Its historical namespace now accepts RightAbelianChart. The
old CentralChart converts to it; the rest of the source, completeness,
representation and ordinary-oracle proofs are reused. This avoids a
second disconnected copy of the source proof.

`formal/Formal/InducedRegularSource.lean` supplies an additive-quotient
chart, the translation/cocycle law, the monomial matrix kernel, and the
ordinary-oracle-to-aligned-scalar statement. Its operational definition
contains only charts, the original f, Fourier labels, the public linear
alignment and the measured spectator. No potential or hidden U is passed
to the instrument.

A concrete vector-BCH chart uses I=B+C, which can be noncentral. Its
right coordinate is (a,(b,c-delta(a,b)/2)), not the raw logarithmic
(a,(b,c)). A nonzero delta(a,b) witnesses failure of centrality. Thus the
generalized interface has a genuine noncentral instantiation.

The new exact Python test starts with canonical ORIGINAL gH labels in
F_p^2 x N, with class-four filiform N at p11. It performs inverse/right-
fiber Fourier contraction by exact phase counts, then the batch shear,
public GL pullback and spectator restriction. The resulting phase agrees
with the compiled polynomial, including its sign. Its fixed subgroup is
chosen before deriving the diagnostic potential. Its projected U is proper.

For b copies the test also verifies the full branch coefficient

```
1/(|V|*|G|^b)
  = [1/(|I|^b*|V|^b*|Z|)] * [1/(|V|*|J|)].
```

This retains the Fourier, shear-outcome and spectator records. Deleting
either the |I| factor or the |V|^b shear factor fails. It is a diagnostic
direct-product source, NOT an assertion N=G' for that example, and it is
not an executed quantum circuit. Its actual translation potential is
linear inside the full degree-two jet chart; no high-degree hardness is
inferred from the finite test.

## Scope And Falsifiers

The algorithmic target remains fixed-class explicit Lie input with
metabelian derived algebra and growing prime p>k*c. The intended bound
is polynomial in input dimension and log(p) for fixed class, conditional
on the remaining uniform receiver/resource proof and fixed-degree SDE
dependency. No matched classical separation or useful hard application
has been established. Existing explicit stabilizer applications may have
efficient classical attacks; arbitrary oracle access is not a substitute
for demonstrating a meaningful application.

The induced/Fourier representation machinery is prior art. For context,
[Moore--Rockmore--Russell](https://arxiv.org/abs/quant-ph/0304064) gives
generic finite-group QFT constructions. The constant-class HSP result
of [Imran--Ivanyos](https://arxiv.org/abs/2304.08376) also bounds the prime
factors; it is not itself a certificate for the growing-prime claim here.
This comparison is not an exhaustive novelty audit.

Remaining: formal specialization to the general explicit Lie/Lazard
input, refinement of the universal symbolic coefficient compiler, full
batch/source/erasure composition with classical records, updated resource
caps, all-input SDE execution, coherent synthesis and independent review.
Falsify the route if any of those requires hidden advice, exponential
large-prime work, unsupported freshness or an uncharged source operation.

## Verification

On 2026-10-22 the full `lake build --wfail` passed (3466 jobs). The new
module is included in the normal build and has eight standard-axiom
guards. There are no proof placeholders. The connected Python selection
passed 84 tests in 34.63s with RuntimeWarning fatal; the subsequently
strengthened composition test passed in 5.49s. Python syntax, formal
crosscheck, all site JavaScript syntax, site checks, `qsearch.py validate`
and whitespace checks passed. The entire repository Python suite was
not run. No background jobs, commits, CLI/UI changes, central registry
admissions or outreach were made.
