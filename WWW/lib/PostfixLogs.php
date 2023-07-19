<?php
class PostfixLogs{
    const PARAMS            = array(
                "month",
                "day",
                "hour",
                "mail_to",
                "mail_to_domain",
                "mail_from",
                "mail_from_domain",
                "satus",
                "msgid"
    );

    const TABLE             = "postfix_logs";
    const LIMIT             = 20;


    static function main($api){        
        $postfix = new PostfixLogs();
        Logs::doResponse($api, $postfix);
    }
    
}   