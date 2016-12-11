#!/usr/bin/python

#
#This file reads the MFCC data of the training recording and constructs a GMM based on it. Then it returns a figure of the model to the user and lets them return to the home page.
#

import numpy as np
#Force matplotlib to bypass display/GUI and just save the .png plots without displaying them
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, sys
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn import mixture
from sklearn.externals import joblib

print "Content-Type: text/html"
print

#Parse arguments to get username/filename
filename = sys.argv[1]
filenameSplit = filename.split("/")
usernamePre = filenameSplit[3]
usernameSplit = usernamePre.split("_")
username = usernameSplit[0]

print "<font face=arial>"
print "<head><center><font size=14>Voice Recognizer</font></head>"
print "<br>"
print "This tool will make a thumbprint of your voice and then use it to tell you if you're the one speaking in another recording."

#Parse mfcc data and get it into a numpy array
filePath = "/home/2016/acoles/public_html/550uploads/mfcc/" + username + "_train.mfc"
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

#Make the gmm
#First "scale" the data so it fits in 64bit floats correctly (necessary for sklearn)
gmix = Pipeline([("scaler", StandardScaler()), ("gmix", mixture.GMM(n_components=3, covariance_type='full'))])
gmix.fit(input)

#Make a plot of the gmm and save it
colors = ['r' if i == 0 else 'r' for i in gmix.predict(input)]
ax = plt.gca()
ax.scatter(input[:, 0], input[:, 1], c=colors, alpha=0.8)
plt.savefig("/home/2016/acoles/public_html/550uploads/gmms/"+username+"_figure.png")

#Save the gmm data itself
gmmFile = "/home/2016/acoles/public_html/550uploads/gmms/"+username+".pkl"
joblib.dump(gmix, gmmFile, compress=1)

#Give a message and the figure to the user (exits back to inside callmakegmm.py where the figure is actually shown)
print "<br><br>"
print "<i><b>Your model has been made, "+username+".</b>"
print "<br>"
print "We made a multivariate Gaussian Mixture Model of your voice based on your MFCCs we extracted from your recording. Here's what it looks like:"