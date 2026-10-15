"""Known coherent sine packets: deterministic preparation, never lattice advice."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister

if __package__:
    from .lattice_qft_precision import CircuitResourcePolicy, integer, _pi_interval, PI_TERMS
else:
    from lattice_qft_precision import CircuitResourcePolicy, integer, _pi_interval, PI_TERMS


def packet_plan(bits):
    integer(bits,"positive packet width",1)
    K=1<<bits
    supported=bits<=1022
    lo,hi=_pi_interval(PI_TERMS)
    encoded=Fraction.from_float(float(np.pi))
    pi_error=max(abs(encoded-lo),abs(encoded-hi))
    weight=Fraction(33,4)-Fraction(7,K)
    return {"packet_bits":bits,"packet_side":K,"logical_qubits":2*bits,
        "clean_AND_work_qubits":bits-1,"known_flag_qubits":1,
        "W_forward_uses":2,"W_inverse_uses":1,"known_zero_reflections":1,
        "H_gates":3*bits+6,"X_gates":2*bits+3,"CCX_gates":2*(bits-1),
        "CP_gates":3*bits+1,"P_gates":bits+1,"logical_instructions":11*bits+9,
        "global_phase_pi_coefficient":"-1/4","retained_absolute_pi_weight":str(weight),
        "encoded_binary64_pi":str(encoded),"Machin_terms":PI_TERMS,
        "pi_lower":str(lo),"pi_upper":str(hi),
        "numeric_normal_angles_supported":supported,
        "encoded_rotation_operator_error_upper":str(min(Fraction(2),weight*pi_error)) if supported else None,
        "known_zero_parent_success_probability":"1","postselection_used":False,
        "flag_clear_for_arbitrary_input_claimed":False,
        "hardware_synthesis_or_simulator_roundoff_certified":False}


@dataclass
class CompiledSinePacket:
    circuit: QuantumCircuit
    data: QuantumRegister
    flag: QuantumRegister
    work: tuple
    plan: dict


def compile_packet(bits,policy=None):
    plan=packet_plan(bits)
    policy=CircuitResourcePolicy() if policy is None else policy
    if not isinstance(policy,CircuitResourcePolicy):raise ValueError("typed circuit policy required")
    policy.check(qubits=plan["logical_qubits"],QFT_instructions=plan["logical_instructions"])
    if not plan["numeric_normal_angles_supported"]:
        raise ValueError("UNKNOWN_NUMERIC_PACKET_ANGLE_RANGE")
    data,flag=QuantumRegister(bits,"packet"),QuantumRegister(1,"flag")
    work=();registers=(data,flag)
    if bits>1:
        and_register=QuantumRegister(bits-1,"and_work")
        work=tuple(and_register);registers=(data,flag,and_register)
    W=QuantumCircuit(*registers)
    W.h(data);W.h(flag[0])
    for j in range(bits):W.cp(math.ldexp(float(np.pi),j+1-bits),data[j],flag[0])
    W.h(flag[0])
    qc=QuantumCircuit(*registers)
    qc.compose(W,inplace=True);qc.p(float(np.pi/2),flag[0]);qc.compose(W.inverse(),inplace=True)
    controls=[*data,flag[0]]
    for q in controls:qc.x(q)
    if bits>1:
        qc.ccx(controls[0],controls[1],work[0])
        for j in range(1,bits-1):qc.ccx(work[j-1],controls[j+1],work[j])
        qc.cp(float(np.pi/2),work[-1],controls[-1])
        for j in range(bits-2,0,-1):qc.ccx(work[j-1],controls[j+1],work[j])
        qc.ccx(controls[0],controls[1],work[0])
    else:qc.cp(float(np.pi/2),controls[0],controls[1])
    for q in controls:qc.x(q)
    qc.compose(W,inplace=True)
    for j in range(bits):qc.p(-math.ldexp(float(np.pi),j-bits),data[j])
    qc.global_phase=-float(np.pi/4);qc.x(flag[0])
    expected={k:plan[k+"_gates"] for k in ("H","X","CCX","CP","P")}
    if {k.upper():v for k,v in qc.count_ops().items()}!={k:v for k,v in expected.items() if v}:
        raise ArithmeticError("packet gate counts disagree with closed plan")
    if len(qc.data)!=plan["logical_instructions"]:raise ArithmeticError("packet instruction count mismatch")
    return CompiledSinePacket(qc,data,flag,work,plan)


class DyadicField:
    """Bounded reference algebra Q[z]/(z^(R/2)+1); NEVER compiler inputs."""
    def __init__(self,root):
        integer(root,"dyadic reference root",4)
        if root&(root-1) or root>128:raise ValueError("UNKNOWN_EXACT_DYADIC_REFERENCE_CAP")
        self.root,self.degree=root,root//2

    def zero(self):return (Fraction(0),)*self.degree
    def scalar(self,x):return (Fraction(x),)+(Fraction(0),)*(self.degree-1)
    def add(self,a,b):return tuple(x+y for x,y in zip(a,b))
    def scale(self,a,x):return tuple(y*x for y in a)
    def monomial(self,power):
        power%=self.root;out=list(self.zero())
        out[power%self.degree]=Fraction(1 if power<self.degree else -1)
        return tuple(out)
    def multiply(self,a,b):
        out=list(self.zero())
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):
                    if y:
                        k=i+j;out[k%self.degree]+=(1 if k<self.degree else -1)*x*y
        return tuple(out)
    def conjugate(self,a):
        result=self.zero()
        for i,x in enumerate(a):result=self.add(result,self.scale(self.monomial(-i),x))
        return result
    def encode(self,a):
        a=list(a)
        while a and not a[-1]:a.pop()
        return tuple(str(x) for x in reversed(a))
    def value(self,a):return sum(float(x)*np.exp(2j*np.pi*j/self.root) for j,x in enumerate(a))


def exact_affinity(K,shift,field):
    integer(K,"dyadic packet side",2)
    if type(shift) is not int:raise ValueError("exact signed packet translation required")
    if K&(K-1) or field.root%(2*K):raise ValueError("compatible dyadic affinity field required")
    if abs(shift)>=K-1:return field.zero()
    out=field.zero();scale=field.root//(2*K)
    for x in range(max(0,shift),min(K,K+shift)):
        for exponent,sign in ((shift,1),(-shift,1),(2*x-shift,-1),(-2*x+shift,-1)):
            out=field.add(out,field.scale(field.monomial(scale*exponent),Fraction(sign,2*K)))
    return out
