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

    def get_one_month(self):
        current_date = datetime.datetime.now().date()
        year, month, day = current_date.year, current_date.month, current_date.day
        startDate = f"{year}-{month}-01"
        endDate = f"{year}-{month}-{day}"
        day_cnt = day - 1
        data = self.getData(startDate=startDate, endDate=endDate)
        # print(data)
        val = self.get_accumulation(data)
        # print(content)
        content = {
            'ysf_total_ts': data['ysfTotalTs'][day_cnt - 1],
            'ysf_accumulated': val[0],
            'esf_total_ts': data['esfTotalTs'][day_cnt - 1],
            'esf_accumulated': val[1]
        }
        return content

    def get_three_month(self):
        data = self.getData(dateType="3months")
        val = self.get_accumulation(data)
        content = ""
        content += f"""一手房成交面积/套数：**{val[2] / val[0]:.0f}m²/套**""" + "\n\n"
        content += f"""二手房成交面积/套数：**{val[3] / val[1]:.0f}m²/套**""" + "\n\n\n\n"
        # print(content)
        return content

    def get_three_year(self):
        current_date = datetime.datetime.now().date()
        year, month, day = current_date.year, current_date.month, current_date.day
        data, tot_num = [], []
        for i in range(0, 4):
            data.append(self.getData(startDate=f"{year - i}-01-01", endDate=f"{year - i}-{month}-{day}"))
            tot_num.append(self.get_accumulation(data[i]))
            # print(data[i])

        cal = {
            "": [f"{year}"],
            f"{year-1}": [f"{(tot_num[0][1] / tot_num[1][1] - 1) * 100:.0f}%"],
            f"{year-2}": [f"{(tot_num[0][1] / tot_num[2][1] - 1) * 100:.0f}%"],
            f"{year-3}": [f"{(tot_num[0][1] / tot_num[3][1] - 1) * 100:.0f}%"],
        }
        df = pd.DataFrame(cal)
        content = "**二手房三年成交同比**\n\n"
        markdown_df = tabulate(df, headers='keys', tablefmt='pipe', showindex=False, maxcolwidths=[10, 20]) + "\n\n"
        content += markdown_df + "\n\n"
        return content

    @staticmethod
    def draw_picture(x_label, x_data, y_data, color):
        fig, ax = plt.subplots()
        ax.bar(x_data, y_data, width=0.5, color=color, label='_nolegend_')  # 添加一个空标签
        ax.set_ylim([0, 500])  # 设置y轴范围
        ax.spines['top'].set_visible(False)  # 去掉上边框
        ax.spines['right'].set_visible(False)  # 去掉右边框
        ax.set_box_aspect(0.35)  # 调整边框显示比例
        n = 80  # 每第n个标签显示
        plt.xticks(np.arange(len(x_data))[::n], x_data[::n])  # 设置x轴刻度间隔
        ax.tick_params(axis='x', labelsize=8)  # 设置x轴刻度标签的字体大小
        # plt.subplots_adjust(top=0.55, bottom=0.45)  # 根据需要调整边距
        plt.tight_layout()  # 调整布局
        legend = ax.get_legend()
        if legend:
            legend.remove()  # 移除图例

        # 添加荣枯线和标注
        y_line = 265  # 荣枯线的y轴值
        plt.axhline(y=y_line, color='red', linestyle='--', linewidth=0.5)  # 添加红色虚线
        plt.rcParams['font.family'] = 'Microsoft YaHei'  # 将字体设置为
        # 调整字体大小
        font_size = 8  # 字体大小
        plt.rcParams['font.size'] = font_size
        # 添加标注
        plt.text(1, y_line - 10, '荣枯线', color='#a64040', fontsize=font_size)

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

    def one_year_picture(self):
        data = self.getData(dateType="1year")
        # print(data)
        x = data['date']
        ysf_values = data['ysfTotalTs']
        # print(ysf_values)
        esf_values = data['esfTotalTs']
        # print(esf_values)
        # 作图
        esf_picture = self.draw_picture('Second-hand house', x, esf_values, color="#b37878")
        ysf_picture = self.draw_picture('First-hand house', x, ysf_values, color="#cc7a7a")
        content = ""
        content += "**二手房成交图表**\n\n" + esf_picture + "\n\n"
        content += "**一手房成交图表**\n\n" + ysf_picture + "\n\n"
        return content

    @staticmethod
    def get_illustration():
        content = ""
        content += (f"""<span style="font-size: 10px; text-align: right;">备注：\n""" +
                    f"""数据来源：深圳市房地产信息平台\n一手房成交数据为网签口径\n二手房成交数据为过户口径\n""" +
                    f"""一二手房面积/套数数值选取自近一年\n""" +
                    f"""一二手房成交图表数值选取自近一年\n</span>""")
        return content

    def get_data(self):
        content = ""
        content += (self.get_one_month() +
                    self.get_illustration() +
                    self.one_year_picture() +
                    self.get_three_year() +
                    self.get_three_month()
                    )
        return content




if __name__ == '__main__':
    crawler = mySpider()
    crawler.get_data()
