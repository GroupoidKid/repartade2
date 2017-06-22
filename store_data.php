<?php
header("Content-Type: text/plain; charset=utf-8");

$rawData = array(
	"6.6+4/3*1.1"=>array(
		"TS.1+AP", "TS.2+AP"
	),
	"5.5"=>array(
		"1S.+AP", "1S.SES+AP"
	),
	"4.4+2/3*1.1"=>array(
		"TES.2+AP"
	),
	"5"=>array(
		"2GT.1+AP", "2GT.2+AP", "2GT.3+AP",
		"2GT.4+AP", "2GT.5+AP", "2GT.6+AP",
		"SIO.1.1", "SIO.1.2", "SIO.2.1.UF2"
	),
	"4.4+1/3*1.1"=>array(
		"TES.1+AP"
	),
	"3.3"=>array(
		"1ES.LES", "1ES", "1ES.SES",
		"1ST2S", "1STMG.1", "1STMG.2", "TST2S"
	),
	"3"=>array(
		"Prépa"
	),
	"2.5"=>array(
		"SIO.2.2.UF2"
	),
	"2.2"=>array(
		"TS.SpéM", "TSTMG.1", "TSTMG.2"
	),
	"1.65"=>array(
		"TES.SpéM"
	),
	"1.5"=>array(
		"2GT.MPS"
	),
	"1.25"=>array(
		"SIO.1.Algo1", "SIO.1.Algo2", "SIO.1.Algo3"
	),
	"1.1"=>array(
		"TS.ISN"
	),
	"0.75"=>array(
		"2GT.ICN"
	),
	"0.55"=>array(
		"1S.TPE", "1S.SES.TPE"
	),
);

# Opening local DB
$connexion=new mysqli("localhost","root","--somepwd--","repart");
if($connexion->connect_errno) {
	printf("Connexion failed:\n%s",$connexion->connect_error);
	exit();
}
$connexion->query("SET NAMES utf8");

$connexion->query("DELETE FROM ClassesCombi");

foreach($rawData as $hours=>$liste_classes) {
	foreach($liste_classes as $idx=>$course) {
		$dotidx = strpos($course,".");
		$type = substr($course, 0, $dotidx);
		if($dotidx==0) {
			$type=$course;
		}
		
		$query =
			"INSERT INTO ClassesCombi VALUES (".
			"\"".$type."\",".
			"\"".$course."\",".
			round(eval("return ".$hours.";"),3).
			")";
		$connexion->query($query);
		if($connexion->connect_errno) {
			printf(
				"Failed inserting course %s:\n%s\n",
				$course,$connexion->connect_error
			);
		};
	}
}

printf("Done.");

# Closing local DB
$connexion->close();

?>
