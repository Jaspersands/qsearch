#!/bin/zsh
P=/opt/anaconda3/bin/python
for args in \
  "5 pow:2 1 1 all" "7 pow:2 1 1 all" "11 pow:2 1 1 all" "13 pow:2 1 1 all" \
  "7 pow:3 1 1 all" "13 pow:3 1 1 all" \
  "7 pow:2 1 2 all" "11 pow:2 1 2 all" "13 pow:2 1 2 all" "7 pow:3 1 2 all" "13 pow:3 1 2 all" \
  "5 int:1 1 1 all" "7 int:1 1 1 all" "11 int:2 1 1 all" "13 int:3 1 1 all" \
  "5 int:1 1 2 all" "7 int:1 1 2 all" "11 int:2 1 2 all" "13 int:3 1 2 all" \
  "5 set:0,1 1 1 all" "7 set:0,1 1 1 all" "5 set:0,1 2 1 nest" "7 set:0,1 2 1 nest" "5 set:0,1 2 1 all" "7 set:0,1 2 1 all" "5 set:0,1 3 1 nest" \
  "3 int:1 1 1 all" "3 int:1 2 2 nest" "3 int:1 2 2 all" ; do
  $P -B gadget_cnf4.py ${=args} --quiet 2>&1 | grep -v Warning
done
