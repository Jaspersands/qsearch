cd /Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-07-rees-sde-subquad-A-break
PY="nice -n 10 /opt/anaconda3/bin/python -B"
$PY attack.py conv 1 > out/conv_1.log 2>&1
$PY attack.py smallp 1 > out/smallp_1.log 2>&1
EX_SECONDS=1200 $PY exhaust.py rnd 1 > out/exhaust_rnd.log 2>&1
CLIMB_SECONDS=1200 $PY climb.py top 3 100 > out/climb_top_3.log 2>&1
echo LANE2DONE
