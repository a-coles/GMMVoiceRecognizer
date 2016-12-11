#!/usr/bin/python

#
#
#This script is called from upload4.php and is executed on the CGI server (cgi.cs.mcgill.ca) in order to pass the form data. However, the CGI server has a too-low version of Python so cannot be used to run the scripts of the rest of the project. Therefore this extra layer is necessary. It performs preliminary file-system functions and then calls featurize2.py to be executed on the Teaching server (mimi.cs.mcgill.ca), which has the correct version of Python, by ssh-ing into acoles' account automatically with a pre-established fingerprint between the two servers.
#
#

import cgi
import os, sys
import cgitb
cgitb.enable()
form = cgi.FieldStorage()

print "Content-Type: text/html"
print

filename = form.getvalue("filename")

#Copy the uploaded file into the recordings folder (changes owner from PHP default www-data to the server user, which allows featurize.py to be run on it; this is a bit of a workaround, but chown does not seem to do the job)
command1 = "ssh acoles@mimi.cs.mcgill.ca cp ~/public_html/550uploads/" + filename + " ~/public_html/550uploads/recordings"

#Call featurize2.py on Teaching server and run it there, where the libraries are installed/appropriate version of Python is
command4 = "ssh acoles@mimi.cs.mcgill.ca python ~/public_html/550uploads/featurize2.py ~/public_html/550uploads/recordings ~/public_html/550uploads/mfcc"

#After the file has been featurized, delete it from the recordings folder
command5 = "ssh acoles@mimi.cs.mcgill.ca rm ~/public_html/550uploads/recordings/" + filename

os.system(command1)
os.system(command4)
os.system(command5)