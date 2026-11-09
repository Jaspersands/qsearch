# RSK composition is not normalized Kronecker sampling

2026-11-06. First exact falsifier; no general classical-sampling lower bound.

## Question and admission

Input two explicit partitions lambda,mu of n. The target is a sample nu
with probability d_nu*g(lambda,mu,nu)/(d_lambda*d_mu), to inverse-polynomial
total-variation accuracy. No character table, Kronecker coefficients or
advice are supplied. [Bravyi et al.,2302.11454v3 Lemma2 and AppendixE](https://arxiv.org/html/2302.11454v3)
give a polynomial-size quantum sampler.
The actual theorem and construction were checked. This is a native
representation-theoretic sampling task, not a hidden-involution decoder.

Proposed classical mechanism: sample independent uniform standard-tableau
pairs of shapes lambda and mu, apply inverse RSK to get permutations a,b,
compose them, and return the RSK shape of a composed with b. Uniform tableau
sampling and RSK have polynomial cost in n; no unknown character or
multiplicity evaluations are hidden in this proposal. If its exact law
were the target, it would supply a classical competitor to this quantum
sampler. No quantum advantage or hardness was assumed.

Corpus been-tried and baselines queries preceded the test; no exact match
was found, which is not evidence of hardness. Prior RSK results in
RECTANGULAR_CHARACTER_SAMPLER.md concern a different character-column law.
The primary literature check also inspected the actual weighted identities
and theorem scope in [Avella-Alaminos--Vallejo,1003.4482](https://arxiv.org/pdf/1003.4482).
Its generalized RSK/minimal-matrix
identities do not license replacing the proposed probability-law proof.
Strong matched baseline for the tiny test is exact Schur internal product
in Sage. No large-n classical runtime claim follows from this calculation.

## First falsifier

Take n=4 and lambda=mu=(2,2). The four RSK preimages are exactly

    2143, 2413, 3142, 3412.

They are uniform under uniform independent tableau pairs. Their16 ordered
products are uniform on 1234,1324,4231,4321, each occurring four times.
The resulting shape law, compared with the target, is:

| nu | RSK-composition law | Target Kronecker law |
|---|---:|---:|
| (4) | 1/4 | 1/4 |
| (3,1) | 1/4 | 0 |
| (2,2) | 0 | 1/2 |
| (2,1,1) | 1/4 | 0 |
| (1,1,1,1) | 1/4 | 1/4 |

The target follows from s_22 internal-product s_22=s_4+s_22+s_1111,
with dimensions1,2,1. Independently, on cycle types1^4,21^2,2^2,31,4,
the character chi_22=(2,0,2,-1,0) has square=(4,0,4,1,0), exactly the
sum of chi_4,chi_22,chi_1111. A single forbidden witness already suffices:

    2143 composed with 2413 = 1324,

whose RSK shape is(3,1). The exact total-variation distance is1/2.

One independent Sage calculation checked the first prescribed instance
and stopped; the parent independently checked the four-element product
law, witness and character decomposition. No larger scan or code artifact
is needed. This closes only this proposed exact sampler. It neither rules
out all classical samplers nor refutes the published quantum construction.
An asymptotic approximation claim would require a separate algorithm and
bound; this proposal supplied neither.

## Next decision

Do not build a sampler wrapper, average more instances or change the native
target to the law actually produced. Re-rank independent constructive
directions. A future Kronecker continuation needs a concrete operation that
pays the desired distribution, with its first exact falsifier specified.
No new implementation or registry record is queued.
