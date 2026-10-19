"""The qsearch command-line interface, split out of the former 30,000-line qsearch.py.

``qsearch.py`` stays the entry point. It is now a short shim: ``build_parser`` and ``main``
come from here, and any name the old module defined or imported still resolves as
``qsearch.<name>`` when it is used.

- ``registry.py``: every subcommand (in --help order), every command function, every flag.
- ``commands/<domain>.py``: the subcommands themselves, one module per research domain.
- ``imports.py``: the names qsearch.py used to import eagerly, now imported on first use.
- ``legacy.py``: binds the former globals that old-style code in qsearch.py reads.

See tools/split_cli/README.md for how this was generated and how to add a command.
"""
