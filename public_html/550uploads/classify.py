#!/usr/bin/python

#
#This file reads the MFCC data of the testing recording and decides which stored GMM it is most likely described by. Then it returns the speaker of that GMM to the user as its guess for the speaker in the testing recording. It also returns a figure of the test GMM and a figure of the original GMM of the guessed speaker.
#

import cgi
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, sys
import math
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn import mixture
from sklearn.externals import joblib

print "Content-Type: text/html"
print

print "<font face=arial>"
print "<head><center><font size=14>Voice Recognizer</font></head>"
print "<br>"
print "This tool will make a thumbprint of your voice and then use it to tell you if you're the one speaking in another recording."
print "<br>"

#Parse arguments to get username/filename
filename = sys.argv[1]
filenameSplit = filename.split("/")
usernamePre = filenameSplit[3]
usernameSplit = usernamePre.split("_")
username = usernameSplit[0]

#Parse mfcc data and get it into a numpy array
filePath = "/home/2016/acoles/public_html/550uploads/mfcc/" + username + "_test.mfc"
with open(filePath, "r") as mfccs:
        content = mfccs.read().splitlines()

tmp = []
tmp2 = []
for line in content:
        tmp = []
        line = line.split(" ")
        for item in line:
                tmp.append(item)
        tmp2.append(tmp)

input = np.array(tmp2)

#Make the gmm, then make a plot of the test data (to show side-by-side later)
#First "scale" the data so it fits in 64bit floats correctly (necessary for sklearn)
testgmix = Pipeline([("scaler", StandardScaler()), ("testgmix", mixture.GMM(n_components=3, covariance_type='full'))])
testgmix.fit(input)

colors = ['r' if i == 0 else 'r' for i in testgmix.predict(input)]
ax = plt.gca()
ax.scatter(input[:, 0], input[:, 1], c=colors, alpha=0.8)
plt.savefig("/home/2016/acoles/public_html/550uploads/testgmms/"+username+"_figure.png")


#Loop through trained stored gmms and put them in a list
traininggmms = []
usernames = []
gmms = "/home/2016/acoles/public_html/550uploads/gmms"
for gmmfile in os.listdir(gmms):
        if gmmfile.endswith('.pkl'):
                traininggmms.append(joblib.load(os.path.join(gmms, gmmfile)))
                username = gmmfile[:-4]
                usernames.append(username)

#Loop through list of trained gmms and store loglikelihoods and likelihoods of predicted fit with testing data
accuracies = []
unLogAccuracies = []
for traininggmm in traininggmms:
        temp = traininggmm.score(input)
        mean = np.mean(temp.ravel())
        accuracies.append(mean)
        unLogAccuracies.append(math.pow(math.e, mean))

#Find highest likelihood in the list
maximum = max(accuracies)
unLogMax = max(unLogAccuracies)
maximumIndex = accuracies.index(maximum)

#If the likelihood is very low, the test data probably doesn't belong to anybody in the system.
#Use e^-25 for the lower threshold.
if unLogMax < math.pow(10, -25):
        print "<br>"
        print "<b>We don't think you're in our system.</b></i><br><br>"
        print "The likelihood of your test sample matching any of the speakers in our database is too low."
else:

        #Get username associated with the match of highest accuracy
        matchUsername = usernames[maximumIndex]

        #Store the matchUsername in a text file to be read by callclassify.py
        with open('/home/2016/acoles/public_html/550uploads/testgmms/match.txt', 'a+') as f:
                f.write(matchUsername)

        #Deliver feedback to user
        print "<br>"
        print "We think you are..."
        print "<br><b>"
        print matchUsername
        print "!</b>"
        print "<br><br></i>"
        print "Here are plots of your GMM voice models. They might be pretty similar."
        print "<br><br>"

        #If the match is very reliable, append the test data mfccs to the original training mfccs and run the gmm maker again.
        #This will create a better model and lets the system learn.
		#Use 10^-6 for the threshold.
        if unLogMatch > math.pow(10, -6):
                print "<i>We are also very certain of this match, so we'll be using its data to refine the model for this speaker."
                #Get the mfccs for the matched training data into a numpy array
                trainingmfccs = "/home/2016/acoles/public_html/550uploads/mfcc/"+matchUsername+"_train.mfc"
                with open(trainingmfccs, "r") as train:
                        traincontent = train.read.splitlines()
                tmp3 = []
                tmp4 = []
                for line in traincontent:
                        tmp3 = []
                        line = line.split(" ")
                        for item in line:
                                tmp3.append(item)
                        tmp4.append(tmp3)
                traininginput = np.array(tmp4)

                #Concatenate the traininginput and just-matched input arrays of mfccs
                learnedinput = numpy.concatenate(input, traininginput)

                #Make a gmm out of the improved learnedinput
                learnedgmm = Pipeline([("scaler", StandardScaler()), ("learnedgmm", mixture.GMM(n_components=3, covariance_type='full'))])
                learnedgmm.fit(learnedinput)
                #Make a plot and save it over the old one
                colors = ['r' if i == 0 else 'r' for i in learnedgmm.predict(learnedinput)]
                ax = plt.gca()
                ax.scatter(learnedinput[:, 0], learnedinput[:, 1],  c=colors, alpha=0.8)
                plt.savefig("/home/2016/public_html/550uploads/gmms/"+matchUsername+"_figure.png")
                #Save the gmm itself and save it over the old one
                learnedgmmFile = "/home/2016/acoles/public_html/550uploads/gmms/"+matchUsername+".pkl"
                joblib.dump(learnedgmm, learnedgmmFile, compress=1)