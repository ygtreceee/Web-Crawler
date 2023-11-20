include_once = "wxBizMsgCrypt.php";

define("TOKEN", "XXXXXX");  //填写自己的token

if (isset($_GET['echostr'])) {          //校验服务器地址URL
    valid();
}else{
    // 业务代码
}

function valid()
{
    $echoStr = $_GET["echostr"];
    if(checkSignature()){
        header('content-type:text');
        echo $echoStr;
        exit;
    }else{
        echo $echoStr.'+++'.TOKEN;
        exit;
    }
}

function checkSignature()
{
    $signature = $_GET["signature"];
    $timestamp = $_GET["timestamp"];
    $nonce = $_GET["nonce"];

    $token = TOKEN;
    $tmpArr = array($token, $timestamp, $nonce);
    sort($tmpArr, SORT_STRING);
    $tmpStr = implode( $tmpArr );
    $tmpStr = sha1( $tmpStr );

    if( $tmpStr == $signature ){
        return true;
    }else{
        return false;
    }
}
