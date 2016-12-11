<?php

//
//
// The upload script for the training file. Uploads the training file to the server and stores it in /550uploads.
// For the sake of security, in this repository mirror, the web address will be replaced with the string "home page".
//
//

//Get basic info set up
$uploaddir = '550uploads/';
$uploadfile = $uploaddir . basename($_FILES['userfile']['name']);
$filename = basename($_FILES['userfile']['name']);
$ext = pathinfo($uploadfile, PATHINFO_EXTENSION);
$user_name = "acoles";


echo '<pre>';
//Make sure the extension of the file is .wav or .WAV
//If it isn't, throw an error
if ($ext !== 'wav' && $ext !=='WAV') {
?>
<html>
<body>
<font face="arial">

<head><center><font size=14>Voice Recognizer</font></head>

This tool will make a thumbprint of your voice and then use it to tell you if you're the one speaking in another recording.

<i><b>Error.</b>

Something went wrong. Make sure you're uploading a .wav file!</i>
<a href="home page">Go Back</a>
<?php
    exit();
    echo "Here is some more debugging info:";

    print_r($_FILES);
}

//Try to upload the file to the server
//If it was successful, build a page to let the user continue, and call callfeaturize.py
if (move_uploaded_file($_FILES['userfile']['tmp_name'], $uploadfile)) {
//Set open permissions on the file
chmod($uploadfile, 0777);
?>
<html>
<body>
<font face="arial">

<head><center><font size=14>Voice Recognizer</font></head>

This tool will make a thumbprint of your voice and then use it to tell you if you're the one speaking in another recording.

<i><b>Success!</b>

The file is valid, and was successfully uploaded.</i>
<br>
<form action="cgi-bin/callfeaturize.py" method="post">
<input type="submit" value="Continue to make the model" name="submit">
<input type="hidden" value="<?php echo $filename; ?>" name="filename">
</form>

<?php
//If it's not successful, throw an error
} else {
?>

<html>
<body>
<font face="arial">

<head><center><font size=14>Voice Recognizer</font></head>

This tool will make a thumbprint of your voice and then use it to tell you if you're the one speaking in another recording.

<i><b>Error.</b>

Something went wrong. Make sure you're uploading a .wav file!</i>
<a href="home page">Go Back</a>
<?php
    echo "Error!\n";
    echo 'Here is some more debugging info:';
    print_r($_FILES);
}


print "</pre>";

?>
