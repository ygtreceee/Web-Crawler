import os.path
import requests
from io import StringIO
import pandas as pd
import numpy as np
import smtplib   # 用于邮件的发信动作
from email.header import Header  # 构建邮件头
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText    # 纯文本，HTML
from email.mime.image import MIMEImage  # 图片
from email.mime.multipart import MIMEMultipart  # 多种组合内容



# 数据采集
def getData():
    # 数据接口地址
    url = 'http://zjj.sz.gov.cn/ris/szfdc/showcjgs/esfcjgs.aspx'
    # 请求头
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": '_gid=GA1.3.1091326087.1696932878; ftzjjszgovcn=0; Hm_lvt_ddaf92bcdd865fd907acdaba0285f9b1=1696938986,1'
                  '696939309; pgv_pvid=9109716550; _ga=GA1.1.1493207979.1696932878; _ga_34B604LFFQ=GS1.1.1697042880.11.0.'
                  '1697042880.60.0.0; szfdc-session-id=1ee9cbbc-042b-44c7-8717-46683af4bf1d; cookie_3.36_8080=85416329; A'
                  'SP.NET_SessionId=0gw5sa45jhjhkv2titceugyo; AD_insert_cookie_89188=41343527',
        "Host": "zjj.sz.gov.cn",
        "Origin": "http://zjj.sz.gov.cn",
        "Referer": "http://zjj.sz.gov.cn/ris/szfdc/showcjgs/esfcjgs.aspx",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0"
                      " Safari/537.36",
    }
    # 请求体参数
    params = {
        "scriptManager1": "updatepanel1|hypAll",
        "__EVENTTARGET": "hypAll",
        "__EVENTARGUMENT": "__VIEWSTATE: vfa0Ry8IbEzcDAJ7N4LvrqDLP2qYAgcNdC51XPDvWvY+OT8BIlXDV/VS7lkMebpc/hh9oGVGiTCslWLd"
                           "LpS8/VSHkH/CdF9mux70U8iSMctsySxR8y6tiWr17EAMmj4w6hD/6VRhuXAQXbTrQ4XLIr+qXD9lh8nn1Xv4aJ43oDEmx"
                           "2rUx/yiKRf6xwXbssj2puZMdeYIRxBD5QgeTEBe8mVtPFzNZTQBddmfJpfoooiNFQSCLhDqwg71F3iUshkI76arvTds1n"
                           "epmXbcBdD8cOoeDk64x+VLTeoX00Nd9/T4qE47mVH2n8LowHvaFLw4OcB/VwxnYKayNMnMuqdX2BKKMUymxNrdzXTsKmB"
                           "w5kC/6I1iuTBQaI1ZUssjLC4vhajnUzwfFiIO29+ewzE4TNX3iGzyFlOobaJFW0m/D6mBSzIWx4jNdFDufFJKRt9sM4oc"
                           "AUO0fLBiKK010r6ymPzG8218o8S2P5gNwvypzUZB7qsNObkemdDveTSP0LRU18cI5fKaJqZK7yj9C7nlsFq9SuV5oEqnB"
                           "XJrJ3wmPMTFr6kmsw9v3xEHpJ0b3XJJ0aSYl2ajRvvkXDpGncY6Qqs/91A=",
        "__VIEWSTATEGENERATOR": "778BEB03",
        "__VIEWSTATEENCRYPTED": "__EVENTVALIDATION: C/u+Aqeh8URvYiu93bTuarHjWYOwuAOA53lEsPJReN5G0ItO96PWICQKueU3kq4BYZU/Z"
                                "HqzDwna9umInUg2ej9umA/ev1aCae9h+Lc5Yn3xvlaEeOlCP2y4WtxotbySdRKuL368Yb7D+jNfzK1ykauQgorjK"
                                "tQUw5TrXXS5d2yOM+NdsNm0db5gJRSJ9qe+LKuBVg==(empty)",
    }
    html = requests.post(url=url, headers=headers, json=params)
    return html

# html.json()返回得到在浏览器看到的json格式数据


# 将数据转化为表格
def toTable(html):

    # df = pd.DataFrame(html.json()['data'])
    # 字段可重命名， 省略
    # df.rename(columns={}, inplace=True)
    # 可reindex为只取我们需要的columns字段
    # df = df.reindex(columns=[])
    # 降维：pass 2-d input. shape=(2, 6, 3)
    rh = pd.read_html(StringIO(html.text))
    data = np.array(rh)
    data_2d = data.reshape(-1, data.shape[-1])
    df = pd.DataFrame(data_2d, columns=['用途', '成交面积(㎡)', '成交套数'])
    return df


# 发送邮件
def sendEmail(title, content, file):
    """
    :param title: 邮件主题
    :param content: 邮件正文
    :param file: 附件正文
    :return:
    """

    global msgobj
    user = "643788048@qq.com"  # 发送人邮箱
    pwd = "yrsniysgrwndbcgb"    # 邮箱授权码
    receivers = ['1211505556@qq.com', '2472062511@qq.com']   # 接收人邮箱
    smtp_server = 'smtp.qq.com'  # 发信服务器
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText('使用python发送邮件测试', 'plain', 'utf-8')
    # 邮件头信息
    msg['From'] = Header('Give<643788048@qq.com>')  # 发送者
    msg['To'] = Header(",".join(receivers))  # 接收者
    subject = 'Python SMTP 邮件测试'
    msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
    try:
        msgobj = smtplib.SMTP_SSL(smtp_server)
        msgobj.connect(smtp_server, 465) # 建立连接--qq邮箱服务和端口号
        msgobj.login(user, pwd)  # 登录--发送者账号和口令
        msgobj.sendmail(user, receivers, msg.as_string())
        print('Successful')
    except smtplib.SMTPException:
        print("Unsuccessful")
    finally:
        msgobj.quit()  # 关闭服务器

    # 构建邮件
    # msg = MIMEMultipart()
    # msg['From'] = user
    # msg['to'] = ",".join(receivers)
    # # 添加邮件主题
    # msg['Subject'] = title
    # msg.attach(MIMEText(content, 'html', 'utf-8'))
    # # 添加附件
    # att = MIMEApplication(open(file, 'rb').read())
    # att.add_header('Content-Disposition',
    #                'attachment',
    #                filename=Header(os.path.basename(file), 'utf-8').encode())
    # msg.attach(att)
    #
    # # 发送邮件
    # smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
    # smtp.login(user, pwd)
    # smtp.sendmail(user, receivers, msg.as_string())
    # print('Successfully send!')
    # smtp.quit()


if __name__ == '__main__':
    html = getData()    # 获取数据
    df = toTable(html)  # 转换为表格

    # 保存为excel文件
    file = './data.xlsx'  # 保存文件路径
    writer = pd.ExcelWriter(file)
    df.to_excel(writer, sheet_name='sheet1', index=False)
    writer._save()

    # 构建邮件内容
    title = '数据报告'
    content = df.to_html(index=True, index_names=True)
    content += '邮件内容为今日数据报告，请各位查收'
    sendEmail(title, content, file)



