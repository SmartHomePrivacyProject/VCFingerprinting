#!/usr/bin/python

import os
import sys
import argparse
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
from sklearn.metrics import classification_report
import numpy as np


def test(mymodel, testData):
    label = mymodel.predict(testData)
    return label

def main(opts):
    modelFile = opts.modelFile
    testDataFile = opts.testDataFile
    mymodel = joblib.load(modelFile)
    testData = readfile(testDataFile)
    prediction = test(model, testData)
    print('predicted label is: {}'.format(prediction))


def parseOpts(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--modelFile', help='path to model file')
    parser.add_argument('-t', '--testDataFile', help='path to test data file')
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    opts = parseOpts(sys.argv)
    main(opts)
