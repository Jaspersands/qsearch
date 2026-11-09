#!/bin/zsh
PY=/opt/anaconda3/bin/python
cd "${0:A:h}"
{
for args in "13 4 3 2 3" "17 4 3 2 3" "11 5 3 1 3" "11 5 3 2 2" "29 4 3 2 2" "13 4 3 3 1"; do
  $PY reduced_sde.py llev ${=args} triangular
  $PY reduced_sde.py llev ${=args} product
done
$PY reduced_sde.py llev 5 4 4 1 3 triangular
$PY reduced_sde.py llev 5 4 4 1 3 product
$PY reduced_sde.py llev 5 4 4 2 1 triangular
} 2>&1 | tee sweep_llevel.out
