<?php
// the message
$msg = "First line of text\nSecond line of text!!!!!!!!!!!!\n test test";

// use wordwrap() if lines are longer than 70 characters
$msg = wordwrap($msg,70);


// send email
mail($_POST["email"],"Confirmation Email",$msg);

// test input
echo $_POST["email"];
?>