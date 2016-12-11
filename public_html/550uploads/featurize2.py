#
#This file extracts MFCCs from the testing recording and stores them in the mfccs folder.
#

import scikits.talkbox.features	#Needed to extract MFCCs
import scikits.talkbox
import scipy.io.wavfile			#Needed to read the wav file
import os, sys

#This methodology to get the MFCCs is modeled from HW5. 
def extract_mfcc(wavfilename):
    fs, wav = scipy.io.wavfile.read(wavfilename)
    return scikits.talkbox.features.mfcc(wav, fs=fs)[0]

if __name__=='__main__':
    print "Content-Type: text/html"
    print

    print "<font face=arial>"
    print "<head><center><font size=14>Voice Recognizer</font></head>"
    print "<br>"
    print "This tool will make a thumbprint of your voice and then use it to tell you if you're the one speaking in another recording."

	#Extract MFCCs and store them
    wavdir = sys.argv[1]
    mfcdir = sys.argv[2]
    for wavfilename in os.listdir(wavdir):
        if wavfilename.endswith('.wav'):
            ceps = extract_mfcc(os.path.join(wavdir, wavfilename))
            scipy.savetxt(os.path.join(mfcdir, os.path.splitext(wavfilename)[0]+'.mfc'), ceps)
            filename = wavfilename

	#Returns a page to the user with the MFCCs
    filenameSplit = filename.split("_")
    username = filenameSplit[0]

    print "<br><br>"
    print "<i><b>Thanks for uploading your file, "+username+". </b>"
    print "<br>"
    print "First we'll extract the MFCCs from your recording. Here they are:"
    print "<font face=\"courier new\" color=\"red\">"
    print "<br><br>"

    print "<table border=\"1\" color=\"red\"><td width=\"500\" height=\"300\">"
    print " <div style=\"width: 500px; height: 300px; overflow: auto\">"

    mfccpath = "/home/2016/acoles/public_html/550uploads/mfcc/"+username+"_test.mfc"
    mfccs = open(mfccpath, "r")
    for line in mfccs:
        print line

	#Let the user continue to callclassify.py
    print "</div></td></table>"
    print "<br><br>"
    print "<form action=\"../cgi-bin/callclassify.py\" method=\"post\">"
    print "<input type=\"submit\" value=\"Continue to the next step - make a model\" name=\"submit\">"
    print "<input type=\"hidden\" value=\""
    print filename
    print "\" name=\"filename\">"
    print "</form>"