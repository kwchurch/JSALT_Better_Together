#!/bin/sh

awk '$2 == 0 {printf "<td bgcolor=\"red\"><b><u>%s</u></b></td>\n", $1}
     $2 == 1 {printf "<td bgcolor=\"green\"><i>%s</i></td>\n", $1}' $* |
awk 'BEGIN {print "<table><tr>"}
   {print}
  NR % 10 == 0 {print "</tr><tr>"}
  END {print "</tr></table>"}'

#  |
# egrep '[0-9]' | 
# egrep -v Page | 
# tr -s ' ' '\t' | 
# $JSALTsrc/tsv_to_html.sh