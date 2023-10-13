import requests
import json
import pandas as pd
from jsonpath import jsonpath

url = 'http://zjj.sz.gov.cn/ris/szfdc/showcjgs/esfcjgs.aspx'
params = {
    "scriptManager1": 'updatepanel1|hypFt',
    "__EVENTTARGET": 'hypFt',
    "__EVENTARGUMENT": '',
    "__VIEWSTATE": 'HnmFz2bGwBaUKNtvOTmx6xR5YEyTBk9JEo0jR4vyfegGAGezW95qTTBrcvq8xr8OFDKDAZcqd8FyrnK/HKRABVDYlDoRR/IUIYAQdloQiMqlrcL4yfV9R/Zsj2EYS0GfHyM/XG3VOYK75R8AsAz3C2kxS7bjcfSPbKQLu9Z5lM3mxquQIJXjme6xMFrAgmrp4zZQVVIgMxTtnianl4SrKTV6kqLCr6R3p9+4oovs/KJheOWjXXuwFNbpArEf6hCuALO9nepijWVc1jWENahS9ousFlkH5ALpX3uD3cZ49/a1EQlOGhwNw5ArbIFfZ8B0pKGgmc2gTo1lnO/jmA/I5QjHRcuc4XqVuSC+AxnNBaWhGAB3YNcfS5OjuvAjV7fUWPWPvSYZhPg6/opTC+/E7dIC04rvavSFAHpN7NYkBdXTCCjcdJ2DbRSlf8IQ9zIcJ2wj1gTNPzC7Xf0B/31Nvl9Jb54QFKRUyElkTWO4EKv4Mrmv4U9DhNCs1xMU5gZ8T2cqt2GYEWHu/YK1QC8u0lhKYMrbzhmGQQs9FFYYPugWv2HO1uWenUZ+j53YYel++okYg7IsqIsZiqnXVzE3pRbqZ32eTOrbsQq0ptu2dO5iaCdQdmWEq6kx4paGr2BLbdrtj81Sg+cMBURqhhQn+WNo6X+cRbvM8jUa+k2nRkHKZDCKh+JvNtAL6W/0oCsnHGdJq2M0OnfD1fpFzBEotICd+NFb+eLaxnrfRc4uMSTZ6rrG1CVGl/PYbW7uQy46k4+V3A==',
    "__VIEWSTATEGENERATOR": '778BEB03',
    "__VIEWSTATEENCRYPTED": '',
    "__EVENTVALIDATION": '3pd9iSZL368ZucrF1UjL2qqzGVjepEwfqbq3h59ePmbp1rzgfLK/LIkOTyQq/r73cdTextXmB7GVUv4TxMdEEa0oldgoWwVkxPB4/rW8qOqVHHDUBJbAgwr/hyA/0BQFwOBQInTgHdeu8aa/zXs8/JdUk2PmpD5r2sMtNDmNoSfm3BEtiGSFYdGld4R7TA8CNopgNA=='}

def get_response(url, params):
    headers = {
        # 'authority': 'zjj.sz.gov.cn:8004',
        # 'method': 'POST',
        # 'path': 'ris/szfdc/showcjgs/esfcjgs.aspx',
        # 'scheme': 'https',
        'content-type': 'application/x-www-form-urlencoded',
        # 'origin': 'http://zjj.sz.gov.cn',
        # 'referer': 'http://zjj.sz.gov.cn/ris/szfdc/showcjgs/esfcjgs.aspx',
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0'
        #               '.0 Safari/537.36',
        # 'cookie': """_gid=GA1.3.1091326087.1696932878; ftzjjszgovcn=0; arialoadData=true; ariawapChangeViewPort=false;ariaFixed=true; ariaReadtype=1; ariaoldFixedStatus=false; ariaStatus=false; Hm_lvt_ddaf92bcdd865fd907acdaba0285f9b1=1696938986,1696939309; pgv_pvid=9109716550; szfdc-session-id=07c9bccf-ab07-435c-b7de-1e512aad8c06; cookie_3.36_8080=85416329; ASP.NET_SessionId=z1lvyimtz3cg0aenlkynkbyc; _ga_34B604LFFQ=GS1.1.1697001288.9.1.1697001320.28.0.0; _ga=GA1.1.1493207979.1696932878; AD_insert_cookie_89188=35415771"""
        # 'x-csrf-token': 'abalGrijwUtgehoA6ShdrPCD'
    }
    r = requests.get(url, headers=headers, data=json.dumps(params))
    return r

response = get_response(url, params)

print(response.status_code)
print(response.text)


# df = pd.read_html(response.text)
# print(df)