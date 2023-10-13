import pandas as pd
import requests
from datetime import datetime
from io import StringIO
from bs4 import BeautifulSoup
from tabulate import tabulate
import numpy as np
import json
import scrapy
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


class mySpider:
    def __init__(self):
        self.ask_url = "http://zjj.sz.gov.cn:8004/api/marketInfoShow/getFjzsInfoData"
        self.send_url = "https://sctapi.ftqq.com/"
        self.send_key = {"qc": "SCT226350TjAo8bNymkSKjzt1gQIyPPIQx", "xr": "SCT226248TNQGtO5oTXqFyB3iBhMku9j8w"}

    def getData(self, url, dateType="", startDate="", endDate=""):
        # 爬取数据
        ask_params = {
            "dateType": dateType,
            "endDate": endDate,
            "startDate": startDate,
        }
        resp = requests.post(url, json=ask_params)
        # 读取数据
        data = resp.json()['data']
        return data

    def get_one_month(self):
        current_date = datetime.now().date()
        year, month, day = current_date.year, current_date.month, current_date.day
        startDate = f"{year}-{month}-01"
        endDate = f"{year}-{month}-{day}"
        day_cnt = day - 1
        data = self.getData(self.ask_url, startDate=startDate, endDate=endDate)
        # print(data)
        ysf_tot, esf_tot = 0, 0
        for i in range(day_cnt):
            ysf_tot += data["ysfTotalTs"][i]
            esf_tot += data["esfTotalTs"][i]
        content = ""
        content += f"1. 前一天一手房成交套数：{data['ysfTotalTs'][day_cnt - 1]}" + "\n\n"
        content += f"2. 前一天二手房成交套数：{data['esfTotalTs'][day_cnt - 1]}" + "\n\n"
        content += f"3. 当月一手房累计成交套数：{ysf_tot}" + "\n\n"
        content += f"4. 当月二手房累计成交套数：{esf_tot}" + "\n\n"
        # print(content)
        return content

    def get_three_month(self):
        data = self.getData(self.ask_url, dateType="3months")
        day_cnt = len(data['ysfTotalTs'])
        ysf_tot_num, esf_tot_num, ysf_tot_area, esf_tot_area = 0, 0, 0, 0
        for i in range(day_cnt):
            ysf_tot_num += data["ysfTotalTs"][i]
            esf_tot_num += data["esfTotalTs"][i]
            ysf_tot_area += data["ysfDealArea"][i]
            esf_tot_area += data["esfDealArea"][i]
        content = ""
        content += f"5. 近三个月一手房成交面积/套数：{ysf_tot_area/ysf_tot_num:.2f}" + "\n\n"
        content += f"6. 近三个月二手房成交面积/套数：{esf_tot_area/esf_tot_num:.2f}" + "\n\n"
        content += f"7. 二手房近三年成交同比数：" + "\n\n"
        # print(content)
        return content

    def get_three_year(self):
        current_date = datetime.now().date()
        year, month, day = current_date.year, current_date.month, current_date.day
        startDate = f"{year-2}-{month}-{day}"
        endDate = f"{year}-{month}-{day}"
        data = self.getData(self.ask_url, startDate=startDate, endDate=endDate)
        day_cnt = len(data['ysfTotalTs'])


    def push_data(self):
        content = ""
        content += self.get_one_month() + self.get_three_month()
        for name, key in self.send_key.items():
            send_params = {
                "pushkey": key,
                "text": datetime.now().date().strftime("%Y-%m-%d") + "数据报告",
                "desp": content,
                "type": "markdown"
            }
            requests.post(self.send_url + key + ".send", send_params)

    def job(self):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.push_data()

    def timer(self):
        shed = BlockingScheduler()
        shed.add_job(self.job, 'interval', seconds=60)
        shed.start()


spiderman = mySpider()
spiderman.push_data()
