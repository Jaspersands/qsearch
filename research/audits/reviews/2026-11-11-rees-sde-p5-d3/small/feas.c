/* Feasibility of label sets L in F_5^3 \ 0 (p = 5, S = {0,+-1}, d = 3) by the decision criterion
 * of the parent note: L feasible <=> some g != 0 has <g,l> in S on L, or
 * Sigma_L = {Hy : y in S^L} (H: relation matrix) contains a 3-dim linear subspace.
 * Exhaustive 3-space search (see small-set section of the note for the argument):
 *   star = {s != 0 : F_5 s in Sigma}; P = projective star points (first nonzero digit 1);
 *   for s1 in P (in order; s1 is removed after its turn): T = one alive representative per line
 *   through s1 lying in star; for s2 < s3 in T test the 20 points s3 + b s2 + a s1 (b != 0).
 * On success it prints an explicit model: Phi(l) = (y1(l), y2(l), y3(l)) with H y_j = s_j and,
 * for each alpha among the 62 class reps (first nonzero coordinate 1 or 2), the smallest gamma_alpha
 * with <alpha,Phi(l)> + <gamma_alpha,l> in S on L; gamma_{-alpha} := -gamma_alpha.
 * With an S-functional g it prints Phi = 0, gamma_alpha = g for every alpha.
 * Input: one label set per line, labels as digit triples.  Output, one line per input:
 *   SF <L> | <g>            or   M <L> | <Phi(l) ...> | <gamma_alpha for the 62 reps> | stats
 *   INF <L> | stats
 * The output is NOT trusted: check_models.py re-checks every SF/M line from the original definition.
 * Build: clang -O2 -o feas feas.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;
static int n, r, L[16][3];
static u64 col[16][5];            /* packed H-column of label l times c */
static int64_t *pre;              /* idx -> y code (base 3), -1 if not in Sigma */
static unsigned char *star, *alive;
static int nidx;                  /* 5^r */
static int bt[8][256];            /* packed byte -> partial index */
static int pw5[12];
static inline u64 add5(u64 x, u64 y) { u64 t = x + y; u64 m = ((t + 0x3333333333333333ULL) & 0x8888888888888888ULL) >> 3; return t - m * 5; }
static inline u64 mul5(u64 x, int c) { u64 s = 0; for (int i = 0; i < c; i++) s = add5(s, x); return s; }
static inline int idxof(u64 x) { int s = 0; for (int j = 0; j * 2 < r; j++) s += bt[j][(x >> (8 * j)) & 255]; return s; }
static u64 packof(int idx) { u64 x = 0; for (int i = 0; i < r; i++) { x |= (u64)(idx % 5) << (4 * i); idx /= 5; } return x; }
static u64 normp(u64 x) { for (int i = 0; i < r; i++) { int d = (x >> (4 * i)) & 15; if (d) { int inv = d == 1 ? 1 : d == 2 ? 3 : d == 3 ? 2 : 4; return mul5(x, inv); } } return 0; }
static const int Sv[3] = {0, 1, 4};
static int inS(int v) { v = ((v % 5) + 5) % 5; return v == 0 || v == 1 || v == 4; }
static void dfs(int k, u64 acc, int64_t code, int64_t mul) {
  if (k == n) { int i = idxof(acc); if (pre[i] < 0) pre[i] = code; return; }
  for (int t = 0; t < 3; t++) dfs(k + 1, add5(acc, col[k][Sv[t]]), code + t * mul, mul * 3);
}
int main(void) {
  for (int j = 0; j < 8; j++) for (int b = 0; b < 256; b++) { int lo = b & 15, hi = b >> 4; bt[j][b] = (lo < 5 && hi < 5) ? (lo + 5 * hi) : 0; for (int q = 0; q < j; q++) bt[j][b] *= 25; }
  pw5[0] = 1; for (int i = 1; i < 12; i++) pw5[i] = pw5[i - 1] * 5;
  char line[4096];
  while (fgets(line, sizeof line, stdin)) {
    n = 0; char *s = line;
    while (*s) { if (*s >= '0' && *s <= '4' && s[1] >= '0' && s[1] <= '4' && s[2] >= '0' && s[2] <= '4') {
        L[n][0] = s[0] - '0'; L[n][1] = s[1] - '0'; L[n][2] = s[2] - '0'; n++; s += 3; } else s++; }
    if (n == 0) continue;
    /* S-functional */
    int sf = -1;
    for (int g = 1; g < 125 && sf < 0; g++) { int G[3] = {g / 25, (g / 5) % 5, g % 5}, ok = 1;
      for (int i = 0; i < n && ok; i++) ok = inS(G[0] * L[i][0] + G[1] * L[i][1] + G[2] * L[i][2]); if (ok) sf = g; }
    char Ls[256]; int pos = 0; for (int i = 0; i < n; i++) pos += sprintf(Ls + pos, "%s%d%d%d", i ? " " : "", L[i][0], L[i][1], L[i][2]);
    if (sf >= 0) { printf("SF %s | %d%d%d\n", Ls, sf / 25, (sf / 5) % 5, sf % 5); fflush(stdout); continue; }
    /* pivots */
    int piv[3], np = 0;
    for (int i = 0; i < n && np < 3; i++) {
      int B[3][3]; for (int q = 0; q < np; q++) for (int c = 0; c < 3; c++) B[q][c] = L[piv[q]][c];
      for (int c = 0; c < 3; c++) B[np][c] = L[i][c];
      /* rank test via determinant / cross products */
      int indep;
      if (np == 0) indep = 1;
      else if (np == 1) { int c0 = (B[0][1] * B[1][2] - B[0][2] * B[1][1]) % 5, c1 = (B[0][2] * B[1][0] - B[0][0] * B[1][2]) % 5, c2 = (B[0][0] * B[1][1] - B[0][1] * B[1][0]) % 5; indep = c0 || c1 || c2; }
      else { int det = (B[0][0] * (B[1][1] * B[2][2] - B[1][2] * B[2][1]) - B[0][1] * (B[1][0] * B[2][2] - B[1][2] * B[2][0]) + B[0][2] * (B[1][0] * B[2][1] - B[1][1] * B[2][0])) % 5; indep = det != 0; }
      if (indep) piv[np++] = i;
    }
    if (np < 3) { printf("NOSPAN %s\n", Ls); continue; }
    r = n - 3; nidx = pw5[r];
    /* coordinates of every label in the pivot basis: solve by brute force over F_5^3 */
    int coord[16][3], ispiv[16] = {0}, nonp[16], nn = 0;
    for (int q = 0; q < 3; q++) ispiv[piv[q]] = 1;
    for (int i = 0; i < n; i++) { if (ispiv[i]) continue; nonp[nn++] = i;
      for (int c = 0; c < 125; c++) { int a = c / 25, b = (c / 5) % 5, d = c % 5, ok = 1;
        for (int u = 0; u < 3; u++) ok &= ((a * L[piv[0]][u] + b * L[piv[1]][u] + d * L[piv[2]][u]) % 5 == L[i][u]);
        if (ok) { coord[i][0] = a; coord[i][1] = b; coord[i][2] = d; break; } } }
    for (int i = 0; i < n; i++) { u64 v = 0;
      if (!ispiv[i]) { for (int j = 0; j < nn; j++) if (nonp[j] == i) v = (u64)1 << (4 * j); }
      else { int q = piv[0] == i ? 0 : piv[1] == i ? 1 : 2; for (int j = 0; j < nn; j++) v |= (u64)((5 - coord[nonp[j]][q]) % 5) << (4 * j); }
      for (int c = 0; c < 5; c++) col[i][c] = mul5(v, c); }
    pre = malloc(sizeof(int64_t) * nidx); for (int i = 0; i < nidx; i++) pre[i] = -1;
    dfs(0, 0, 0, 1);
    star = calloc(nidx, 1); alive = calloc(nidx, 1);
    int nsig = 0, nstar = 0; int *P = malloc(sizeof(int) * nidx); int nP = 0;
    for (int i = 1; i < nidx; i++) { if (pre[i] >= 0) nsig++; u64 x = packof(i); if (pre[i] >= 0 && pre[idxof(mul5(x, 2))] >= 0) { star[i] = 1; nstar++; } }
    for (int i = 1; i < nidx; i++) if (star[i]) { u64 x = packof(i); if (normp(x) == x) { P[nP++] = i; alive[i] = 1; } }
    int found = 0, F[3] = {0, 0, 0}; long long tests = 0;
    u64 *T = malloc(sizeof(u64) * nP);
    for (int a1 = 0; a1 < nP && !found; a1++) {
      u64 s1 = packof(P[a1]); u64 s1m[5]; for (int c = 0; c < 5; c++) s1m[c] = mul5(s1, c);
      int nT = 0;
      for (int a2 = 0; a2 < nP; a2++) { if (a2 == a1 || !alive[P[a2]]) continue; u64 s2 = packof(P[a2]); int ok = 1, isrep = 1;
        for (int c = 1; c < 5 && ok; c++) { u64 w = add5(s2, s1m[c]); int wi = idxof(w); if (!star[wi]) ok = 0; else if (idxof(normp(w)) < P[a2]) isrep = 0; }
        if (ok && isrep) T[nT++] = s2; }
      for (int i = 0; i < nT && !found; i++) { u64 w[20]; int m = 0;
        for (int b = 1; b < 5; b++) for (int a = 0; a < 5; a++) w[m++] = add5(mul5(T[i], b), s1m[a]);
        for (int j = i + 1; j < nT; j++) { int ok = 1; tests++;
          for (int q = 0; q < 20 && ok; q++) ok = star[idxof(add5(T[j], w[q]))];
          if (ok) { found = 1; F[0] = P[a1]; F[1] = idxof(T[i]); F[2] = idxof(T[j]); break; } } }
      alive[P[a1]] = 0;
    }
    if (!found) { printf("INF %s | sigma %d star %d proj %d tests %lld\n", Ls, nsig, nstar, nP, tests); }
    else {
      int Phi[16][3];
      for (int j = 0; j < 3; j++) { int64_t c = pre[F[j]]; for (int i = 0; i < n; i++) { Phi[i][j] = Sv[c % 3]; c /= 3; } }
      printf("M %s |", Ls);
      for (int i = 0; i < n; i++) printf(" %d%d%d", Phi[i][0], Phi[i][1], Phi[i][2]);
      printf(" |");
      for (int x = 1; x < 125; x++) { int A[3] = {x / 25, (x / 5) % 5, x % 5}; int f = A[0] ? A[0] : A[1] ? A[1] : A[2]; if (f != 1 && f != 2) continue;
        int got = -1;
        for (int g = 0; g < 125 && got < 0; g++) { int G[3] = {g / 25, (g / 5) % 5, g % 5}, ok = 1;
          for (int i = 0; i < n && ok; i++) ok = inS(A[0] * Phi[i][0] + A[1] * Phi[i][1] + A[2] * Phi[i][2] + G[0] * L[i][0] + G[1] * L[i][1] + G[2] * L[i][2]);
          if (ok) got = g; }
        if (got < 0) printf(" ???"); else printf(" %d%d%d", got / 25, (got / 5) % 5, got % 5); }
      printf(" | sigma %d star %d proj %d tests %lld\n", nsig, nstar, nP, tests);
    }
    fflush(stdout);
    free(pre); free(star); free(alive); free(P); free(T);
  }
  return 0;
}
