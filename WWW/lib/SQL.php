<?php

class SQL{

    private $host;
    private $user;
    private $password;
    private $database;
    private $port;

    public function setHost($host){
        $this->host =$host;
    }

    public function setUser($user){
        $this->user =$user;
    }

    public function setPassword($password){
        $this->password =$password;
    }

    public function setDatabase($database){
        $this->database =$database;
    }

    public function setPort($port){
        $this->port =$port;
    }

    public function connect(){
        // Create connection
        $this->conn = new mysqli(
            $this->host, 
            $this->user, 
            $this->password, 
            $this->database,
            $this->port
        );

        if ($this->conn->connect_error){
            $this->showError($this->conn->connect_error);
        }
        
    }

    public function close(){
        $this->conn =null;
    }

    public function showError($msg){
        ob_clean();
        header('Content-Type: application/json; charset=utf-8');
        die("{\"msg\":\"".$msg."\"}");
        http_response_code(403);
    }

    public function showConfig(){
        echo $this->host ."<br>";
        echo $this->user ."<br>";
        echo $this->password ."<br>";
        echo $this->database ."<br>";
        echo $this->port ."<br>";
    }

    public function print($sql ){
        $this->connect();
        $stmt =$this->conn->prepare($sql);
        $stmt->execute($sql);
        var_dump($stmt->get_result()); 
        $stmt->close();
        $this->close();
    }
    
    static public function doBind($toBind, $stmt){
        $bindParams="";
        for ($i=0; $i<count($toBind); $i++){
            if ( $i!= 0 )
                $bindParams.=", ";
            $bindParams.="\$toBind[".$i."]";
        }
        if ($bindParams!=""){
            eval("\$stmt->bind_param(\"".str_repeat("s", count($toBind))."\",".$bindParams.");");
        }
    }
}