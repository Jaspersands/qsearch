"""Run exact public-label SDE controls without promoting discovery claims."""
import json


def add_prime_power_sde(subparsers):
    parser = subparsers.add_parser("prime-power-sde", help="Verify simultaneous regular SDE lifts in mixed prime-power modules")
    parser.add_argument("--write", action="store_true")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--random-kernel", action="store_true",
                        help="Use bounded randomized regular blocks without a rank-dependent prime guard")
    modes.add_argument("--span-blocks", action="store_true",
                       help="Precondition field SDEs with spanning raw-label blocks")
    modes.add_argument("--pilots", action="store_true",
                       help="Compile pilot coordinates and verify cancellation in the original module")
    modes.add_argument("--receiver-policy", action="store_true",
                       help="Check padded source-slot plans and complete-instrument falsifiers")
    modes.add_argument("--unit-kernel", action="store_true",
                       help="Test fixed-bank unit-power cancellation with paid mixed-order pilots")
    modes.add_argument("--subset-kernel", action="store_true",
                       help="Use small-prime Boolean residue completion and regular mixed-order lifting")
    modes.add_argument("--rank-reduction", action="store_true",
                       help="Check explicit Lie p-torsion and exact mixed-abelian readout controls")
    parser.set_defaults(func=command_prime_power_sde)


def command_prime_power_sde(args):
    if args.rank_reduction or args.subset_kernel or args.unit_kernel or args.receiver_policy:
        from fractions import Fraction
        if args.rank_reduction:
            from theorems.lie_torsion_reduction import report
            filename = "ring_to_field_rank_reduction.json"
        elif args.subset_kernel:
            from theorems.small_prime_module import report
            filename = "small_prime_module.json"
        elif args.unit_kernel:
            from theorems.unit_power_module import report
            filename = "unit_power_module.json"
        else:
            from theorems.pilot_receiver_policy import report
            filename = "pilot_receiver_policy.json"
        def encode(value):
            if isinstance(value,Fraction):
                return {"numerator":value.numerator,"denominator":value.denominator}
            raise TypeError(f"unsupported report value: {type(value).__name__}")
    elif args.pilots:
        from theorems.pilot_module_descent import report
        filename = "pilot_module_descent.json"
    elif args.span_blocks:
        from theorems.span_regular_sde import report
        filename = "span_regular_sde.json"
    elif args.random_kernel:
        from theorems.random_regular_sde import report
        filename = "random_regular_sde.json"
    else:
        from theorems.prime_power_rees_descent import regular_module_report as report
        filename = "prime_power_regular_sde.json"
    payload = json.dumps(report(), indent=2,default=encode if args.rank_reduction or args.subset_kernel or args.unit_kernel or args.receiver_policy else None)+"\n"
    if args.write:
        destination = args.root/"research/reductions"/filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(payload)
    print(payload, end="")
    return 0


def add_cubic_sde(subparsers):
    parser = subparsers.add_parser("cubic-sde", help="Compare cubic SDE constructions on public labels")
    parser.add_argument("--write", action="store_true")
    parser.set_defaults(func=command_cubic_sde)


def command_cubic_sde(args):
    from theorems.cubic_diagonal_solver import report
    payload = json.dumps(report(), indent=2)+"\n"
    if args.write:
        destination = args.root/"research/reductions/cubic_diagonal_solver.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(payload)
    print(payload, end="")
    return 0


def add_odd_power_sde(subparsers):
    parser = subparsers.add_parser("odd-power-sde", help="Run guarded odd-power exterior SDE controls")
    parser.add_argument("--write", action="store_true")
    parser.set_defaults(func=command_odd_power_sde)


def command_odd_power_sde(args):
    from theorems.odd_power_sde import report
    payload = json.dumps(report(), indent=2)+"\n"
    if args.write:
        destination = args.root/"research/reductions/odd_power_sde.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(payload)
    print(payload, end="")
    return 0


