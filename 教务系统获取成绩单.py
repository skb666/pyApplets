import requests
import time
import base64
import rsa
import csv
from bs4 import BeautifulSoup as bs


def getScores(username, password):
    #站点访问需要的信息
    website = {
        "publickey": {
            "url": f"https://jwxt.cjlu.edu.cn/xtgl/login_getPublicKey.html?time={str(time.time()).replace('.','')[:13]}",
            "headers": {
                "Host": "jwxt.cjlu.edu.cn",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://jwxt.cjlu.edu.cn/xtgl/login_slogin.html",
                "X-Requested-With": "XMLHttpRequest",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "no-cors",
                "Sec-Fetch-Site": "same-origin",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
            },
        },
        "login": {
            "url": "https://jwxt.cjlu.edu.cn/xtgl/login_slogin.html",
            "headers": {
                "Host": "jwxt.cjlu.edu.cn",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0",
            },
        },
        "scores": {
            "url": f"https://jwxt.cjlu.edu.cn/cjcx/cjcx_cxXsKcList.html?gnmkdm=N305007&su={username}",
            "headers": {
                "Host": "jwxt.cjlu.edu.cn",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": f"https://jwxt.cjlu.edu.cn/cjcx/cjcx_cxDgXsxmcj.html?gnmkdm=N305007&layout=default&su={username}",
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://jwxt.cjlu.edu.cn",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "no-cors",
                "Sec-Fetch-Site": "same-origin",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
            },
            "data": {
                "_search": "false",
                "nd": f"{str(time.time()).replace('.','')[:13]}",
                "queryModel.showCount": "300",
                "queryModel.currentPage": "1",
                "queryModel.sortOrder": "asc",
                "time": "1"
            },
        },
    }

    #新建Session
    session = requests.Session()

    try:
        #获取公钥需要的参数
        publickey = session.get(url=website["publickey"]["url"], headers=website["publickey"]["headers"]).json()
        b_modulus = base64.b64decode(publickey['modulus'])      #将base64解码转为bytes
        b_exponent = base64.b64decode(publickey['exponent'])    #将base64解码转为bytes
        #公钥生成,python3从bytes中获取int:int.from_bytes(bstring,'big')
        mm_key = rsa.PublicKey(int.from_bytes(b_modulus,'big'),int.from_bytes(b_exponent,'big'))
        #利用公钥加密,bytes转为base64编码
        rsa_mm = base64.b64encode(rsa.encrypt(password, mm_key))
        #获取认证口令csrftoken
        page = session.get(url=website["login"]["url"], headers=website["login"]["headers"])
        soup = bs(page.text,"html.parser")
        csrftoken = soup.find(id="csrftoken").get("value")

        #登入
        postdata = {'csrftoken': csrftoken, 'yhm': username, 'mm': rsa_mm}
        reponse = session.post(url=website["login"]["url"], headers=website["login"]["headers"], data=postdata)

        #获取成绩明细
        response = session.post(website["scores"]["url"], headers=website["scores"]["headers"], data=website["scores"]["data"])

        #解析、存表
        if 200 == response.status_code:
            xf_z = 0
            scores = response.json()['items']
            with open(f"{username[-4:]}_{str(time.time())[4:10]}.csv", 'w', encoding='utf-8', newline='') as f_obj:
                csv_writer = csv.writer(f_obj)
                csv_writer.writerow(["学年", "学期", "开课学院", "课程代码", "课程名称", "教学班", "学分", "总评"])
                for score in scores:
                    xf_z += float(score.get("xf", "0"))
                    csv_writer.writerow([score.get("xnmmc", None), score.get("xqmmc", None), \
                                         score.get('kkbmmc', None), score.get("kch", None), \
                                         score.get("kcmc", None), score.get("jxbmc", None), \
                                         score.get("xf", None), score.get("zpcj", None)])
            print(f"获取成功 (^ v ^)\n\t{username}的总学分为： {xf_z}")
        else:
            print("成绩获取失败 (V ~ V)")
    except Exception as err:
        print(f"出错啦！\n{err}")

    del session


if __name__ == '__main__':
    #学号 | 密码
    account = [
        ("1832331405", b"我的密码"),
        ("1832331431", b"你的密码"),
    ]

    for username, password in account:
        getScores(username, password)
