#!/bin/zsh
# Re-run referee C's 64 LRAT-checked runs (2026-11-09-rees-sde-fq-nest-referee-C/*.out) with the
# fixed lrat-check. The commands are the referee's own (taken from its session log), with nice 19
# instead of 10 and LRAT_CHECK set to ../lrat-check. Outputs: refC/<same file names>; compare with
# refC_compare.py. usage: WORK=<scratch dir> ./refC_rerun.sh
set -u
D=${0:A:h}; R=${D:h}; REV=${R:h}
RC=$REV/2026-11-09-rees-sde-fq-nest-referee-C; FQ=$REV/2026-11-08-rees-sde-fq-nest
export LRAT_CHECK=$R/lrat-check
O=$D/refC; mkdir -p $O
W=${WORK:?set WORK to a scratch directory}/refC; mkdir -p $W
P=/opt/anaconda3/bin/python
$R/controls.sh $LRAT_CHECK - > $W/controls_pre.out || { print "controls failed; stop"; exit 1; }
print "start $(date); checker sha256 $(shasum -a 256 $LRAT_CHECK | cut -c1-16); $(tail -1 $W/controls_pre.out)"
cd $RC
( while read c; do nice -n 19 $P -B free_cnf.py 7 pow:2 2 nest --proof --fix "$c"; done < $FQ/cases7.txt
  while read c; do nice -n 19 $P -B free_cnf.py 7 pow:2 2 all --proof --fix "$c"; done < $FQ/cases7.txt ) > $O/free_p7_k2.out 2>&1
( while read c; do nice -n 19 $P -B free_cnf.py 7 pow:2 2 nest --noR --proof --fix "$c"; done < $FQ/cases7.txt ) > $O/free_p7_k2_noR.out 2>&1
nice -n 19 $P -B free_cnf.py 7 pow:3 2 nest --proof > $O/free_p7_k3kappa.out 2>&1
for a in "11 int:2 1 all" "13 int:3 1 all" "7 int:1 2 nest" "5 int:1 2 nest"; do
  timeout 900 nice -n 19 $P -B free_cnf.py ${=a} --proof; done > $O/free_interval.out 2>&1
cd $FQ
: > $O/rerun_k3_7.out
for f in "1,0,1:0,0,0" "1,0,1:3,0,0;1,1,0:2,5,1" "1,0,1:0,3,0;1,1,0:4,0,6"; do
  timeout 900 nice -n 19 $P -B gadget_cnf5.py 7 pow:2 3 2 nest --quiet --work $W --fix "$f" >> $O/rerun_k3_7.out 2>&1; done
print "end $(date)"
