<?php
class AuthLogs{
    const PARAMS    = array(
            "month",
            "day",
            "hour",
            "domain",
            "ip",
            "email",
            "log"
        );

    const TABLE     = "auth_logs";
    const LIMIT     = 20;

    static function main($api){       
        $auth = new AuthLogs();
        Logs::doResponse($api, $auth);
    }
    
}   