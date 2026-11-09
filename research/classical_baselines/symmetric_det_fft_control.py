"""Finite raw-Gauss/FFT controls for SYMMETRIC_DETERMINANT_CHARACTER_READOUT.md."""
import itertools, json
import numpy as np

def ranks_dets(matrices,p):
    A=matrices.copy().astype(np.int64)
    count,n,_=A.shape
    ranks=np.zeros(count,dtype=np.int64)
    det=np.ones(count,dtype=np.int64)
    inv=np.array([0]+[pow(i,-1,p) for i in range(1,p)],dtype=np.int64)
    for col in range(n):
        old=ranks.copy()
        for r in range(n):
            ix=np.flatnonzero(old==r)
            if not len(ix): continue
            nz=A[ix,r:,col]!=0
            good=nz.any(axis=1)
            ix=ix[good]
            if not len(ix): continue
            pivotrow=r+nz[good].argmax(axis=1)
            tmp=A[ix,r,:].copy()
            A[ix,r,:]=A[ix,pivotrow,:]
            A[ix,pivotrow,:]=tmp
            det[ix]=(det[ix]*np.where(pivotrow==r,1,-1)*A[ix,r,col])%p
            for row in range(r+1,n):
                factor=A[ix,row,col]*inv[A[ix,r,col]]%p
                A[ix,row,:]=(A[ix,row,:]-factor[:,None]*A[ix,r,:])%p
            ranks[ix]+=1
    det[ranks<n]=0
    return ranks,det

def run(n,p):
    pairs=[(i,j) for i in range(n) for j in range(i,n)]
    N=len(pairs); shape=(p,)*N; M=p**N
    x=np.indices(shape,dtype=np.int64).reshape(N,-1).T
    matrices=np.zeros((M,n,n),dtype=np.int64)
    for k,(i,j) in enumerate(pairs):
        matrices[:,i,j]=x[:,k]
        matrices[:,j,i]=x[:,k]
    ranks,det=ranks_dets(matrices,p)
    chi=np.array([0]+[1 if pow(i,(p-1)//2,p)==1 else -1 for i in range(1,p)],dtype=np.int64)
    f=np.where(det==0,1,chi[det])
    fft=np.fft.fftn(f.reshape(shape)/np.sqrt(M),norm='ortho').ravel()
    us=np.array(list(itertools.product(range(p),repeat=n)),dtype=np.int64)
    z=np.array([[int(u[i]*u[j]*(1 if i==j else 2))%p for i,j in pairs] for u in us],dtype=np.int64)
    mask=np.zeros(M,dtype=bool)
    for t in range(1,p):
        y=t*z%p
        ids=np.ravel_multi_index(y.T,shape)
        mask[ids]=True
    mask[0]=False
    # Direct finite additive sums; no rank/diagonalization formula is used for G.
    roots=np.exp(2j*np.pi*np.arange(p)/p)
    nu=next(k for k in range(1,p) if chi[k]==-1)
    G1=np.zeros(M,dtype=np.complex128)
    Gn=np.zeros(M,dtype=np.complex128)
    for v in z:
        qval=(x@v)%p
        G1+=roots[qval]
        Gn+=roots[nu*qval%p]
    G1/=p**(n/2); Gn/=p**(n/2)
    gamma=sum(roots[k*k%p] for k in range(p))/np.sqrt(p)
    H=(G1+(-1)**n*Gn)/(2*gamma**n)
    Hfft=np.fft.fftn(H.reshape(shape)/np.sqrt(M),norm='ortho').ravel()
    singular=ranks<n
    off=~mask.copy(); off[0]=False
    full=ranks==n; corank1=ranks==n-1
    out={
        'n':n,'p':p,'N':N,'source_count':M,'rank_histogram':np.bincount(ranks,minlength=n+1).tolist(),
        'rankone_dual_count':int(mask.sum()),'actual_norm2':float(np.vdot(fft,fft).real),
        'actual_rankone_mass':float(np.sum(abs(fft[mask])**2)),
        'actual_zero_mass':float(abs(fft[0])**2),
        'actual_off_rankone_and_zero_mass':float(np.sum(abs(fft[off])**2)),
        'singularity_mass':float(singular.mean()),
        'gamma':[float(gamma.real),float(gamma.imag)],'nu':nu,
        'ideal_fullrank_maxerr':float(max(abs(H[full]-chi[det[full]]))),
        'ideal_corank1_maxabs':float(max(abs(H[corank1]))),
        'ideal_norm2':float(np.mean(abs(H)**2)),
        'ideal_norm2_predicted':float(1 if n%2==0 else 1-p**(-n)),
        'ideal_rankone_mass':float(np.sum(abs(Hfft[mask])**2)),
        'ideal_zero_mass':float(abs(Hfft[0])**2),
        'ideal_off_rankone_and_zero_mass':float(np.sum(abs(Hfft[off])**2)),
        'ideal_odd_total_off_rankone_mass':float(np.sum(abs(Hfft[~mask])**2)) if n%2 else None,
        'mean_squared_H_minus_padded':float(np.mean(abs(H-f)**2)),
        '4_singularity_mass':float(4*singular.mean()),
    }
    # Independent exact determinant checksum using Leibniz expansion.
    det2=np.zeros(M,dtype=np.int64)
    for perm in itertools.permutations(range(n)):
        parity=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))%2
        term=np.ones(M,dtype=np.int64)
        for i in range(n): term=term*matrices[:,i,perm[i]]%p
        det2=(det2+(-1 if parity else 1)*term)%p
    out['exact_determinant_mismatches']=int(np.count_nonzero(det2!=det))
    return out

if __name__ == '__main__':
    results = [run(n,p) for n,p in [(3,5),(4,3)]]
    for row in results:
        assert row['exact_determinant_mismatches'] == 0
        assert row['ideal_fullrank_maxerr'] < 1e-10
        assert row['ideal_corank1_maxabs'] < 1e-10
        assert abs(row['ideal_norm2'] - row['ideal_norm2_predicted']) < 1e-10
        assert row['ideal_off_rankone_and_zero_mass'] < 1e-20
        assert row['mean_squared_H_minus_padded'] <= row['4_singularity_mass'] + 1e-10
    print(json.dumps({'scope': 'Classical finite normalization falsifiers only; below theorem threshold; no quantum execution', 'results': results}, indent=2))
