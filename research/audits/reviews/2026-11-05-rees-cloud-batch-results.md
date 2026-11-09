# Cloud batch A-G (5 Nov 2026): results collected 21:55-22:30 AEDT

AI-only. Read from claude.ai/code session transcripts; nothing was committed from the cloud.
Every cloud run used the same dfs2b.c (source md5 244a31ed79c5cb95b294a35c75cc0137, test
vectors matched). The cross-check against the local verdicts found 0 conflicts.

## dfs2b screens

| session | scope | outcome |
|---|---|---|
| A (session_01B1JoChvkoXMWE83AhewpBp) | 7 kappa=8 primes 18617-19961; kappa=9 >= 18397 | all 7 kappa=8 FEASIBLE (also decided locally, same verdict); kappa=9 19819, 19531 FEASIBLE (also local); 4 long kappa=9 jobs (19963, 19927, 19891, 19801) lost to a container restart at 07:50 UTC; rest not started |
| B (session_01B1JoCgWF8vyi5ChruKtrvM) | kappa=9 16741-17497 | 13 of 17 decided: 17011 FEASIBLE; INFEASIBLE 16921, 16993, 17029, 17047, 17137, 17191, 17209, 17299, **17317, 17389, 17443, 17497** (bold = not yet decided locally); node counts for 17191/17209/17299 equal the local runs exactly; 16741, 16759, 16831, 16903 were still running at the last report |
| C (session_01B1JoCkCXskkZs8rsQ2nyir) | kappa=9 exceptions 21313-24373 | none decided; 21313, 21493, 21529, 21601 at ~8 CPU-h and ~976M nodes each, estimated days |
| F (session_01B1JoCjDFWZeezQEzETgejU) | kappa=9 exceptions 24391-27271 | none decided; 24391, 24481, 24499, 24517 at 4 h with no output |

New lines from B (verbatim):

```
INFEASIBLE k=9 p=17317 nodes=337544696 secs=9086.823
INFEASIBLE k=9 p=17389 nodes=348949673 secs=9523.448
INFEASIBLE k=9 p=17443 nodes=347300053 secs=9428.797
INFEASIBLE k=9 p=17497 nodes=349992327 secs=9610.724
```

These four are cloud-only until the local screen dfs2b_9_14501 (range to 17500) reaches them.

## Plain-mode cross-checks (independent of the symmetry pruning)

- D (session_01B1JoCiAN6VYKzwrGGNWsLK), kappa=8 members <= 10753: 166 of 213 confirmed
  INFEASIBLE in plain mode, contiguous through p = 7577; no FEASIBLE/BUG/LIMIT line.
- E (session_01B1JoChGL1AHNHBYm96WJF2), kappa=9 members <= 14149: 174 of 211 confirmed
  INFEASIBLE in plain mode, contiguous through p = 11593; no FEASIBLE/BUG/LIMIT line.
  (Before: 51 kappa=8 and 42 kappa=9 members cross-checked, largest ~6070.)

## Exact state after merging local + cloud (22:30 AEDT)

- E_2(8) on [3, 20000]: all 556 primes p = 1 (mod 8) decided; 293 members, largest 14281;
  276 FEASIBLE witnesses above 13873 re-verified by independent Python code (0 bad).
- E_2(9) on [3, 20000]: 358 of 372 decided; 328 members, largest 18793; open: 18919, 18973,
  19009, 19081, 19207, 19333, 19387, 19423, 19441, 19477, 19603, 19801, 19891, 19963.
- kappa=9 exception list above 20000: 16 of 1373 decided; 15 members (20071-20809),
  one non-member (304687).

## G: native-application literature search (session_01B1JoCjKN7ufUCvmhd9g8Jm)

Verdict: no independently motivated problem in the residual regime (3 <= c < p, p growing,
non-normal H, not already solved) was found; 19 candidates tabled, all killed except
constructed ones. The shortlist for a human expert:
1. The Imran-Ivanyos open problem (QIP 2024, section 6), which is a motivation, not an
   application. The black-box to explicit-chart step must be paid for.
2. S1 in its narrow residual: circuit input, high p-weight, D and p growing. No natural F
   is known.
3. C9, a triangular-tower symmetry: class 3 at p = 5, no abelian maximal subgroup, but it
   is constructed. It still needs a GAP recheck at p = 7 and 11.
4. Learning qudit phase states. This probably reduces to IS15 Cor 8, and the access is to
   states only.

Priority facts it confirmed (the paper already states 1-3):
1. ISS 2012 Thm 2 reduces arbitrary H to the case of exponent p with |H| <= p.
2. Bacon-Childs-van Dam, IS15 Cor 8 and Morales Thm C cover subfamilies.
3. Imran-Ivanyos list the general case as open.
4. No later paper claiming the general case was found through October 2026.

Citation items still to check against the paper:
- BoucherFouqueShen2026: the result is "Theorem 3 in section 4.3", not "Theorem 4.3".
- MicciancioPeikert2013: binary-error LWE is Thm 1.2, not Thm 1.1.
- FIMSS: the polynomial result is Thm 4.16 (arXiv v4) / Cor 4 (STOC).
- Khukhro: Lazard correspondence Thm 10.13, BCH Lemma 9.15.
- AKS Thm 5.3: has an ineffective constant.
- IS15 Cor 8: stated only for order-p H not contained in F_p^m. This bears on the
  outreach wording.
- HoltSubramanian2026 title case.
- Di Concilio-Flores-Kahrobaei-Noce survey (ePrint 2026/2678): not read (HTTP 403).

G ran without Sage/GAP, so its small group computations should be redone in GAP.
