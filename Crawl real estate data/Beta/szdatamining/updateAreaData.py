import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import requests
import datetime
import calendar
from apscheduler.schedulers.blocking import BlockingScheduler


def getData(dateType="", startDate="", endDate=""):
    # 爬取数据
    ask_params = {
        "dateType": dateType,
        "endDate": endDate,
        "startDate": startDate,
    }
    resp = requests.post("http://zjj.sz.gov.cn:8004/api/marketInfoShow/getFjzsInfoData", json=ask_params)
    data = resp.json()['data']
    # print(data)
    return data


def get_accumulation(data):
    return [sum(data["ysfTotalTs"]),
            sum(data["esfTotalTs"]),
            sum(data["ysfDealArea"]),
            sum(data["esfDealArea"])]


def getAreaData_month():
    dataDict = []
    # 创建 Chrome WebDriver 实例
    browser = webdriver.Chrome()
    # 设置显式等待时间，最长等待时间为 10 秒
    wait = WebDriverWait(browser, 10)
    # 访问网页
    browser.get('http://zjj.sz.gov.cn/ris/szfdc/showcjgs/esfcjgs.aspx')
    areas = ['hypBa', 'hypFt', 'hypLg', 'hypLh', 'hypNs', 'hypYt', 'hypLhQ', 'hypGm', 'hypPs', 'hypDp']
    areaName = ['宝安', '福田', '龙岗', '罗湖', '南山', '盐田', '龙华', '光明', '坪山', '大鹏新区']
    for item, name in zip(areas, areaName):
        # 找到链接元素并模拟点击
        link_element = wait.until(EC.element_to_be_clickable((By.ID, item)))  # 假设要点击的链接的 id 是 'hypAll'
        link_element.click()
        # 等待页面加载完成
        time.sleep(5)
        # 等待页面加载完成
        wait.until(EC.presence_of_element_located((By.ID, 'clientList2_ctl02_lblHTTS2')))  # 假设要提取的节点的 id 是 'clientList2_ctl02_lblHTTS2'
        # 提取节点的文本内容
        target_element = browser.find_element(By.ID, 'clientList2_ctl02_lblHTTS2')  # 假设要提取的节点的 id 是 'clientList2_ctl02_lblHTTS2'
        print(f"Get data of {item} : {target_element.text}")
        dataDict.append({name: int(target_element.text)})
    # print("Result: ", dataList)
    # print("The number of areas : ", len(dataList))
    # print("The sum of data : ", sum(dataList))
    # 关闭 WebDriver
    current_date = datetime.datetime.now().date()
    year = current_date.year - (current_date.month == 1)
    month = (current_date.month - 2 + 12) % 12 + 1
    data = {
        "year": year,
        "month": month,
        "content": dataDict,
    }
    updateData("http://114.132.235.86:3001/api/v1/ratioInformation", data)
    browser.close()
    print("Successfully update!")


def getTotalData_month():
    url = "http://114.132.235.86:3001/api/v1/soldInformation"
    current_date = datetime.datetime.now().date()
    yesterday = current_date - datetime.timedelta(days=1)
    year, month = yesterday.year, yesterday.month
    _, last_day = calendar.monthrange(year, month)
    first_day_str = yesterday.replace(day=1).strftime("%Y-%m-%d")
    last_day_str = yesterday.strftime("%Y-%m-%d")
    # print(last_day_str, first_day_str)
    value = get_accumulation(getData(startDate=first_day_str, endDate=last_day_str))
    data = {
        "year": year,
        "month": month,
        "content": value[1]
    }
    updateData(url, data)


def getTotalData_months():
    # 设置日期
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2023, 11, 30)
    current_date = start_date
    months_data = ['data']
    months_date = ['date']
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        _, last_day = calendar.monthrange(year, month)
        first_day_str = current_date.strftime("%Y-%m-%d")
        last_day_str = current_date.replace(day=last_day).strftime("%Y-%m-%d")
        # print(f"firstday：{first_day_str}，lastday：{last_day_str}" )
        value = getData(startDate=first_day_str, endDate=last_day_str)
        value = get_accumulation(value)
        # print(value)
        data = {
            "year": year,
            "month": month,
            "content": value[1]
        }
        updateData("http://114.132.235.86:3001/api/v1/soldInformation", data)
        months_data.append(value[1])
        months_date.append(f"{current_date.year}-{current_date.month}")
        current_date = current_date.replace(day=1) + datetime.timedelta(days=32)
        current_date = current_date.replace(day=1)
    print(months_data)
    print(months_date)
    print("Successfully update!")


def updateData(url, data):
    resp = requests.post(url, json=data)


def getInformation():
    resp = requests.get("http://114.132.235.86:3001/api/v1/information")
    data = resp.json()['data']
    # print(data)
    print(data['soldInformation'])
    print(data['ratioInformation'])


def deleteData():
    # url = "http://114.132.235.86:3001/api/v1/ratioInformation"
    url = "http://114.132.235.86:3001/api/v1/soldAllInformation"
    data = {
        "year": 2023,
        "month": 10,
    }
    # resp = requests.delete(url, json=data)
    resp = requests.delete(url)


def job():
    # 在这里编写要执行的工作
    today = datetime.date.today()
    if today.day == 1:
        getAreaData_month()
        getTotalData_month()


def timer():
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', day='1')
    scheduler.start()


if __name__ == "__main__":
    # timer()
    deleteData()
    getTotalData_months()
    getInformation()
