<?php

class Api{
    private $access=[];
    private $api_key;
    public  $db;
    function __construct(){
        $this->db=new SQL();
        Config::readFile($this);
        //check IP
        $this->checkIP();
    }

    public function setAccess($access){
        
        $this->access = json_decode($access);
        if ($this->access == NULL) { 
            Api::block("Invalid access IP's format in conf file");
        }
    }

    public function setKey($key){
        $this->api_key = $key;
    }

    public function checkIP(  ) {
        $ip = Api::getIP();
        foreach($this->access as $ip_allowed){
            if ( $ip === $ip_allowed ){
                return;
            }
        }
        Api::block("Permission denied");
      }



    public static function getIP(){
        return $_SERVER['REMOTE_ADDR'];
    }


    public static function block($msg){
        ob_clean();
        header('Content-Type: application/json; charset=utf-8');
        die("{\"msg\":\"".$msg."\"}");
        http_response_code(403);
    }

    public static function response($msg){
        ob_clean();
        header('Content-Type: application/json; charset=utf-8');
        die($msg);
        http_response_code(200);
    }

    public static function main(){
        
        $api=new Api();
        
        /***
         * 
         * ?table=auth_logs
         * ?table=dovecot_logs
         * ?table=postfix_logs
         */

        if ( isset($_GET['table']) && $_GET['table']==="auth_logs"){
           AuthLogs::main($api);
        }
        if ( isset($_GET['table']) && $_GET['table']==="dovecot_logs"){
           DovecotLogs::main($api);
        }
        if ( isset($_GET['table']) && $_GET['table']==="postfix_logs"){
           PostfixLogs::main($api);
        }
        
        $resp="{";
        $resp.="\"auth_logs\":[\"month\",\"day\",\"hour\",\"domain\",\"ip\",\"email\",\"log\"],";
        $resp.="\"dovecot_logs\":[\"month\",\"day\",\"hour\",\"domain\",\"email\",\"msgid\",\"log\"],";
        $resp.="\"postfix_logs\":[\"month\",\"day\",\"hour\",\"mail_to\",\"mail_to_domain\",\"mail_from\",\"mail_from_domain\",\"status\",\"msgid\"]";
        $resp.="}";
        Api::response($resp);
    }
}


/**
 * 
 * 
 * 
 */