#!/usr/bin/python

import httplib
import urllib

def httpGetRequest(url):
    print "====================="
    print "GET %s" % url
    httpClient.request('GET', url)
    response = httpClient.getresponse()
    print response.status
    print response.reason
    print response.read()
   
def httpPostRequest():
    print "====================="
    print "POST"
    params = urllib.urlencode({'@number': 12524, 
                               '@type': 'issue', '@action': 'show'})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    httpClient.request("POST", "", params, headers)
    response = httpClient.getresponse()
    print response.status
    print response.reason
    print response.read()

try:
    httpClient = httplib.HTTPConnection('localhost', 8000, timeout=30)
    httpGetRequest("/fib/1")
    httpGetRequest("/fib/5")
    httpGetRequest("/fib/100")

    httpGetRequest("/fib/1.1")
    httpGetRequest("/fib/-1")
    httpGetRequest("/fib/hello")
    httpGetRequest("/fib/10001")

    httpPostRequest()

except Exception, e:
    print e
finally:
    if httpClient:
        httpClient.close()
