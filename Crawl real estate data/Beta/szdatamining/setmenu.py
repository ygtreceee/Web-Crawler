import requests

def get_access_token():
    global access_token
    ask_url = "https://api.weixin.qq.com/cgi-bin/token?"
    params = {
        "grant_type": "client_credential",
        "appid": "wx8dc9b83b9a5720ac",  # AppId
        "secret": "cb8aeffb8e8d5b477b7ad97379aadfbc",  # AppSecret
    }
    resp = requests.get(ask_url, params=params)
    data = resp.json()
    print(data)
    access_token = data


access_token = ('75_E1SvljoWOBa06JFXiAtBwq-cLhnG4VfnDdrezijKa9N5HP2q2ngnfn06DzqOnD5bRZBEN8p5sN6WMA6fWie1g4rb-vEEc702u3'
                'Xgr7XtYL46-mFw6GtpgAF3aqIATJgADAUND')


def setMenu():
    global access_token
    ask_url = "https://api.weixin.qq.com/cgi-bin/menu/create"
    ask_params = {
        "access_token": access_token
    }
    # param_jsonstr = json.dumps(parameters, ensure_ascii=False).encode('utf-8')
    ask_data = {
        "button": [
            {
                "type": "view",
                "name": "See report",
                "url":"http://szdatamining.com/#/3"
            },
            {
                "name": "Menu",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "Search",
                        "url":"http://www.soso.com/"
                    }
                ]
            }
        ]
    }
    resp = requests.post(ask_url, params=ask_params, json=ask_data)
    print(resp.json())

def deleteMenu():
    global access_token
    ask_url = "https://api.weixin.qq.com/cgi-bin/menu/delete"
    ask_params = {
        "access_token": access_token
    }
    resp = requests.post(ask_url, params=ask_params)
    print(resp.json())

if __name__ == "__main__":
    # setMenu()
    deleteMenu()
