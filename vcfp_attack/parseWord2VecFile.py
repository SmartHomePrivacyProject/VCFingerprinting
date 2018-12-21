#!/usr/bin/python

import os
import sys
import argparse
from collections import defaultdict
import re

import fileUtils


def isBegining(line):
    m = re.match(r'^[A-Za-z]+.*', line)
    return True if m else False


def isEnd(line):
    return True if line.startswith('#end') else False


def getItem(item):
    m = re.match(r'[\"\[]*([-\.0-9e]*)[\]\"\,]*', item)
    if m:
        return m.group(1)
    else:
        raise ValueError('pattern failed here {}'.format(item))


def readline(line):
    tmpList = line.split(' ')
    tmpList = list(filter(lambda x: x!='', tmpList))
    rtnList = []
    for item in tmpList:
        item = item.strip()
        if item.startswith('"[') or item.endswith(']","'):
            item = getItem(item)
        if not item:
            continue
        try:
            rtnList.append(fileUtils.str2float(item))
        except ValueError:
            raise ValueError('item is: {} and line is: {}'.format(item, line))
    return rtnList


def loadData(fpath):
    vecDict = defaultdict(list)
    vecList = []
    with open(fpath, 'r') as f:
        for line in f:
            if line == '"\n':
                continue
            if isBegining(line):
                tmp = line.split(',')
                title = tmp[0]
                title = title.replace(' ', '_')
                title = title.replace('?', '')
                title = title.replace('.', '')
                title = title.lower()
                tmpList = readline(tmp[1])
                vecList.extend(tmpList)
            elif isEnd(line):
                vecDict[title] = vecList
                vecList = []
                title = ''
            else:
                tmpList = readline(line)
                vecList.extend(tmpList)

    return vecDict


def main(opts):
    import pdb
    pdb.set_trace()
    dataList = loadData(opts.file)
    print(dataList)


def parseOpts(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='file to word2vec file')
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    opts = parseOpts(sys.argv)
    main(opts)
