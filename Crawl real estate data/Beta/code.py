import io
import pandas as pd
import requests
from tabulate import tabulate
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import matplotlib.pyplot as plt
import base64
from requests.exceptions import JSONDecodeError
import time


class mySpider:
    ask_url = "http://zjj.sz.gov.cn:8004/api/marketInfoShow/getFjzsInfoData"
    send_url = "https://sctapi.ftqq.com/"
    developer_key = {"qc": "SCT226350TjAo8bNymkSKjzt1gQIyPPIQx", "xr": "SCT226248TNQGtO5oTXqFyB3iBhMku9j8w"}
    send_key = {"qc": "SCT226350TjAo8bNymkSKjzt1gQIyPPIQx"}

    def __init__(self):
        pass

    @staticmethod
    def getData(dateType="", startDate="", endDate=""):
        # 爬取数据
        ask_params = {
            "dateType": dateType,
            "endDate": endDate,
            "startDate": startDate,
        }
        while True:
            try:
                resp = requests.post(spiderman.ask_url, json=ask_params)
                data = resp.json()['data']
            except JSONDecodeError as e:  # 处理 JSONDecodeError 异常
                print("JSON解码错误")
                print("Push failed!")
                spiderman.push_error(type(e))
                time.sleep(30)  # 等待60s后再进行下次尝试
                # sys.exit(1)  # 强行结束程序
            else:
                # print(resp.status_code)
                # print(resp.text)  # 读取数据
                # print(data)
                return data

    @staticmethod
    def get_accumulation(data):
        return [sum(data["ysfTotalTs"]),
                sum(data["esfTotalTs"]),
                sum(data["ysfDealArea"]),
                sum(data["esfDealArea"])]

    def get_one_month(self):
        current_date = datetime.now().date()
        year, month, day = current_date.year, current_date.month, current_date.day
        startDate = f"{year}-{month}-01"
        endDate = f"{year}-{month}-{day}"
        day_cnt = day - 1
        data = self.getData(startDate=startDate, endDate=endDate)
        # print(data)
        val = self.get_accumulation(data)
        content = ""
        content += f"当日一手房成交：{data['ysfTotalTs'][day_cnt - 1]:.0f}套" + "\n\n"
        content += f"当月一手房累计成交：{val[0]:.0f}套" + "\n\n\n\n"
        content += f"当日二手房成交：{data['esfTotalTs'][day_cnt - 1]:.0f}套" + "\n\n"
        content += f"当月二手房累计成交：{val[1]:.0f}套" + "\n\n\n\n"
        # print(content)
        return content

    def get_three_month(self):
        data = self.getData(dateType="3months")
        val = self.get_accumulation(data)
        content = ""
        content += f"一手房成交面积/套数：{val[2]/val[0]:.2f}m²/套" + "\n\n"
        content += f"二手房成交面积/套数：{val[3]/val[1]:.2f}m²/套" + "\n\n\n\n"
        # print(content)
        return content

    def get_three_year(self):
        current_date = datetime.now().date()
        year, month, day = current_date.year, current_date.month, current_date.day
        data, tot_num = [], []
        for i in range(0, 4):
            data.append(self.getData(startDate=f"{year-i}-{month}-01", endDate=f"{year-i}-{month}-{day}"))
            tot_num.append(self.get_accumulation(data[i]))
        cal = {
            "": [f"{year-1}", f"{year-2}", f"{year-3}"],
            f"{year}": [f"{tot_num[0][1]/tot_num[1][1]-1:.2f}",
                        f"{tot_num[0][1]/tot_num[2][1]-1:.2f}",
                        f"{tot_num[0][1]/tot_num[3][1]-1:.2f}"],
        }
        df = pd.DataFrame(cal)
        content = "二手房三年成交同比\n\n"
        markdown_df = tabulate(df, headers='keys', tablefmt='pipe', showindex=False, maxcolwidths=[10, 20]) + "\n\n"
        content += markdown_df + "\n\n"
        return content

    @staticmethod
    def draw_picture(x_label, x_data, y_data, title, color):
        fig, ax = plt.subplots()
        ax.bar(x_data, y_data, width=0.5, label=x_label, color=color)
        ax.set_title(title)
        ax.set_xlabel('Date')
        ax.set_ylabel('Volume')
        ax.legend()
        n = 30  # 每第n个标签显示
        plt.xticks(np.arange(len(x_data))[::n], x_data[::n])  # 设置x轴刻度间隔
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
        # print(markdown_str)
        return markdown_str

    def three_month_picture(self):
        data = self.getData(dateType="3months")
        # print(data)
        x = data['date']
        ysf_values = data['ysfTotalTs']
        esf_values = data['esfTotalTs']
        # 作图
        ysf_picture = spiderman.draw_picture('First-hand house', x, ysf_values, "First-hand House Data", color="blue")
        esf_picture = spiderman.draw_picture('Second-hand house', x, esf_values, "Second-hand House Data", color="orange")
        content = ""
        content += "一手房成交图表\n\n" + ysf_picture + "\n\n"
        content += "二手房成交图表\n\n" + esf_picture + "\n\n"
        return content

    @staticmethod
    def send(key, text, content):
        send_url = "https://sctapi.ftqq.com/"
        send_params = {
            "pushkey": key,
            "text": text,
            "desp": content,
            "type": "markdown"
        }
        requests.post(send_url + key + ".send", send_params)

    @staticmethod
    def get_illustration():
        content = ""
        content += "1. 数据参考自深圳市房地产信息平台" + "\n\n"
        content += "2. 一二手房面积/套数数值选取自近三个月" + "\n\n"
        content += "3. 一二手房成交图表数值选取自近三个月" + "\n\n"
        return content

    def push_data(self):
        print("pushing...")
        content = ""
        content += (self.get_one_month() +
                    self.get_three_month() +
                    self.three_month_picture() +
                    self.get_three_year() +
                    self.get_illustration()
                    )
        # print(content)
        for name, key in self.send_key.items():
            date = datetime.now().date()
            self.send(key, f"{date.year}-{date.month}-{date.day-1}" + "深圳成交简报", content)
        print("Successfully pushed!")

    def push_error(self, error_type):
        content = datetime.now().date().strftime("%Y-%m-%d") + "数据推送发生错误" + "\n\n"
        content += "错误类型为 " + f"{error_type}"
        self.send(self.developer_key, "错误报告", content)
        content = "推送发生错误，请联系开发者"
        for name, key in self.send_key.items():
            self.send(key, datetime.now().date().strftime("%Y-%m-%d") + "数据报告", content)

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


if __name__ == "__main__":
    spiderman = mySpider()
    spiderman.push_data()
