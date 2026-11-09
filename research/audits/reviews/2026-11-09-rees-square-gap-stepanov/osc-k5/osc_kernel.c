/* C kernel for the kappa = 4, 5 separable-type enumerator (osc_k5.py).
 *
 * Same object as ../types/orbit_types_fast.py: labelled (S, T, z) on P^1 mod PGL_2 with
 * (S, T) in (C1), normal form s_0 = inf, s_1 = 0, s_2 = 1.  Two reductions:
 *   - S is enumerated UNLABELLED mod PGL_2: a normal form (s_3[, s_4]) is kept iff it is the
 *     lexicographic minimum of the k! normal forms of its point set; it is weighted by its
 *     orbit size k!/|Stab|; the V-labels are re-symmetrised over S_k in Python afterwards.
 *   - T is unlabelled and not enumerated: for each (S, z, bucket b) the U-value counts
 *     m_a = #{t in b, t != z : -ind(t - z) = a} are formed and every multiset n <= m with
 *     |n| = k is added with weight prod_a C(m_a, n_a).
 * Output acc[comp(n) * KV + Vc], Vc = sum_{j>=1} ((g_j - ind(s_j - z)) mod k) k^(j-1).
 */
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

#define INF (-1)
#define MAXB 256

static int64_t P_;
static const int32_t *INV_;

static inline int64_t md(int64_t x) { x %= P_; return x < 0 ? x + P_ : x; }

/* image of x under the Moebius map a -> inf, b -> 0, c -> 1 (points distinct; INF = -1) */
static inline int64_t cr(int64_t x, int64_t a, int64_t b, int64_t c) {
    int64_t num, den;
    if (x == INF) { num = md(c - a); den = md(c - b); }
    else if (a == INF) { num = md(x - b); den = md(c - b); }
    else if (b == INF) { num = md(c - a); den = md(x - a); }
    else if (c == INF) { num = md(x - b); den = md(x - a); }
    else { num = md(md(x - b) * md(c - a)); den = md(md(x - a) * md(c - b)); }
    return md(num * INV_[den]);
}

static uint64_t BIN[MAXB][8];

static void enum_comp(int k, int a, int rem, const int *m, int code, uint64_t wt,
                      const int16_t *code2idx, uint64_t *row_acc, int KV, int Vidx, uint64_t w,
                      uint64_t *tot, const int *pw6) {
    if (a == k - 1) {
        if (rem <= m[a]) {
            uint64_t ww = wt * BIN[m[a]][rem];
            int c = code + rem * pw6[a];
            row_acc[(int64_t)code2idx[c] * KV + Vidx] += w * ww;
            *tot += w * ww;
        }
        return;
    }
    int top = rem < m[a] ? rem : m[a];
    for (int na = 0; na <= top; na++)
        enum_comp(k, a + 1, rem - na, m, code + na * pw6[a], wt * BIN[m[a]][na], code2idx, row_acc, KV,
                  Vidx, w, tot, pw6);
}

void init_bin(void) {
    for (int i = 0; i < MAXB; i++)
        for (int j = 0; j < 8; j++)
            BIN[i][j] = (j == 0) ? 1 : (i == 0 ? 0 : BIN[i - 1][j - 1] + BIN[i - 1][j]);
}

/* call init_bin() once before run_chunk.  returns 0 on success, negative on error.
 * info[0] = #canonical S reps, info[1] = sum of orbit sizes (= #labelled normal forms),
 * info[2] = sum_w #(unlabelled T, z) (= N1 / k!), info[3] = max bucket size seen */
