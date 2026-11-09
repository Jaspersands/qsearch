/* rectp.c -- randomized witness search for RC(D; R -> K) without an index table
 * (coset test by exponentiation), for large p.  Same conventions and output as rectu.c,
 * strict cells only (all cells nonzero).  Usage: rectp D "R" "K" plo phi [seed] [tries] [mod]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef long long ll; typedef unsigned __int128 u128;
static ll mulm(ll a, ll b, ll p){ return (ll)((u128)a*b%p); }
static ll pw(ll b, ll e, ll p){ ll r=1; b%=p; if(b<0)b+=p; while(e){ if(e&1) r=mulm(r,b,p); b=mulm(b,b,p); e>>=1;} return r; }
static int isprime(ll n){ if(n<2) return 0; if(n%2==0) return n==2; for(ll d=3; d*d<=n; d+=2) if(n%d==0) return 0; return 1; }
static ll primroot(ll p){ ll f[64]; int nf=0; ll n=p-1; for(ll d=2; d*d<=n; d++) if(n%d==0){ f[nf++]=d; while(n%d==0) n/=d; } if(n>1) f[nf++]=n;
  for(ll g=2; g<p; g++){ int ok=1; for(int k=0;k<nf;k++) if(pw(g,(p-1)/f[k],p)==1){ok=0;break;} if(ok) return g; } return -1; }
static uint64_t rs=88172645463325252ULL; static uint64_t xr(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static int parse(const char*s, int*a){ int n=0; const char*q=s; while(*q){ a[n++]=atoi(q); while(*q && *q!=',') q++; if(*q==',') q++; } return n; }
static int D,r,nk,Rw[64],Kw[64]; static uint64_t allow[64][64]; static ll p, e, zt[64];
static int indx(ll v){ ll y=pw(v,e,p); for(int t=0;t<D;t++) if(zt[t]==y) return t; return -1; }
static inline int ok(ll v, uint64_t mask){ if(v==0) return 0; return (mask>>indx(v))&1ULL; }
int main(int argc,char**argv){
  D=atoi(argv[1]); r=parse(argv[2],Rw); nk=parse(argv[3],Kw); ll plo=atoll(argv[4]), phi=atoll(argv[5]);
  if(argc>6) rs^=(uint64_t)atoll(argv[6])*2654435761ULL; int tries=argc>7?atoi(argv[7]):20; ll mod=argc>8?atoll(argv[8]):D;
  for(int k=0;k<r;k++) for(int j=0;j<D;j++){ uint64_t mk=0; for(int t=0;t<nk;t++){ int c=((Kw[t]-(Rw[k]+j))%D+D)%D; mk|=1ULL<<c; } allow[k][j]=mk; }
  ll start = plo - ((plo-1)%mod); if(start<plo) start+=mod;
  for(p=start;p<=phi;p+=mod){ if(p%D!=1 || !isprime(p)) continue;
    ll g=primroot(p); e=(p-1)/D; ll z=pw(g,e,p); zt[0]=1; for(int t=1;t<D;t++) zt[t]=mulm(zt[t-1],z,p);
    ll beta[64], alpha[64]; beta[0]=0; alpha[0]=1; int found=0;
    for(int tr=0;tr<tries && !found;tr++){
      int okb=1;
      for(int k=1;k<r;k++){ int got=0; for(int t=0;t<100000;t++){ ll b=xr()%p; if(!ok((1+b)%p,allow[k][0])) continue; int dup=0; for(int kk=0;kk<k;kk++) if(beta[kk]==b) dup=1; if(dup) continue; beta[k]=b; got=1; break; } if(!got){okb=0;break;} }
      if(!okb) continue;
      int all=1;
      for(int j=1;j<D && all;j++){ int got=0; ll lim = 200000; for(ll t=0;t<lim;t++){ ll x=xr()%p; int gd=1; for(int k=0;k<r;k++) if(!ok((x+beta[k])%p,allow[k][j])){gd=0;break;} if(gd){alpha[j]=x; got=1; break;} } if(!got) all=0; }
      if(all) found=1; }
    if(!found){ printf("%lld NOTFOUND\n",p); fflush(stdout); continue; }
    printf("%lld FEASIBLE g=%lld beta",p,g); for(int k=0;k<r;k++) printf(" %lld",beta[k]); printf(" alpha"); for(int j=0;j<D;j++) printf(" %lld",alpha[j]); printf("\n");
  }
  return 0; }
