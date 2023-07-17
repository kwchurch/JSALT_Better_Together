#!/usr/bin/bash
irvingsrc='/work/nlp/b.irving/prone/prone_benchmarks'
# where the graphs are stored
u_graphs='/scratch/k.church/JSALT-2023/semantic_scholar/j.ortega/cumgraphs.V2'
cumgraphs='/work/k.church/JSALT-2023/semantic_scholar/j.ortega/cumgraphs.V2'
benscratch='/scratch/irving.b/JSALT'
cd $benscratch
K=280
iteration=10
glim=0

date=$(date +'%m%d%Y')
generate_run_id=$(date +%s%N | sha256sum | head -c 10)
# Extract the first 6 characters to get the 6-digit hash
run_id=${generate_run_id:0:6}
for ((g=0; g<=$glim; g+=2))
   do 
      output=/scratch/irving.b/JSALT/finish_actual
      cheby=/scratch/irving.b/JSALT/cheby_actual
      cd $cheby
      graph_prefix=$(printf "%03d" $g).sym.shrunk.G2.npz
      u_graph=$(printf "%03d" $g).sym.shrunk.G2.U.K280.npy
      temp_prefix=$(printf "%03d" $g)
      output_prefix=$(printf "%03d" $g).sym.shrunk.G2.O.K280
      for ((i=0; i<=$iteration; i++))
         do
            iter=$(printf "%03d" $i)
            filename=$temp_prefix"_"$iter"_"$run_id
            if [ -e $u_graphs/$u_graph ] && [ -e $cumgraphs/$graph_prefix ]; then
               time_input=$(echo "0.2432 * $g + 37.17 * $g + 1000" | bc)

               rounded_time=$(echo "scale=0; ($time_input+0.5)/1" | bc)
               #formatted_time=$(date -u -d @${rounded_time} +"%T")

               mem=$(echo "-0.01273 * $g + 6.693 * $g" | bc)
               rounded_mem=$(echo "scale=0; ($mem+0.5)/1" | bc)"G"
               
               finish_time_input=$(echo "1.76 * $g + 43.87 * $g + 126.5 + 1000" | bc)
               rounded_finish_time=$(echo "scale=0; ($finish_time_input+0.5)/1" | bc)

               total_time=$((rounded_time + rounded_finish_time))
               formatted_finish_time=$(date -u -d @${total_time} +"%T")
               echo $formatted_finish_time

               finish_mem=$(echo "0.02269 * $g + 8.012 * $g + 5" | bc)
               rounded_finish_mem=$(echo "scale=0; ($finish_mem+0.5)/1" | bc)"G"

               if [ $i == 0 ]
               then
               job=`sbatch --mem=$rounded_finish_mem -p short --time=$formatted_finish_time --output=$cheby/$filename-%j.out $irvingsrc/run_finish_cheby.py -G $cumgraphs/$graph_prefix -U $u_graphs/$u_graph --temp_file_prefix $temp_prefix"_"$run_id --iteration $i -O $output/$output_prefix".i$i" | awk '{print $NF}'`
               jobnext=$job
               echo $job
               else
               job=`sbatch --mem=$rounded_finish_mem -d afterany:$jobnext -p short --time=$formatted_finish_time --output=$cheby/$filename-%j.out $irvingsrc/run_finish_cheby.py -G $cumgraphs/$graph_prefix -U $u_graphs/$u_graph --temp_file_prefix $temp_prefix"_"$run_id --iteration $i -O $output/$output_prefix".i$i" | awk '{print $NF}'`
               jobnext=$job
               echo $job
               fi
            fi
        done
done