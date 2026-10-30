"""Certified public-label coordinates, not quantum source certification.

For G=[D B], L=G Z^m and a column basis H of L, C'=L/D Z^R.
If U*(H^-1 D)*V=S, intrinsic coordinates are U*H^-1*label mod S.
The embedding is H*U^-1, not V. Both lattice containments are retained.
"""
from dataclasses import asdict, dataclass
from functools import cached_property
from math import prod

from flint import fmpq_mat, fmpz_mat
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

from theorems.prime_power_rees_descent import _module_contract


def _rows(matrix):
    return tuple(tuple(int(x) for x in row) for row in matrix.tolist())


def _integer(matrix):
    if any(x.denominator != 1 for row in matrix.tolist() for x in row):
        raise ArithmeticError("nonintegral lattice containment")
    return fmpz_mat(_rows(matrix))


def _diagonal(values):
    return fmpz_mat([[v if i==j else 0 for j in range(len(values))] for i,v in enumerate(values)])


def _matrix(rows, height, width):
    if (len(rows)!=height or any(len(row)!=width for row in rows)
            or any(type(x) is not int for row in rows for x in row)):
        raise ValueError("exact integer matrix of certificate dimensions required")
    return fmpz_mat(rows)


def _ambient(prime, exponents):
    exponents = tuple(exponents)
    _,exponents,moduli = _module_contract([(0,)*len(exponents)],exponents,prime,1)
    return exponents,moduli


@dataclass(frozen=True)
class PilotFrame:
    prime: int
    ambient_exponents: tuple
    pilot_columns: tuple
    lattice_basis: tuple
    basis_from_generators: tuple
    generators_from_basis: tuple
    relation_matrix: tuple
    smith_left: tuple
    smith_right: tuple
    smith_orders: tuple

    @property
    def active_indices(self):
        return tuple(i for i,s in enumerate(self.smith_orders) if s>1)

    @property
    def intrinsic_exponents(self):
        result = []
        for i in self.active_indices:
            order,exponent = self.smith_orders[i],0
            while order>1 and order%self.prime==0:
                order //= self.prime
                exponent += 1
            if order!=1:
                raise ArithmeticError("Smith factor is not a prime power")
            result.append(exponent)
        return tuple(result)

    @cached_property
    def _inverse_lattice(self):
        return fmpq_mat(self.lattice_basis).inv()

    @cached_property
    def _embedding(self):
        left = fmpz_mat(self.smith_left)
        # Installed FLINT's integer=True path loses the sign when det=-1.
        inverse = _integer(fmpq_mat(left).inv())
        identity = _diagonal([1]*len(self.ambient_exponents))
        if left*inverse!=identity or inverse*left!=identity:
            raise ArithmeticError("Smith inverse failed exact identity check")
        return fmpz_mat(self.lattice_basis)*inverse

    def encode(self, label):
        """Return intrinsic coordinates or None for a nonmember of C'."""
        label = tuple(label)
        _module_contract([label],self.ambient_exponents,self.prime,1)
        coordinates = self._inverse_lattice*fmpq_mat([[x] for x in label])
        if any(row[0].denominator!=1 for row in coordinates.tolist()):
            return None
        transformed = fmpz_mat(self.smith_left)*_integer(coordinates)
        result = tuple(int(transformed[i,0])%self.smith_orders[i] for i in self.active_indices)
        if self.decode(result)!=label:
            raise ArithmeticError("intrinsic coordinates failed ambient roundtrip")
        return result

    def decode(self, coordinates):
        coordinates = tuple(coordinates)
        active = self.active_indices
        if (len(coordinates)!=len(active) or any(type(x) is not int or not 0<=x<self.smith_orders[i]
                                                for x,i in zip(coordinates,active))):
            raise ValueError("canonical intrinsic coordinates required")
        vector = [0]*len(self.ambient_exponents)
        for i,x in zip(active,coordinates):
            vector[i] = x
        ambient = self._embedding*fmpz_mat([[x] for x in vector])
        return tuple(int(ambient[i,0])%self.prime**e for i,e in enumerate(self.ambient_exponents))

    def certificate(self):
        verify_pilot_frame(self)
        return dict(asdict(self),intrinsic_exponents=self.intrinsic_exponents,
                    subgroup_order=prod(self.smith_orders),certificate_verified=True,
                    hidden_support_completeness_certified=False)


