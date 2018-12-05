#!/usr/bin/env python3

import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import subprocess

'''
We have converted our purchases to a dataframe that is appropriate for decision
tree learning. Now, let's have the tree perform it's magic and see what
insights we can gain.abs
'''

def getMinSplit(df, minPercent):
    '''
    Determine the minimum number of samples required to split a node of the
    decision tree. Experiment with different percentages of input examples.
    '''
    return int(len(df.index) * (minPercent/100.00))


def learnDecisionTree(df, minSplitSample, maxD, plotFName,
        targetFeature='brandCode', plot=False):
    '''
    Train a decision tree to predict a feature. Then plot using graphviz
    '''
    y = df[targetFeature]
    nonTargetFeatures = [var for var in df.columns if var != targetFeature]
    X = df[nonTargetFeatures]
    decTree = DecisionTreeClassifier(min_samples_split = minSplitSample,
            criterion='entropy', max_depth=maxD)
    decTree.fit(X,y)

    if plot:
        with open('dt.dot', 'w') as f:
            export_graphviz(decTree, out_file = f, feature_names=nonTargetFeatures,
                    filled=True, rounded=True)

        command = ["dot","-Tpng","dt.dot","-o",plotFName]
        try:
            subprocess.check_call(command)
        except:
            print('Could not call \'dot\' program...')

    return (decTree, nonTargetFeatures)


def getTopFeatureSplitQuality(dTree):
    '''
    For the most important feature, which splits the root node, determine how
    well this feature partitions the purchases into target vs. non-target
    brands.
    '''
    ROOT_IDX = 0
    ROOT_LFT_IDX = dTree.tree_.children_left[0]
    ROOT_RT_IDX = dTree.tree_.children_right[0]

    # Get class index of target brand by searching for class with most samples
    # in root node. tree_.value = class membership at that node.
    rootClassMembership = (dTree.tree_.value[ROOT_IDX])[0]
    targetIdx = max(enumerate(rootClassMembership), key=lambda kv: kv[1])[0]
    rightTargetCount = ((dTree.tree_.value[ROOT_RT_IDX])[0])[targetIdx]
    leftTargetCount = ((dTree.tree_.value[ROOT_LFT_IDX])[0])[targetIdx]
    rootTargetCount = rootClassMembership[targetIdx]
    percentClassified = max([leftTargetCount,rightTargetCount])/rootTargetCount

    return percentClassified * 100.00

def collectTreeStats(dtree, feats, pID, fID, ofile):
    '''
    Collect statistics on each learned tree.
    '''
    ROOT_IDX = 0
    LEFT_IDX = dtree.tree_.children_left[0]
    RIGHT_IDX = dtree.tree_.children_right[0]

    node_features = dtree.tree_.feature
    entropies = dtree.tree_.impurity

    # % of fav/switch in each branch
    leftNodeClassCounts = dtree.tree_.value[LEFT_IDX][0]
    rightNodeClassCounts = dtree.tree_.value[RIGHT_IDX][0]
    rootNodeClassCounts = dtree.tree_.value[ROOT_IDX][0]

    numFav = rootNodeClassCounts[1]
    numSwitch = rootNodeClassCounts[0]

    percFavRight = float(rightNodeClassCounts[1] / numFav)
    percSwitchRight = float(rightNodeClassCounts[0] / numSwitch)

    percFavLeft = float(leftNodeClassCounts[1] / numFav)
    percSwitchLeft = float(leftNodeClassCounts[0] / numSwitch)

    topFeat = feats[node_features[ROOT_IDX]]
    leftEnt = entropies[LEFT_IDX]
    rightEnt = entropies[RIGHT_IDX]
    maxDepth = dtree.tree_.max_depth
    nNodes = dtree.tree_.node_count

    output = [pID,
            fID,
            topFeat,
            str(leftEnt),
            str(rightEnt),
            str(percFavLeft),
            str(percSwitchLeft),
            str(percFavRight),
            str(percSwitchRight),
            str(nNodes),
            str(maxDepth),
            ]

    ofile.write('\t'.join(output) + '\n')
