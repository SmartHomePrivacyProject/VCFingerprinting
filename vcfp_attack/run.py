#!/usr/bin/python

import os
import sys
import argparse
import subprocess

import nFoldCrossValidation
import draw_graph

import utils

class MyOptions():
    def __init__(self, model, dataDir, nFold, word2vec, file2store, itv):
        self.model = model
        self.dataDir = dataDir
        self.nFold = nFold
        self.word2vec = word2vec
        self.file2store = file2store
        self.interval = itv

def main(opts):
    '''In this script, we will run all the test, collect the results and generate all the figures'''
    ## impact of rounding test (if has any) and semantic test
    ## semantic test will use two word2vec model
    figureSaveDir = os.path.abspath('../data/results/figures/')
    word2vecList = ['/home/carl/work_dir/network_fingerprint_proj/data/csv_echo_1213/corresponding_vectors_new_files/vectors_queries_ya_e100_v300.csv', '/home/carl/work_dir/network_fingerprint_proj/data/csv_echo_1213/corresponding_vectors_new_files/vectors_queries_qu_e100_v300.csv']
    if not os.path.isdir(figureSaveDir):
        os.makedirs(figureSaveDir)
    if opts.roundTest:
        datapath = '../data/csv_echo_1213/csv_echo_sean_haipeng/'
        # 1. Bayes test
        intervals = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        y1 = []
        y2 = []
        y3 = []
        for itv in intervals:
            file2store = utils.makeTempFile()
            opts = MyOptions('Bayes', datapath, 5, word2vecList[0], file2store, itv)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            y1.append(avg_acc)
            y2.append(avg_rank)

            opts = MyOptions('Bayes', datapath, 5, word2vecList[1], file2store, itv)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            y3.append(avg_rank)

        xLabel = 'Rounding Parameter'
        y1Label = 'Accuracy'
        y2Label = 'Normalized Semantic Distance'

        file2save = os.path.join(figureSaveDir, 'Bayes_test.eps')
        data = draw_graph.DataArray(intervals, y1, 0, y2, y3)
        y1Lim = [0.1, 0.5]
        y2Lim = [20, 60]
        label1 = 'Accuracy'
        label3 = 'Normalized SD (Yahoo)'
        label4 = 'Normalized SD (Quora)'
        xTicks = intervals
        y1Ticks = [0.1, 0.2, 0.3, 0.4, 0.5]
        y2Ticks = [20, 30, 40, 50, 60]
        context = draw_graph.Context(xLabel, y1Label, y2Label=y2Label, file2save=file2save,
                                     y1Lim=y1Lim, y2Lim=y2Lim, label1=label1, label3=label3,
                                     label4=label4, xTicks=xTicks, y1Ticks=y1Ticks, y2Ticks=y2Ticks)
        draw_graph.draw_results(data, 2, context)

        # 2. VNGpp test
        intervals = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
        y1 = []
        y2 = []
        y3 = []
        for itv in intervals:
            file2store = utils.makeTempFile()
            opts = MyOptions('VNGpp', datapath, 5, word2vecList[0], file2store, itv)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            y1.append(avg_acc)
            y2.append(avg_rank)

            opts = MyOptions('VNGpp', datapath, 5, word2vecList[1], file2store, itv)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            y3.append(avg_rank)

        xLabel = 'Rounding Parameter'
        y1Label = 'Accuracy'
        y2Label = 'Normalized Semantic Distance'

        file2save = os.path.join(figureSaveDir, 'VNGpp_test.eps')
        data = draw_graph.DataArray(intervals, y1, 0, y2, y3)
        y1Lim = [0.1, 0.5]
        y2Lim = [20, 60]
        label1 = 'Accuracy'
        label3 = 'Normalized SD (Yahoo)'
        label4 = 'Normalized SD (Quora)'
        xTicks = [2000, 4000, 6000, 8000, 10000]
        y1Ticks = [0.1, 0.2, 0.3, 0.4, 0.5]
        y2Ticks = [20, 30, 40, 50, 60]
        context = draw_graph.Context(xLabel, y1Label, y2Label=y2Label, file2save=file2save,
                                     y1Lim=y1Lim, y2Lim=y2Lim, label1=label1, label3=label3,
                                     label4=label4, xTicks=xTicks, y1Ticks=y1Ticks, y2Ticks=y2Ticks)
        draw_graph.draw_results(data, 2, context)

    elif opts.padSizeTest:
        # 3. padding size impact test
        dpath = '/home/carl/work_dir/network_fingerprint_proj/data/csv_echo_1213/csv_echo_sean_haipeng_obfuscated'
        paddingSize = [1000, 1100, 1200, 1300, 1400, 1500]
        yNBAccYa = []
        yVNGAccYa = []
        yNBDistYa = []
        yVNGDistYa = []

        for ps in paddingSize:
            # for yahoo
            file2store = utils.makeTempFile()
            subPath = '{}/{}_50_20'.format(ps, ps)
            fullpath = os.path.join(dpath, subPath)
            opts = MyOptions('Bayes', fullpath, 5, word2vecList[0], file2store, 100)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            yNBAccYa.append(avg_acc)
            yNBDistYa.append(avg_rank)

            file2store = utils.makeTempFile()
            opts = MyOptions('VNGpp', fullpath, 5, word2vecList[0], file2store, 2000)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            yVNGAccYa.append(avg_acc)
            yVNGDistYa.append(avg_rank)

        # draw yahoo
        xLabel = 'Fixed Package Size'
        y1Label = 'Accuracy'
        y2Label = 'Normalized Semantic Distance'

        file2save = os.path.join(figureSaveDir, 'padTestYahoo.eps')
        data = draw_graph.DataArray(paddingSize, yNBAccYa, yVNGAccYa, yNBDistYa, yVNGDistYa)
        y1Lim = [0, 0.2]
        y2Lim = [30, 60]
        label1='Accuracy of LL-NB'
        label2='Accuracy of VNG++'
        label3='Normalized SD of LL-NB'
        label4='Normalized SD of VNG++'
        xTicks = paddingSize
        y1Ticks = [0, 0.1, 0.2]
        y2Ticks = [30, 40, 50, 60]
        context = draw_graph.Context(xLabel, y1Label, y2Label=y2Label, file2save=file2save,
                                     y1Lim=y1Lim, label1=label1, label2=label2, label3=label3,
                                     label4=label4, xTicks=xTicks,
                                     y1Ticks=y1Ticks, y2Ticks=y2Ticks)
        draw_graph.draw_results(data, 2, context)

    elif opts.tradeOffTest:
        dpath = '/home/carl/work_dir/network_fingerprint_proj/data/csv_echo_1213/csv_echo_sean_haipeng_obfuscated'
        packSizeList = [1000, 1100, 1200, 1300, 1400, 1500]
        timeList = []
        overHeadList = []
        for ohl in packSizeList:
            fname = 'overhead info_{}_50_20.csv'.format(ohl)
            fullName = os.path.join(dpath, fname)
            with open(fullName, 'r') as f:
                lines = f.readlines()
                tmpLine = lines[-1].strip()
                tmpList = tmpLine.split(',')

            timevar = '{:10.2f}'.format(float(tmpList[-2]))
            overheadvar = int(float(tmpList[-1])/1024)
            timeList.append(timevar)
            overHeadList.append(overheadvar)

        # draw yahoo
        xLabel = 'Fixed Package Size'
        y1Label = 'Communication Overhead (kb)'
        y2Label = 'Time Delay (seconds)'

        file2save = os.path.join(figureSaveDir, 'tradeOff.eps')
        data = draw_graph.DataArray(packSizeList, overHeadList, y3=timeList)
        y1Lim = 0
        y2Lim = 0
        label1 = 'Communication Overhead'
        label3 = 'Time Delay'
        xTicks = packSizeList
        y1Ticks = []
        y2Ticks = []
        context = draw_graph.Context(xLabel, y1Label, y2Label=y2Label, file2save=file2save,
                                     y1Lim=y1Lim, y2Lim=y2Lim, label1=label1, label3=label3)
        draw_graph.draw_results(data, 2, context)

    elif opts.epochTest:
        # epoch times impact test
        dpath = '/home/carl/work_dir/network_fingerprint_proj/data/csv_echo_1213/corresponding_vectors_new_files'
        datapath = '../data/csv_echo_1213/csv_echo_sean_haipeng/'
        epochTimes = [100, 125, 150, 175]
        yBayesYaDist = []
        yBayesQuDist = []
        yVNGppYaDist = []
        yVNGppQuDist = []
        for et in epochTimes:
            # for yahoo
            file2store = utils.makeTempFile()
            fpath = 'vectors_queries_ya_e{}_v300.csv'.format(et)
            word2vecPath = os.path.join(dpath, fpath)
            opts = MyOptions('Bayes', datapath, 5, word2vecPath, file2store, 100)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            yBayesYaDist.append(avg_rank)

            file2store = utils.makeTempFile()
            opts = MyOptions('VNGpp', datapath, 5, word2vecPath, file2store, 2000)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            yVNGppYaDist.append(avg_rank)

            # for quora
            file2store = utils.makeTempFile()
            fpath = 'vectors_queries_qu_e{}_v300.csv'.format(et)
            word2vecPath = os.path.join(dpath, fpath)
            opts = MyOptions('Bayes', datapath, 5, word2vecPath, file2store, 100)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            yBayesQuDist.append(avg_rank)

            file2store = utils.makeTempFile()
            opts = MyOptions('VNGpp', datapath, 5, word2vecPath, file2store, 2000)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            yVNGppQuDist.append(avg_rank)

        xLabel = 'Number of Epochs'
        yLabel = 'Normalized Semantic Distance'

        # draw Bayes
        file2save = os.path.join(figureSaveDir, 'epochNB.eps')
        data = draw_graph.DataArray(epochTimes, yBayesYaDist, yBayesQuDist)
        y1Lim = [30, 50]
        label1='Normalized SD (Yahoo)'
        label2='Normalized SD (Quora)'
        xTicks = epochTimes
        yTicks = [30, 40, 50]
        context = draw_graph.Context(xLabel, yLabel, file2save=file2save, y1Lim=y1Lim,
                                     label1=label1, label2=label2, xTicks=xTicks, y1Ticks=yTicks)
        draw_graph.draw_results(data, 1, context)

        # draw VNGpp
        file2save = os.path.join(figureSaveDir, 'epochVNG.eps')
        data = draw_graph.DataArray(epochTimes, yVNGppYaDist, yVNGppQuDist)
        y1Lim = [30, 50]
        label1='Normalized SD (Yahoo)'
        label2='Normalized SD (Quora)'
        xTicks = epochTimes
        yTicks = [30, 40, 50]
        context = draw_graph.Context(xLabel, yLabel, file2save=file2save, y1Lim=y1Lim,
                                     label1=label1, label2=label2, xTicks=xTicks, y1Ticks=yTicks)
        draw_graph.draw_results(data, 1, context)

    elif opts.vectorSizeTest:
        # vector size impact test
        dpath = '/home/carl/work_dir/network_fingerprint_proj/data/csv_echo_1213/corresponding_vectors_new_files'
        datapath = '../data/csv_echo_1213/csv_echo_sean_haipeng/'
        epochTimes = [300, 325, 350, 375]
        yBayesYaDist = []
        yBayesQuDist = []
        yVNGppYaDist = []
        yVNGppQuDist = []
        for et in epochTimes:
            # for yahoo
            file2store = utils.makeTempFile()
            fpath = 'vectors_queries_ya_e100_v{}.csv'.format(et)
            word2vecPath = os.path.join(dpath, fpath)
            opts = MyOptions('Bayes', datapath, 5, word2vecPath, file2store, 100)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            yBayesYaDist.append(avg_rank)

            file2store = utils.makeTempFile()
            opts = MyOptions('VNGpp', datapath, 5, word2vecPath, file2store, 2000)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            yVNGppYaDist.append(avg_rank)

            # for quora
            file2store = utils.makeTempFile()
            fpath = 'vectors_queries_qu_e100_v{}.csv'.format(et)
            word2vecPath = os.path.join(dpath, fpath)
            opts = MyOptions('Bayes', datapath, 5, word2vecPath, file2store, 100)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            yBayesQuDist.append(avg_rank)

            file2store = utils.makeTempFile()
            opts = MyOptions('VNGpp', datapath, 5, word2vecPath, file2store, 2000)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            yVNGppQuDist.append(avg_rank)

        xLabel = 'Vector Size'
        yLabel = 'Normalized Semantic Distance'

        # draw Bayes
        file2save = os.path.join(figureSaveDir, 'vectorNB.eps')
        data = draw_graph.DataArray(epochTimes, yBayesYaDist, yBayesQuDist)
        y1Lim = [30, 50]
        label1='Normalized SD (Yahoo)'
        label2='Normalized SD (Quora)'
        xTicks = epochTimes
        yTicks = [30, 40, 50]
        context = draw_graph.Context(xLabel, yLabel, file2save=file2save, y1Lim=y1Lim,
                                     label1=label1, label2=label2, xTicks=xTicks, y1Ticks=yTicks)
        draw_graph.draw_results(data, 1, context)

        # draw VNGpp
        file2save = os.path.join(figureSaveDir, 'vectorVNG.eps')
        data = draw_graph.DataArray(epochTimes, yVNGppYaDist, yVNGppQuDist)
        y1Lim = [30, 50]
        label1 = 'Normalized SD (Yahoo)'
        label2='Normalized SD (Quora)'
        xTicks = epochTimes
        yTicks = [30, 40, 50]
        context = draw_graph.Context(xLabel, yLabel, file2save=file2save, y1Lim=y1Lim,
                                     label1=label1, label2=label2, xTicks=xTicks, y1Ticks=yTicks)
        draw_graph.draw_results(data, 1, context)

    elif opts.miniTimeTest:
        # minimal amount time impact test
        datapath = '/home/carl/work_dir/network_fingerprint_proj/data/csv_echo_1213/csv_echo_sean_haipeng_obfuscated/1000'
        miniTimes = [10, 20, 30, 40, 60, 80, 100]

        yNBAccYa = []
        yVNGAccYa = []
        yNBDistYa = []
        yVNGDistYa = []

        for mt in miniTimes:
            # for yahoo
            subpath = '1000_50_{}'.format(mt)
            fulpath = os.path.join(os.path.realpath(datapath), subpath)
            file2store = utils.makeTempFile()
            opts = MyOptions('Bayes', fulpath, 5, word2vecList[0], file2store, 100)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            yNBAccYa.append(avg_acc)
            yNBDistYa.append(avg_rank)

            file2store = utils.makeTempFile()
            opts = MyOptions('VNGpp', fulpath, 5, word2vecList[0], file2store, 2000)
            avg_rank, avg_acc = nFoldCrossValidation.main(opts)
            yVNGAccYa.append(avg_acc)
            yVNGDistYa.append(avg_rank)

        xLabel = 'Minimum Amount of Time'
        y1Label = 'Accuracy'
        y2Label = 'Normalized Semantic Distance'

        # draw yahoo
        file2save = os.path.join(figureSaveDir, 'miniTimes.eps')
        data = draw_graph.DataArray(miniTimes, yNBAccYa, yVNGAccYa, yNBDistYa, yVNGDistYa)
        y1Lim = [0, 0.3]
        y2Lim = [30, 70]
        label1 = 'Accuracy of LL-NB'
        label2 = 'Accuracy of VNG++'
        label3 = 'Normalized SD of LL-NB'
        label4 = 'Normalized SD of VNG++'
        xTicks = miniTimes
        y1Ticks = [0, 0.1, 0.2, 0.3]
        y2Ticks = [30, 40, 50, 60, 70]
        context = draw_graph.Context(xLabel, y1Label, y2Label=y2Label, file2save=file2save,
                                     y1Lim=y1Lim, y2Lim=y2Lim, label1=label1, label2=label2,
                                     label3=label3, label4=label4, xTicks=xTicks,
                                     y1Ticks=y1Ticks, y2Ticks=y2Ticks)
        draw_graph.draw_results(data, 2, context)

    else:
        raise ValueError('you should choose from -r/-p/-v')


def parseOpts(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--roundTest', action='store_true', default=False,
                        help='run round parameter test')
    parser.add_argument('-p', '--padSizeTest', action='store_true', default=False,
                        help='run pad size test')
    parser.add_argument('-e', '--epochTest', action='store_true', default=False,
                        help='run epoch times test')
    parser.add_argument('-v', '--vectorSizeTest', action='store_true', default=False,
                        help='run vector size test')
    parser.add_argument('-t', '--tradeOffTest', action='store_true', default=False,
                        help='run trade off test')
    parser.add_argument('-m', '--miniTimeTest', action='store_true', default=False,
                        help='run minimum amount of time test')
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    opts = parseOpts(sys.argv)
    main(opts)
