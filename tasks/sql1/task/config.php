<?php
   /*replace parameter's values with your local or remote database values */
   define('DB_SERVER', 'db:3306');
   define('DB_USERNAME', 'sqli');
   define('DB_PASSWORD', 'sqli');
   define('DB_DATABASE', 'sqli');
   $db = mysqli_connect(DB_SERVER,DB_USERNAME,DB_PASSWORD,DB_DATABASE);
?>
