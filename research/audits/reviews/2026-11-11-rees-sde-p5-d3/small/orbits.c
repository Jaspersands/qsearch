/* Orbit representatives of GL_3(F_5) acting on SPANNING k-subsets of Q, the 62 classes {v,-v}
 * of nonzero vectors of F_5^3 (k = 3..KMAX).  Class rep vector: the one of +-v whose first
 * nonzero coordinate is 1 or 2.
 * Canonical form of X: min, over ordered independent triples (a,b,c) of X and signs
 * (s,t) in {1,-1}^2, of the bitmask of the image of X under the g with g(a) = e1,
 * g(s b) = e2, g(t c) = e3.  This is an orbit invariant (for h in G the frames of hX are
 * the h-images of the frames of X and give the same images), and it is an image of X.
 * Level k+1 = canonical forms of X + {x} over level-k reps X and x not in X (every spanning
 * (k+1)-set contains a spanning k-set).  Output: one line per orbit, rep vectors as digit triples.
 * usage: orbits KMAX OUTPREFIX     (writes OUTPREFIX_k.txt)
 * Build: clang -O2 -o orbits orbits.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int rv[62][3];          /* class rep vectors */
static int clsof[125];         /* vector code -> class */
static unsigned char *tab;     /* tab[frame*62 + x] = class of g x, frame = ((a*62+b)*62+c)*4+st; 255 = invalid */
static int enc(const int *v) { return v[0] * 25 + v[1] * 5 + v[2]; }
static int cmpu64(const void *a, const void *b) { uint64_t x = *(const uint64_t *)a, y = *(const uint64_t *)b; return x < y ? -1 : x > y; }
static uint64_t canon(const int *X, int k) {
  uint64_t best = ~0ULL;
  for (int i = 0; i < k; i++) for (int j = 0; j < k; j++) { if (j == i) continue;
    for (int l = 0; l < k; l++) { if (l == i || l == j) continue;
      size_t f0 = ((size_t)(X[i] * 62 + X[j]) * 62 + X[l]) * 4;
      if (tab[f0 * 62] == 255) continue;
      for (int st = 0; st < 4; st++) {
        const unsigned char *T = tab + (f0 + st) * 62; uint64_t m = 0;
        for (int q = 0; q < k; q++) m |= 1ULL << T[X[q]];
        if (m < best) best = m;
      } } }
  return best;
}
int main(int argc, char **argv) {
  int KMAX = atoi(argv[1]); const char *pre = argv[2];
  int n = 0;
  for (int x = 1; x < 125; x++) clsof[x] = -1;
  for (int x = 1; x < 125; x++) { int v[3] = {x / 25, (x / 5) % 5, x % 5}; int f = v[0] ? v[0] : v[1] ? v[1] : v[2];
    if (f == 1 || f == 2) { memcpy(rv[n], v, sizeof v); n++; } }
  for (int c = 0; c < 62; c++) { int w[3]; for (int i = 0; i < 3; i++) w[i] = (5 - rv[c][i]) % 5; clsof[enc(rv[c])] = c; clsof[enc(w)] = c; }
  tab = malloc((size_t)62 * 62 * 62 * 4 * 62);
  for (int a = 0; a < 62; a++) for (int b = 0; b < 62; b++) for (int c = 0; c < 62; c++) for (int st = 0; st < 4; st++) {
    int s = (st & 1) ? 4 : 1, t = (st & 2) ? 4 : 1;
    int B[3][3]; for (int r = 0; r < 3; r++) { B[r][0] = rv[a][r]; B[r][1] = s * rv[b][r] % 5; B[r][2] = t * rv[c][r] % 5; }
    int det = (B[0][0] * (B[1][1] * B[2][2] - B[1][2] * B[2][1]) - B[0][1] * (B[1][0] * B[2][2] - B[1][2] * B[2][0])
             + B[0][2] * (B[1][0] * B[2][1] - B[1][1] * B[2][0])) % 5; det = (det + 5) % 5;
    unsigned char *T = tab + ((((size_t)a * 62 + b) * 62 + c) * 4 + st) * 62;
    if (det == 0) { memset(T, 255, 62); continue; }
    int di = 1; while (di * det % 5 != 1) di++;
    int A[3][3]; /* inverse = adj / det */
    for (int r = 0; r < 3; r++) for (int q = 0; q < 3; q++) {
      int r1 = (q + 1) % 3, r2 = (q + 2) % 3, c1 = (r + 1) % 3, c2 = (r + 2) % 3;
      int cof = B[r1][c1] * B[r2][c2] - B[r1][c2] * B[r2][c1];
      A[r][q] = ((cof * di) % 5 + 5) % 5; }
    for (int r = 0; r < 3; r++) for (int q = 0; q < 3; q++) { int e = 0; for (int u = 0; u < 3; u++) e += A[r][u] * B[u][q]; if (e % 5 != (r == q)) { fprintf(stderr, "inverse bug\n"); return 1; } }
    for (int x = 0; x < 62; x++) { int w[3]; for (int r = 0; r < 3; r++) w[r] = (A[r][0] * rv[x][0] + A[r][1] * rv[x][1] + A[r][2] * rv[x][2]) % 5; T[x] = clsof[enc(w)]; }
  }
  int e[3] = {clsof[25], clsof[5], clsof[1]};
  uint64_t *cur = malloc(8); size_t ncur = 1; cur[0] = canon(e, 3);
  for (int k = 3; k <= KMAX; k++) {
    char fn[1024]; snprintf(fn, sizeof fn, "%s_%d.txt", pre, k); FILE *fo = fopen(fn, "w");
    for (size_t i = 0; i < ncur; i++) { int first = 1;
      for (int x = 0; x < 62; x++) if (cur[i] >> x & 1) { fprintf(fo, "%s%d%d%d", first ? "" : " ", rv[x][0], rv[x][1], rv[x][2]); first = 0; }
      fprintf(fo, "\n"); }
    fclose(fo); printf("k=%d orbits %zu\n", k, ncur); fflush(stdout);
    if (k == KMAX) break;
    size_t cap = ncur * (62 - k), nn = 0; uint64_t *nxt = malloc(cap * 8);
    for (size_t i = 0; i < ncur; i++) { int X[16], m = 0; for (int x = 0; x < 62; x++) if (cur[i] >> x & 1) X[m++] = x;
      for (int x = 0; x < 62; x++) if (!(cur[i] >> x & 1)) { X[k] = x; nxt[nn++] = canon(X, k + 1); } }
    qsort(nxt, nn, 8, cmpu64); size_t u = 0; for (size_t i = 0; i < nn; i++) if (!u || nxt[i] != nxt[u - 1]) nxt[u++] = nxt[i];
    free(cur); cur = nxt; ncur = u;
  }
  return 0;
}
