cd /Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-07-rees-sde-subquad-A-break
PY="nice -n 10 /opt/anaconda3/bin/python -B"
while pgrep -f "sh lane1.sh" >/dev/null; do sleep 20; done
$PY attack.py topstall 1 > out/topstall_1.log 2>&1
$PY cross_interesting.py 40 > out/cross_interesting.log 2>&1
echo LANE3DONE
