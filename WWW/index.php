<?php

require_once __DIR__.'/lib/autoload.php';

if ( explode("/",explode("?",$_SERVER['REQUEST_URI'])[0] )[1] == "api" ){
    Api::main();
}


?>

