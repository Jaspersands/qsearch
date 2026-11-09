/* rectu.c -- general refinement-step contraction RC(D; R -> K).
 * Rows R subset Z_D (0 in R), columns Z_D, target union K subset Z_D (0 in K):
 *   alpha_j + beta_i in  U_{k in K} Q_{k-(i+j)}  u {0}     (i in R, j in Z_D)
 *   alpha_0 + beta_0 in Q_0 (nonzero).   Normal form beta_0 = 0, alpha_0 = 1.
 * Q_c = g^c (F_p^x)^D, g primitive root.  (K = {0}: rectangular contraction;
 * R = Z_D, K = {0}: two-level contraction, E_2(D).)
 * Usage: rectu D "r0,r1,..." "k0,k1,..." plo phi mode [zeros] [seed] [tries] [mod]
 *   only primes p = 1 (mod mod) are run (default mod = D).
 *   env ALLOWDUP=1 also allows beta_i = beta_i' (needed for union targets K; for K = {0} distinct beta is forced).
 *   mode 0 randomized witness search (FEASIBLE / NOTFOUND); mode 1 complete (FEASIBLE / INFEASIBLE)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef long long ll;
static ll pw(ll b, ll e, ll p){ ll r=1; b%=p; if(b<0)b+=p; while(e){ if(e&1) r=r*b%p; b=b*b%p; e>>=1;} return r; }
static int isprime(ll n){ if(n<2) return 0; for(ll d=2; d*d<=n; d++) if(n%d==0) return 0; return 1; }
static ll primroot(ll p){ ll f[64]; int nf=0; ll n=p-1; for(ll d=2; d*d<=n; d++) if(n%d==0){ f[nf++]=d; while(n%d==0) n/=d; } if(n>1) f[nf++]=n;
  for(ll g=2; g<p; g++){ int ok=1; for(int k=0;k<nf;k++) if(pw(g,(p-1)/f[k],p)==1){ok=0;break;} if(ok) return g; } return -1; }
static uint64_t rs=88172645463325252ULL; static uint64_t xr(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static int D, r, nk, zeros, allowdup; static int Rw[64], Kw[64]; static ll p; static unsigned char *ind;
static uint64_t allow[64][64]; /* allow[row k][col j] bitmask of coset indices */
static inline int ok(ll v, uint64_t mask){ if(v==0) return zeros; return (mask>>ind[v])&1ULL; }
static ll beta[64], alpha[64];
static ll *L[65][64]; static int Ln[65][64]; static long long nodes;
static int parse(const char*s, int*a){ int n=0; const char*q=s; while(*q){ a[n++]=atoi(q); while(*q && *q!=',') q++; if(*q==',') q++; } return n; }
static int colfeas(int j){ ll st=xr()%p; for(ll t=0;t<p;t++){ ll x=(st+t)%p; int g=1; for(int k=0;k<r;k++) if(!ok((x+beta[k])%p,allow[k][j])){g=0;break;} if(g){alpha[j]=x; return 1;} } return 0; }
static int dfs(int k){ nodes++;
  if(k==r){ for(int j=1;j<D;j++) alpha[j]=L[k][j][0]; return 1; }
  for(ll b=0;b<p;b++){ if(!ok((1+b)%p,allow[k][0])) continue; int dup=0; for(int kk=0;kk<k;kk++) if(beta[kk]==b) dup=1; if(dup && !allowdup) continue;
    beta[k]=b; int alive=1;
    for(int j=1;j<D && alive;j++){ int n=0; for(int t=0;t<Ln[k][j];t++){ ll x=L[k][j][t]; if(ok((x+b)%p,allow[k][j])) L[k+1][j][n++]=x; } Ln[k+1][j]=n; if(!n) alive=0; }
    if(alive && dfs(k+1)) return 1; }
  return 0; }
int main(int argc,char**argv){
  allowdup = getenv("ALLOWDUP") && atoi(getenv("ALLOWDUP"));
  D=atoi(argv[1]); r=parse(argv[2],Rw); nk=parse(argv[3],Kw); ll plo=atoll(argv[4]), phi=atoll(argv[5]); int mode=atoi(argv[6]);
  zeros= argc>7?atoi(argv[7]):1; if(argc>8) rs^=(uint64_t)atoll(argv[8])*2654435761ULL; int tries=argc>9?atoi(argv[9]):200; ll mod=argc>10?atoll(argv[10]):D;
  if(Rw[0]!=0){ fprintf(stderr,"R must start with 0\n"); return 1; }
  for(int k=0;k<r;k++) for(int j=0;j<D;j++){ uint64_t mk=0; for(int t=0;t<nk;t++){ int c=((Kw[t]-(Rw[k]+j))%D+D)%D; mk|=1ULL<<c; } allow[k][j]=mk; }
  for(p=plo;p<=phi;p++){ if(p%mod!=1 || p%D!=1 || !isprime(p)) continue;
    ll g=primroot(p); ind=malloc(p); ind[0]=255; ll x=1; for(ll e=0;e<p-1;e++){ ind[x]=(unsigned char)(e%D); x=x*g%p; }
    beta[0]=0; alpha[0]=1; int found=0;
    /* note: cell (0,0) = 1 in Q_0 automatically */
    if(mode==0){
      for(int tr=0;tr<tries && !found;tr++){ int okb=1;
        for(int k=1;k<r;k++){ ll st=xr()%p; int got=0; for(ll t=0;t<p;t++){ ll b=(st+t)%p; if(!ok((1+b)%p,allow[k][0])) continue; int dup=0; for(int kk=0;kk<k;kk++) if(beta[kk]==b) dup=1; if(dup && !allowdup) continue; beta[k]=b; got=1; break; } if(!got){okb=0;break;} }
        if(!okb) continue; int all=1; for(int j=1;j<D;j++) if(!colfeas(j)){all=0;break;} if(all) found=1; }
      if(!found){ printf("%lld NOTFOUND\n",p); fflush(stdout); free(ind); continue; }
    } else {
      for(int j=1;j<D;j++){ L[0][j]=malloc(sizeof(ll)*p); int n=0; for(ll xx=0;xx<p;xx++) if(ok(xx,allow[0][j])) L[0][j][n++]=xx; Ln[0][j]=n; }
      for(int k=1;k<=r;k++) for(int j=1;j<D;j++) L[k][j]=malloc(sizeof(ll)*(Ln[0][j]+1));
      for(int j=1;j<D;j++){ memcpy(L[1][j],L[0][j],sizeof(ll)*Ln[0][j]); Ln[1][j]=Ln[0][j]; }
      nodes=0; int alive=1; for(int j=1;j<D;j++) if(!Ln[1][j]) alive=0;
      found = alive && dfs(1);
      for(int k=0;k<=r;k++) for(int j=1;j<D;j++) free(L[k][j]);
      if(!found){ printf("%lld INFEASIBLE nodes=%lld\n",p,nodes); fflush(stdout); free(ind); continue; }
    }
    printf("%lld FEASIBLE g=%lld beta",p,g); for(int k=0;k<r;k++) printf(" %lld",beta[k]); printf(" alpha"); for(int j=0;j<D;j++) printf(" %lld",alpha[j]); printf("\n"); fflush(stdout); free(ind);
  }
  return 0; }
