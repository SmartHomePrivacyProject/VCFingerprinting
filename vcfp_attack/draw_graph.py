#!/usr/bin/python

import os
import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager
import matplotlib

# The purpose of these  following three lines is to generate figures without type 3 fonts
matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts']
matplotlib.rcParams['text.usetex']

# setting for plt
plt.rcParams['axes.unicode_minus'] = False
plt.ion()   # open the interactive mode

LABELSIZE = 18
LEGENDSIZE = 18
TICKSIZE = 16

class DataArray():
    def __init__(self, x, y1, y2=0, y3=0, y4=0):
        self.x = np.array(x)
        self.y1 = np.array(y1)

        if not 0 == y2:
            self.y2 = np.array(y2)
        else:
            self.y2 = y2

        if not 0 == y3:
            self.y3 = np.array(y3)
        else:
            self.y3 = y3

        if not 0 == y4:
            self.y4 = np.array(y4)
        else:
            self.y4 = y4

class Context():
    def __init__(self, xLabel, y1Label, y2Label='', file2save='', y1Lim=0,
                 y2Lim=0, label1='', label2='', label3='', label4='',
                 label5='', xTicks=0, y1Ticks=0, y2Ticks=0):
        self.xLabel = xLabel
        self.y1Label = y1Label
        self.y2Label = y2Label
        self.file2save = file2save
        self.y1Lim = y1Lim
        self.y2Lim = y2Lim
        self.label1 = label1
        self.label2 = label2
        self.label3 = label3
        self.label4 = label4
        self.label5 = label5
        self.xTicks = xTicks
        self.y1Ticks = y1Ticks
        self.y2Ticks = y2Ticks

def getColor():
    colorSet = []
    for c in colorSet:
        yield c

def getLineStyle():
    lineStyleSet = []
    for l in lineStyleSet:
        yield l

def draw_results(data, axis_num, context):
    xLabel = context.xLabel
    y1Label = context.y1Label
    y2Label = context.y2Label
    filename = context.file2save
    label1 = context.label1
    label2 = context.label2
    label3 = context.label3
    label4 = context.label4
    label5 = context.label5
    y1Lim = context.y1Lim
    y2Lim = context.y2Lim
    xTicks = context.xTicks
    y1Ticks = context.y1Ticks
    y2Ticks = context.y2Ticks

    if 1 == axis_num:
        X = data.x
        Y1 = data.y1
        Y2 = data.y2
        Y3 = data.y3
        Y4 = data.y4

        fig = plt.figure(figsize=(14, 10))
        fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.1, hspace=0.1)

        ax1 = fig.add_subplot(111)
        lns1 = ax1.plot(X, Y1, marker='+', markersize=12, c='', color='k', label=label1)
        if not isinstance(Y2, int):
            lns2 = ax1.plot(X, Y2, marker='*', markersize=12, c='', color='r', label=label2)
        if not isinstance(Y3, int):
            lns3 = ax1.plot(X, Y3, marker='o', markersize=12, c='', color='g', label=label3)
        if not isinstance(Y4, int):
            lns4 = ax1.plot(X, Y4, marker='^', markersize=12, c='', color='b', label=label4)

        lns = lns1
        if not isinstance(Y2, int):
            lns = lns + lns2
        if not isinstance(Y3, int):
            lns = lns + lns3
        if not isinstance(Y4, int):
            lns = lns + lns4

        labs = [l.get_label() for l in lns]
        legend = ax1.legend(lns, labs, loc=0, fontsize='x-large')
        legend.get_title().set_fontsize(fontsize=LEGENDSIZE)

        ax1.set_xlabel(xLabel, fontsize=LABELSIZE)
        ax1.set_ylabel(y1Label, fontsize=LABELSIZE)

        ax1.tick_params(labelsize=TICKSIZE)
        if not isinstance(xTicks, int):
            ax1.set_xticks(xTicks)
        if not isinstance(y1Ticks, int):
            ax1.set_yticks(y1Ticks)

        if 0 != y1Lim:
            ax1.set_ylim(y1Lim[0], y1Lim[1])

        plt.savefig(filename)
        plt.show()
        plt.pause(1)
        plt.close('all')

    elif 2 == axis_num:
        X = data.x
        Y1 = data.y1
        Y2 = data.y2
        Y3 = data.y3
        Y4 = data.y4

        fig = plt.figure(figsize=(14,10))
        fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.1, hspace=0.1)

        ax1 = fig.add_subplot(111)
        lns1 = ax1.plot(X, Y1, marker='*', markersize=12, c='', color='g', label=label1)
        if not isinstance(Y2, int):
            lns2 = ax1.plot(X, Y2, marker='v', markersize=12, c='', color='k', label=label2)

        ax2 = ax1.twinx()   # this is the import function
        lns3 = ax2.plot(X, Y3, marker='+', markersize=12, c='', color='b', label=label3)
        if not isinstance(Y4, int):
            lns4 = ax2.plot(X, Y4, marker='o', markersize=12, c='', color='r', label=label4)

        lns = lns1
        if not isinstance(Y2, int):
            lns = lns + lns2
        lns = lns + lns3
        if not isinstance(Y4, int):
            lns = lns + lns4

        labs = [l.get_label() for l in lns]
        legend = ax1.legend(lns, labs, loc=0, fontsize='x-large')
        legend.get_title().set_fontsize(fontsize=LEGENDSIZE)

        ax1.set_xlabel(xLabel, fontsize=LABELSIZE)
        ax1.set_ylabel(y1Label, fontsize=LABELSIZE)
        ax2.set_ylabel(y2Label, fontsize=LABELSIZE)

        ax1.tick_params(labelsize=TICKSIZE)
        ax2.tick_params(labelsize=TICKSIZE)

        if not isinstance(xTicks, int):
            ax1.set_xticks(xTicks)
        if not isinstance(y1Ticks, int):
            ax1.set_yticks(y1Ticks)
        if not isinstance(y2Ticks, int):
            ax2.set_yticks(y2Ticks)

        if 0 != y1Lim:
            ax1.set_ylim(y1Lim[0], y1Lim[1])
        if 0 != y2Lim:
            ax2.set_ylim(y2Lim[0], y2Lim[1])

        plt.savefig(filename)
        plt.show()
        plt.pause(2)
        plt.close('all')
    else:
        raise ValueError('only accept <=2 axis num, axis_num now = {}'.format(axis_num))

def loadResData(fpath):
    X = []
    Y1 = []
    Y2 = []
    Y3 = []
    with open(fpath, 'r') as f:
        for line in f:
            tmpList = line.split(',')
            X.append(float(tmpList[0]))
            Y1.append(float(tmpList[1]))
            Y2.append(float(tmpList[2]))
            Y3.append(float(tmpList[3]))

    return DataArray(X, Y1, Y2, Y3)

def main(opts):
    data = loadResData(opts.dataFile)
    context = Context('label1', 'label2', 'test.png')
    draw_results(data, opts.method, int(opts.axis_num), context)

def parseOpts(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataFile', help='')
    parser.add_argument('-m', '--method', help='')
    parser.add_argument('-a', '--axis_num', help='')
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    opts = parseOpts(sys.argv)
    main(opts)
