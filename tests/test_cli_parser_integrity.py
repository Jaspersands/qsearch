"""The CLI must construct before any scientific workflow can run."""

from pathlib import Path

import qsearch


def test_cli_source_compiles_with_legal_future_import_order():
    path = Path(qsearch.__file__)
    compile(path.read_bytes(), str(path), "exec")


def test_parser_builds_and_preserves_the_integrated_swap_command():
    # argparse raises on duplicate registration during build_parser itself.
    parser=qsearch.build_parser()
    validation=parser.parse_args(["validate"])
    assert validation.func is qsearch.command_validate
    swap=parser.parse_args(["native-higher-call-two-copy-swap-purity-bridge","--no-write"])
    assert swap.no_write is True
    assert swap.func is qsearch.command_native_higher_call_two_copy_swap_purity_bridge
