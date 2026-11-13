/* RC(D;R->K) contraction search, written from fragment.tex Def. def:rc only.
   stdin lines:  p D mode budget seed nR R_1..R_nR nK K_1..K_nK
   mode: r = random trials (budget = #trials), e = exhaustive DFS (budget = node cap)
   stdout: FOUND a_0..a_{D-1} | b_{R_1}..b_{R_nR}   or  NONE  or  UNKNOWN
   Normalisation (WLOG by translation and P_D-scaling): beta_0 = 0, alpha_0 = 1.
   Zero entries alpha_j+beta_i = 0 are allowed except at (0,0), as in Def. def:rc.
   Classes: cl_D(x) = log_g(x) mod D, g = least primitive root.                      */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;
static long P = 0; static int *LG = NULL;
static u64 rng_s;
static u64 rnd(void){ rng_s ^= rng_s<<13; rng_s ^= rng_s>>7; rng_s ^= rng_s<<17; return rng_s; }
static long pw(long b,long e,long m){ long r=1; b%=m; while(e){ if(e&1) r=(__int128)r*b%m; b=(__int128)b*b%m; e>>=1;} return r; }
static long primroot(long p){ long n=p-1, f[64]; int nf=0; long m=n; for(long d=2; d*d<=m; d++) if(m%d==0){ f[nf++]=d; while(m%d==0) m/=d; } if(m>1) f[nf++]=m;
  for(long g=2;;g++){ int ok=1; for(int i=0;i<nf;i++) if(pw(g,n/f[i],p)==1){ok=0;break;} if(ok) return g; } }
static void setp(long p){ if(p==P) return; free(LG); LG=malloc(sizeof(int)*p); long g=primroot(p); long x=1; LG[0]=-1;
  for(long i=0;i<p-1;i++){ LG[x]=(int)i; x=x*g%p; } P=p; }
static int D, nR, nK, R[64], K[64], inK[64];
static long W; /* words for p bits */
static u64 *Z2[64]; /* Z_c doubled: bit y (0<=y<2p) set iff (y mod p) in Z_c */
static long nodes, cap; static int found;
static long beta[64], alpha[64];
static u64 *Xst; /* stack of X sets: (depth)(D)(W) */
static long *dom[64]; static long ndom[64];
static inline int getbit(const u64*b,long i){ return (b[i>>6]>>(i&63))&1; }
static inline void setbit(u64*b,long i){ b[i>>6]|=1ULL<<(i&63); }
/* dst = src & window(Z2[c], off) over p bits; return nonempty */
static int and_win(u64*dst,const u64*src,const u64*z2,long off){
  long q=off>>6; int s=off&63; u64 any=0;
  for(long w=0;w<W;w++){ u64 lo=z2[q+w], v; if(s){ u64 hi=z2[q+w+1]; v=(lo>>s)|(hi<<(64-s)); } else v=lo;
    if(w==W-1 && (P&63)) v &= (1ULL<<(P&63))-1; dst[w]=src[w]&v; any|=dst[w]; }
  return any!=0; }
static long lowbit(const u64*b){ for(long w=0;w<W;w++) if(b[w]) return w*64+__builtin_ctzll(b[w]); return -1; }
static void dfs(int t){ /* t = index into R (R[0]=0 skipped) */
  if(found || nodes>cap) return;
  if(t==nR){ found=1; u64*X=Xst+(long)t*D*W; alpha[0]=1; for(int j=1;j<D;j++) alpha[j]=lowbit(X+(long)j*W); return; }
  int i=R[t]; u64*X=Xst+(long)t*D*W, *Y=Xst+(long)(t+1)*D*W;
  for(long a=0;a<ndom[t] && !found && nodes<=cap;a++){ long b=dom[t][a]; nodes++; int ok=1;
    for(int j=1;j<D && ok;j++) ok=and_win(Y+(long)j*W, X+(long)j*W, Z2[(i+j)%D], b);
    if(ok){ beta[i]=b; dfs(t+1); } }
}
int main(void){ char mode[8]; long p, budget; u64 seed;
  while(scanf("%ld %d %s %ld %llu",&p,&D,mode,&budget,(unsigned long long*)&seed)==5){
    scanf("%d",&nR); for(int i=0;i<nR;i++) scanf("%d",&R[i]); scanf("%d",&nK); memset(inK,0,sizeof inK); for(int i=0;i<nK;i++){ scanf("%d",&K[i]); inK[K[i]]=1; }
    /* put 0 first in R */
    for(int i=0;i<nR;i++) if(R[i]==0){ int tmp=R[0]; R[0]=0; R[i]=tmp; }
    setp(p); W=(p+63)/64; rng_s=seed*2654435761ULL+88172645463325252ULL;
    for(int c=0;c<D;c++){ Z2[c]=calloc(2*W+2,sizeof(u64)); for(long y=0;y<p;y++){ int in = (y==0) || inK[(LG[y]%D + c)%D]; if(in){ setbit(Z2[c],y); setbit(Z2[c],y+p);} } }
    /* domains for beta_i (t>=1): 1+beta in Z_i  (pair (i,j=0)) */
    for(int t=1;t<nR;t++){ int i=R[t]; dom[t]=malloc(sizeof(long)*p); ndom[t]=0; for(long z=0;z<p;z++) if(getbit(Z2[i],z)) dom[t][ndom[t]++]=(z-1+p)%p; }
    Xst=calloc((long)(nR+4)*D*W,sizeof(u64));
    for(int j=1;j<D;j++) memcpy(Xst+(long)1*D*W+(long)j*W, Z2[j%D], W*sizeof(u64)); /* level t=1: after i=0 */
    /* mask last word */
    for(int j=1;j<D;j++) if(p&63) Xst[(long)D*W+(long)j*W+W-1] &= (1ULL<<(p&63))-1;
    found=0; nodes=0; beta[0]=0;
    if(mode[0]=='e'){ cap=budget; dfs(1); }
    else { cap=1L<<62; for(long tr=0;tr<budget && !found;tr++){ int ok=1; u64*X=Xst+(long)D*W;
        u64*A=Xst+(long)2*D*W; /* scratch two layers */ u64*B2=A+(long)D*W; memcpy(A,X,(long)D*W*sizeof(u64));
        for(int t=1;t<nR && ok;t++){ int i=R[t]; long b=dom[t][rnd()%ndom[t]]; beta[i]=b;
          for(int j=1;j<D && ok;j++) ok=and_win(B2+(long)j*W, A+(long)j*W, Z2[(i+j)%D], b);
          if(ok) memcpy(A,B2,(long)D*W*sizeof(u64)); }
        if(nR==1) ok=1;
        if(ok){ found=1; alpha[0]=1; for(int j=1;j<D;j++) alpha[j]=lowbit(A+(long)j*W); } } }
    if(found){ printf("FOUND"); for(int j=0;j<D;j++) printf(" %ld",alpha[j]); printf(" |"); for(int t=0;t<nR;t++) printf(" %ld",beta[R[t]]); printf(" | nodes %ld\n",nodes); }
    else if(mode[0]=='e' && nodes<=cap) printf("NONE | nodes %ld\n",nodes); else printf("UNKNOWN | nodes %ld\n",nodes);
    fflush(stdout);
    for(int c=0;c<D;c++) free(Z2[c]); for(int t=1;t<nR;t++) free(dom[t]); free(Xst);
  }
  return 0; }
