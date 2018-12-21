#!/usr/bin/python

import os
import sys
import argparse

import fileUtils
import testByJaccard
from collections import defaultdict


def main(opts):
    fileList = fileUtils.genfilelist(opts.dirpath)
    count = 0
    tmpSet = set()
    for fpath in fileList:
        fname = os.path.basename(fpath)
        fname = testByJaccard.getLabel(fname)
        tmpSet.add(fname)
        count = count + 1

    tmpList = list(tmpSet)
    tmpList.sort()

    with open(opts.respath, 'w') as f:
        content = '\n'.join(tmpSet)
        f.write(content)

    print('write {} file names'.format(count))

def parseOpts(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dirpath', help='dir path to those files')
    parser.add_argument('-r', '--respath', help='result path to store result')
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    opts = parseOpts(sys.argv)
    main(opts)
