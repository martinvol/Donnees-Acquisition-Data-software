<?


$status=fopen("http://volteck.net/proyecto/ph-actual.txt","r"); 
$line = fgets ($status);
echo $line;
fclose($status);

$status=fopen("http://volteck.net/proyecto/02-actual.txt","r"); 
$line = fgets ($status);
echo $line;
fclose($status);

$status=fopen("http://volteck.net/proyecto/tem-actual.txt","r"); 
$line = fgets ($status);
echo $line;
fclose($status);


$status=fopen("http://volteck.net/proyecto/quehace.txt","r");
$line = fgets ($status);
echo $line;
fclose($status);

$status=fopen("http://volteck.net/proyecto/status-caldera.txt","r");
$line = fgets ($status);
echo $line;
fclose($status);

$status=fopen("http://volteck.net/proyecto/status.txt","r");
$line = fgets ($status);
echo $line;
fclose($status);

$status=fopen("http://volteck.net/proyecto/bomba.txt","r");
$line = fgets ($status);
echo $line;
fclose($status);
?>
