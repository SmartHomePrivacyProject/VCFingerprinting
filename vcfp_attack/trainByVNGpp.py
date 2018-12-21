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


def calculateBursts(tupleList):
    tuple_length = len(tupleList)
    for i in range(tuple_length):
        item = tupleList[i]
        if 0 == i:
            direction = item[-1]
            burstList = []
            tmp_burst = item[0] * item[1]
            continue

        tmp_direc = item[-1]
        if direction != tmp_direc:
            burstList.append(tmp_burst)
            direction = tmp_direc
            tmp_burst = (item[0] * item[1])
        else:
            tmp_burst += (item[0] * item[1])

    burstList.append(tmp_burst)

    return burstList


def readfile(fpath):
    UpStreamTotal = 0
    DownStreamTotal = 0
    UpPackNum = 0
    DownPackNum = 0
    traceTimeList = []
    tupleList = []
    for line in fileUtils.readTxtFile(fpath, ','):
        tmp = line.split(',')
        if len(tmp) > 4:
            flag = fileUtils.str2int(tmp[4])
            traceTimeList.append(fileUtils.str2float(tmp[2]))
            tmpTuple = (fileUtils.str2int(tmp[3]), fileUtils.str2int(tmp[4]))
        else:
            flag = fileUtils.str2int(tmp[-1])
            traceTimeList.append(fileUtils.str2float(tmp[1]))
            tmpTuple = (fileUtils.str2int(tmp[-2]), fileUtils.str2int(tmp[-1]))

        tupleList.append(tmpTuple)

        if 1 == flag:
            UpStreamTotal += fileUtils.str2int(tmp[-2])
            UpPackNum += 1
        elif -1 == flag:
            DownStreamTotal += fileUtils.str2int(tmp[-2])
            DownPackNum += 1
        else:
            raise ValueError('unexpected flag value: {}'.format(flag))

    return UpPackNum, DownPackNum, UpStreamTotal, DownStreamTotal, traceTimeList, tupleList


def computeFeature(fpath, rangeList):
    _, _, UpStreamTotal, DownStreamTotal, traceTimeList, tupleList = readfile(fpath)

    burstList = calculateBursts(tupleList)
    start, end, interval = rangeList[0], rangeList[1], rangeList[2]
    rangeList, sectionList = tools.getSectionList(start, end, interval)
    for feat in burstList:
        index = tools.computeRange(rangeList, feat)
        sectionList[index] += 1
    TotalBurstByte = sectionList

    traceTimeList.sort()
    TotalTraceTime = traceTimeList[-1] - traceTimeList[0]

    #import pdb
    #pdb.set_trace()
    tmp_rtn = [TotalTraceTime, UpStreamTotal, DownStreamTotal]
    tmp_rtn.extend(TotalBurstByte)
    return tmp_rtn


def train(trainData, trainLabel):
    gnb = GaussianNB()
    y_pred = gnb.fit(trainData, trainLabel)
    return y_pred


def loadTrainData(dataDir):
    fList = fileUtils.genfilelist(dataDir)


def main(opts):
    trainDataDir = opts.trainDataDir
    data, label = loadTrainData(trainDataDir)
    mymodel = train(data, label)
    saveModel(mymodel, fpath)


def parseOpts(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--trainDataDir', help='path to training data dir')
    opts = parser.parse_args()
    return opts

if __name__ == "__main__":
    opts = parseOpts(sys.argv)
    main(opts)
