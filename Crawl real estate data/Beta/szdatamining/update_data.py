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


class mySpider:
    def __init__(self):
        self.ask_url = "http://zjj.sz.gov.cn:8004/api/marketInfoShow/getFjzsInfoData"

    def getData(self, dateType="", startDate="", endDate=""):
        # 爬取数据
        ask_params = {
            "dateType": dateType,
            "endDate": endDate,
            "startDate": startDate,
        }
        resp = requests.post(self.ask_url, json=ask_params)
        data = resp.json()['data']
        return data

    @staticmethod
    def get_accumulation(data):
        return [sum(data["ysfTotalTs"]),
                sum(data["esfTotalTs"]),
                sum(data["ysfDealArea"]),
                sum(data["esfDealArea"])]

    def get_lastMonth(self):
        current_date = datetime.datetime.now().date()
        year, month, day = current_date.year, current_date.month, current_date.day
        startDate = f"{year}-{month - 1}-01" if day == 1 else f"{year}-{month}-01"
        yesterday = current_date - datetime.timedelta(days=1)
        endDate = f"{yesterday.year}-{yesterday.month}-{yesterday.day}"
        data = self.getData(startDate=startDate, endDate=endDate)
        # print(startDate, endDate)
        # print(data)
        val = self.get_accumulation(data)
        content = {
            "yesterdayYsf": data['ysfTotalTs'][-1],
            "lastMonthYsf":  val[0],
            "yesterdayEsf": data['esfTotalTs'][-1],
            "lastMonthEsf": val[1],
        }
        # print(content)
        return content

    def one_year_ratio(self):
        data = self.getData(dateType="3months")
        val = self.get_accumulation(data)
        content = {
            "firstArea": val[2] / val[0],
            "secondeArea": val[3] / val[1],
        }
        return content

    def get_yearOnyear(self):
        current_date = datetime.datetime.now().date()
        year, month, day = current_date.year, current_date.month, current_date.day
        data, tot_num = [], []
        for i in range(0, 4):
            data.append(self.getData(startDate=f"{year - i}-01-01", endDate=f"{year - i}-{month}-{day}"))
            tot_num.append(self.get_accumulation(data[i]))
            # print(data[i])
        content = {
            "yearOnyear": [
            ["", f"{year - 1}", f"{year - 2}", f"{year - 3}"],
            [f"{year}",
             f"{round((tot_num[0][1] / tot_num[1][1] - 1) * 100)}",
             f"{round((tot_num[0][1] / tot_num[2][1] - 1) * 100)}",
             f"{round((tot_num[0][1] / tot_num[3][1] - 1) * 100)}"],
        ]
        }
        return content

    def get_lastYear(self):
        data = self.getData(dateType="1year")
        # print(data)
        x = data['date']
        ysf_values = data['ysfTotalTs']
        # print(ysf_values)
        esf_values = data['esfTotalTs']
        content = {
            "lastYearEsf": [x, esf_values],
            "lastYearYsf": [x, ysf_values],
        }
        return content

    def get_lastThreeMonth(self):
        data = self.getData(dateType="3months")
        x = data['date']
        ysf_values = data['ysfTotalTs']
        # print(ysf_values)
        esf_values = data['esfTotalTs']
        # print(esf_values)
        content = {
            "lastThreeMonthEsf": [x, esf_values],
            # "lastThreeMonthYsf": [x, ysf_values],
        }
        return content

    def get_transactionRatio(self):
        current_date = datetime.datetime.now().date()
        year, month, day = current_date.year, current_date.month, current_date.day
        data = []
        period = [""]
        ratio = []
        for i in range(1, 6):
            startDate = f"{year}-{str(month - i * 3).zfill(2)}-{day}" if month - i * 3 > 0 else f"{year - 1}-{str(12 + month - i * 3).zfill(2)}-{day}"
            endDate = f"{year}-{str(month - (i - 1) * 3).zfill(2)}-{day}" if month - (i - 1) * 3 > 0 else f"{year - 1}-{str(12 + month - (i - 1) * 3).zfill(2)}-{day}"
            # print(self.getData(startDate=startDate, endDate=endDate))
            data.append(self.get_accumulation(self.getData(startDate=startDate, endDate=endDate)))
            if i > 1:
                ratio.append(f"{round((data[0][1] / data[i - 1][1] - 1) * 100)}")
            startDate = startDate[:4] + '.' + startDate[5:7]
            endDate = endDate[:4] + '.' + endDate[5:7]
            if i == 1:
                ratio.append(startDate[2:7] + '-' + endDate[2:7])
            else:
                period.append(startDate[2:7] + '-' + endDate[2:7])
        content = {
            "transactionRatio": [
                period,
                ratio,
            ]
        }
        return content

    def upload_data(self):    # 更新每日成交数据
        url = "http://114.132.235.86:3000/api/v1/information"
        weekday = datetime.date.today().weekday()
        current_date = datetime.datetime.now().date()
        yesterday = current_date - datetime.timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        # print(yesterday_str)
        content = {
            "title": yesterday_str,
            **(self.get_lastMonth()),
            **(self.get_transactionRatio()),
            **(self.get_yearOnyear()),
            **(self.get_lastThreeMonth()),
            **(self.get_lastYear()),
            # **(self.one_year_ratio()),
        }
        print("Got data!")
        # print(content)
        data = {
            "weekday": weekday + 1,
            "content": content,
        }
        # 网站抓取数据或者此处抓取并上传
        resp = requests.post(url, json=data)
        # print(resp.status_code)
        print("Successfully update!")

    def job(self):
        print("job is running, time is ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.upload_data()

    def timer(self):
        sched = BlockingScheduler()
        # 截止到2023-10-31 00:00:00 每周一到周日早上0点01分运行job_function
        sched.add_job(self.job, 'cron', day_of_week='mon-sun', hour=0, minute=1, id='task')
        sched.start()
        # 移除任务
        sched.remove_job('task')


if __name__ == "__main__":
    spiderman = mySpider()
    spiderman.upload_data()
    # spiderman.timer()
