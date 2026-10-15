# Clean Cube Source Arithmetic Circuit

`lattice_cube_source_circuit.py` compiles a real logical circuit using the
installed Qiskit CDKM fixed-width modular ripple-carry adder. This is not
legacy circuit search: no gates are optimized to fit toy oracle tasks.
The circuit evaluates the PUBLIC lattice cube function from the source
reference, without a shortest vector, hidden shift or preimage table.

## Exact Contract And Argument

With input(t,a), cell output z, and arithmetic workspace initially zero:

    |t,a,z,0> -> |t,a,z XOR encode_signed(F(t,a)),0>.

Each input bit controls addition of a known lattice-basis multiple into a
shared signed point accumulator. The coordinate i0 uses prime p; the colour
bit adds m*b_i0. Negative constants use two's-complement modular encoding.
The constant register is prepared and unprepared around every addition;
the CDKM fixed adder preserves that register and cleans its helper.
Subtract the public offset J_i. The exact width certificate ensures that
all partial signed sums fit: their magnitude is bounded by the sum of
absolute coefficient contributions plus W. No wrap changes the signed point.

For W=2^k copy accumulator bits k..w_i-1 into that coordinate's output.
These bits are the signed floor division, INCLUDING negative points. Run
the entire coordinate computation backward. Constants, carries, the full
physical point and discarded low remainder bits all return to zero.
The cell output and original input are not touched by this inverse.
Repeat coordinates using the same clean workspace. This proves the stated
XOR evaluator by linearity, including arbitrary superposed inputs/outputs.

The compiler also prepares the uniform parent by Hadamards on the actual
1+n*log2M input wires then the clean evaluator. It never enumerates fibres
to prepare this state. Measuring its cell outputs therefore realizes the
reference Born weights and coherent conditional two-point states when the
geometry promises hold. Wrong parameters still produce invalid fibres;
compilation does not certify the unique-SVP/source-failure promises.

## Resources And Unresolved Work

One shared w-bit constant, w-bit accumulator and helper use2w+1 workspace
qubits, plus the original inputs and signed cell outputs. There are at most
2n(n*log2M+2) constant additions including full uncomputation, each using
the explicit library's O(w) ripple structure and one optional input control.
Thus construction is polynomial in n, logM and public arithmetic bit sizes,
not in the exponential count2M^n of original source inputs. The compiler
has explicit safety caps, which are not impossibility theorems.

Finite statevector tests compare amplitudes, not merely basis truth tables:
all arithmetic workspace must be zero and no input-dependent phase may
appear. They cover signed inputs, nonzero cell output XOR, arbitrary complex
input superpositions, a measured two-point cell, and the parent inverse.
The large lattice control is COMPILED, not densely simulated. Instruction
counts are logical-library counts, not hardware/native-gate or fault-tolerant
costs. Controlled-adder synthesis and exact inverses rely on the installed
library; independent formal circuit verification remains desirable.

The earlier source reference's false compilation fields describe that
reference module only. This separate artifact establishes the clean
evaluator/uniform-parent compiler, NOT the complete position embedding,
position QFT, DCP phase-label readout or an efficient noisy DCP receiver.
Those remain next steps. The public LLL baseline still solves the calibration.
No speedup, novelty, global no-go or active negative is admitted.

Run `python theorems/lattice_cube_source_circuit.py --write`.
