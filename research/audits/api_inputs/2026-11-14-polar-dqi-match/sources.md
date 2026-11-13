# korada_source_raw.txt
URL https://arxiv.org/pdf/0903.0307
Raw textsha256 485e2ba029ece0320e40b13be640a8449f576fcddd4121ccba9d9b36443451cb


## Physical LF540-716
{0,1}|F|
be a fixed vector. In the sequel we use the shorthand
“SM(F,ũF )” to denote the Standard Model with frozen set F
whose components are fixed to ũF . It is defined as follows.
Encoding: Let fũF
: {0,1}N
→ {0,1}N−|F|
denote the
encoding function. For a given ȳ we first compute ū, as
described below, where ū = (u0,...,uN−1). Then fũF
(ȳ) =
ūFc.
Given ȳ, for each i in the range 0 till N − 1:
(i) Compute
li(ȳ,ui−1
0 ) ,
W(i)
(ȳ,ui−1
0 |ui = 0)
W(i)(ȳ,ui−1
0 |ui = 1)
.
(ii) If i ∈ Fc
then set ui = 0 with probability li
1+li
and equal
to 1 otherwise; if i ∈ F then set ui = ũi.
Decoding: The decoding function ˆ fũF
: {0,1}N−|F|
→
{0,1}N
maps ūFc back to the reconstruction point x̄ via x̄ =
ūHn, where ūF = ũF .
Distortion: The average distortion incurred by this scheme
is given by E[d(Ȳ ,X̄)], where the expectation is over the 5
source randomness and the randomness involved in the ran-
domized rounding at the encoder.
Complexity: The encoding (decoding) task for source coding
is the same as the decoding (encoding)task for channel coding.
As remarked before, both have complexity Θ(N logN).
Remark: Recall that li is the posterior of the variable
Ui given the observations Ȳ as well as Ūi−1
0 , under the
assumption that Ū has uniform prior and that Ȳ is the result
of transmitting ŪHn over a BSC(D).
B. Computation of Average Distortion
The encoding function fũF
is random. More precisely, in
step i of the encoding process, i ∈ Fc
, we fix the value
of Ui proportional to the posterior (randomized rounding)
PUi |Ui−1
0 ,Ȳ (ui |ui−1
0 ,ȳ). This implies that the probability of
picking a vector ū given ȳ is equal to
(
0, ūF 6= ũF ,
Q
i∈Fc PUi |Ui−1
0 ,Ȳ (ui |ui−1
0 ,ȳ), ūF = ũF .
Therefore, the average (over ȳ and the randomness of the
encoder) distortion of SM(F,ũF ) is given by
DN(F,ũF ) =
X
ȳ∈{0,1}N
1
2N
X
ūFc∈{0,1}|Fc|
Y
i∈Fc
P(ui |ui−1
0 ,ȳ)d(ȳ,ūHn), (8)
where Ui = ũi for i ∈ F.
We want to to show that there exists a set F of cardinality
roughly Nh2(D) and a vector ũF such that DN(F,ũF ) ≈
D. This will show that polar codes achieve the rate-distortion
bound.
For the proof it is more convenient not to determine the
distortion for a fixed choice of ũF but to compute the average
distortion over all possible choices (with a uniform distribution
over these choices). Later, in Section V, we will see that the
distortion does not depend on the choice of ũF . A convenient
choice is therefore to set it to zero. This will lead to the desired
final result.
Let us therefore start by computing the average distor-
tion. Let DN(F) denote the distortion obtained by averaging
DN(F,ũF ) over all 2|F|
possible values of ũF . We will show
that DN(F) is close to D.
The distortion DN(F) can be written as
DN(F) =
X
ũF ∈{0,1}|F|
1
2|F|
DN(F,ũF )
=
X
ũF
1
2|F|
X
ȳ
1
2N
X
ūFc
Y
i∈Fc
P(ui |ui−1
0 ,ȳ)d(ȳ,ūHn)
=
X
ȳ
1
2N
X
ū
1
2|F|
Y
i∈Fc
P(ui |ui−1
0 ,ȳ)d(ȳ,ūHn).
Let QŪ,Ȳ denote the distribution defined by QȲ (ȳ) = 1
2N and
QŪ |Ȳ defined by
Q(ui |ui−1
0 ,ȳ) =
  1
2, if i ∈ F,
PUi |Ui−1
0 ,Ȳ (ui |ui−1
0 ,ȳ), if i ∈ Fc
.
(9)
Then,
DN(F) = EQ[d(Ȳ ,ŪHn)],
where EQ[·] denotes expectation with respect to the distribu-
tion QŪ,Ȳ .
Similarly, let EP [·] denote the expectation with respect to
the distribution PŪ,Ȳ . Recall that PȲ (ȳ) = 1
2N and that we
can write PŪ |Ȳ in the form
PŪ |Ȳ (ū|ȳ) =
N−1 Y
i=0
PUi |Ui−1
0 ,Ȳ (ui |ui−1
0 ,ȳ).
If we compare Q to P we see that they have the same structure
except for the components i ∈ F. Indeed, in the following
lemma we show that the total variation distance between Q
and P can be bounded in terms of how much the posteriors
QUi |Ui−1
0 ,Ȳ and PUi |Ui−1
0 ,Ȳ differ for i ∈ F.
Lemma 2 (Bound on the Total Variation Distance): Let F
denote the set of frozen indices and let the probability dis-
tributions Q and P be as defined above. Then
X
ū,ȳ
|Q(ū,ȳ) − P(ū,ȳ)|
≤ 2
X
i∈F
EP
 
1
2
− PUi |Ui−1
0 ,Ȳ (0|Ui−1
0 ,Ȳ )
 
.

## Physical LF833-975
Lemma 3 (Distortion under Q versus Distortion under P):
Let F be chosen such that for i ∈ F
EP
 
1
2
− PUi |Ui−1
0 ,Ȳ (0|Ui−1
0 ,Ȳ )
 
≤ δN. (10)
The average distortion is then bounded by
1
N
EQ[d(Ȳ ,ŪHn)] ≤
1
N
EP [d(Ȳ ,ŪHn)] + |F|2δN.
Proof:
EQ[d(Ȳ ,ŪHn)] − EP [d(Ȳ ,ŪHn)]
=
X
ū,ȳ
 
Q(ū,ȳ) − P(ū,ȳ)
 
d(ȳ,ūHn)
≤ N
X
ū,ȳ
Q(ū,ȳ) − P(ū,ȳ)
Lem. 2
≤ 2N
X
i∈F
EP
 
1
2
− PUi |Ui−1
0 ,Ȳ (0|Ui−1
0 ,Ȳ )
 
≤ |F|2NδN.
From Lemma 3 we see that the average (over ȳ as well as
ũF ) distortion of the Standard Model is upper bounded by the
average distortion with respect to P plus a term which bounds
the “distance” between Q and P.
Lemma 4 (Distortion under P):
EP [d(Ȳ ,ŪHn)] = ND.
Proof: Let X̄ = ŪHn and write
EP [d(Ȳ ,ŪHn)]
=
X
ū,ȳ
PŪ,Ȳ (ū,ȳ) d(ȳ,ūHn)
=
X
ȳ,ū,x̄
PŪ,X̄,Ȳ (ū,x̄,ȳ) d(ȳ,ūHn)
=
X
ȳ,ū,x̄
PX̄,Ȳ (x̄,ȳ)PŪ |X̄,Ȳ (ū|x̄,ȳ)
| {z }
{0,1}-valued
d(ȳ,x̄)
=
X
ȳ,x̄
PX̄,Ȳ (x̄,ȳ) d(ȳ,x̄).
Note that the unconditional distribution of X̄ as well as Ȳ is
the uniform one and that the channel between X̄ and Ȳ is
memoryless and identical for each component. Therefore, we
can write this expectation as
EP [d(Ȳ ,ŪHn)] = N
X
x0,y0
PX0,Y0(x0,y0) d(y0,x0)
(a)
= N
X
x0
PX0 (x0)
X
y0
W(y0 |x0) d(y0,x0)
= NW(0|1)
(b)
= ND.
In the above equation, (a) follows from the fact that
PY |X(y |x) = W(y |x), and (b) follows from our assumption
that W is a BSC(D).
This implies that if we use all the variables {Ui} to represent
the source word, i.e., F is empty, then the algorithm results in
an average distortion D. But the rate of such a code would be
1. Fortunately, the last problem is easily fixed. If we choose F
to consist of those variables which are “essentially random,”
then there is only a small distortion penalty (namely, |F|2δN)
to pay with respect to the previous case. But the rate has been
decreased to 1 − |F|/N.
Lemma 3 shows that the guiding principle for choosing the
set F is to include the indices with small δN in (10). In the
following lemma, we find a sufficient condition for an index
to satisfy (10), which is easier to handle.
Lemma 5 (Z(i)
Close to 1 is Good): If Z(i)
≥ 1 − 2δ2
N,
then
EP
 
1
2
− PUi |Ui−1
0 ,Ȳ (0|Ui−1
0 ,Ȳ )
 
≤ δN.
Proof:
EP
hq
PUi |Ui−1
0 ,Ȳ (0|Ui−1
0 ,Ȳ )PUi |Ui−1
0 ,Ȳ (1|Ui−1
0 ,Ȳ )
i
=
X
ui−1
0 ,ȳ
PUi−1
0 ,Ȳ (ui−1
0 ,ȳ)
q
PUi |Ui−1
0 ,Ȳ (0|ui−1
0 ,ȳ)PUi |Ui−1
0 ,Ȳ (1|ui−1
0 ,ȳ)
=
X

## Physical LF1144-1505
DN(FN,ũFN ) ≤ D + O(2−(Nβ
)
)
for any 0 < β < 1
2.
The complexity of the encoding and decoding algorithms
are of the order Θ(N log(N)) as shown in [15].  
V. VALUE OF FROZEN BITS DOES NOT MATTER
In the previous sections we have considered DN(F), the
average distortion if we average over all choices of ũF . We
will now show a stronger result, namely we will show that all
choices for ũF lead to the same distortion, i.e., DN(F,ũF )
is independent of ũF . This implies that the components
belonging to the frozen set F can be set to any value. A
convenient choice is to set them to 0. In the following let F
be a fixed set. The results here do not dependent on the set
F.
Lemma 6 (Gauge Transformation): Consider the Standard
Model introduced in the previous section. Let ȳ,ȳ′
∈ {0,1}N
and let ui−1
0 = u′i−1
0 ⊕ ((ȳ ⊕ ȳ′
)H−1
n )i−1
0 . Then
li(ȳ,ui−1
0 ) =
 
li(ȳ′
,u′i−1
0 ), if ((ȳ ⊕ ȳ′
)H−1
n )i = 0,
1/li(ȳ′
,u′i−1
0 ), if ((ȳ ⊕ ȳ′
)H−1
n )i = 1.
Proof:
li(ȳ,ui−1
0 )
=
W(i)
(ȳ,ui−1
0 |0)
W(i)(ȳ,ui−1
0 |1)
=
P
uN−1
i+1
P(ȳ |ui−1
0 ,0,uN−1
i+1 )
P
uN−1
i+1
P(ȳ |ui−1
0 ,1,uN−1
i+1 )
(7)
=
P
uN−1
i+1
P(ȳ′
|(ui−1
0 ,0,uN−1
i+1 ) ⊕ (ȳ ⊕ ȳ′
)H−1
n )
P
uN−1
i+1
P(ȳ′ |(ui−1
0 ,1,uN−1
i+1 ) ⊕ (ȳ ⊕ ȳ′)H−1
n )
=
P
uN−1
i+1
P(ȳ′
|(u′i−1
0 ,0 ⊕ ((ȳ ⊕ ȳ′
)H−1
n )i,uN−1
i+1 )
P
uN−1
i+1
P(ȳ′ |(u′i−1
0 ,1 ⊕ ((ȳ ⊕ ȳ′)H−1
n )i,uN−1
i+1 )
=
W(i)
(ȳ′
,u′i−1
0 |0 ⊕ ((ȳ ⊕ ȳ′
)H−1
n )i)
W(i)(ȳ′,u′i−1
0 |1 ⊕ ((ȳ ⊕ ȳ′)H−1
n )i)
.
The claim follows by considering the two possible values of
((ȳ ⊕ ȳ′
)H−1
n )i.
Recall that the decision process involves randomized rounding
on the basis of li. Consider at first two tuples (ȳ,ui−1
0 ) and
(ȳ′
,u′i−1
0 ) so that their associated li values are equal; we have
seen in the previous lemma that many such tuples exist. In
this case, if both tuples have access to the same source of
randomness, we can couple the two instances so that they
make the same decision on Ui. An equivalent statement is
true in the case when the two tuples have the same reliability
|log(li(ȳ,ui−1
0 ))| but different signs. In this case there is a
simple coupling that ensures that if for the first tuple the
decision is lets say Ui = 0 then for the second tuple it is
Ui = 1 and vice versa. Hence, if in the sequel we compare
two instances of “compatible” tuples which have access to
the same source of randomness, then we assume exactly this
coupling.
Lemma 7 (Symmetry and Distortion): Consider the Stan-
dard model introduced in the previous section. Let ȳ,ȳ′
∈
{0,1}N
, F ⊆ {0,...,N − 1}, and ũF ,ũ′
F ∈ {0,1}|F|
. If
ũF = ũ′
F ⊕((ȳ⊕ȳ′
)H−1
n )F , then under the coupling through
a common source of randomness fũF
(ȳ) = fũ′
F (ȳ′
) ⊕ ((ȳ ⊕
ȳ′
)H−1
n )Fc .
Proof: Let ū,ū′
be the two N dimensional vectors
generated within the Standard Model. We use induction. Fix
0 ≤ i ≤ N − 1. We assume that for j < i, uj = u′
j ⊕ ((ȳ ⊕
ȳ′
)H−1
n )j. This is in particular correct if i = 0, which serves
as our anchor.
By Lemma 6 we conclude that under our coupling the
respective decisions are related as ui = u′
i ⊕ ((ȳ ⊕ ȳ′
)H−1
n )i
if i ∈ Fc
. On the other hand, if i ∈ F, then the claim is true
by assumption.
Let v̄ ∈ {0,1}|F|
and let A(v̄) ⊂ {0,1}N
denote the coset
A(v̄) = {ȳ : (ȳH−1
n )F = v̄}. 8
The set of source words {0,1}N
can be partitioned as
{0,1}N
= ∪v̄∈{0,1}|F|A(v̄).
Note that all the cosets A(v̄) have equal size.
The main result of this section is the following lemma. The
lemma implies that the distortion of SM(F,ũF ) is independent
of ũF .
Lemma 8 (Independence of Average Distortion w.r.t. ũF ):
Fix F ⊆ {0,...,N − 1}. The average distortion DN(F,ũF )
of the model SM(F,ũF ) is independent of the choice of
ũF ∈ {0,1}|F|
.
Proof: Let ũF ,ũ′
F ∈ {0,1}|F|
be two fixed vectors. We
will now show that DN(F,ũF ) = DN(F,ũ′
F ). Let ȳ,ȳ′
be
two source words such that ȳ ∈ A(v̄) and ȳ′
∈ A(v̄⊕ũF ⊕ũ′
F ),
i.e., ũ′
F = ũF ⊕ ((ȳ ⊕ ȳ′
)H−1
n )F . Lemma 7 implies that
fũ′
F (ȳ′
) = fũF
(ȳ) ⊕ ((ȳ ⊕ ȳ′
)H−1
n )Fc.
This implies that the reconstruction words are related as
ˆ fũF
(fũF
(ȳ)) = ˆ fũ′
F (fũ′
F (ȳ′
)) ⊕ (ȳ ⊕ ȳ′
)H−1
n .
Note that ˆ fũF
(fũF
(ȳ))⊕ȳ is the quantization error. Therefore
d(ȳ, ˆ fũF
(fũF
(ȳ))) = d(ȳ′
, ˆ fũF
(fũ′
F (ȳ′
))),
which further implies
X
ȳ∈A(v̄)
d(ȳ, ˆ fũF
(fũF
(ȳ))) =
X
ȳ∈A(v̄⊕ũF ⊕ũ′
F )
d(ȳ, ˆ fũ′
F (fũ′
F (ȳ))).
Hence, the average distortions satisfy
X
ȳ
1
2N
d(ȳ, ˆ fũF
(fũF
(ȳ)))
=
X
v̄∈{0,1}|F|
1
2N
X
ȳ∈A(v̄)
d(ȳ, ˆ fũF
(fũF
(ȳ)))
=
X
v̄∈{0,1}|F|
1
2N
X
ȳ∈A(v̄⊕ũF ⊕ũ′
F )
d(ȳ, ˆ fũ′
F (fũ′
F (ȳ)))
=
X
v̄∈{0,1}|F|
1
2N
X
ȳ∈A(v̄)
d(ȳ, ˆ fũ′
F (fũ′
F (ȳ)))
=
X
ȳ
1
2N
d(ȳ, ˆ fũ′
F (fũ′
F (ȳ))).
As mentioned before, the functions fũF
and fũ′
F are not
deterministic and the above equality is valid under the assump-
tion of coupling with a common source of randomness. Av-
eraging over this common randomness, we get DN(F,ũF ) =
DN(F,ũ′
F ).
Let QũF
denote the empirical distribution of the quantiza-
tion noise, i.e.,
QũF
(x̄) = E[1{Ȳ ⊕ ˆ fũF (fũF (Ȳ ))=x̄}],
where the expectation is over the randomness involved in
the source and randomized rounding. Continuing with the
reasoning of the previous lemma, we can indeed show that
the distribution QũF
is independent of ũF . Combining this
with Lemma 2, we can bound the distance between QũF
and
an i.i.d. Ber(D) noise. This will be useful in settings which
involve both channel and source coding, like the Wyner-Ziv
problem, where it is necessary to show that the quantization
noise is close to a Bernoulli random variable.
Lemma 9 (Distribution of the Quantization Error): Let the
frozen set F be
F = {i : Z(i)
≥ 1 − 2δ2
N}.
Then for ũF fixed,
X
x̄
|QũF
(x̄) −
Y
i
W(xi |0)| ≤ 2|F|δN.
Proof: Recall that PX̄ |Ȳ (x̄|ȳ) =
Q
i W(xi |yi). Let
v̄ ∈ {0,1}|F|
be a fixed vector. Consider a vector ȳ ∈ A(v̄)
and set ȳ′
= 0̄. Lemma 7 implies that fũF
(ȳ) = fũF ⊕v̄
(0̄) ⊕
(ȳH−1
n )Fc. Therefore,
ȳ ⊕ ˆ fũF
(fũF
(ȳ)) = 0̄ ⊕ ˆ fũF ⊕v̄
(fũF ⊕v̄
(0̄)).
This implies that all vectors belonging to A(v̄) have the same
quantization error and this error is equal to the error incurred
by the all-zero word when the frozen bits are set to ũF ⊕ v̄.
Moreover, the uniform distribution of the source induces a
uniform distribution on the sets A(v̄) where v̄ ∈ {0,1}|F|
.
Therefore, the distribution of the quantization error QũF
is
the same as first picking the coset uniformly at random, i.e.,
the bits ũF , and then generating the error x̄ according to x̄ =
ˆ fũF
(fũF
(0̄)). The distribution of the vector ū where ū =
x̄H−1
n is indeed the distribution Q defined in (9). Recall that in
the distribution PŪ,X̄,Ȳ , Ū and X̄ are related as Ū = X̄H−1
n .
Therefore, the distribution induced by W(x̄|ȳ) on Ū is PŪ |Ȳ .
Since multiplication with H−1
n is a one-to-one mapping, the
total variation distance can be bounded as
X
x̄
|QũF
(x̄) −
Y
i
W(x̄|0̄)| =
X
# renes_duality.txt
URL https://arxiv.org/pdf/1701.05583
Raw textsha256 ba237d67af276959a43d8422a3442915a77e731f6d7531054dd07e5ec02b705b


## Physical LF365-387
states, or PZ |Y “ y is concentrated on only one value of Z, and the output is the same for all inputs. In the former
case, the input is completely recoverable from the output in C, while for the latter recovery better than blind
guessing is completely impossible. Thus the only classical channels which have classical duals are erasure-like
channels in which the output y in D indicates whether the input is perfectly recoverable from C or has been
essentially erased.
    For binary-input channels, since the quantum outputs Z x |η y y are pure states, they are completely char-
acterized by their overlap cos ϑ y “ |xη y | Z |η y y|{xη y |η y y. Working this out explicitly, one finds

                                               cos ϑ y “ | PZ |Y “ y p0q ´ PZ |Y “ y p1q| ,                                         (23)


                                                                           5
 which is just the | D|-density of the original binary-input classical channel [22, Eq. 4.12]. The duals of binary
symmetric and erasure channels are computed in [4], and the results can be immediately understood using
(23). The BEC is its own dual, in the sense that BECp pqK “ BECp1´ pq. This can be seen because the overlaps
are either zero ( y “?) or one ( y “ 0, 1), corresponding to quantum outputs ?12 p|0y ` p´1q x |1yq or |0y
respectively. Thus, the value of x is perfectly recoverable when y “? but not at all when y “?0, 1. The dual of
                                                                                     ?
the BSC, meanwhile, has pure state outputs (up to equivalence), taking x to p|0y ` p´1q x 1 ´ p|1y. Again
using (23), it is clear that the overlap |1 ´ 2p| is the same for both values of y, so we can dispense with this
part of the output of the dual. Comparing to the form of (22), the fact that that any symmetric binary-input
classical channel can be thought of as a heralded mixture of BSCs (see, e.g. [23]) is reflected in the fact that
its dual is a heralded mixture of BSCs.

## Physical LF435-527
polar codes. Essentially the same notion also appears in belief propagation decoding of general binary linear
codes, as the update rules for messages at check and variable nodes [22]. The check pfq and variable pfq
convolutions are defined by

                             rW f W 1 spz q :“ W pz q b W 1 pz q,                                                 (25)
                             rW f W spz q :“ 12 W pz q b W 1 p0q ` 21 W pz ` 1q b W 1 p1q.
                                      1
                                                                                                                  (26)


                                                            6
 In the context of polar coding, the check convolution is precisely the “worse” channel synthesized from W
and W 1 , call it W a W 1 , while for symmetric W and W 1 , the variable convolution is equivalent to the “better”
synthesized channel W ‘ W 1 . Formally,
                                                  W a W1 “ W f W1                  and                             (27)
                                                  W ‘ W1 » W f W1 .                                                (28)
To see the latter, first observe that the better channel has outputs
                   rW ‘ W 1 qspz q “ 12 |0yx0| b W pz q b W 1 pz q ` 12 |1yx1| b W pz ` 1q b W 1 pz q .            (29)
                                                                                                          ˚
Symmetry of W amounts to the existence of a unitary operator U such that W pz ` 1q “ UW pz qU for z “ 0, 1.
Therefore,      applying U if the first system is in the state |1y and doing nothing otherwise results in the state
1ř        1     1
2  z 1 |z   yxz   | b W pz q b W 1 pz q for input z. Since the first system is independent of the second two, we have
W ‘ W » W f W 1 for symmetric W , as intended.
          1

   The compatibility of convolution with the dual is the following theorem.
Theorem 1. For any two binary-input CQ channels W and W 1 ,
                                          pW f W 1 qK » W K f W 1K                   and                           (30)
                                                          1 K    K        1K
                                          pW f W q » W f W                     .                                   (31)

Proof. Let ϕz and ϕz1 be the outputs of W and W 1 , and similarly θ x and θ x1 the outputs of W K and W 1K ,
respectively. Now consider the states |ψy and |ψ1 y from (19) associated with W and W 1 , and denote the
respective systems involved by ABC D and A1 B 1 C 1 D1 . Applying a CNOT operation from A1 to A yields
                                                          1
                                |ηy “ UACNOT
                                         1 ÑA |ψyABC D |ψ yA1 B 1 C 1 D 1                                          (32)
                                    “ 21 |z ` z 1 yA|z 1 yA1 |z yC |z 1 yC 1 |ϕz yBD |ϕz1 1 yB1 D1 .
                                        ÿ
                                                                                                                   (33)
                                          z,z 1

In the conjugate basis the CNOT gate has the same action as in the standard basis, but with control and target
reversed. Therefore we may write

                                |ηy “ 12    | x yA| x ` x 1 yA1 |θ x yBC D |θ x1 1 yB1 C 1 D1 ,
                                         ÿ
                                                                                                          (34)
                                                  x,x 1

where we have abused notation by omitting tildes on the A and A1 basis states to denote use of the conjugate
basis.
    The outputs of W f W 1 can be generated from this state by measuring system A1 in the |z y basis, discarding
the C and D systems, and making use of channel symmetry. In the binary-input setting, symmetry amounts to
the existence of a unitary operator U such that W pz ` 1q “ UW pz qU ˚ for z “ 0, 1. Applying U to B conditional
on the value of z ` z 1 in A therefore gives the state

                               |η1 y “ 21 |z ` z 1 yA|z 1 yA1 |z yC |z 1 yC 1 |ϕz 1 yBD |ϕz1 1 yB1 D1 .
                                         ÿ
                                                                                                            (35)
                                          z,z 1

Measuring A1 and discarding C D gives output states 12 z |z yxz |A b pϕz 1 qB b pϕz1 1 qB1 for measurement result
                                                                    ř
z 1 . Since the A part of the state is independent of the rest, the outputs are equivalent to rW f W 1 spz 1 q. By
Proposition 1, the outputs of the dual can therefore be obtained by measuring system A1 of |η1 y in the Fourier-
conjugate basis and discarding systems ABB 1 . But since |η1 y differs from |ηy only by a unitary action on AB,
which will anyway be discarded, the outputs of the dual can just as well be obtained from |ηy. Using (34),
these are easily seen to be just rW K f W 1K sp x q.
      For the second statement, return to (33) and note that measuring A in the |z y basis and discarding
A1 C C 1 DD1 gives the states rW f W 1 spz q. Thus, the outputs of pW f W 1 qK can be generated by measuring
A in the |rx y basis and discarding BB 1 , for which it is convenient to use (34). Again using channel symmetry to
shift the index x 1 to x in |θ x1 1 yB1 C 1 D1 , the outputs are easily seen to be equivalent to those of pW K f W 1K q.

     In the context of polar coding over memoryless channels, one considers repeated convolution of a channel
with itself, with a random choice of which convolution to use at each step. Theorem 1 immediately gives a
duality relation, a weaker version of which was recently used by the author and collaborators to study the
capability of polar codes constructed for a given channel to be used for another [4]. Suppose y n P t0, 1un for
integer n ą 0 and let ȳ n “ 1n ` y n (understood modulo 2), where 1n is the length-n string of 1s. Then define
W y n recursively as W y n´1 f W y n´1 if bn “ 0 and W y n´1 f W y n´1 if bn “ 1. Repeatedly applying Theorem 1 gives
the following:


                                                                 7
 Corollary 2. For any symmetric CQ channel W , pW y n qK » pW K q ȳ n .

This is an improvement over [4], which showed that pW K q ȳ n is a degraded version of pW y n qK .

3.5     Entropic relations between a channel and its dual
Entropic uncertainty relations constrain the behavior of a channel by that of its dual. In fact, due to the use
of conjugate bases and the form the dual, the entropic uncertainty relations hold with equality, not just as
inequalities, as is generally the case. Thus, the behavior of a channel is in fact completely characterized by

## Physical LF533-566
Theorem 2. For any CQ channel W with input Z and any conditional entropy H,

                                              HpW q ` HK pW K q “ log | Z | .                                     (36)

    The proof is based entirely on the following uncertainty equality for the kinds of tripartite states that
are found in the state-based definition of the dual channel. Indeed, using (19), both entropy terms can be
computed from the state |ψyABC D : HpW q “ Hp ZA|B qψ while HK pW K q “ HpX A|C Dqψ . Invoking the following
lemma with E “ B and F “ C D gives (36). Its proof is given in Appendix A.

Lemma 1. For any tripartite pure state |ψyAE F in which the unnormalized conditional states pσz q F :“ TrAE r|z yxz |AψAE F s
are pairwise disjoint, i.e. σz σz 1 “ 0 for z ‰ z 1 , we have

                                          Hp ZA| E qψ ` HK pX A| F qψ “ log |A| ,                                 (37)

for H any entropy defined as in (1), (2), (13), or (14).

    Theorem 2 has several important implications. First, from duality of min- and max-entropy, the guessing
probability of the channel is directly related to the decoupling of the dual channel. For W taking Z to B, let
P pW q “ P p Z |W p Z qq and QpW q “ Qp Z |W p Z qq, with Z uniformly distributed. Then, taking H to be Hmin and
Hmax , respectively, leads to

Corollary 3. For any CQ channel W ,

                                                  P pW q “ QpW K q and                                            (38)
                                                                   K
                                                  QpW q “ P pW q .                                                (39)

    Second, from self-duality of the von Neumann entropy, the capacity of the channel is determined by
the capacity of the dual, and vice versa. For I pW q :“ max PZ pH p Z q ´ H p Z |W p Z qqq, since the optimal input
distribution for symmetric channels is the uniform distribution, we have

Corollary 4. For any symmetric CQ channel W with input Z,

                                                I pW q ` I pW K q “ log | Z | .                                   (40)
# local_decoder.txt
URL https://arxiv.org/pdf/2611.12718
Raw textsha256 faeacf2b999347c395719fb286820a783fdebc91629206b621d5dfe715a134be


## Physical LF428-466
solving 𝐵𝑧 = 𝑥 + 𝑥 0 .
     DQI prepares |Φ⟩ together with a uniform superposition of the codewords of 𝐶 = 𝐾 ⊥ , and applies the
phases (−1)𝑐 · (𝑥 −𝑥 0 ) . For each codeword 𝑐, the state in the received register is, up to a global phase,

                                           |𝜓𝑐Φ ⟩ =
                                                    ∑︁
                                                         Φ(𝑥) (−1)𝑐 ·𝑥 |𝑥⟩ .
                                              𝑥 ∈Z𝑚
                                                  2


The codeword register is then uncomputed by recovering its label from this state. Thus the decoder must
distinguish the states |𝜓𝑐Φ ⟩ when 𝑐 is uniformly distributed on 𝐶. We write 1 − 𝜀 for its block success, the
probability of recovering the whole codeword.
    For the product amplitude function Φ𝛽 , the received state is a product over the symbols. Each bit 𝑦 is
transmitted through the pure-state channel
                             √                  √                                 1
                        𝑦 ↦−→ 1 − 𝛼 |0⟩ + (−1) 𝑦 𝛼 |1⟩ ,        𝛼 = 𝑝 𝛽 (1) =          .
                                                                                1 + 𝑒𝛽
Measuring the √︁
              qubits individually in the Fourier basis instead produces independent bit flips with proba-
        ⊥  1
bility 𝛼 = 2 − 𝛼 (1 − 𝛼), which is also the error rate of the decoding problem. Quantum decoding retains
the pure channel outputs rather than first converting them into these classical outcomes.




                                                      9
 From decoding to the objective. Decoding success controls the distribution of the samples produced
by DQI and their expected objective value. If Φ has positive mass on every coset of 𝐾, the output distribu-
               √
tion is within 𝜀 in expected total variation of the target distribution, averaged over a uniformly random
offset. For every amplitude function and every objective with values in [0, 1], its expectation under the
                                         √
output distribution differs by at most 2 𝜀 from its expectation under |Φ(𝑥)| 2 on all of Z𝑚2 . Shutty et al.
proved these guarantees over finite fields [SMR+ 26], and Theorem 3.3 gives the form we use over Z𝑞 . The
latter guarantee allows us to study the expected cost in |Φ⟩ without analyzing its separately normalized
projection onto each coset.

## Physical LF3880-3965
    For 𝑥𝑋 ∈ 𝑋 , the overlap ⟨𝜙𝑋 |𝜓𝑐 ⟩ = 𝜔 𝑐 ·𝑥𝑋 𝑍𝑋 gives Ψ −1/2 |𝜓𝑐 ⟩ = 𝑋 𝜔 𝑐 ·𝑥𝑋 |𝜙ˆ𝑋 ⟩, with the inverse taken
                                                                        Í
on S. The normalized PGM vectors |𝑏𝑐 ⟩ = |𝐶 | −1/2 Ψ −1/2 |𝜓𝑐 ⟩ are therefore
                                                  1 ∑︁ 𝑐 ·𝑥𝑋 ˆ
                                        |𝑏𝑐 ⟩ = √︁        𝜔 |𝜙 𝑋 ⟩ ,              𝑐 ∈ 𝐶.                    (26)
                                                   |𝐶 | 𝑋

The phases do not depend on the representatives because 𝑐 ∈ 𝐾 ⊥ , and character orthogonality shows that
the |𝑏𝑐 ⟩ form an orthonormal basis of S. Hence the PGM effects restricted to S are the projectors |𝑏𝑐 ⟩⟨𝑏𝑐 |;
their completion outside S will not matter. Since 𝑊Φ𝛽 (𝑋 ) = 𝑍𝑋 , Lemma 7.2 shows that the block success

                                                              69
                                                    Í √  2
of the PGM is 𝑃 PGM (𝐵, 𝛽) := 𝑃PGM (Φ𝛽 ) = |𝐶 | −1 𝑋 𝑍𝑋 , which is the quantity (27) in Proposition 7.3
below.
    The coherent constructions below require only positive mass on every coset. They therefore also hold
for any amplitude function Φ with 𝑊Φ (𝑋 ) > 0 for every 𝑋 , with normalized target states in place of Gibbs
states and with efficient preparation of |Φ⟩ assumed in the complexity statements.
    A coherent implementation can map each |𝜙ˆ𝑋 ⟩ to its coset label and apply a Fourier transform over
the labels. Reversing this change of basis prepares a specified Gibbs state from a Fourier superposition of
codeword labels. Proposition 7.3 applies more generally to any exact coherent PGM circuit that retains
all work registers and has an available inverse. Regev’s reduction compares the decoded and original
codeword labels without measuring either one. On the successful branch, applying the inverse circuit
prepares the Gibbs state of the specified offset. The success probability is 𝑃 PGM , independently of the
offset.
    This construction has been analyzed for the zero offset [CT24, Section 6.3 of the full version] and for
arbitrary offsets over finite fields [BCT26, Section 4.4, Algorithm 4.4]. Related reductions solve bounded-
distance instances on the dual code from an exact quantum decoder [FGC26, Proposition 3], or from a
coherent PGM and its inverse with an amplitude function chosen for the instance and a constant expected
number of repetitions [FGC26, Theorem 7]. Here the amplitude function is fixed, its coset states are the
primal Gibbs states, and the construction is stated over Z𝑞 for every 𝑞.
    Conversely, coherent preparation of all |𝜙ˆ𝑋 ⟩ and its inverse implement the PGM by the change of
basis (26) (Proposition 7.4), as in [PR25, CH26]. The two tasks are equivalent up to polynomial overhead
whenever 𝑃 PGM is at least inverse polynomial (Corollary 7.5).
Proposition 7.3 (Gibbs preparation from a coherent PGM). Suppose that a unitary 𝑈 implements the PGM
coherently: for every unit vector |𝑣⟩ ∈ S, applying 𝑈 to |𝑣⟩ |0⟩ and measuring an outcome register 𝑂 yields
𝑐 ∈ 𝐶 with probability |⟨𝑏𝑐 |𝑣⟩| 2 . The ancillary input |0⟩ includes all work registers and the outcome register,
and all output registers are retained. Given access to 𝑈 and 𝑈 † , for every offset 𝑥 0 ∈ Z𝑚𝑞 there is a heralded
                                                  ˆ
procedure whose successful output is exactly |𝜙𝑥 0 +𝐾 ⟩, with all auxiliary registers returned to zero. Its success
probability is
                                                                    !2
                                                       1 ∑︁ √︁
                                             𝑃 PGM :=            𝑍𝑋 ,                                          (27)
                                                      |𝐶 | 𝑋
which is also the block success of the PGM on the uniform codeword ensemble. Each attempt uses at most
one application of 𝑈 and one of 𝑈 † , together with polynomial overhead for preparing the DQI input and
comparing and subtracting codeword labels, assuming efficient preparation of the single-symbol factors. For
fixed 𝑞, an efficient implementation of 𝑈 with 𝑃PGM ≥ 1/poly(𝑚+𝑛) therefore yields polynomial expected-time
preparation of the Gibbs state.
     The proof of Proposition 7.3 is given in Appendix C.
     To state the converse, we label the cosets of 𝐾 and the codewords by coordinates in which the pairing
(𝑐, 𝑥) ↦→ 𝜔 𝑐 ·𝑥 is explicit. The group 𝐶 need not be isomorphic to Zℎ𝑞 for any ℎ, so we use its invariant
factors, which the Smith normal form computes. Let 𝑈 𝐵 ⊤𝑉 = 𝑆 be the Smith normal form of 𝐵 ⊤ over the
integers, with 𝑈 ∈ 𝐺𝐿𝑛 (Z), 𝑉 ∈ 𝐺𝐿𝑚 (Z), and 𝑆 the 𝑛 × 𝑚 matrix with diagonal entries 𝑒 1, . . . , 𝑒𝑛 ≥ 0 and
zeros elsewhere, and set 𝑒 𝑗 = 0 for 𝑛 < 𝑗 ≤ 𝑚. For 𝑐 ∈ Z𝑚                          −1               ⊤
                                                                    𝑞 and 𝑢 = 𝑉 𝑐, we have 𝐵 𝑐 = 0 in Z𝑞 if
                                                                                                                   𝑛

and only if 𝑒 𝑗 𝑢 𝑗 = 0 in Z𝑞 for every 𝑗, that is, if and only if 𝑢 𝑗 is a multiple of 𝑞/𝑔 𝑗 , where 𝑔 𝑗 = gcd(𝑒 𝑗 , 𝑞)
                                                                                                 Î
and gcd(0, 𝑞) = 𝑞. Hence the map 𝑦 ↦→ 𝑐 (𝑦) = 𝑉 (𝑞/𝑔 𝑗 ) 𝑦 𝑗 𝑗 is an isomorphism from 𝑗 Z𝑔 𝑗 onto 𝐶. For
𝑥 ∈ Z𝑚
                      Î                                      ⊤
      𝑞 , let 𝜏 (𝑥) ∈    𝑗 Z𝑔 𝑗 have coordinates 𝜏 𝑗 (𝑥) = (𝑉 𝑥) 𝑗 mod 𝑔 𝑗 . Then
                                                              ∑︁ 𝑦 𝑗 𝜏 𝑗 (𝑥)  
                                         𝜔 𝑐 (𝑦) ·𝑥 = exp 2𝜋𝑖                  ,                                   (28)
                                                               𝑗
                                                                     𝑔𝑗

                                                           70
 so 𝜏 (𝑥) = 0 exactly when 𝑥 is orthogonal to 𝐶, that is, when 𝑥 ∈ 𝐶 ⊥ = 𝐾. The map 𝜏 is onto, because
                            Î
  𝑞 /𝐾
|Z𝑚
     Î                                                                                 𝑞 : 𝜏 (𝑥) = 𝜏 } with
       | = 𝑞𝑚 /|𝐾 | = |𝐶 | = 𝑗 𝑔 𝑗 . The cosets of 𝐾 are therefore the sets 𝑋𝜏 = {𝑥 ∈ Z𝑚
𝜏 ∈ 𝑗 Z𝑔 𝑗 . Factors with 𝑔 𝑗 = 1 can be omitted. For fixed 𝑞, the Smith normal form, the maps 𝑦 ↦→ 𝑐 (𝑦)
and 𝑥 ↦→ 𝜏 (𝑥), and the inverse of 𝑦 ↦→ 𝑐 (𝑦) on 𝐶 can be computed in polynomial time.

Proposition 7.4 (Coherent PGM from coherent Gibbs states). Suppose that a unitary 𝑉 satisfies 𝑉 |𝜏⟩ |0⟩ =
|𝜏⟩ |𝜙ˆ𝑋𝜏 ⟩ for every 𝜏 ∈ 𝑗 Z𝑔 𝑗 , where the second register consists of 𝑚 qudits, and that 𝑉 † is available. Then the
                          Î
reversible computation of the coset label 𝜏 (𝑥), one application of 𝑉 † , the inverse quantum Fourier transform
       Î
over 𝑗 Z𝑔 𝑗 , and the reversible computation of 𝑐 (𝑦) from 𝑦, applied in this order, form a unitary 𝑈 with