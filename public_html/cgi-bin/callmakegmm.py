#!/usr/bin/python

#
#
#This script is called from featurize.py and is executed on the CGI server (cgi.cs.mcgill.ca) in order to pass the form data. However, the CGI server has a too-low version of Python so cannot be used to run the scripts of the rest of the project. Therefore this extra layer is necessary. It performs preliminary file-system functions and then calls makegmm.py to be executed on the Teaching server (mimi.cs.mcgill.ca), which has the correct version of Python, by ssh-ing into acoles' account automatically with a pre-established fingerprint between the two servers.
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
filename = filename.rstrip('\r\n')
filename = filename.lstrip()
filename = filename[:-4]	#Strips off file extension

username = filename[:-6]	#Strips off '_train'

#Call makegmm.py on Teaching server
command1 = "ssh acoles@mimi.cs.mcgill.ca python ~/public_html/550uploads/makegmm.py ../550uploads/mfcc/"+filename+".mfc"

os.system(command1)

#Print the gmm figure to the user (for an unknown reason, when this bit of HTML is executed from within makegmm.py, the image cannot be shown)
print "<img src=\"../550uploads/gmms/"+username+"_figure.png\" alt=\"GMM\">"
print "<br><br>"
print "<a href=\"http://cgi.cs.mcgill.ca/~acoles/speechindex.php\">Go Back</a>"