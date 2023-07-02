import json,sys

print('authorid\tname\taffliations\tcitationcount\thindex')

for line in sys.stdin:
    rline = line.rstrip()
    j = json.loads(rline)
    print('\t'.join(map(str, [j['authorid'], 
                              j['name'],
                              j['affiliations'],
                              j['papercount'],
                              j['citationcount'],
                              j['hindex']])))
