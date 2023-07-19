<?php
class DovecotLogs{    
    const PARAMS    = array(
            "month",
            "day",
            "hour",
            "domain",
            "email",
            "msgid",
            "log"
        );
    const TABLE     = "dovecot_logs";
    const LIMIT     = 20; 

    static function main($api){
        $dovecot = new DovecotLogs();
        Logs::doResponse($api, $dovecot);

    }    
}   