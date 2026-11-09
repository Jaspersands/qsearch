/* Independent complete search for RC(D; R -> K) contractions (threshold-7 check).
 *
 * Normal form alpha_0 = 1, beta_0 = 0 (translation + scaling by alpha_0^{-1} in P_D).
 * Cell (i,j), i in R, j in Z_D:  alpha_j + beta_i in B_{i+j},
 *   B_m = {0} u { y != 0 : log_g(y) mod D  in  K - m }.
 * Column 0 is alpha_0 = 1, so beta_i ranges over B_i - 1; the other columns are kept as
 * bitsets S_j = B_j  n  /\_{i assigned} (B_{i+j} - beta_i).  Repeated beta values and zero
 * cells are allowed.  No symmetry breaking and no prune other than "some S_j empty".
 * Written from the definition only; it shares no code with rectu.c.
 *
 * Build: cc -O2 -shared -fPIC -o librcdfs.so rcdfs.c
 * Return: 1 feasible (alpha[D], beta[r] filled; beta in the order of R), 0 infeasible,
 *        -1 node limit reached (undecided).
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static int P, D, NR, WD;
static int *Rrow;
static uint64_t *T;          /* T[(m*P + b)*WD + w] : bitset of {x : x + b in B_m} */
static int **dom; static int *domn;
static long long nodes, limit;
static int *betaval;
static uint64_t *stack;      /* (NR) levels x (D) columns x WD words */

static inline int nonempty(const uint64_t *s) { for (int w = 0; w < WD; w++) if (s[w]) return 1; return 0; }

static int dfs(int t) {
    if (++nodes > limit) return -1;
    if (t == NR - 1) return 1;                    /* rows 1..NR-1 assigned (row 0 is beta_0 = 0) */
    int i = Rrow[t + 1];
    uint64_t *cur = stack + (size_t)t * D * WD, *nxt = stack + (size_t)(t + 1) * D * WD;
    for (int v = 0; v < domn[t + 1]; v++) {
        int b = dom[t + 1][v], ok = 1;
        for (int j = 1; j < D && ok; j++) {
            const uint64_t *tb = T + ((size_t)(((i + j) % D) * P + b)) * WD;
            uint64_t any = 0;
            for (int w = 0; w < WD; w++) { uint64_t x = cur[j * WD + w] & tb[w]; nxt[j * WD + w] = x; any |= x; }
            if (!any) ok = 0;
        }
        if (!ok) continue;
        betaval[t + 1] = b;
        int res = dfs(t + 1);
        if (res != 0) return res;
    }
    return 0;
}

int rc_feasible(int p, int g, int Dm, const int *R, int r, const int *K, int k,
                long long node_limit, unsigned seed, int *alpha_out, int *beta_out, long long *nodes_out) {
    P = p; D = Dm; NR = r; WD = (p + 63) / 64; limit = node_limit; nodes = 0;
    int *cls = malloc(sizeof(int) * p);
    cls[0] = -1;
    long long x = 1;
    for (int e = 0; e < p - 1; e++) { cls[x] = e % D; x = x * g % p; }
    if (x != 1) { free(cls); return -2; }
    /* inK[c] = 1 if c in K (mod D) */
    int *inK = calloc(D, sizeof(int));
    for (int a = 0; a < k; a++) inK[((K[a] % D) + D) % D] = 1;
    /* B_m membership */
    char *B = malloc((size_t)D * p);
    for (int m = 0; m < D; m++)
        for (int y = 0; y < p; y++)
            B[(size_t)m * p + y] = (y == 0) ? 1 : inK[(cls[y] + m) % D];   /* cls(y) in K - m  <=>  cls(y)+m in K */
    T = calloc((size_t)D * p * WD, sizeof(uint64_t));
    for (int m = 0; m < D; m++)
        for (int b = 0; b < p; b++) {
            uint64_t *row = T + ((size_t)(m * P + b)) * WD;
            for (int xx = 0; xx < p; xx++) if (B[(size_t)m * p + (xx + b) % p]) row[xx >> 6] |= 1ULL << (xx & 63);
        }
    Rrow = malloc(sizeof(int) * r);
    for (int a = 0; a < r; a++) Rrow[a] = ((R[a] % D) + D) % D;
    /* row 0 must be first and equal to 0 */
    if (Rrow[0] != 0) { return -3; }
    dom = malloc(sizeof(int *) * r); domn = calloc(r, sizeof(int));
    srand(seed);
    for (int a = 1; a < r; a++) {
        dom[a] = malloc(sizeof(int) * p);
        int i = Rrow[a];
        for (int b = 0; b < p; b++) if (B[(size_t)i * p + (1 + b) % p]) dom[a][domn[a]++] = b;   /* 1 + beta_i in B_{i+0} */
        if (seed) for (int u = domn[a] - 1; u > 0; u--) { int w = rand() % (u + 1); int tmp = dom[a][u]; dom[a][u] = dom[a][w]; dom[a][w] = tmp; }
    }
    stack = calloc((size_t)(r + 1) * D * WD, sizeof(uint64_t));
    for (int j = 1; j < D; j++) memcpy(stack + (size_t)j * WD, T + ((size_t)(j * P + 0)) * WD, WD * 8);  /* row 0: alpha_j in B_j */
    int ok0 = 1;
    for (int j = 1; j < D; j++) if (!nonempty(stack + (size_t)j * WD)) ok0 = 0;
    betaval = calloc(r, sizeof(int));
    int res = ok0 ? dfs(0) : 0;
    if (res == 1) {
        uint64_t *fin = stack + (size_t)(r - 1) * D * WD;
        alpha_out[0] = 1;
        for (int j = 1; j < D; j++) {
            uint64_t *s = fin + (size_t)j * WD; int found = -1;
            for (int w = 0; w < WD && found < 0; w++) if (s[w]) found = w * 64 + __builtin_ctzll(s[w]);
            alpha_out[j] = found;
        }
        beta_out[0] = 0;
        for (int a = 1; a < r; a++) beta_out[a] = betaval[a];
    }
    *nodes_out = nodes;
    free(cls); free(inK); free(B); free(T); free(Rrow);
    for (int a = 1; a < r; a++) free(dom[a]);
    free(dom); free(domn); free(stack); free(betaval);
    return res;
}
