<?
$status = $_GET['status'];
$fp = fopen("todo.txt","w+");
fwrite($fp, $status);
fclose($fp); 
?>
