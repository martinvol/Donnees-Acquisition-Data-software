<?
$status=fopen("http://volteck.net/proyecto/quehace.txt","r");
$line = fgets ($status);
echo $line;
fclose($status);
?>
