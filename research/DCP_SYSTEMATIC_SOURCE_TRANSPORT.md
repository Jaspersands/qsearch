# Native Systematic Source Transport

LOCAL DERIVATION / REVIEW PENDING. This resolves a source-coordinate obligation,
not residue decoding, an accepted candidate, natural lattice composition or a
quantum speedup. It uses only known public modular arithmetic.

## An Identity Binary Prefix Need Not Be Exponentially Rare

Assume original public labels A are IID uniform columns in Z_q^n, q=2^h>=8.
Let B=A mod2. Allocate a whole packet before examining its first n columns.
Retain the packet if the binary prefix P is invertible. This event has mass

    p_n = product_(j=1)^n (1-2^(-j)),

not 2^(-n^2). The latter is the mass of the LITERAL event P=I, without any
public row normalization. Do not conflate those events.

Choose T by lifting P^-1 over F2 to the integer matrix with entries0/1. Its
determinant is odd, hence it is invertible modulo q and every lower power of2.
T depends ONLY on the original binary prefix, never on its higher bits.
The new public labels are A'=T A mod q. The underlying unknown phase states
are unchanged: relabel the unknown coordinates as s'=T^(-transpose)*s, so

    <A'_i,s'> = <A_i,s> mod q.

This operation does not prepare, copy or query an unknown state. A supplied
decoder for the transformed coordinates would return s=T^transpose*s'.
There is no such full decoder in this project yet. Each packet can have a
different T; intermediate secret coordinates must be reconciled before results
are combined. Residue coordinates modulo q/2 transform back only modulo q/2.
The lost original top bits still require the existing fresh completion step.

## The Entire Higher-Label Law Is Preserved

Condition on P and on the original entire binary matrix B. Write each column

    A_i = B_i + 2 H_i,      H_i uniform in Z_(q/2)^n.

Let B'_i=T B_i mod2 with canonical binary representatives. Then

    H'_i = (T B_i - B'_i)/2 + T H_i mod(q/2).       (1)

The integer division is componentwise exact. Since T is invertible modulo q/2,
(1) is a bijection of each higher-label vector. Thus conditional on B, the
transformed higher labels on EVERY column are IID uniform, including the
prefix columns. There is no independence assumption between individual
background rank events.

Conditional on invertible P, the original tail binary columns are independent
uniform and independent of P. Invertible T mod2 keeps them so. Their transformed
full labels are IID uniform in Z_q^n and independent of P. The transformed
binary prefix is exactly I, while its HIGHER bits remain IID uniform. This is
precisely the systematic source used by the current finite packet profiles.

The source identity removes a prefix rarity concern, but does NOT prove that
the particular finite profiles are typical, that any proposed subcode has
large source mass, or that its normalizer iterates. In particular, a specially
chosen TAIL signature such as R=[I_n|1] still has conditional source mass
2^(-n(n+1)) when that literal tail is required. Prefix normalization does not
manufacture a structured tail.

## Wrong Inverse: A Source Countercontrol

Using the ACTUAL full-label prefix inverse would instead set the full prefix
matrix to I. Already at n1,q8 it maps all four odd prefix labels to1 and removes
their random higher bits. The higher-source law above would be false.
Such a transformation can be legal, but it requires a different conditional
source model. The implemented compiler is deliberately low-selected.

Its modular inverse is computed by Newton lifting: start with Y=P modulo2
and replace Y by Y(2I-TY) at doubled bit precision. The compiler verifies both
inverse identities modulo q. Complexity is polynomial in n and log q; no
floating-point field arithmetic or search over residues is used.

## Fixed Secrets And Source Supply

For each ORIGINAL fixed secret s and each accepted P, the transformed secret
s'(P) is fixed before the remaining transformed label randomness. The full
systematic label law is the same for every P. Therefore a systematic decoder
guarantee that holds uniformly for EACH fixed secret can be applied conditional
on P, then transformed back. A uniform-secret mean alone does not provide that
guarantee. A label-dependent secret cannot be silently treated as independent
when the transform depends on higher labels; this construction avoids that
particular problem by using P only.

With R independent preallocated packets, all-prefix rejection is (1-p_n)^R.
Every failed packet is charged: the ledger records R*m original phase states.
Expected attempts until acceptance is1/p_n<4. For n>=2, the first two factors
give3/8 and the tail product is at least1-sum_(j>=3)2^(-j)=3/4, so p_n>=9/32;
n1 has p_1=1/2. These constant source costs are not an algorithmic speedup.
Total lattice state supply, precision, other selection gates and decoding cost
remain separate obligations.

## Verification And Next Decision

Eight focused tests check every invertible binary prefix at n1 and n2,q8,
every higher prefix table, every tail column/coset, and all fixed-secret phase
identities for deterministic calibration packets. They also check a65-bit
modulus, both inverse directions, residue-coordinate covariance, packet-specific
secret coordinates, rejection budgets and the wrong full-prefix-inverse control.
Large integers in the saved transport are encoded in hexadecimal.
An independent Node certificate reconstructs these identities with BigInt.

GPT next: use the actual systematic native law to analyze the prevalence of
NEW low-selected code subspaces with useful correlated Schur-product variation,
and establish higher-carry closure or a genuinely different quantum readout.
Do not treat prefix normalization, high-bit IID preservation or small-profile
survival as a decoder. Gemini retains CLI/registry wiring, full production
regressions and scaling runs from the theory contracts.
