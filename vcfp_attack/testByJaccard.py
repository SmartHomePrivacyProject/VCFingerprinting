#!/usr/bin/python

import os
import sys
import argparse
import re

import fileUtils
import csvList2Set
import trainByJaccard


def computeJaccardDist(setA, setB):
    intersec_set = setA.intersection(setB)
    union_set = setA.union(setB)
    return len(intersec_set) / len(union_set)


def getLabel(fpath):
    '''need to negotiate the file name pattern first'''
    pattern = '([a-zA-Z\']*[a-zA-Z_]+)_[0-9].*'
    fname = os.path.basename(fpath)
    m = re.match(pattern, fname)
    if m:
        return m.group(1)
    else:
        return os.path.basename(fpath)


def str2int(tmpSet):
    return set(map(lambda x: int(x), tmpSet))


def computeLabel(testFile, classFiles):
    max_value = 0
    max_file = ''
    testData = trainByJaccard.readfile(testFile)
    for cfile in classFiles:
        cfile = os.path.abspath(cfile)
        classData = trainByJaccard.readfile(cfile)
        tmp_value = computeJaccardDist(str2int(testData), str2int(classData))
        if tmp_value > max_value:
            max_value = tmp_value
            max_file = cfile

    label = getLabel(max_file)
    return label


def test(testList, modelFileDir):
    classFiles = fileUtils.genfilelist(modelFileDir)
    predictions = []
    for testfile in testList:
        predict = computeLabel(testfile, classFiles)
        predictions.append(predict)
    return predictions


def main(opts):
    testFiles = fileUtils.genfilelist(opts.testFileDir)
    classFiles = fileUtils.genfilelist(opts.modelDir)

    for testFile in testFiles:
        predict = computeLabel(testFile, classFiles)
        print('the label for given test file {} is: {}'.format(testFile, predict))


def parseOpts(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--testFileDir', help='path to test file dir')
    parser.add_argument('-m', '--modelDir', help='path to model dir')
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    opts = parseOpts(sys.argv)
    main(opts)
