#!/usr/bin/env python3

'''
Compute different statistics per family for each of the 9 focus products.
'''

import pandas as pd

import readMetaData as rmd
import prepDecisionTree as pdt
import dataFrameStats as dfs
import featureEng as fe
from constants import (TRIP_METADATA, EXTRA_PRODUCT_METADATA, UPC_METADATA,
        NAME_MAP)

# For statistics, we will only analyze these data fields (non-categorical)
ANALYZE_COLS = ['origUnitCost', 'unitCost', 'coupVal', 'percOff', 'deal', 'brandCode',
        'retailCode']


####### 11/25/2018 USE JUST FOR PRIVATE LABEL PRICE ######
def getFamilyStats(pID, famFile, prodDict, tripDict):
    '''
    Collect statistics on family purchases of a certain product.
    '''
    print(famFile)
    famID = famFile.strip('\n').split('/')[-1].split('_')[0]
    famDF = pdt.getFamilyProductDF(pID, famFile, prodDict, tripDict, stand=False)
    pdt.stringToNum(famDF)
    loyalRow,  otherRow = fe.getLoyalProductIndices(famDF)
    fe.changeProdIDtoBinary(famDF, loyalRow, otherRow)
    #return dfs.returnAllStatistics(pID, famID, famDF, loyalRow, otherRow, nan=False)

    privP, nonprivP = dfs.getPrivateLabelPriceData(famDF)
    return [pID, famID, privP, nonprivP]


if __name__ == '__main__':
    tripD, prodD, upcD, nameD = rmd.getAllMetaData(TRIP_METADATA,
            EXTRA_PRODUCT_METADATA, UPC_METADATA, NAME_MAP)
    productFiles = rmd.getCandidateProductFileList()

    # Iterate through each focus product and get purchase files for families
    # that show brand loyalty toward this product
    prodStatsDF = []
    for pf in productFiles:
        pID = (pf.split('/')[-1])[:4]
        pName = nameD[pID]
        famFiles = rmd.getLoyalFamilies(pf)

        print('Starting product: ' + pID + ' - ' + pName)

        # Iterate through each family, collecting statistics
        for ff in famFiles:
            famStats = getFamilyStats(pID, ff, prodD, tripD)
            prodStatsDF.append(famStats)

    # Write the statistics to a tsv file
    statsHeader = ['pID','famID','privPrice','nonPrivPrice'] 
    prodStatsDF = pd.DataFrame(prodStatsDF, columns=statsHeader)

    csvName = 'allProduct_DFStats_PRIVATE_AVG_PRICE.tsv'
    prodStatsDF.to_csv(csvName, sep='\t',float_format='%.2f', index=False)
