<?
$status=fopen("http://volteck.net/proyecto/status.txt","r");
$line = fgets ($status);
echo $line;
fclose($status);
?>
