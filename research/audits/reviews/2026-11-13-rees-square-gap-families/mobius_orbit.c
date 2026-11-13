/* Mobius-orbit family for the two-level contraction problem (prime kappa, odd).
 *
 * Configuration on P^1(F_p): S = mu_kappa, T = t*mu_kappa (t in F_p^*), chart point z
 * (z = infinity or z in F_p \ (S u T)).  In the chart z the alpha-points are
 * a_j = 1/(zeta^j - z) and the beta-values are b_i = -1/(t zeta^i - z)
 * (for z = infinity: a_j = zeta^j, b_i = -t zeta^i).  A pair (t,z) is a SOLUTION
 * when some labelling of the a's and b's by Z_kappa makes (alpha,beta) a two-level
 * contraction for the coset generator xi = g (least primitive root).
 *
 * The test: cell index matrix M_ji = ind(a_j + b_i) (zero cells allowed, flagged) must be
 * u_j + v_i on nonzero cells with u, v bijective Z_kappa -> Z_kappa, and some nonzero
 * cell has u_j + v_i = 0 (that cell becomes (0,0)).  Then sigma(j) = -u_j, pi(i) = -v_i.
 *
 * (C1) is chart independent, so t is prefiltered in the chart z = infinity.
 * Usage: mobius_orbit kappa pmin pmax [w [stride]]  (stride: every stride-th admissible prime)
 * Output per prime: p  p mod kappa^2  nC1  nsol  fixedchart_ok  n_generic_chart_t_notin_mu  [t z]  nP(t in mu, z generic)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int64_t pw(int64_t b, int64_t e, int64_t m){int64_t r=1;b%=m;if(b<0)b+=m;while(e){if(e&1)r=r*b%m;b=b*b%m;e>>=1;}return r;}
static int isprime(int64_t n){if(n<2)return 0;for(int64_t d=2;d*d<=n;d++)if(n%d==0)return 0;return 1;}
static int64_t primroot(int64_t p){int64_t f[64];int nf=0;int64_t n=p-1;for(int64_t d=2;d*d<=n;d++)if(n%d==0){f[nf++]=d;while(n%d==0)n/=d;}if(n>1)f[nf++]=n;
  for(int64_t g=2;;g++){int ok=1;for(int i=0;i<nf;i++)if(pw(g,(p-1)/f[i],p)==1){ok=0;break;}if(ok)return g;}}
static int64_t inv(int64_t a,int64_t p){return pw(a,p-2,p);}

#define KMAX 16
static int K;
static unsigned char *IND; /* ind mod K, IND[0] unused */

/* generic check: M[j][i] indices, Z[j][i]=1 zero cell. returns 1 if labelling exists */
static int check_matrix(int M[KMAX][KMAX], int Z[KMAX][KMAX]){
  int u[KMAX],v[KMAX],su[KMAX],sv[KMAX];
  for(int a=0;a<K;a++){su[a]=0;sv[a]=0;}
  /* BFS on bipartite graph of nonzero cells */
  int qj[2*KMAX],qt[2*KMAX],head=0,tail=0;
  u[0]=0;su[0]=1;qj[tail]=0;qt[tail]=0;tail++;
  while(head<tail){int x=qj[head],side=qt[head];head++;
    if(side==0){for(int i=0;i<K;i++)if(!Z[x][i]){int val=((M[x][i]-u[x])%K+K)%K;
        if(!sv[i]){sv[i]=1;v[i]=val;qj[tail]=i;qt[tail]=1;tail++;} else if(v[i]!=val) return 0;}}
    else {for(int j=0;j<K;j++)if(!Z[j][x]){int val=((M[j][x]-v[x])%K+K)%K;
        if(!su[j]){su[j]=1;u[j]=val;qj[tail]=j;qt[tail]=0;tail++;} else if(u[j]!=val) return 0;}}
  }
  for(int a=0;a<K;a++) if(!su[a]||!sv[a]) return 0; /* disconnected: not handled */
  int mu=0,mv=0; for(int a=0;a<K;a++){mu|=1<<u[a];mv|=1<<v[a];}
  if(mu!=(1<<K)-1||mv!=(1<<K)-1) return 0;
  for(int j=0;j<K;j++)for(int i=0;i<K;i++) if(!Z[j][i] && (u[j]+v[i])%K==0) return 1;
  return 0;
}

