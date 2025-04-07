#!/usr/bin/env python

import requests,sys

# import httplib2,sys
# from urllib.parse import urlparse

# def checkUrl(url):
#     p = urlparse(url)
#     conn = httplib2.HTTPConnection(p.netloc)
#     conn.request('HEAD', p.path)
#     resp = conn.getresponse()
#     return resp.status < 400

def url_exists(url):
    r = requests.head(url)
    return r.status_code

if __name__ == '__main__':
    for line in sys.stdin:
        rline = line.strip()
        print(str(url_exists(line)) + '\t' + rline)

