<?php
class Utils
{
    public static function traceHttp()
    {
        $content = date('Y-m-d H:i:s')."\n\rremote_ip：".$_SERVER["REMOTE_ADDR"].
            "\n\r".$_SERVER["QUERY_STRING"]."\n\r\n\r";
        $max_size = 1000;
        $log_filename = "./query.xml";
        if (file_exists($log_filename) and (abs(filesize($log_filename))) > $max_size){
            unlink($log_filename);
        }else {

        }
        file_put_contents($log_filename, $content, FILE_APPEND);
    }

    public static function logger($log_content, $type = '用户')
    {
        $max_size = 3000;
        $log_filename = "./log.xml";
        if (file_exists($log_filename) and (abs(filesize($log_filename)) >
                $max_size)) {
            unlink($log_filename);
        }
        file_put_contents($log_filename, "$type  ".date('Y-m-d H:i:s')."\n\r".$log_content."\n\r",
            FILE_APPEND);
    }
}