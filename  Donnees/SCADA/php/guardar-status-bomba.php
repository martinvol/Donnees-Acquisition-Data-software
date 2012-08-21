<?
$status = $_GET['status'];
$fp = fopen("bomba.txt","w+");
fwrite($fp, $status);
fclose($fp); 
?>