def add_power_sde(subparsers):
    parser = subparsers.add_parser("power-sde", help="Run large-field symmetric power-SDE controls")
    parser.add_argument("--write", action="store_true")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--bounded-randomness", action="store_true",
                        help="Cap root splitting and bit rejection under one failure budget")
    modes.add_argument("--rees-budget", action="store_true",
                       help="Compute whole-grade Rees source and randomness bounds, not a receiver run")
    modes.add_argument("--codimension-budget", action="store_true",
                       help="Compute conditional hybrid codimension bounds, not an HSP solver run")
    modes.add_argument("--uniform-instrument", action="store_true",
                       help="Count uniform Rees Fourier/arithmetic primitives, not emitted circuits")
    modes.add_argument("--random-column", action="store_true",
                       help="Test fixed-bank power-kernel search and conditional IID Rees bounds")
    modes.add_argument("--coherent-gram", action="store_true",
                       help="Run filiform invariant-Gram controller controls, not quantum execution")
    parser.set_defaults(func=command_power_sde)


def command_power_sde(args):
    if args.coherent_gram:
        from theorems.invariant_gram_selector import report
        filename = "invariant_gram_selector.json"
    elif args.random_column:
        from theorems.random_column_rees_budget import report
        filename = "random_column_rees.json"
    elif args.uniform_instrument:
        from theorems.rees_uniform_instrument import report
        filename = "rees_uniform_instrument.json"
    elif args.codimension_budget:
        from theorems.codimension_hybrid_budget import report
        filename = "codimension_hybrid_budget.json"
    elif args.rees_budget:
        from theorems.uniform_bch_rees import symmetric_rees_report as report
        filename = "rees_full_grade_budget.json"
    elif args.bounded_randomness:
        from theorems.power_sde_budget import report
        filename = "power_sde_bounded_randomness.json"
    else:
        from theorems.power_sde import report
        filename = "power_sde.json"
    from fractions import Fraction
    def encode(value):
        if isinstance(value, Fraction):
            return {"numerator": value.numerator, "denominator": value.denominator}
        raise TypeError(f"unsupported report value: {type(value).__name__}")
    payload = json.dumps(report(), indent=2, default=encode)+"\n"
    if args.write:
        destination = args.root/"research/reductions"/filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(payload)
    print(payload, end="")
    return 0


def add_phase_copy_baseline(subparsers):
    parser = subparsers.add_parser("phase-copy-baseline", help="Audit copy-only phase-learning resource bounds")
    parser.add_argument("--write", action="store_true")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--phase-noise", action="store_true",
                       help="Check exterior-state public maps for finite-support phase noise")
    modes.add_argument("--peaked-noise", action="store_true",
                       help="Check peak-weight source bounds without a low-rank noise promise")
    modes.add_argument("--pauli-symmetry", action="store_true",
                       help="Check purity-gap full Pauli conjugation symmetry bounds")
    modes.add_argument("--partition-source", action="store_true",
                       help="Run the matched classical query-and-discard source filter")
    parser.set_defaults(func=command_phase_copy_baseline)


def command_phase_copy_baseline(args):
    directory = "reductions"
    if args.partition_source:
        from theorems.partition_source_filter import report
        filename = "partition_source_filter.json"
        directory = "classical_baselines"
    elif args.pauli_symmetry:
        from theorems.pauli_symmetry_source import report
        filename = "pauli_symmetry_source.json"
    elif args.peaked_noise:
        from theorems.peaked_phase_source import report
        filename = "peaked_phase_source.json"
    elif args.phase_noise:
        from theorems.exterior_phase_learning import report
        filename = "exterior_phase_learning.json"
    else:
        from theorems.polynomial_phase_copy_learning import report
        filename = "polynomial_phase_copy_learning.json"
    payload = json.dumps(report(), indent=2,
                         default=lambda x: {"numerator": x.numerator, "denominator": x.denominator})+"\n"
    if args.write:
        destination = args.root/"research"/directory/filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(payload)
    print(payload, end="")
    return 0
