import sys,json

j=json.loads(sys.stdin.read())
for f in j['files']:
    print(f)
