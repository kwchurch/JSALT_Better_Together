
year_int_dict = {}
with open('uniq_dates.txt', 'r') as f:
    for line in f:
        line = line.strip()
        line_arr = line.split()
        year = line_arr[0]
        integ = line_arr[1]
        year_int_dict[year] = integ

with open('corp_by_date.tsv', 'r') as f:
    for line in f:
        line = line.strip()
        line_arr = line.split('\t')
        if line_arr[0]:
            if len(line_arr[0]) > 0:
                corp_id = line_arr[0]
                year = line_arr[2]
                if year in year_int_dict:
                    print(line,'\t',year_int_dict[year])

