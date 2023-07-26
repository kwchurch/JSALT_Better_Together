#!/bin/sh

awk '$2 == 1 {col="green"};
     $2 == 0 {col="red"};
    {printf "<td bgcolor=\"%s\">%s</td>\n", col, $1}' $* |
awk 'BEGIN {print "<table><tr>"}
   {print}
  NR % 10 == 0 {print "</tr><tr>"}
  END {print "</tr></table>"}'

#  |
# egrep '[0-9]' | 
# egrep -v Page | 
# tr -s ' ' '\t' | 
# $JSALTsrc/tsv_to_html.sh
