cd /Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-07-rees-sde-subquad-A-break
PY="nice -n 10 /opt/anaconda3/bin/python -B"
while pgrep -f "sh lane2.sh" >/dev/null; do sleep 20; done
$PY attack.py smallp 2 > out/smallp_2.log 2>&1
EX_SECONDS=1200 $PY exhaust.py rnd 2 > out/exhaust_rnd_2.log 2>&1
echo LANE4DONE
