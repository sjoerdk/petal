<?php
// write_to_file.php
// Author : Sjoerd Kerkstra
//
// Small utility to write content to a file. I entend to use this in ajax calls
// from jquery because writing files in jquery is just too annoying

//Versions
//V1 		10/02/2013   -  First working version


// ================ globals ==============================

$_DIRECTORY = "./";
define("DEBUG_PRINT",true);


// =============== get url params =======================

if(array_key_exists('report', $_GET)){
	$report = $_GET['report'];
	//do not allow going up the dir tree. Is this safe enough?
	$report = str_replace("..", "", $report);

}else
{
	$report = "";
}
$URL_file = getUrlParamOrDefault("file","","file to write to");
$URL_content = getUrlParamOrDefault("content","","Content for file");

// ================ main code ===========================



//check input dir
if(file_exists($_DIRECTORY)==False){
  echo("Error: reports dir '".$_DIRECTORY."' could not be found. Stopping script.<br/>\n");
  exit;
}



if(dataWasPosted()==true){
	//if data was posted that means a save should be done
	$text = getAllPostedKeysAsText();
	debugPrint("DEBUG Data was posted<br>\n");

	debugPrint("Received the following values:\n". $text);
	
	writeToFile($URL_content,$URL_file);
}
else{ echo("no post received");}


// =================== functions ======================

function writeToFile($content,$file_in){
	
	// Open the file to get existing content
	$current = file_get_contents($file_in);
	// write over 
	$current = $content;
	// Write the contents back to the file
	file_put_contents($file_in, $current);
	debugPrint("Wrote '".$content."' to file '".$file_in."'");
}


//if a form was posted, return all key values as text 
function getAllPostedKeysAsText(){
	$text = "";
	foreach(array_keys($_POST) as $key){		
		$value = $_POST[$key];		
		$text = $text.keyValuePairToText($key,$value);
	}
	return $text;
}


function getArrayAsText($arrayIn){
	$text = "";
	foreach($arrayIn as $element){		
			
		$text = $text.$element;
	}
	return $text;
}

function dataWasPosted(){
	if(count(array_keys($_POST)) > 0){
	
		return true;
	}else{
		return false;
	}
				
}

function keyValuePairToText($key,$value){
	//TODO: some type checking? 
	debugPrint("before:".$value);
	$text = htmlspecialchars($key."::".$value); 	
	$text = str_replace("\r\n", "<br/>", $text)."\n";
	debugPrint("after:".$text);
	return $text;
	

}


// get a parameter from the URL used to call this script (e.g. ?doThisAndThat = 1&name=kees etc..). Put default if not found.
function getUrlParamOrDefault($URLParamStr,$DefaultIfNotSet,$paramDescription){
		
	$value = $_POST[$URLParamStr];
	if($value != ""){	
	// if a value is given keep that 

	}else{
	    $value = $DefaultIfNotSet; 		// default value
	}
	
	registerUrlParam($URLParamStr,$DefaultIfNotSet,$paramDescription,$value);
	
	return $value;
}

// to be able to print help later
function registerUrlParam($URLParamStr,$DefaultIfNotSet,$paramDescription,$currentValue){

	debugPrint("Registering URL param '".$URLParamStr."'...");
	
	$param = createUrlParam($URLParamStr,$DefaultIfNotSet,$paramDescription,$currentValue);
		
	global $_URLPARAMS;	
	$_URLPARAMS[$URLParamStr] = $param;	
		
}

// to hold important info on a single url parameter for this script. 
// TODO: this is almost object oriented but not quite. How to do this properly in PHP?
function createUrlParam($URLParamStr,$DefaultIfNotSet,$paramDescription,$currentValue){
	$param = array();
	$param["string"] 			= $URLParamStr;
	$param["defaultValue"] 		= $DefaultIfNotSet;
	$param["paramDescription"] 	= $paramDescription;
	$param["currentValue"] 		= $currentValue;
	
	return $param;
}


//for printing debug info during development.
function debugPrint($msg){
	$trace=debug_backtrace();	 // get trace of all functions
	$caller=array_shift($trace); // get first element of trace
	$line = $caller["line"];	 // get printing line here because you want to know where the print statement is.
	$caller=array_shift($trace); // get second element for function name to skip this function (myPrint) and get function before.

	if(DEBUG_PRINT == True){
		echo "DEBUG - ".$caller["function"]." (".$line."): " .$msg."<br/>\n";
	}
}




?>
