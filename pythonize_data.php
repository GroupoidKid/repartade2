<?php
header("Content-Type: text/plain; charset=utf-8");

# Ouverture DB
$connexion=new mysqli("localhost","root","--somepwd--","repart");
if($connexion->connect_errno) {
	printf("Echec de la connexion:\n%s",$connexion->connect_error);
	exit();
}
$connexion->query("SET NAMES utf8");

$query = "SELECT * FROM ClassesCombi ORDER BY heures_prof DESC, classe ASC";
$answer = $connexion->query($query);

while($data=$answer->fetch_array()) {
	list($type,$classe,$heures) = $data;
	printf("r.addClass(\"%s\",%.3f)\n",$classe,$heures);
}

printf("Done.");

# Fermeture DB
$connexion->close();

?>
