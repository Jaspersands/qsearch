"""Density-matrix falsifiers; no HSP receiver or quantum speedup benchmark."""
import numpy as np
from sage.libs.gap.libgap import libgap

def trace_distance(A,B):
    return np.abs(np.linalg.eigvalsh(A-B)).sum()/2

G = libgap.SmallGroup(27,4)
es = list(G.Elements())
index = {str(x):i for i,x in enumerate(es)}
subs = [J for cl in libgap.ConjugacyClassesSubgroups(G) for J in cl.Elements()]
def permutes(A,B):
    return int(libgap.ClosureGroup(A,B).Size())*int(libgap.Intersection(A,B).Size()) == int(A.Size())*int(B.Size())
H = next(J for J in subs if int(J.Size()) == 3 and not bool(libgap.IsNormal(G,J))
         and all(permutes(J,K) for K in subs))
def coset_vector(a):
    v = np.zeros(27)
    for h in H.Elements():
        v[index[str(a*h)]] = 1/np.sqrt(3)
    return v
e = G.One()
a = next(x for x in es if not bool(x in H))
v,w = coset_vector(e),coset_vector(a)
u = np.ones(27)/np.sqrt(27)
gamma = 0.4
rho = (1-gamma)*np.outer(u,u)+gamma*(np.outer(v,v)+np.outer(w,w))/2
assert np.linalg.matrix_rank(rho,tol=1e-10) == 3
reps = []
for g in es:
    R = np.zeros((27,27))
    for j,x in enumerate(es):
        R[index[str(x*g.Inverse())],j] = 1
    reps.append(R)
chi = {str(g):np.trace(R@rho) for g,R in zip(es,reps)}
for g in es:
    assert abs(chi[str(g)]-(1 if g in H else 1-gamma)) < 1e-12
ideal = np.array([[1 if y.Inverse()*x in H else 0 for y in es] for x in es],dtype=float)/27
kernel = np.array([[np.trace(Rx@rho@Ry.T) for Ry in reps] for Rx in reps])/27
formula = np.array([[chi[str(y.Inverse()*x)] for y in es] for x in es])/27
assert np.max(np.abs(kernel-formula)) < 1e-12
for t in [1,2,4,8]:
    out = (27*kernel)**int(t)/27
    assert abs(np.trace(out)-1) < 1e-12
    assert np.linalg.eigvalsh(out).min() > -1e-12
    distance = trace_distance(out,ideal)
    assert abs(distance-(1-gamma)**int(t)*(1-1/9)) < 1e-12
    assert distance <= np.sqrt(27)/2*(1-gamma)**int(t)+1e-12
print('PASS: mixed rank3 M27 state with nonnormal permutable Bose H; exact overlap law and trace bound at t=1,2,4,8.')

# Two different sections of N_G(H)/H give the same kernel, with no H<=G normality.
S = libgap.Normalizer(G,H)
assert int(S.Size()) == 9 and bool(libgap.IsNormal(S,H))
section = []
covered = set()
for x in S.Elements():
    if str(x) not in covered:
        section.append(x)
        covered.update(str(x*h) for h in H.Elements())
h0 = next(x for x in H.Elements() if x != e)
other = [x*h0 for x in section]
def section_kernel(xs):
    return np.array([[chi[str(y.Inverse()*x)] for y in xs] for x in xs])/len(xs)
assert len(section) == 3
assert np.max(np.abs(section_kernel(section)-section_kernel(other))) < 1e-12
print('PASS: two sections of N_G(H)/H agree; only normality inside S is used.')

# C2 gives decisive phase, mixed-state interpretation and independence controls.
Z = np.diag([1.,-1.])
phase_state = np.diag([0.,1.])
z = np.trace(Z@phase_state)
naive = np.array([[1,z**2],[z**2,1]])/2
flagged = np.array([[1,((1+z)/2)**2],[((1+z)/2)**2,1]])/2
assert trace_distance(naive,np.eye(2)/2) == 0.5
assert np.array_equal(flagged,np.eye(2)/2)
mixed = np.eye(2)/2
assert np.array_equal(Z@mixed@Z,mixed) and np.trace(Z@mixed) == 0
correlated = np.diag([0.5,0.,0.,0.5])
independent = np.eye(4)/4
assert np.trace(np.kron(Z,Z)@correlated) == 1
assert np.trace(np.kron(Z,Z)@independent) == 0
print('PASS: phase aliasing, conjugation-vs-Bose distinction, and correlated-copy false symmetry are detected.')
