<?php
header("Content-Type: text/plain; charset=utf-8");

# Opening local DB
$connexion=new mysqli("localhost","root","--somepwd--","repart");
if($connexion->connect_errno) {
	printf("Connexion failed:\n%s",$connexion->connect_error);
	exit();
}
$connexion->query("SET NAMES utf8");

$query = "SELECT DISTINCT heures_prof FROM ClassesCombi ORDER BY heures_prof DESC";
$answer_hp = $connexion->query($query);

$indent="    ";
$convert = array(
	"8.067"=>"6.6+4/3*1.1",
	"5.133"=>"4.4+2/3*1.1",
	"4.767"=>"4.4+1/3*1.1"
);

printf("lecturesDataRaw = [\n");
$stringToWrite = "";
while($data_hp=$answer_hp->fetch_array()) {
	$heures = $data_hp[0];
	if($stringToWrite) {
		$stringToWrite .= $indent."}, {\n";
	} else {
		$stringToWrite = $indent."{\n";
	}
	
	$query = "SELECT classe FROM ClassesCombi WHERE heures_prof LIKE ".$heures;
	$answer_cl = $connexion->query($query);
	$classes = "";
	while($data_cl=$answer_cl->fetch_array()) {
		if($classes) {
			$classes .= "\", \"";
		}
		$classes .= $data_cl[0];
	}
	
	if(array_key_exists($heures,$convert)) {
		$heures = $convert[$heures];
	}
	$stringToWrite .=
		$indent.$indent."\"duration\": \"".$heures."\",\n".
		$indent.$indent."\"sections\": [\"".$classes."\"]\n";
}
printf($stringToWrite.$indent."}\n]\n\n");

printf("Done.");

# Closing local DB
$connexion->close();

?>
