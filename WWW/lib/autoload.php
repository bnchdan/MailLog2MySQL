<?php


function autoloader( $class_name ){
    $file = __DIR__.'/'.$class_name.'.php';

    if ($class_name == "mysqli"){
        return 0;
    }

    if ( file_exists($file) ) {
        require_once $file;
    }
}

// add a new autoloader by passing a callable into spl_autoload_register()
spl_autoload_register( 'autoloader' );

