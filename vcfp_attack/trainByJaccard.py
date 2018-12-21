#!/usr/bin/python

import os
import sys
from collections import defaultdict
import math
import argparse

import fileUtils
import testByJaccard


def generateDictOfClass(fileNameList):
    def getKeyFromName(fName):
        return testByJaccard.getLabel(fName)
    keySet = set()
    for fileName in fileNameList:
        tmp = getKeyFromName(fileName)
        keySet.add(tmp)

    fListDict = defaultdict(list)

    for fpath in fileNameList:
        for key in keySet:
            fileName = os.path.basename(fpath)
            if fileName.startswith(key):
                tmp = os.path.join(fpath)
                fListDict[key].append(tmp)

    return fListDict


def readfile(fpath):
    #print('start to load file {}'.format(fpath))
    tmpSet = set()
    fpath = os.path.abspath(fpath)
    for line in fileUtils.readTxtFile(fpath, ','):
        tmp = line.split(',')
        if len(tmp) == 4 :
            elem = fileUtils.str2int(tmp[-1]) * fileUtils.str2int(tmp[-2])
        elif len(tmp) == 1:
            elem = tmp[0]
        else:
            #import pdb
            #pdb.set_trace()
            elem = fileUtils.str2int(tmp[4]) * fileUtils.str2int(tmp[3])
        tmpSet.add(elem)

    #print('finish load file {}'.format(fpath))
    return tmpSet


def getListOfSet(fList):
    listOfSet = []
    for f in fList:
        tmpSet = readfile(f)
        listOfSet.append(tmpSet)
    return listOfSet


def trainFromList(fList):
    def numCount(elem, listOfSet):
        count = 0
        for tmpSet in listOfSet:
            if elem in tmpSet:
                count = count + 1
        return count

    listOfSet = getListOfSet(fList)
    Threshold = math.ceil(len(listOfSet)/2)

    tmpSet = set()
    for tmp in listOfSet:
         tmpSet = tmpSet.union(tmp)

    finalSet = set()
    for elem in tmpSet:
        if numCount(elem, listOfSet) >= Threshold:
            finalSet.add(elem)
        else:
            continue

    return finalSet


def writeDict2File(dpath, dictContent):
    def num2str(tmpSet):
        return set(map(lambda x: str(x), tmpSet))

    for key in dictContent.keys():
        fpath = os.path.join(dpath, key)
        tmp = '\n'.join(num2str(dictContent[key]))
        fileUtils.writeTxtFile(fpath, tmp)
    print('write dict to file completed')


def train(filepathList, classDictFileDir):
    '''
    it will write a file named class file which list
    all class file and its corresponding file path
    '''
    #import pdb
    #pdb.set_trace()
    fListDict = generateDictOfClass(filepathList)

    classDict = defaultdict(list)
    for key in fListDict.keys():
        if 1 == len(fListDict[key]):
            tmp = readfile(fListDict[key][0])
        else:
            tmp = trainFromList(fListDict[key])
        classDict[key] = tmp

    writeDict2File(classDictFileDir, classDict)


def parseOpts(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--trainFileDir', help='train file dir')
    parser.add_argument('-c', '--classDictFileDir', help='class file store dir')
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    opts = parseOpts(sys.argv)
    fileNameList = os.listdir(opts.trainFileDir)
    filepathList = list(map(lambda x: os.path.join(opts.trainFileDir, x), fileNameList))
    train(filepathList, opts.classDictFileDir)
