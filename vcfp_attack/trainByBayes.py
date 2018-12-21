#!/usr/bin/python

import os
import sys
import sklearn
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
import argparse
import numpy as np

import fileUtils
import tools


def saveModel(modelData, fpath):
    joblib.dump(modelData, fpath)


def readfile(fpath):
    tmpList = []
    for line in fileUtils.readTxtFile(fpath, ','):
        tmp = line.split(',')
        if len(tmp) > 4:
            tmp_multi = fileUtils.str2int(tmp[3]) * fileUtils.str2int(tmp[4])
        else:
            tmp_multi = fileUtils.str2int(tmp[-1]) * fileUtils.str2int(tmp[-2])
        tmpList.append(tmp_multi)
    return tmpList


def computeFeature(fpath, rangeList):
    start, end, interval = rangeList[0], rangeList[1], rangeList[2]
    rangeList, sectionList = tools.getSectionList(start, end, interval)
    features = readfile(fpath)
    for feat in features:
        index = tools.computeRange(rangeList, feat)
        sectionList[index] += 1

    return sectionList


def computeAllFeature(dpath):
    fileList = fileUtils.genfilelist(dpath)
    allFeatures = []
    for fpath in fileList:
        tmpFeat = computeFeature(fpath)
        allFeatures.append(tmpFeat)

    return np.array(allFeatures)


def train(trainData, trainLabel):
    gnb = GaussianNB()
    y_pred = gnb.fit(trainData, trainLabel)
    return y_pred


def main(opts):
    trainDataDir = opts.trainDataDir
    data, label = loadTrainData(trainDataDir)
    mymodel = train(data, label)
    saveModel(mymodel, opts.modelSaveDir)
    print('model saved at {}'.format(opts.modelSaveDir))


def parseOpts(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--trainDataDir', help='path to training data dir')
    parser.add_argument('-m', '--modelSaveDir', help='path to model save dir')
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    opts = parseOpts(sys.argv)
    main(opts)
