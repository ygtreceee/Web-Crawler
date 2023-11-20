import io
import json

import pandas as pd
import requests
from tabulate import tabulate
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import matplotlib.pyplot as plt
import base64
from requests.exceptions import JSONDecodeError
import time


class Transmitter:
    def __init__(self):
        self.access_token = ""
        self.openid_list = []
        self.get_access_token()
        self.get_openid()

    def get_access_token(self):
        ask_url = "https://api.weixin.qq.com/cgi-bin/token?"
        params = {
            "grant_type": "client_credential",
            "appid": "wx8dc9b83b9a5720ac",  # AppId
            "secret": "cb8aeffb8e8d5b477b7ad97379aadfbc",  # AppSecret
        }
        resp = requests.get(ask_url, params=params)
        data = resp.json()
        # print(data)
        # self.access_token = data
        self.access_token = ('74_ZQvd5PeDEHn_DBmgiR08gjTHM4gNHr6C-MIk5GjV9mXBeR5NBxLbqT1Aa4VeqUIXa2-7KR8OCAQB_oUsbG8K4NXe6RiqV9ubqEwNVLvkOnnX-HNpGNUVkBKpHfgKJVaAEACBN')

    def get_openid(self):
        ask_url = "https://api.weixin.qq.com/cgi-bin/user/get?"
        params = {"access_token": self.access_token, }
        resp = requests.get(ask_url, params=params)
        data = resp.json()['data']
        openid_list = data['openid']  # type: list
        # print(openid)
        # self.openid_list = openid_list
        # self.openid_list = ["oAPA46nJ6ofI5PrehMws0NJQn_80", "oAPA46gUnzHyRjk9Zy-FO1zd6XIg", "oAPA46s-sR_do8ezueAbghwuUrtA", "oAPA46jqd9Nmkw24MYsQbrJa77Kc"]
        # self.openid_list = ["oAPA46nJ6ofI5PrehMws0NJQn_80", "oAPA46gUnzHyRjk9Zy-FO1zd6XIg"]
        # self.openid_list = ["oAPA46nJ6ofI5PrehMws0NJQn_80"]


    def send(self, openid, template_id, data):
        send_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?"
        weekday = datetime.date.today().weekday()
        tran_url = f"http://szdatamining.com/#/{weekday + 1}"
        # tran_url = "http://www.szdatamining.com"
        params = {
            "touser": openid,
            "template_id": template_id,
            "url": tran_url,
            "data": data,
        }
        resp = requests.post(send_url + "access_token=" + self.access_token, json=params)

    def push_data(self):
        print("pushing...")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 获取当前日期
        current_date = datetime.datetime.now().date()
        # 计算昨天的日期
        yesterday = current_date - datetime.timedelta(days=1)
        # 将昨天的日期格式化为字符串
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        data = {
            "thing1": {
                "value": yesterday_str + "深圳成交简报"
            },
            "time4": {
                "value": current_time
            },
        }
        # print(self.openid_list)
        # print(self.access_token)
        for openid in self.openid_list:
            self.send(openid, "Y1tqQNRLFq_n6MKU42eFzoYAKcGz_tSknjKz_EZTg8A", data)
        print("Successfully pushed!")

    def job(self):
        print("job is running, time is ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.get_access_token()  # 每日重新获取access_token
        self.get_openid()        # 每日重新获取openid
        self.push_data()              # 发送数据日报

    def timer(self):
        sched = BlockingScheduler()
        # 截止到2023-10-31 00:00:00 每周一到周日早上九点半运行job_function
        sched.add_job(self.job, 'cron', day_of_week='mon-sun', hour=9, minute=30, id='task')
        # sched.add_job(self.job, 'interval', seconds=2)
        sched.start()
        # 移除任务
        sched.remove_job('task')


if __name__ == "__main__":
    transmitter = Transmitter()
    transmitter.push_data()
    # transmitter.timer()
