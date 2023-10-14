import io
import pandas as pd
import requests
import time
from datetime import datetime
from io import StringIO
from tabulate import tabulate
import numpy as np
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import matplotlib.pyplot as plt
import base64


class mySpider:
    def __init__(self):
        self.ask_url = "http://zjj.sz.gov.cn:8004/api/marketInfoShow/getFjzsInfoData"
        self.send_url = "https://sctapi.ftqq.com/"
        self.send_key = {"qc": "SCT226350TjAo8bNymkSKjzt1gQIyPPIQx", "xr": "SCT226248TNQGtO5oTXqFyB3iBhMku9j8w"}

    @staticmethod
    def getData(url, dateType="", startDate="", endDate=""):
        # 爬取数据
        ask_params = {
            "dateType": dateType,
            "endDate": endDate,
            "startDate": startDate,
        }
        resp = requests.post(url, json=ask_params)
        # print(resp.status_code)
        # 读取数据
        # print(resp.text)
        data = resp.json()['data']
        return data

    @staticmethod
    def get_accumulation(data):
        day_cnt = len(data['ysfTotalTs'])
        ysf_tot_num, esf_tot_num, ysf_tot_area, esf_tot_area = 0, 0, 0, 0
        for i in range(day_cnt):
            ysf_tot_num += data["ysfTotalTs"][i]
            esf_tot_num += data["esfTotalTs"][i]
            ysf_tot_area += data["ysfDealArea"][i]
            esf_tot_area += data["esfDealArea"][i]
        return [ysf_tot_num, esf_tot_num, ysf_tot_area, esf_tot_area]

    def get_one_month(self):
        current_date = datetime.now().date()
        year, month, day = current_date.year, current_date.month, current_date.day
        startDate = f"{year}-{month}-01"
        endDate = f"{year}-{month}-{day}"
        day_cnt = day - 1
        data = self.getData(self.ask_url, startDate=startDate, endDate=endDate)
        # print(data)
        val = self.get_accumulation(data)
        content = ""
        content += f"1. 前一天一手房成交套数：{data['ysfTotalTs'][day_cnt - 1]}" + "\n\n"
        content += f"2. 前一天二手房成交套数：{data['esfTotalTs'][day_cnt - 1]}" + "\n\n"
        content += f"3. 当月一手房累计成交套数：{val[0]}" + "\n\n"
        content += f"4. 当月二手房累计成交套数：{val[1]}" + "\n\n"
        # print(content)
        return content

    def get_three_month(self):
        data = self.getData(self.ask_url, dateType="3months")
        val = self.get_accumulation(data)
        content = ""
        content += f"5. 近三个月一手房成交面积/套数：{val[2]/val[0]:.2f}" + "\n\n"
        content += f"6. 近三个月二手房成交面积/套数：{val[3]/val[1]:.2f}" + "\n\n"
        content += f"7. 二手房近三年成交同比数：" + "\n\n"
        # print(content)
        return content

    def get_three_year(self):
        current_date = datetime.now().date()
        year, month, day = current_date.year, current_date.month, current_date.day
        startDate = f"{year}-{month}-01"
        endDate = f"{year}-{month}-{day}"
        exx_data = self.getData(self.ask_url, startDate=f"{year-2}-{month}-01", endDate=f"{year-2}-{month}-{day}")
        ex_data = self.getData(self.ask_url, startDate=f"{year-1}-{month}-01", endDate=f"{year-1}-{month}-{day}")
        pr_data = self.getData(self.ask_url, startDate=f"{year}-{month}-01", endDate=f"{year}-{month}-{day}")
        exx_val = self.get_accumulation(exx_data)
        ex_val = self.get_accumulation(ex_data)
        pr_val = self.get_accumulation(pr_data)
        data = {
            "": [f"同比{year-1}年", f"同比{year-2}年"],
            f"{year}年二手房成交量变化": [f"{pr_val[1]/ex_val[1]-1:.2f}", f"{pr_val[1]/exx_val[1]-1:.2f}"],
        }
        df = pd.DataFrame(data)
        markdown_df = tabulate(df, headers='keys', tablefmt='pipe', showindex=False) + "\n\n"
        return markdown_df

    def three_month_picture(self):
        data = self.getData(self.ask_url, dateType="3months")
        # print(data)
        x = data['date']
        ysf_values = data['ysfTotalTs']
        esf_values = data['esfTotalTs']
        # 作图
        bar_width = 0.5
        fig, ax = plt.subplots()
        ysf_bars = ax.bar(x, ysf_values, bar_width, label='First-hand house')
        esf_bars = ax.bar(x, esf_values, bar_width, label='Second-hand house', alpha=0.5)
        ax.set_title('Data Visualization')
        ax.set_xlabel('date')
        ax.set_ylabel('Volume')
        ax.legend()
        n = 30  # 每第n个标签显示
        plt.xticks(np.arange(len(x))[::n], x[::n])  # 设置x轴刻度间隔
        plt.tight_layout()  # 调整布局
        ax.legend()  # 添加图例
        # 将图形转换为字节流
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        # 将字节流转换为Base64编码的字符串
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        # 构建Markdown字符串
        markdown_str = f"![chart](data:image/png;base64,{image_base64})"
        # 输出Markdown字符串
        print(markdown_str)
        content = "8. 近三个月成交套数图表" + "\n\n"
        return content + markdown_str

    def push_data(self):
        content = ""
        content += (self.get_one_month() +
                    self.get_three_month() +
                    self.get_three_year() +
                    self.three_month_picture())
        # print(content)
        for name, key in self.send_key.items():
            send_params = {
                "pushkey": key,
                "text": datetime.now().date().strftime("%Y-%m-%d") + "数据报告",
                "desp": content,
                "type": "markdown"
            }
            requests.post(self.send_url + key + ".send", send_params)

    def job(self):
        print("job is running, time is ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.push_data()

    def timer(self):
        sched = BlockingScheduler()
        # 截止到2023-10-31 00:00:00 每周一到周日早上九点半运行job_function
        sched.add_job(self.job, 'cron', day_of_week='mon-sun', hour=9, minute=30, end_date='2023-10-31', id='task')
        sched.start()
        # 移除任务
        sched.remove_job('task')


spiderman = mySpider()
spiderman.push_data()

# timer
# get error