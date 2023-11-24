<?php
//设置时区
date_default_timezone_set("Asia/Shanghai");
//定义TOKEN常量，这里的"weixin"就是在公众号里配置的TOKEN
define("TOKEN", "abc123456");

require_once("Utils.php");
//打印请求的URL查询字符串到query.xml
Utils::traceHttp();

$wechatObj = new wechatCallBackapiTest();
/**
 * 如果有"echostr"字段，说明是一个URL验证请求，
 * 否则是微信用户发过来的信息
 */
if (isset($_GET["echostr"])){
    $wechatObj->valid();
}else {
    $wechatObj->responseMsg();
}

class wechatCallBackapiTest
{
    /**
     * 用于微信公众号里填写的URL的验证，
     * 如果合格则直接将"echostr"字段原样返回
     */
    public function valid()
    {
        $echoStr = $_GET["echostr"];
        if ($this->checkSignature()){
            echo $echoStr;
            exit;
        }
    }

    /**
     * 用于验证是否是微信服务器发来的消息
     * @return bool
     */
    private function checkSignature()
    {
        $signature = $_GET["signature"];
        $timestamp = $_GET["timestamp"];
        $nonce = $_GET["nonce"];

        $token = TOKEN;
        $tmpArr = array($token, $timestamp, $nonce);
        sort($tmpArr);
        $tmpStr = implode($tmpArr);
        $tmpStr = sha1($tmpStr);

        if ($tmpStr == $signature){
            return true;
        }else {
            return false;
        }
    }

    /**
     * 响应用户发来的消息
     */
    public function responseMsg()
    {
        //获取post过来的数据，它一个XML格式的数据
//         $postStr = $GLOBALS["HTTP_RAW_POST_DATA"];
        $postStr = file_get_contents('php://input');
        //将数据打印到log.xml
        Utils::logger($postStr);
        // if (!empty($postStr)){
            //将XML数据解析为一个对象
            $postObj = simplexml_load_string($postStr, 'SimpleXMLElement', LIBXML_NOCDATA);
            $RX_TYPE = trim($postObj->MsgType);

            // //消息类型分离
            // switch($RX_TYPE){
            //     case "event":
            $result = $this->receiveEvent($postObj);
                //     break;
                // default:
                //     $result = "unknow msg type:".$RX_TYPE;
                //     break;
            // }
            //打印输出的数据到log.xml

            Utils::logger($result, '公众号');
            echo $result;
        // }else{
        //     echo "";
        //     exit;
        // }
    }

    /**
     * 接收事件消息
     */
    private function receiveEvent($object)
    {
        switch ($object->Event){
            //关注公众号事件
            case "subscribe":
                // $pythonScript = './python_script.py';

                // $pythonCode = "print(222)";
                // $output = shell_exec("/usr/bin/python3 -c '{$pythonCode}'");
                // echo $output;
                $content = "感谢您关注深房先知！\n 欢迎您查看昨日数据报告，点击下方链接即可进入查看。\n http://114.132.235.86/#/0 ";
                // $content_first = "感谢您关注深房先知！";
                // $content_second = "欢迎您查看昨日数据报告，点击下方链接即可进入查看。\n http://114.132.235.86/#/0";
                // exec('/usr/bin/python3 /www/wwwroot/crawler/connectVxServer/a.py', $output, $return_var);
                // $content = $return_var;
                // $content = $this->f();

                // $pythonCode = "print('Hello, from Python!')";
                // exec("python3 -c '{$pythonCode}' 2>&1", $output);
                // $content = implode("\n", $output);
                $weekday = date('N');
                $url = 'http://szdatamining.com/#/' . $weekday;
                $contentArray = array(
                    array(
                        'title' => '感谢您关注深房先知！',
                        'description' => 'Thanks for following szdatamining!',
                        'picUrl' => '',
                        'url' => ''
                    ),

                     array(
                        'title' => "每日9:30自动推送深圳一二手房成交信息",
                        'description' => '',
                        'picUrl' => '',
                        'url' => "",
                    ),
                    array(
                        'title' => "欢迎查看昨日数据报告，点击即可进入查看",
                        'description' => '',
                        'picUrl' => '',
                        'url' => $url
                    ),
                    // 添加更多的消息
                );
//              $result = transmitTexts($object, $contentArray);
//              echo $result;
                break;
            default:
                $content = "hhh";
                break;
        }
        // Utils::logger("hhh", '公众号');
        $result = $this->transmitTexts($object, $contentArray);
        return $result;
    }

    /**
     * 回复多条文本消息
     * @param object $object 消息对象
     * @param array $contentArray 回复的消息内容数组
     */
    private function transmitTexts($object, $contentArray)
    {
        $xmlTpl = "<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime><![CDATA[%s]]></CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>%s</ArticleCount>
        <Articles>%s</Articles>
        </xml>";

        $itemTpl = "<item>
        <Title><![CDATA[%s]]></Title>
        <Description><![CDATA[%s]]></Description>
        <PicUrl><![CDATA[%s]]></PicUrl>
        <Url><![CDATA[%s]]></Url>
        </item>";

        $itemStr = '';
        foreach ($contentArray as $content) {
            $itemStr .= sprintf($itemTpl, $content['title'], $content['description'], $content['picUrl'], $content['url']);
        }

        $result = sprintf($xmlTpl, $object->FromUserName, $object->ToUserName, time(), count($contentArray), $itemStr);
        return $result;
    }
}