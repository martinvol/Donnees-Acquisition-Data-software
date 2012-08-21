<?
$status=fopen("http://volteck.net/proyecto/status-caldera.txt","r");
$line = fgets ($status);
echo $line;
fclose($status);
?>
