import numpy as np
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

corp_dict = {}
john_dir = "/work/nlp/j.ortega/paper_recommender/semantic_scholar_specter/time_separations/"
with open(john_dir + 'uniq_dates.txt', 'r') as f:
    for line in f:
        line = line.strip()
        line_arr = line.split()
        corp_dict[int(float(line_arr[1]))] = line_arr[0]

years_file = []
with open(john_dir + 'create_100_files.cnt', 'r') as f:
    for line in f:
        line = line.strip()
        line_arr = line.split()
        years_file.append(int(line_arr[1]))

lins_arr = np.array([-9025257600, -8917199128, -8809140655, -8701082182, -8593023710,
       -8484965237, -8376906764, -8268848291, -8160789819, -8052731346,
       -7944672873, -7836614400, -7728555928, -7620497455, -7512438982,
       -7404380510, -7296322037, -7188263564, -7080205091, -6972146619,
       -6864088146, -6756029673, -6647971200, -6539912728, -6431854255,
       -6323795782, -6215737310, -6107678837, -5999620364, -5891561891,
       -5783503419, -5675444946, -5567386473, -5459328000, -5351269528,
       -5243211055, -5135152582, -5027094110, -4919035637, -4810977164,
       -4702918691, -4594860219, -4486801746, -4378743273, -4270684800,
       -4162626328, -4054567855, -3946509382, -3838450910, -3730392437,
       -3622333964, -3514275491, -3406217019, -3298158546, -3190100073,
       -3082041600, -2973983128, -2865924655, -2757866182, -2649807710,
       -2541749237, -2433690764, -2325632291, -2217573819, -2109515346,
       -2001456873, -1893398400, -1785339928, -1677281455, -1569222982,
       -1461164510, -1353106037, -1245047564, -1136989091, -1028930619,
        -920872146,  -812813673,  -704755200,  -596696728,  -488638255,
        -380579782,  -272521310,  -164462837,   -56404364,    51654109,
         159712581,   267771054,   375829527,   483888000,   591946472,
         700004945,   808063418,   916121890,  1024180363,  1132238836,
        1240297309,  1348355781,  1456414254,  1564472727,  1672531200])

year_arr = []
for val in lins_arr:
    for int_key, year_val in corp_dict.items():
        if val <= int_key:
            year_arr.append(year_val)
            break

years_dict = {}
cntr = 0
for year in year_arr:
    if year not in years_dict:
        years_dict[year] = 0
    years_dict[year] = years_dict[year] + years_file[cntr]
    cntr += 1

data_plot = pd.DataFrame({"Years": years_dict.keys(), "Papers": years_dict.values()})

ax = sns.lineplot(x="Years", y="Papers", data=data_plot)

def closest_year(year):
    return min(data_plot["Years"], key=lambda x:abs(int(x)-year))
x_ticks_positions = [data_plot[data_plot["Years"]==closest_year(label)].index[0] for label in labels]

ax.set_xticks(x_ticks_positions)
ax.set_xticklabels(labels)
ax.tick_params(axis='both', which='major', pad=15)

# Display or save the plot
plt.show()