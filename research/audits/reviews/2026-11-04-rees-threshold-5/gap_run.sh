#!/bin/sh
# Run the randomized dfs2r on every prime of a list (one per line); output appended to $2.
# Usage: sh gap_run.sh LIST OUT SEED
while read p; do nice ./dfs2r 8 $p $p 300000 nosym print rand 400 $3 >> $2 2>&1; done < $1
