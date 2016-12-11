## GMM Voice Recognizer

This is a MFCC-GMM-based voice recognizer implemented in Python. This repository contains a mirror of the directory structure for the web-hosted version as well as a standalone application to be used for testing.

## What is in here?

* The mirror of the web-hosted version is contained in the public_html directory.
* The standalone version is contained in voicerecognizer.py.
* More information about the implementation can be found in the GMM Voice Recongnizer - Writeup file.

## Using the standalone version

### Dependencies

* [NumPy](http://www.numpy.org/)
* [SciPy](https://www.scipy.org/)
* [scikits.talkbox](https://scikits.appspot.com/talkbox)
* [scikit-learn](http://scikit-learn.org/)

### Deployment

voicerecognizer.py can be run from the commandline as such:
```
python voicerecognizer.py trainingdir testdir
```
where trainingdir is a directory containing all of the training files and testdir is a directory containing all the testing files.

## Authors

Arlie Coles and Ines Patino Anaya built this tool for the course LING 550 - Computational Linguistics at McGill University.
