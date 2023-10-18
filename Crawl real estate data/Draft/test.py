import requests
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

url = "http://zjj.sz.gov.cn:8004/api/marketInfoShow/getYsfCjxxGsData"

resp = requests.post(url)
print(resp.text)
print(type(resp))
json_data = json.loads(resp.text)
content = json_data['data']['dataTs']

title = json_data['data']['xmlDateDay'] + ' 全市商品住房成交套数'
result = ''
for i in range (0,len(content)):
    result = result + content[i]['name'] + ' ' + str(content[i]['value']) + "\n\n"

data = {
    "title": title,
    "desp": result,
}


# "xr": "SCT226248TNQGtO5oTXqFyB3iBhMku9j8w"
# "zl": "SCT226491T0oXTmmmRBCUkynwJU3tEITRx"
qc = "PDU25968T53KADnbXVe3tgyL1HqwBupeEbvgk3pWM"
# re = requests.post("https://sc.ftqq.com/"+ qc + ".send" ,data = data)

data2 = {
    "pushkey": "PDU25968T53KADnbXVe3tgyL1HqwBupeEbvgk3pWM",
    "text": title,
    "desp": result,
    "type": "markdown"
}

# requests.post("https://api2.pushdeer.com/message/push?pushkey=<key>&text=标题&desp=<markdown>&type=markdown")
requests.post("https://api2.pushdeer.com/message/push", data2)


def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    requests.post("https://api2.pushdeer.com/message/push", data2)


# 定义BlockingScheduler
sched = BlockingScheduler()
sched.add_job(job, 'interval', seconds=60)
sched.start()


