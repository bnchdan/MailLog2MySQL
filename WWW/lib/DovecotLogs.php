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

        return 0;
        $sql="SELECT * FROM ".DovecotLogs::TABLE;
        $limit="0,".DovecotLogs::LIMIT;
        if (isset( $_GET["page"]) && is_numeric($_GET["page"]) ){
            $limit = ($_GET["page"] - 1 )*DovecotLogs::LIMIT.", ";
            $limit.= DovecotLogs::LIMIT;
        }
             
        $toBind=array();
        $where="";
        SQL::createWhere(DovecotLogs::PARAMS,$where, $toBind );
        $sql.=" ". $where." LIMIT ".$limit;       
        $api->db->connect();
        $stmt= $api->db->conn->prepare($sql);        
        SQL::doBind($toBind, $stmt);
        $stmt->execute();
       
        $res = json_encode( $stmt->get_result()->fetch_all(MYSQLI_ASSOC) );

        $sql="SELECT count(*) as 'number of logs' FROM ".DovecotLogs::TABLE." ".$where;
        $stmt=$api->db->conn->prepare($sql);
        SQL::doBind($toBind, $stmt);
        $stmt->execute();
        $num_logs  = $stmt->get_result()->fetch_all()[0][0];
        $num_pages = floor($num_logs/DovecotLogs::LIMIT + 0.5);

        $msg ="{";
        $msg.="\"number of logs\":".$num_logs.",";
        $msg.="\"number of pages\":".$num_pages.",";
        $msg.="\"data\":".$res;
        $msg.="}";

        Api::response($msg);
    }    
}   