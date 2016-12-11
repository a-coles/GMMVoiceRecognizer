<!DOCTYPE html>

<!-- The front-end home page of the system. Provides a training upload & instructions and a testing upload & instructions. -->


<html>
<body>
<font face="arial">

<head><center><font size=14>Voice Recognizer</font></head>
<br>
This tool will make a thumbprint of your voice and then use it to tell you if you're the one speaking in another recording.
</center>
<br>

<table cellpadding="20">
<th>1. Training</th><th>2. Testing</th>
<tr>
<td width="50%">

<!-- Training upload and instructions -->
<form action="upload3.php" method="post" enctype="multipart/form-data">
        First we need to train a model of your voice. Please follow the directions below to get started:
        <ol>
                <li>Pick a username for yourself. This is what we'll be identifying you by in our system, so you might not want to use your full name if you'd rather not have that information publicly available. Don't use any spaces or special characters; stick to alphanumeric characters.</li>
                <li>Record yourself speaking. You can say anything you want, as long as it lasts from 5-10 seconds.</li>
                <li>Save the file in the format <i>username_train.wav</i>. It's important that the recording be in .wav format; otherwise you'll be asked to upload again.</li>
                <li>Upload the file below.</li>
        </ol>
        <input type="file" name="userfile" id="userfile">
        <input type="submit" value="Upload" name="submit">
</form>
<br>
</td>

<td width="50%">

<!-- Testing upload and instructions -->
Once we've trained a model for you, you can see if we can recognize your voice in another recording. To do that, please follow these directions:
<ol>
        <li>Pick a second username for yourself different from the one you used to train (otherwise we could cheat and simply match your usernames instead of running an analysis!).</li>
        <li>Record yourself saying whatever you want again. Make it different from what you said for the training data, if possible. Again, keep it between 5-10 seconds in length.</li>
        <li>Save the file in the format <i>newusername_test.wav</i>. Again, make sure it's in .wav format.</li>
        <li>Upload the file below.</li>
</ol>
<form action="upload4.php" method="post" enctype="multipart/form-data">
        <input type="file" name="userfile" id="userfile">
        <input type="submit" value="Upload" name="submit">
</form>
</td>
</tr>
</table>

</body>
</html>