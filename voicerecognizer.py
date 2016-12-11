#This is a standalone version of the MFCC-GMM voice recognizer, to be used for testing.

#This code loops through a folder of training .wavs and a folder of testing .wavs and sees whether it can recognize the testing items after being trained on the training data. Outputs accuracy.
#Call it like this in the command line:
#python voicerecognizer.py trainingdir testdir
#Where trainingdir is the directory of training .wavs and testdir is the directory of test .wavs.
#Store this script in the same folder that contains trainingdir and testdir (NOT inside either trainingdir or testdir).

import scikits.talkbox.features
import scikits.talkbox
import scipy.io.wavfile
import os, sys
import numpy as np
import sklearn
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn import mixture
from sklearn.externals import joblib
import warnings

warnings.filterwarnings("ignore")

#Extracts mfccs
def extract_mfccCall(wavfilename):
    fs, wav = scipy.io.wavfile.read(wavfilename)
    return scikits.talkbox.features.mfcc(wav, fs=fs)[0]

def extract_mfcc(wavdir):
    mfccList = []
    for wavfilename in os.listdir(wavdir):
        ceps = extract_mfccCall(os.path.join(wavdir, wavfilename))
        mfccList.append(ceps)
    return mfccList


if __name__ == '__main__':
    trainingdir = sys.argv[1]
    testdir = sys.argv[2]

    #----------------------------#
    #----------Training----------#
    #----------------------------#

    #Get the MFCCs from the training data into a list.
    allTrainingMFCCs = extract_mfcc(trainingdir)


    #Get a list of the usernames of the training data
    trainingUsernames = []
    for trainingFile in os.listdir(trainingdir):
        trainingFileSplit = trainingFile.split("_") #Split before "_train.wav"
        username = trainingFileSplit[0] #Should just contain the username

        trainingUsernames.append(username)

    #Make a GMM for each training data file's MFCCs. Store the GMMs in a list.
    trainingGMMs = []
    for trainingfileMFCCs in allTrainingMFCCs: #For each item in the list

        #Convert the list into a numpy array
        input = np.array(trainingfileMFCCs)


        #Make a GMM from the numpy array of MFCCs
        gmix = Pipeline([("scaler", StandardScaler()), ("gmix", mixture.GMM(n_components=3, covariance_type='full'))])
        gmix.fit(input)

        #Put the GMM in the training GMM list
        trainingGMMs.append(gmix)


    #---------------------------#
    #----------Testing----------#
    #---------------------------#

    #Get the MFCCs from the test data into a list.
    allTestMFCCs = extract_mfcc(testdir)

    # Get a list of the usernames of the testing data
    testUsernames = []
    for testFile in os.listdir(testdir):
        testFileSplit = testFile.split("_")  # Split before "_train.wav"
        username = testFileSplit[0]  # Should just contain the username
        testUsernames.append(username)

    #Prepare counters for percent calculating at the end.
    totalCounter = 0
    correctCounter = 0

    #Test each test item.
    for testfileMFCCs in allTestMFCCs:
        #Convert the list into a numpy array
        input2 = np.array(testfileMFCCs)

        #Loop through list of trained GMMs and store loglikelihoods of fit with testing data.
        accuracies = []
        matchUsername = ""
        for trainingGMM in trainingGMMs:
            temp = trainingGMM.score(input2)
            mean = np.mean(temp.ravel())
            accuracies.append(mean)

            #The highest likelihood in the list corresponds to the match GMM
            maximum = max(accuracies)
            maximumIndex = accuracies.index(maximum)
            matchUsername = trainingUsernames[maximumIndex] #Username of matched GMM

        #If the username we just found as the most likely match from the training GMMs is the same as the username of this particular test file, then the recognizer got it right.
        if(testUsernames[totalCounter] == matchUsername):
            correctCounter = correctCounter + 1


        totalCounter = totalCounter + 1 #Increment with each pass of the outer for loop
        print (totalCounter)


    #Get percentage success rate
    percentCorrect = (correctCounter / totalCounter) * 100
    print("The recognizer recognizes correctly ")
    print(percentCorrect)
    print(" of the time.")