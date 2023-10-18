import pandas as pd
import requests
from io import StringIO
from bs4 import BeautifulSoup
from tabulate import tabulate
import numpy as np
import json
import scrapy
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from requests.exceptions import JSONDecodeError


def getData():
    ask_url = "http://zjj.sz.gov.cn/ris/szfdc/showcjgs/ysfcjgs.aspx?cjType=0"
    send_url = "https://sctapi.ftqq.com/SCT226350TjAo8bNymkSKjzt1gQIyPPIQx.send"
    qc_key = "SCT226350TjAo8bNymkSKjzt1gQIyPPIQx"
    # 爬取数据
    resp = requests.post(ask_url)
    try:
        data = resp.json()['data']
    except JSONDecodeError as e:
        print("JSON解码错误")
        print(e)
        print(type(e))


    # 读取列表数据
    ls = pd.read_html(StringIO(resp.text))
    # print(ls)
    tb = pd.DataFrame(ls[0], columns=['用途', '成交套数', '成交面积(㎡)', '可售套数', '可售面积(㎡)'])
    markdown_tb = tabulate(tb, headers='keys', tablefmt='pipe')
    print(markdown_tb)

    # 读取日期
    soup = BeautifulSoup(resp.text, 'html.parser')
    data = soup.find('span', attrs={'id': "ctl03_lblCurTime2"}).text.strip()
    title = data + ' 全市商品房(一手房）成交套数'

    # 将内容转为markdown格式
    content = ""


    # 设置推送参数
    send_params = {
        "pushkey": qc_key,
        "text": title,
        "desp": markdown_tb,
        "type": "markdown"
    }

    # 推送消息
    requests.post(send_url, send_params)


# def job():
#     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     getData()
#
#
# # 定义BlockingScheduler定时器
# shed = BlockingScheduler()
# shed.add_job(job, 'interval', seconds=60)
# shed.start()

getData()