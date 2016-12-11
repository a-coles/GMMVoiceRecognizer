#!/usr/bin/python

#
#
#This script is called from featurize2.py and is executed on the CGI server (cgi.cs.mcgill.ca) in order to pass the form data. However, the CGI server has a too-low version of Python so cannot be used to run the scripts of the rest of the project. Therefore this extra layer is necessary. It performs preliminary file-system functions and then calls classify.py to be executed on the Teaching server (mimi.cs.mcgill.ca), which has the correct version of Python, by ssh-ing into acoles' account automatically with a pre-established fingerprint between the two servers.
#
# For the sake of security, in this repository mirror, the web address will be replaced with the string "home page".
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

username = filename[:-5]	#Strips off '_test'

#Call classify.py on non-cgi server

command1 = "ssh acoles@mimi.cs.mcgill.ca python ~/public_html/550uploads/classify.py ../550uploads/mfcc/"+ filename + ".mfc"

os.system(command1)

#Display side-by-side GMMs to the user (for an unknown reason, when this bit of HTML is executed from within classify.py, the images cannot be shown)
#Also retrieve the username of the match found from the file written to by classify.py, if there is a match. If there's not, catch the error and direct user back to the home page.
try:
		#Open the file containing the username (if it exists)
        with open('/home/2016/acoles/public_html/550uploads/testgmms/match.txt', 'r') as f:
                match = f.readline()
        match = match.rstrip('\r\n')

        print "<table><tr><td align=\"center\"><img src=\"../550uploads/gmms/"+match+"_figure.png\" style=\"width: 75%; height: 75%\"></td>"
        print "<td align=\"center\"><img src=\"../550uploads/testgmms/"+username+"_figure.png\" style=\"width: 75%; height: 75%\"></td></tr>"
        print "<tr><td align=\"center\">GMM for <b>"+match+"</b> (training data)</td>"
        print "<td align=\"center\">GMM for <b>"+username+"</b> (test data)</td></tr></table>"
        print "<br><br>"
        print "<a href=\"home page">Back Home</a>"

        #Delete the file containing the username (it will be created again at the next call, etc.)
        os.system("ssh acoles@mimi.cs.mcgill.ca rm ~/public_html/550uploads/testgmms/match.txt")

except IOError:
        print "<br><br>"
        print "<a href=\"home page">Back Home</a>"
