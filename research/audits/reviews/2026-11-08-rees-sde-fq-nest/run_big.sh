#!/bin/zsh
# one case per argument string; each runs as its own process, no timeout
P=/opt/anaconda3/bin/python
$P -B gadget_cnf4.py ${=1} --quiet 2>&1 | grep -v Warning
