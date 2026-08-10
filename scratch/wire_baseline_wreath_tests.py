import re

BASELINE_16 = [
    (
        "self_dual_wreath_all_unequal_third_moment",
        "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-THIRD-MOMENT",
        "test_wreath_all_unequal_third_moment_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_carrier_orbit_growth",
        "EXP-CODE-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH",
        "test_wreath_carrier_orbit_growth_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_character_moments",
        "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-MOMENTS",
        "test_wreath_character_moments_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_commutant_transfer_audit",
        "EXP-CODE-SELF-DUAL-WREATH-COMMUTANT-TRANSFER-AUDIT",
        "test_wreath_commutant_transfer_audit_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_complete_w3_tuple_audit",
        "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-W3-TUPLES",
        "test_wreath_complete_w3_tuples_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_equal_commutator_audit",
        "EXP-CODE-SELF-DUAL-WREATH-EQUAL-COMMUTATOR-AUDIT",
        "test_wreath_equal_commutator_audit_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_harmonic_carrier_schema",
        "EXP-CODE-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA",
        "test_wreath_harmonic_carrier_schema_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_pgm_polar_audit",
        "EXP-CODE-SELF-DUAL-WREATH-PGM-POLAR-AUDIT",
        "test_wreath_pgm_polar_audit_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_physical_frame_blocks",
        "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCKS",
        "test_wreath_physical_frame_blocks_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_spectrum",
        "EXP-CODE-SELF-DUAL-WREATH-SPECTRUM",
        "test_wreath_spectrum_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_stable_commutator_rank",
        "EXP-CODE-SELF-DUAL-WREATH-STABLE-COMMUTATOR-RANK",
        "test_wreath_stable_commutator_rank_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_subset_carrier_algebra",
        "EXP-CODE-SELF-DUAL-WREATH-SUBSET-CARRIER-ALGEBRA",
        "test_wreath_subset_carrier_algebra_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_third_moment_contraction",
        "EXP-CODE-SELF-DUAL-WREATH-THIRD-MOMENT-CONTRACTION",
        "test_wreath_third_moment_contraction_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_typical_partition_portfolio",
        "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-PARTITION-PORTFOLIO",
        "test_wreath_typical_partition_portfolio_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_typical_recoupling_transfer",
        "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-RECOUPLING-TRANSFER",
        "test_wreath_typical_recoupling_transfer_dispatches_from_clean_registry",
    ),
    (
        "self_dual_wreath_unequal_frame_blocks",
        "EXP-CODE-SELF-DUAL-WREATH-UNEQUAL-FRAME-BLOCKS",
        "test_wreath_unequal_frame_blocks_dispatches_from_clean_registry",
    ),
]


def add_baseline_tests():
    with open("tests/test_experiment_runner.py") as f:
        code = f.read()

    new_methods = []
    for mod_name, exp_id, test_func_name in BASELINE_16:
        if test_func_name in code:
            continue
        method = f"""    def {test_func_name}(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "{exp_id}"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "{mod_name}",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])\n\n"""
        new_methods.append(method)

    if new_methods:
        target = '\nif __name__ == "__main__":'
        inserted_code = "".join(new_methods) + "\n"
        code = code.replace(target, inserted_code + target)
        with open("tests/test_experiment_runner.py", "w") as f:
            f.write(code)
        print(f"Added {len(new_methods)} baseline unit tests inside ExperimentRunnerTests class!")
    else:
        print("All baseline unit tests already present.")


if __name__ == "__main__":
    add_baseline_tests()
