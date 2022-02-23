<?php
   include('session.php');
?>
<html>
<!--
Author:Dnyaneshwar Giri
Date:26-03-2019
-->
   <head>
      <title>Welcome </title>
   </head>
   <body>
      <h1>Welcome <?php echo $login_session; ?></h1>
      <h2><a href = "logout.php">Sign Out</a></h2>
      <p>Your first flag is <b>HITS{g00d_st4rt_br0}</b></p>
	</body>
</html>
