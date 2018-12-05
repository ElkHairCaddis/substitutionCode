#!/usr/bin/env python3

'''
Learn a decision tree for individual families for the focus products.
'''

import readMetaData as rmd
import prepDecisionTree as pdt
import learnDecisionTree as ldt
import featureEng as fe
import onlyCost as oc
from constants import (TRIP_METADATA, EXTRA_PRODUCT_METADATA, UPC_METADATA,
NAME_MAP)


ONLY_PRICE = True
TREE_STATS_FNAME = 'onlyPriceNoOrigUC_treeStats.tsv'
TREE_STATS_FIELDS = ['productID',
        'famID',
        'topFeat',
        'leftEnt',
        'rightEnt',
        'perFavLeft',
        'perSwtchLeft',
        'perFavRight',
        'perSwtchRight',
        'nNodes',
        'maxDepth']
TREE_STATS_HEADER = '\t'.join(TREE_STATS_FIELDS)

def learnFamilyTree(prodID, famFile, prodMeta, tripMeta, pn, of):
    '''
    Learn a tree using all possible features.
    '''
    famDF = pdt.individualFamPurchtoDF(prodID, famFile, prodMeta, tripMeta,
            stand=True)
    famDF = fe.dateToDays(famDF)
    famDF = fe.addBrandSaturation(famDF)
    famDF = famDF.drop('date',axis=1)
#    famDF = famDF.drop('private',axis=1)

    famID = famFile.strip('\n').split('/')[-1].split('_')[0]

    SPLIT_MIN_PERCENT = 25
    minSplit = ldt.getMinSplit(famDF, SPLIT_MIN_PERCENT)
    outFolder = '../indFamProdTree/noPrivateLabel_11_15/'
    ofName = outFolder + pn + '_' + famID + '_tree.png'
    dt, feats = ldt.learnDecisionTree(famDF, minSplit, 5, ofName)
    ldt.collectTreeStats(dt, feats, prodID, famID, of)


def learnPricingFamilyTree(prodID, famFile,pn, of):
    '''
    Learn a tree using only pricing features.
    '''
    famDF = oc.famPurchToDF(prodID, famFile)
    famDF = famDF.drop('origUC',axis=1)
    famID = famFile.strip('\n').split('/')[-1].split('_')[0]
    SPLIT_MIN_PERCENT = 25
    minSplit = ldt.getMinSplit(famDF, SPLIT_MIN_PERCENT)
    outFolder = '../indFamProdTree/noOrigUC_11_16/'
    ofName = outFolder + pn + '_' + famID + '_tree.png'
    dt, feats = ldt.learnDecisionTree(famDF, minSplit, 5, ofName, plot=True)
    ldt.collectTreeStats(dt, feats, prodID, famID, of)


if __name__ == '__main__':
    tripDict, prodDict, upcDict, nameDict = rmd.getAllMetaData(TRIP_METADATA,
            EXTRA_PRODUCT_METADATA, UPC_METADATA, NAME_MAP)
    productsToAnalyze = rmd.getCandidateProductFileList()

    with open(TREE_STATS_FNAME, 'w') as outfile:
        outfile.write(TREE_STATS_HEADER)

        for productFile in productsToAnalyze:
            productID = (productFile.split('/')[-1])[:4]
            productName = nameDict[productID]

            print('Starting product: ' + productID)

            familyPurchaseFiles = rmd.getLoyalFamilies(productFile)
            for famFile in familyPurchaseFiles:
                if ONLY_PRICE:
                    learnPricingFamilyTree(productID, famFile, productName,
                            outfile)
                else:
                    learnFamilyTree(productID, famFile, prodDict, tripDict,
                            productName, outfile)


            print('Finished product: ' + productID)
