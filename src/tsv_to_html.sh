#!/bin/sh

awk -F'\t' 'NR == 1 { print("<html><table><tr>"); 
               for(i=1;i<=NF;i++) print("<th>" $i "</th>"); print("</tr>")}
     NR > 1 { print("<tr>"); for(i=1;i<=NF;i++) print("<td>" $i "</td>"); print("</tr>")}
     END { print "</table></html>" }' $*

