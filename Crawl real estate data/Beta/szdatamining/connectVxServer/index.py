from flask import Flask, request

app = Flask(__name__)

# 设置TOKEN常量
TOKEN = "abc123456"


@app.route('/', methods=['GET', 'POST'])
def wechat_callback():
    # 设置时区
    # 在Python中，时区设置通常不需要手动指定，而是由操作系统自动识别
    # 如果需要自定义时区，可以使用第三方库，例如pytz
    # date_default_timezone_set("Asia/Shanghai")

    # 打印请求的URL查询字符串到query.xml
    # Utils::traceHttp()
    trace_http()

    # 如果有"echostr"字段，说明是一个URL验证请求，
    # 否则是微信用户发过来的信息
    if 'echostr' in request.args:
        return valid()
    else:
        return response_msg()


def valid():
    echo_str = request.args.get('echostr', '')
    if check_signature():
        return echo_str
    return ''


def check_signature():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')

    token = TOKEN
    tmp_arr = [token, timestamp, nonce]
    tmp_arr.sort()
    tmp_str = ''.join(tmp_arr)
    tmp_str = hashlib.sha1(tmp_str.encode()).hexdigest()

    if tmp_str == signature:
        return True
    return False


def response_msg():
    post_str = request.data
    # 将数据打印到log.xml
    logger(post_str)
    if post_str:
        # 将XML数据解析为一个对象
        post_obj = ET.fromstring(post_str)
        rx_type = post_obj.find('MsgType').text.strip()
        # 消息类型分离
        if rx_type == 'event':
            result = receive_event(post_obj)
        else:
            result = "unknown msg type: " + rx_type
        # 打印输出的数据到log.xml
        logger(result, '公众号')
        return result
    return ''


def receive_event(obj):
    event_type = obj.find('Event').text.strip()
    if event_type == 'subscribe':
        content = "Thanks for following!!"
    else:
        content = "hhh"
    return transmit_text(obj, content)


def transmit_text(obj, content):
    xml_tpl = """<xml>
    <ToUserName><![CDATA[{to_user}]]></ToUserName>
    <FromUserName><![CDATA[{from_user}]]></FromUserName>
    <CreateTime>{create_time}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{content}]]></Content>
</xml>"""
    result = xml_tpl.format(
        to_user=obj.find('FromUserName').text.strip(),
        from_user=obj.find('ToUserName').text.strip(),
        create_time=int(time.time()),
        content=content
    )
    return result


def trace_http():
    # 打印请求的URL查询字符串到query.xml
    # Utils::traceHttp()
    pass


def logger(data, logger_name=''):
    # 将数据打印到log.xml
    pass


if __name__ == '__main__':
    app.run()