int main(int argc,char**argv){
  K=atoi(argv[1]); int64_t pmin=atoll(argv[2]), pmax=atoll(argv[3]); int wit=argc>4; int stride=argc>5?atoi(argv[5]):1; long pcount=0;
  for(int64_t p=pmin;p<=pmax;p++){
    if(p%K!=1||!isprime(p)) continue;
    if((pcount++)%stride) continue;
    int64_t g=primroot(p), h=(p-1)/K;
    IND=(unsigned char*)malloc(p);
    {int64_t x=1; for(int64_t e=0;e<p-1;e++){IND[x]=(unsigned char)(e%K); x=x*g%p;}}
    int64_t zeta=pw(g,h,p); int64_t zp[KMAX]; zp[0]=1; for(int d=1;d<K;d++) zp[d]=zp[d-1]*zeta%p;
    int c=IND[zeta];
    long nC1=0,nsol=0,ngen=0,nP=0; int fixed_ok=0; int64_t wt=-1,wz=-2;
    char *inS=calloc(p,1); for(int d=0;d<K;d++) inS[zp[d]]=1;
    for(int64_t t=1;t<p;t++){
      int M[KMAX][KMAX],Z[KMAX][KMAX]; int64_t tz[KMAX];
      for(int i=0;i<K;i++) tz[i]=t*zp[i]%p;
      /* chart infinity: a_j = zeta^j, b_i = -t zeta^i; cell = zeta^j - t zeta^i */
      int u[KMAX],v[KMAX]; int fast=!inS[t];
      if(fast){
        int F[KMAX]; for(int d=0;d<K;d++) F[d]=IND[((zp[d]-t)%p+p)%p];
        int th=((F[1]-F[0])%K+K)%K, ok=1;
        for(int d=2;d<K;d++) if(F[d]!=(F[0]+d*th)%K){ok=0;break;}
        if(!ok) continue;
        nC1++;
        for(int j=0;j<K;j++) u[j]=F[j];
        for(int i=0;i<K;i++) v[i]=((i*c+F[(K-i)%K]-F[0])%K+K)%K;
        for(int i=0;i<K;i++)for(int j=0;j<K;j++) Z[j][i]=0;
      } else {
        for(int j=0;j<K;j++)for(int i=0;i<K;i++){int64_t x=((zp[j]-tz[i])%p+p)%p; Z[j][i]=(x==0); M[j][i]=x?IND[x]:0;}
        /* separability with zeros: test via check-like BFS but without bijectivity */
        int su[KMAX]={0},sv[KMAX]={0}; int qj[2*KMAX],qt[2*KMAX],hd=0,tl=0,ok=1;
        u[0]=0;su[0]=1;qj[tl]=0;qt[tl]=0;tl++;
        while(hd<tl&&ok){int x=qj[hd],sd=qt[hd];hd++;
          if(sd==0){for(int i=0;i<K;i++)if(!Z[x][i]){int val=((M[x][i]-u[x])%K+K)%K; if(!sv[i]){sv[i]=1;v[i]=val;qj[tl]=i;qt[tl]=1;tl++;} else if(v[i]!=val){ok=0;break;}}}
          else {for(int j=0;j<K;j++)if(!Z[j][x]){int val=((M[j][x]-v[x])%K+K)%K; if(!su[j]){su[j]=1;u[j]=val;qj[tl]=j;qt[tl]=0;tl++;} else if(u[j]!=val){ok=0;break;}}}}
        for(int a=0;a<K;a++) if(!su[a]||!sv[a]) ok=0;
        if(!ok) continue;
        nC1++;
      }
      /* charts */
      for(int64_t z=-1;z<p;z++){ /* z=-1 encodes infinity */
        if(z>=0 && (inS[z])) continue;
        int Uz[KMAX],Vz[KMAX]; int bad=0;
        if(z>=0){ for(int i=0;i<K;i++) if(tz[i]==z){bad=1;break;} if(bad) continue; }
        int mu=0,mv=0;
        for(int j=0;j<K;j++){int s=(z<0)?0:IND[((zp[j]-z)%p+p)%p]; Uz[j]=((u[j]-s)%K+K)%K; mu|=1<<Uz[j];}
        if(mu!=(1<<K)-1) continue;
        for(int i=0;i<K;i++){int s=(z<0)?0:IND[((tz[i]-z)%p+p)%p]; Vz[i]=((v[i]-s)%K+K)%K; mv|=1<<Vz[i];}
        if(mv!=(1<<K)-1) continue;
        int okc=0; for(int j=0;j<K&&!okc;j++)for(int i=0;i<K;i++) if(!Z[j][i] && (Uz[j]+Vz[i])%K==0){okc=1;break;}
        if(!okc) continue;
        nsol++; if(z<0) fixed_ok=1; if(z>0 && fast) ngen++; if(z>0 && !fast) nP++; if(wt<0){wt=t;wz=z;}
      }
    }
    printf("%lld %lld %ld %ld %d %ld",(long long)p,(long long)(p%(K*K)),nC1,nsol,fixed_ok,ngen); printf(" %ld",nP);
    if(wit && wt>=0) printf(" %lld %lld",(long long)wt,(long long)wz);
    printf("\n"); fflush(stdout);
    free(IND); free(inS);
  }
  return 0;
}