def verify_pilot_frame(frame):
    """Check algebraic certificates without rerunning HNF/SNF or enumeration."""
    if not isinstance(frame,PilotFrame):
        raise ValueError("PilotFrame certificate required")
    exponents,moduli = _ambient(frame.prime,frame.ambient_exponents)
    r = len(exponents)
    pilots = tuple(tuple(c) for c in frame.pilot_columns)
    if pilots:
        _module_contract(pilots,exponents,frame.prime,1)
    D = _diagonal(moduli)
    G = fmpz_mat(list(D.tolist())+list(pilots)).transpose()
    H = _matrix(frame.lattice_basis,r,r)
    F = _matrix(frame.basis_from_generators,r+len(pilots),r)
    Q = _matrix(frame.generators_from_basis,r,r+len(pilots))
    T = _matrix(frame.relation_matrix,r,r)
    U,V = _matrix(frame.smith_left,r,r),_matrix(frame.smith_right,r,r)
    orders = frame.smith_orders
    if (len(orders)!=r or any(type(s) is not int or s<1 for s in orders)
            or any(b%a for a,b in zip(orders,orders[1:]))):
        raise ArithmeticError("positive ordered Smith factors required")
    if H.det()==0 or G*F!=H or H*Q!=G or H*T!=D:
        raise ArithmeticError("two-way lattice/relation certificate failed")
    if abs(U.det())!=1 or abs(V.det())!=1 or U*T*V!=_diagonal(orders):
        raise ArithmeticError("unimodular Smith transformation certificate failed")
    if (any(e>max(exponents) for e in frame.intrinsic_exponents)
            or prod(orders)*abs(int(H.det()))!=prod(moduli)):
        raise ArithmeticError("subgroup exponent/order certificate failed")
    for column in pilots:
        if frame.encode(column) is None:
            raise ArithmeticError("pilot not represented in certified frame")
    for k,e in enumerate(frame.intrinsic_exponents):
        unit = [0]*len(frame.active_indices)
        unit[k] = 1
        generator = frame.decode(unit)
        if (any(x*frame.prime**e%m for x,m in zip(generator,moduli))
                or not any(x*frame.prime**(e-1)%m for x,m in zip(generator,moduli))):
            raise ArithmeticError("embedded cyclic generator has wrong exact order")
    return True


def compile_pilot_frame(*, prime, ambient_exponents, pilot_columns):
    exponents,moduli = _ambient(prime,ambient_exponents)
    pilots = tuple(tuple(c) for c in pilot_columns)
    if pilots:
        _module_contract(pilots,exponents,prime,1)
    r = len(exponents)
    D = _diagonal(moduli)
    generator_rows = fmpz_mat(list(D.tolist())+list(pilots))
    reduced,transform = generator_rows.hnf(transform=True)
    H = fmpz_mat(reduced.tolist()[:r]).transpose()
    F = fmpz_mat(transform.tolist()[:r]).transpose()
    inverse = fmpq_mat(H).inv()
    Q = _integer(inverse*fmpq_mat(generator_rows.transpose()))
    T = _integer(inverse*fmpq_mat(D))
    domain = DomainMatrix([[ZZ(int(x)) for x in row] for row in T.tolist()],(r,r),ZZ)
    smith,left,right = smith_normal_decomp(domain)
    S,U,V = (fmpz_mat([[int(x) for x in row] for row in m.to_list()]) for m in (smith,left,right))
    for i in range(r):
        if S[i,i]<0:
            for j in range(r):
                S[i,j],U[i,j] = -S[i,j],-U[i,j]
    frame = PilotFrame(prime,exponents,pilots,_rows(H),_rows(F),_rows(Q),_rows(T),
                       _rows(U),_rows(V),tuple(int(S[i,i]) for i in range(r)))
    verify_pilot_frame(frame)
    return frame