int run_chunk(int k, int p, const uint8_t *ind, const int32_t *inv, const int8_t *perms, int nperm,
              const int16_t *code2idx, int s3_start, int s3_step, uint64_t *acc, int64_t *info) {
    if (k < 4 || k > 5) return -1;
    P_ = p; INV_ = inv;
    int nfree = k - 3;
    int KV = 1; for (int j = 1; j < k; j++) KV *= k;
    int pwk[8]; pwk[0] = 1; for (int j = 1; j < 8; j++) pwk[j] = pwk[j - 1] * k;
    int pw6[8]; pw6[0] = 1; for (int j = 1; j < 8; j++) pw6[j] = pw6[j - 1] * (k + 1);
    uint8_t neg[256]; for (int e = 0; e < 256; e++) neg[e] = (uint8_t)((k - (e % k)) % k);
    int32_t *keyt = (int32_t *)malloc(sizeof(int32_t) * p);
    int32_t *members = (int32_t *)malloc(sizeof(int32_t) * p);
    int32_t *cnt = (int32_t *)malloc(sizeof(int32_t) * (KV + 1));
    int32_t *bst = (int32_t *)malloc(sizeof(int32_t) * (KV + 1));
    int32_t *fill = (int32_t *)malloc(sizeof(int32_t) * (KV + 1));
    int32_t *big = (int32_t *)malloc(sizeof(int32_t) * (KV + 1));
    uint8_t *kd = (uint8_t *)malloc((size_t)KV * 4);
    for (int key = 0; key < KV; key++) for (int j = 0; j < k - 1; j++) kd[key * 4 + j] = (key / pwk[j]) % k;
    int64_t nrep = 0, sumw = 0, maxb = 0;
    uint64_t tot = 0;
    int64_t pts[5];
    pts[0] = INF; pts[1] = 0; pts[2] = 1;
    for (int64_t s3 = 2 + s3_start; s3 < p; s3 += s3_step) {
        int64_t s4lo = (nfree == 2) ? 2 : 0, s4hi = (nfree == 2) ? p : 1;
        for (int64_t s4 = s4lo; s4 < s4hi; s4++) {
            if (nfree == 2 && s4 == s3) continue;
            pts[3] = s3; if (nfree == 2) pts[4] = s4;
            /* canonical test */
            int stab = 0, rej = 0;
            for (int q = 0; q < nperm && !rej; q++) {
                const int8_t *pq = perms + q * k;
                int64_t a = pts[pq[0]], b = pts[pq[1]], c = pts[pq[2]];
                int cmp = 0;
                for (int i = 0; i < nfree; i++) {
                    int64_t v = cr(pts[pq[3 + i]], a, b, c);
                    if (v < pts[3 + i]) { cmp = -1; break; }
                    if (v > pts[3 + i]) { cmp = 1; break; }
                }
                if (cmp < 0) rej = 1; else if (cmp == 0) stab++;
            }
            if (rej) continue;
            if (stab == 0 || nperm % stab) { free(keyt); return -2; }
            uint64_t w = (uint64_t)(nperm / stab);
            nrep++; sumw += (int64_t)w;
            /* keys of t */
            memset(cnt, 0, sizeof(int32_t) * (KV + 1));
            for (int64_t t = 0; t < p; t++) {
                int key = 0, ok = 1;
                for (int j = 1; j < k; j++) {
                    int64_t d = pts[j] - t; if (d < 0) d += p;
                    uint8_t e = ind[d];
                    if (e == 255) { ok = 0; break; }
                    key += e * pwk[j - 1];
                }
                keyt[t] = ok ? key : -1;
                if (ok) cnt[key]++;
            }
            bst[0] = 0;
            for (int key = 0; key < KV; key++) bst[key + 1] = bst[key] + cnt[key];
            for (int key = 0; key < KV; key++) fill[key] = bst[key];
            for (int64_t t = 0; t < p; t++) if (keyt[t] >= 0) members[fill[keyt[t]]++] = (int32_t)t;
            int nbig = 0;
            for (int key = 0; key < KV; key++) if (cnt[key] >= k) { big[nbig++] = key; if (cnt[key] > maxb) maxb = cnt[key]; }
            if (maxb >= MAXB) { return -3; }
            if (!nbig) continue;
            for (int64_t z = 0; z < p; z++) {
                int kz = keyt[z];
                if (kz < 0) continue;
                const uint8_t *zd = kd + kz * 4;
                for (int bi = 0; bi < nbig; bi++) {
                    int g = big[bi];
                    int sz = cnt[g] - (g == kz ? 1 : 0);
                    if (sz < k) continue;
                    const uint8_t *gd = kd + g * 4;
                    int Vidx = 0;
                    for (int j = 0; j < k - 1; j++) Vidx += ((gd[j] + k - zd[j]) % k) * pwk[j];
                    int m[5] = {0, 0, 0, 0, 0};
                    const int32_t *mem = members + bst[g];
                    int nm = cnt[g];
                    for (int i = 0; i < nm; i++) {
                        int64_t d = mem[i] - z;
                        if (d == 0) continue;
                        if (d < 0) d += p;
                        m[neg[ind[d]]]++;
                    }
                    if (sz == k) {
                        int c = 0;
                        for (int a = 0; a < k; a++) c += m[a] * pw6[a];
                        acc[(int64_t)code2idx[c] * KV + Vidx] += w;
                        tot += w;
                    } else {
                        enum_comp(k, 0, k, m, 0, 1, code2idx, acc, KV, Vidx, w, &tot, pw6);
                    }
                }
            }
        }
    }
    info[0] = nrep; info[1] = sumw; info[2] = (int64_t)tot; info[3] = maxb;
    free(keyt); free(members); free(cnt); free(bst); free(fill); free(big); free(kd);
    return 0;
}
