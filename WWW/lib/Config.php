<?php

class Config{

    const CONF_FILE = "/etc/MailLog2MySQL.conf";

    function __construct(){
    }

    public static function readFile($api){
        $handle = fopen(Config::CONF_FILE, "r");
        if ($handle) {
            while (($line = fgets($handle)) !== false) {
                
                $line =  preg_replace('/\s+/', '', $line);
                $type = explode("=", $line);

                #look for IP's
                if ($type[0] == "access"){
                    $api->setAccess( $type[1] );
                }

                if ($type[0] == "host"){
                    $api->db->setHost( $type[1] );
                }

                if ($type[0] == "user"){
                    $api->db->setUser( $type[1] );
                }

                if ($type[0] == "password"){
                    $api->db->setPassword( $type[1] );
                }

                if ($type[0] == "database"){
                    $api->db->setDatabase( $type[1] );
                }

                if ($type[0] == "port"){
                    $api->db->setPort( $type[1] );
                }
            }

            fclose($handle);
        }
    }
}
