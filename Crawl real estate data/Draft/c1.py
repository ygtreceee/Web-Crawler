import requests
import json
import pandas as pd
from jsonpath  import jsonpath

# 通过日期数据
url = 'http://zjj.sz.gov.cn:8004/api/marketInfoShow/getFjzsInfoData'

params = {
    "dateType": "week",
    "endDate": "",
    "startDate": ""}


def get_response(url, params):
    headers = {
        # 'authority': 'zjj.sz.gov.cn:8004',
        'method': 'POST',
        'path': '/api/marketInfoShow/getFjzsInfoData',
        'scheme': 'https',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'http://zjj.sz.gov.cn:8004',
        'referer': 'http://zjj.sz.gov.cn:8004/marketInfoShow/FjzsReport.html?t=1696986654006',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'cookie': '_gid=GA1.3.1091326087.1696932878; ftzjjszgovcn=0; arialoadData=true; ariawapChangeViewPort=false; ariaFixed=true; ariaReadtype=1; ariaoldFixedStatus=false; ariaStatus=false; Hm_lvt_ddaf92bcdd865fd907acdaba0285f9b1=1696938986,1696939309; pgv_pvid=9109716550; szfdc-session-id=07c9bccf-ab07-435c-b7de-1e512aad8c06; cookie_3.36_8080=85416329; ASP.NET_SessionId=z1lvyimtz3cg0aenlkynkbyc; _ga_34B604LFFQ=GS1.1.1696985611.7.1.1696986614.60.0.0; _ga=GA1.1.1493207979.1696932878; AD_insert_cookie_89188=33156713',
        # 'x-csrf-token': 'abalGrijwUtgehoA6ShdrPCD'
    }
    r = requests.post(url, headers=headers, data=json.dumps(params))
    json_data = json.loads(r.text)
    return json_data


json_data = get_response(url, params)
print(json_data)
print(type(json_data))

df = pd.DataFrame(json_data)
print(df)

# df.to_excel('data2.xlsx', index=True)
# print(json_data['data']['data'][5])
# print(json_data['esfDealArea']['data'][5])
# print(json_data['esfTotalTs']['data'][5])



