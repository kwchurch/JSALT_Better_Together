import numpy as np
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

corp_dict={}
with open('uniq_dates.txt', 'r') as f:
    for line in f:
        line = line.strip()
        line_arr = line.split()
        corp_dict[int(float(line_arr[1]))] = line_arr[0]

years_file = []
with open('create_100_files.cnt', 'r') as f:
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
#print(year_arr)
#print(years_file)

# the year_arr had duplicate years in it so we need to sum up
# year_arr has the year and years_file has the count
years_dict = {}

cntr = 0
for year in year_arr:
    if year not in years_dict:
        years_dict[datetime.date(int(year),1,1)] = 0
    years_dict[datetime.date(int(year),1,1)] = years_dict[datetime.date(int(year),1,1)] + years_file[cntr]
    cntr+=1
#print(years_dict)






data_plot = pd.DataFrame({"Years":years_dict.keys(), "Papers":years_dict.values()})

#ax = sns.lineplot(x = "Years", y = "Papers", data=data_plot)
#ax.set_xticks(9, rotation = 45, ha = 'right')
# set the labels
#ax.set_xticklabels([1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000, 2050])
#ax.set_xlim(datetime.date(2022, 1, 1))
#fig.autofmt_xdate()
# set visible false
# ax.tick_params(axis='both', which='major', pad=15)


fig, ax = plt.subplots(figsize=(15,8))
sns.lineplot(data=data_plot, x='Years', y='Papers', ci=None, ax=ax)
sns.set_style("white")
sns.set_style('ticks')
ax.set_xlabel("Years")
ax.set_ylabel("Papers")
#ax.set_xlim([datetime.date(1640, 12, 31), datetime.date(2023, 12, 31)])
ax.set_xlim([datetime.date(1640, 1, 1), datetime.date(2023, 1, 1)])
fig.autofmt_xdate()
plt.savefig("seaborn_plot.png")

#https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.tick_params.html
#https://stackoverflow.com/questions/54822884/how-to-change-the-x-axis-range-in-seaborn


