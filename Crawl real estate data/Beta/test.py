import requests
from datetime import datetime


def get_access_token():
    ask_url = "https://api.weixin.qq.com/cgi-bin/token?"
    params = {
        "grant_type": "client_credential",
        "appid": "wx8dc9b83b9a5720ac",                 # AppId
        "secret": "cb8aeffb8e8d5b477b7ad97379aadfbc",  # AppSecret
    }
    # ip: 183.11.219.52
    resp = requests.get(ask_url, params=params)
    data = resp.json()
    print(data)
    # print(access_token)
    return data["access_token"]


def get_openid(ACCESS_TOKEN):
    ask_url = "https://api.weixin.qq.com/cgi-bin/user/get?"
    params = {
        "access_token": ACCESS_TOKEN,
        # "access_token": "73_6rZx9P1kNQfF1NEBdLaa5DX1uJaZ1QOkutNxeDqbMl4J_bzm2kNgaiM-k0zyslaILYyyZbRXw7OFI21-lFLWIAP9U1hurfi7UhUd88t54X1osk1FD0tjG42il0sNIFeAHAQLI",
    }
    resp = requests.get(ask_url, params=params)
    data = resp.json()['data']
    openid = data['openid']   # type: list
    # print(openid)
    return openid


def send_message(ACCESS_TOKEN):
    send_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?"
    tran_url = "http://www.szdatamining.com"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # access_token = "73_6rZx9P1kNQfF1NEBdLaa5DX1uJaZ1QOkutNxeDqbMl4J_bzm2kNgaiM-k0zyslaILYyyZbRXw7OFI21-lFLWIAP9U1hurfi7UhUd88t54X1osk1FD0tjG42il0sNIFeAHAQLI"
    # openid_list = get_openid(ACCESS_TOKEN)
    openid_list = ["oAPA46nJ6ofI5PrehMws0NJQn_80",]
    template_id = "yNC8coLEOfspayMEHX-Qmoj_3qpPNhZ26ej4bd8la1A"
    data = {
        "thing10": {
            "value": "接口测试"
        },
        "time4": {
            "value": current_time
        },
    }
    for openid in openid_list:
        params = {
            # "access_token": ACCESS_TOKEN,
            "touser": openid,
            "template_id": template_id,
            "url": tran_url,
            "data": data,
            # "client_msg_id": "MSG_000001",
            # "access_token": get_access_token(),
            # "touser": get_openid(ACCESS_TOKEN),
        }
        resp = requests.post(send_url+"access_token="+ACCESS_TOKEN, json=params)
    # data = resp.json()
    # print(data)


# get_access_token()
# get_openid()
# access_token = get_access_token()
access_token = "73_ztTYNDaTSM3O7M9fltR_achv7G23HLzQVwFgAC7TOQRRXYk2NH9sTuvjrGQcGQKKL6ZcDo40CF6_Ok1o_3HLdchi8ccMmBiWq36LsaerSikviKUNotNca4FLH04LSNcAAABID"
send_message(access_token)

