<?php


class Logs{

    static function doResponse($api, $log){
        $sql="SELECT * FROM ".$log::TABLE;
        $limit="0,".$log::LIMIT;
        if (isset( $_GET["page"]) && is_numeric($_GET["page"]) ){
            $limit = ($_GET["page"] - 1 )*$log::LIMIT.", ";
            $limit.= $log::LIMIT;
        }
             
        $toBind=array();
        $where="";
        Logs::createWhere($log::PARAMS,$where, $toBind );
        $sql.=" ". $where." LIMIT ".$limit;       
        $api->db->connect();
        $stmt= $api->db->conn->prepare($sql);        
        SQL::doBind($toBind, $stmt);
        $stmt->execute();
       
        $res = json_encode( $stmt->get_result()->fetch_all(MYSQLI_ASSOC) );

        $sql="SELECT count(*) as 'number of logs' FROM ".$log::TABLE." ".$where;
        $stmt=$api->db->conn->prepare($sql);
        SQL::doBind($toBind, $stmt);
        $stmt->execute();
        $num_logs  = $stmt->get_result()->fetch_all()[0][0];
        $num_pages = ceil($num_logs/$log::LIMIT);

        $msg ="{";
        $msg.="\"number of logs\":".$num_logs.",";
        $msg.="\"number of pages\":".$num_pages.",";
        $msg.="\"data\":".$res;
        $msg.="}";

        Api::response($msg);
    }

    static public function createWhere($params,&$where, &$toBind){
        $where="WHERE ";
        for ($i=0; $i<count($params); $i++){
            echo $params[$i];
            if (isset( $_GET[$params[$i]])){
                $where.=" ".$params[$i]." =? AND";
                array_push($toBind, $_GET[$params[$i]]);
            }
        }
        if ( count($toBind) == 0){
            $where=NULL;
            return 0;
        }
        $where = substr($where, 0, strlen($where) - 4);
    }   
}