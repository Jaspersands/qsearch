cd /Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-07-rees-sde-subquad-A-break
PY="nice -n 10 /opt/anaconda3/bin/python -B"
CLIMB_SECONDS=1500 $PY climb.py slack 1 120 > out/climb_slack_1.log 2>&1
$PY attack.py agent 1 > out/agent_1.log 2>&1
CLIMB_SECONDS=1200 $PY climb.py load 2 100 > out/climb_load_2.log 2>&1
$PY attack.py budgetC 1 > out/budgetC_1.log 2>&1
echo LANE1DONE
