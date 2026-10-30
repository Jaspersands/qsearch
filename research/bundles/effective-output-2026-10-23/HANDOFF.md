# Handoff

Keep this bundle outside the moving source/staging checkout.

- Review EFFECTIVE_OUTPUT_AUDIT.md before wiring. The output is conditional
  postprocessing of a correct secret kernel, not a kernel-recovery method.
- Integrate the left-module interface only after migration verification.
  Preserve T_(xy)=T_y*T_x and the actual geometric reference-order identity.
- Keep p>3, fixed dimension, compatible model and the imported parameter
  scope explicit. Do not promote p=3 algebra controls to geometric coverage.
- The numerical scalar-field check does not prove that the input's full
  order or isogeny is defined over the claimed field.
- The twist controls are genuine small curve computations, not PPAV
  converter executions or evidence of quantum advantage.
- Do not implement a new giant geometric dilation for arbitrary endomorphisms:
  the reviewed module-conversion theorem already addresses effective output.
- After integration, run repository tests, syntax checks and qsearch.py
  validate in the verified stable checkout.

Local verification:

    env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache \
      PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python \
      -m pytest -q -p no:cacheprovider
