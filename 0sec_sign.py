# -*- coding:utf-8 -*-

import requests
import base64
import json

base64_image =''
base64_uuid =''
SCKEY=''#Server酱申请的skey


def get_code_uuid():

    global base64_image,base64_uuid
    code_url = "https://wiki.0-sec.org/api/user/captchaImage"
    code_image = requests.get(code_url)
    json_data = json.loads(code_image.content)
    base64_image = json_data['data']['img']
    base64_uuid = json_data['data']['uuid']
    


def base64_api():

    global base64_image,base64_uuid
    b64 = base64_image
    data = {"username": "", "password": "", "image": b64}##你的验证码api账户，需要去ttshitu.com打码平台注册充值
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        print("验证码识别抽风了，再执行一遍吧")

def login(uuid):
    username = ""#文库用户名
    password = ""#文库密码
    headers = {'Accept': 'application/json, text/plain, */*','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36','Content-Type': 'application/json;charset=UTF-8','Accept-Encoding': 'gzip, deflate','Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
    url = "https://wiki.0-sec.org/api/user/login"
    login_data = {"account":username,"password":password,"code":base64_api(),"uuid":uuid}##字典
    data_json = json.dumps(login_data)##转json格式
    logins = requests.post(url=url,headers=headers,data=data_json)
    token = json.loads(logins.content)['data']['token']

    return token

def sign(token):
    headers = {'Zero-Token':token}
    url = "https://wiki.0-sec.org/api/profile"
    old_sign_data_json = requests.get(url=url,headers=headers)
    print(old_sign_data_json.content)
    old_sign_data_credit = json.loads(old_sign_data_json.content)['data']['credit']

    url1 = "https://wiki.0-sec.org/api/front/user/sign"
    requests.post(url=url1, headers=headers)

    new_sign_data_json = requests.get(url=url, headers=headers)
    new_sign_data_credit = json.loads(new_sign_data_json.content)['data']['credit']

    if new_sign_data_credit > old_sign_data_credit:
        print("签到成功，您的当前积分为：",new_sign_data_credit)
        datamsg={"text":"0sec文库签到成功！您的当前积分为：","desp":new_sign_data_credit}
    else:
        print("兄弟，你已经签到过了，你的积分为：",new_sign_data_credit)
        datamsg={"text":"0sec文库签到失败！您的当前积分为：","desp":new_sign_data_credit}
    if datamsg:
        requests.post("https://sc.ftqq.com/"+SCKEY+".send",data=datamsg)

def main():
    get_code_uuid()
    tokens = login(base64_uuid)
    sign(tokens)

def main_handler(event, context):
    return main()
if __name__ == '__main__':
    main()
