#!/usr/bin/python

import os
import sys
import argparse

import fileUtils


def list2set(opts):
    listfilepath = opts.source
    setfilepath = opts.target

    #import pdb
    #pdb.set_trace()
    tmpList = []
    ignore = ',time'
    for elem in fileUtils.readTxtFile(listfilepath, ignore):
        tmpList.append(elem)

    tmpset = set(tmpList)
    content = '\n'.join(tmpset)

    fileUtils.writeTxtFile(setfilepath, content)


def parseOpts(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', help='source file input')
    parser.add_argument('-t', '--target', help='target file output')
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    opts = parseOpts(sys.argv)
    list2set(opts)
