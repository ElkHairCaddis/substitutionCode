#!/usr/bin/env python3

'''
For each product, gather all purchases of that product from each family into
one dataframe. Feature engineer and add to larger dataframe containing all
families.
'''

import numpy as np
import pandas as pd

from featureEng import COLUMN_NAMES, CATEGORICAL_VARS
from featureEng import (stringToNum, getLoyalProductIndices,
changeProdIDtoBinary, rawValToBinary, removeNAColumns)
from featureEng import individualRawValToBinary, individualRemoveNAColumns

from constants import CHANGE, SAME, NA
from constants import PVT_LABEL_LOW, PVT_LABEL_HIGH

from constants import waterContainer, waterFlav, waterType
from constants import (iceCreamFormula, iceCreamOrganic, iceCreamProduct,
iceCreamVar)
from constants import milkForm, milkOrganic, milkType
from constants import paperTowelScent
from constants import (chipForm, chipFormula, chipOrganic, chipProduct,
chipSalt, chipStyle, chipType, chipVariety)
from constants import dressingFormula, dressingOrganic, dressingType
from constants import (drinkContainer, drinkForm, drinkFormula, drinkOrganic,
drinkSalt, drinkType, drinkScent)
from constants import  soupForm, soupFormula, soupOrganic
from constants import yogurtFormula, yogurtProduct, yogurtStyle, yogurtType

def getPurchaseFeatures(fields, prodMetaDict, tripMetaDict, standardize, pID,
        onlyPrice=False):
    '''
    Retain specific fields from the input data and add additional metadata.
    '''
    def isPrivateLabel(fields):
        '''
        Determine if product is privatel label.
        '''
        brandID = int(fields[7])
        if  PVT_LABEL_LOW <= brandID and brandID <= PVT_LABEL_HIGH:
            return 1
        else:
            return 0

    def getPercentSavings(fields):
        '''
        Calculate percent savings.
        '''
        rawCost = float(fields[3])
        rawSavings = float(fields[4])

        try:
            percOff = (rawSavings / rawCost) * 100
        except ZeroDivisionError:
            percOff = 100.00

        return percOff

    def getFinalUnitCost(fields):
        '''
        Calculate final unit cost after coupon.
        '''
        total = float(fields[3])
        coupon = float(fields[4])
        quant = float(fields[2])

        return (total - coupon) / quant

    def getPreUnitCost(fields):
        '''
        Calculate original unit cost.
        '''
        total = float(fields[3])
        quant = float(fields[2])

        return (total / quant)

    def getUnitCouponVal(fields):
        '''
        Calculate value of coupon per unit.
        '''
        coupon = float(fields[4])
        quant = float(fields[2])

        return coupon / quant

    def returnAllFeatures(fields):
        '''
        Return all above features. Plus:
        fields[5] = deal
        fields[7] = brandCode
        '''
        return [
                isPrivateLabel(fields),
                getPreUnitCost(fields),
                getFinalUnitCost(fields),
                getUnitCouponVal(fields),
                getPercentSavings(fields),
                fields[5],
                fields[7]
                ]

    ##### Main Function #####
    try:
        productMetaData = prodMetaDict[fields[1]]
        tripMetaData = tripMetaDict[fields[0]]

        if standardize:
            standardizeColumns(productMetaData, pID)

        if onlyPrice:
            return returnAllFeatures(fields)
        else:
            return returnAllFeatures(fields) + productMetaData + tripMetaData

    except KeyError:
        print('Could map trip ID or UPC...')
        pass


def standardizeColumns(fields, product):
    '''
    For certain columns in each product, use the annotated lexicons to
    standardize certain feature descriptions.
    '''
    # FEATURE INDICES
    FLAVOR = 0
    FORM = 1
    FORMULA = 2
    CONTAINER = 3
    SALT = 4
    STYLE = 5
    TYPE = 6
    PRODUCT = 7
    VARIETY = 8
    ORGANIC = 9
    STRENGTH = 10
    SCENT = 11
    DOSAGE = 12
    GENDER = 13
    SIZECODE = 14
    SIZEAMOUNT = 15
    SIZEUNIT = 16

    def standardizeWater(fields):
        for i in [CONTAINER, FLAVOR, TYPE]:
            if i == CONTAINER:
                fields[i] = waterContainer.get(fields[i], fields[i])
            elif i == FLAVOR:
                fields[i] = waterFlav.get(fields[i], fields[i])
            elif i == TYPE:
                fields[i] = waterType.get(fields[i], fields[i])

    def standardizeIceCream(fields):
        for i in [FORMULA, ORGANIC, PRODUCT, VARIETY]:
            if i == FORMULA:
                fields[i] = iceCreamFormula.get(fields[i], fields[i])
            elif i == ORGANIC:
                fields[i] = iceCreamOrganic.get(fields[i], fields[i])
            elif i == PRODUCT:
                fields[i] = iceCreamProduct.get(fields[i], fields[i])
            elif i == VARIETY:
                fields[i] = iceCreamVar.get(fields[i], fields[i])

    def standardizeMilk(fields):
        for i in [TYPE, ORGANIC, FORM]:
            if i == TYPE:
                fields[i] = milkType.get(fields[i], fields[i])
            elif i == ORGANIC:
                fields[i] = milkOrganic.get(fields[i], fields[i])
            elif i == FORM:
                fields[i] = milkForm.get(fields[i], fields[i])

    def standardizePaperTowel(fields):
        for i in [SCENT]:
            if i == SCENT:
                fields[i] = paperTowelScent.get(fields[i], fields[i])

    def standardizeChip(fields):
        for i in [FORM, FORMULA, ORGANIC, PRODUCT, SALT, STYLE, TYPE, VARIETY]:
            if i == FORM:
                fields[i] = chipForm.get(fields[i], fields[i])
            elif i == FORMULA:
                fields[i] = chipFormula.get(fields[i], fields[i])
            elif i == ORGANIC:
                fields[i] = chipOrganic.get(fields[i], fields[i])
            elif i == PRODUCT:
                fields[i] = chipProduct.get(fields[i], fields[i])
            elif i == SALT:
                fields[i] = chipSalt.get(fields[i], fields[i])
            elif i == STYLE:
                fields[i] = chipStyle.get(fields[i], fields[i])
            elif i == TYPE:
                fields[i] = chipType.get(fields[i], fields[i])
            elif i == VARIETY:
                fields[i] = chipVariety.get(fields[i], fields[i])

    def standardizeDressing(fields):
        for i in [FORMULA, ORGANIC, TYPE]:
            if i == FORMULA:
                fields[i] = dressingFormula.get(fields[i], fields[i])
            elif i == ORGANIC:
                fields[i] = dressingOrganic.get(fields[i], fields[i])
            if i == TYPE:
                fields[i] = dressingType.get(fields[i], fields[i])

    def standardizeDrink(fields):
        for i in [CONTAINER, FORM, FORMULA, ORGANIC, SALT, SCENT, TYPE]:
            if i == FORM:
                fields[i] = drinkForm.get(fields[i], fields[i])
            elif i == FORMULA:
                fields[i] = drinkFormula.get(fields[i], fields[i])
            elif i == ORGANIC:
                fields[i] = drinkOrganic.get(fields[i], fields[i])
            elif i == SCENT:
                fields[i] = drinkScent.get(fields[i], fields[i])
            elif i == SALT:
                fields[i] = drinkSalt.get(fields[i], fields[i])
            elif i == TYPE:
                fields[i] = drinkType.get(fields[i], fields[i])
            elif i == CONTAINER:
                fields[i] = drinkContainer.get(fields[i], fields[i])

    def standardizeSoup(fields):
        for i in [FORM, FORMULA, ORGANIC]:
            if i == FORM:
                fields[i] = soupForm.get(fields[i], fields[i])
            elif i == FORMULA:
                fields[i] = soupFormula.get(fields[i], fields[i])
            elif i == ORGANIC:
                fields[i] = soupOrganic.get(fields[i], fields[i])

    def standardizeYogurt(fields):
        for i in [FORMULA, PRODUCT, STYLE, TYPE]:
            if i == FORMULA:
                fields[i] = yogurtFormula.get(fields[i], fields[i])
            elif i == PRODUCT:
                fields[i] = yogurtProduct.get(fields[i], fields[i])
            if i ==  STYLE:
                fields[i] = yogurtStyle.get(fields[i], fields[i])
            if i == TYPE:
                fields[i] = yogurtType.get(fields[i], fields[i])

    ######## MAIN FUNCTION##########
    product = str(product)
    if product == '7734':
        standardizePaperTowel(fields)
    elif product == '1177':
        standardizeDressing(fields)
    elif product == '1323':
        standardizeChip(fields)
    elif product == '1553':
        standardizeDrink(fields)
    elif product == '1290':
        standardizeSoup(fields)
    elif product == '2672':
        standardizeIceCream(fields)
    elif product == '3625':
        standardizeMilk(fields)
    elif product == '1487':
        standardizeWater(fields)
    elif product == '3603':
        standardizeYogurt(fields)
    else:
        print('NO MATCHING PRODUCT ID')

def getFamilyProductDF(prodID, famFile, prodMeta, tripMeta, stand):
    '''
    Subset each family purchase file to only include a particular product.
    '''
    productPurchases = []
    with open(famFile, 'r') as infile:
        for line in infile:
            fields = line.strip('\n').split('\t')
            product = fields[6]

            if product == prodID:
                purchInfo = getPurchaseFeatures(fields, prodMeta, tripMeta,
                        stand, prodID)
                if not purchInfo:
                    break

                # Set empty fields to NAN
                for i,field in enumerate(purchInfo):
                    if (field == '' or field == 'NA' or field == 'N/A' or field
                    == 'NOT STATED' or field == ' '):
                        purchInfo[i] = np.nan

                productPurchases.append(purchInfo)

    return pd.DataFrame(productPurchases, columns=COLUMN_NAMES)


def famPurchToDF(prodID, famFile, prodMeta, tripMeta, NADict):
    '''
    Read a family purchase file. Extract purchases of a specific product.
    Create cleaned dataframe where categorical vars only take on binary values:
    a '1' if variable consistent with favorite brand and 0 otherwise.
    '''
    famID = famFile.strip('\n').split('/')[-1].split('_')[0]
    famDF = getFamilyProductDF(prodID, famFile, prodMeta, tripMeta)
    stringToNum(famDF)

    # Get rows indices of 'favorite' brand
    loyalRow, otherRow = getLoyalProductIndices(famDF)
    changeProdIDtoBinary(famDF, loyalRow, otherRow)
    rawValToBinary(famDF, loyalRow, NADict)

    return famDF


def individualFamPurchtoDF(prodID, famFile, prodMeta, tripMeta, stand=False):
    '''
    Read a family purchase file. Extract purchases of a specific product.
    Create cleaned dataframe where categorical vars only take on binary values:
    a '1' if variable consistent with favorite brand and 0 otherwise.
    '''
    famID = famFile.strip('\n').split('/')[-1].split('_')[0]
    famDF = getFamilyProductDF(prodID, famFile, prodMeta, tripMeta, stand)
    ofName = 'famProdData/' + str(prodID) + '_' + str(famID) + '_DF.tsv'
    #famDF.to_csv(ofName, sep='\t', float_format='%.2f')
    stringToNum(famDF)

    # Get rows indices of 'favorite' brand
    loyalRow, otherRow = getLoyalProductIndices(famDF)
    changeProdIDtoBinary(famDF, loyalRow, otherRow)
    individualRawValToBinary(famDF, loyalRow)

    return individualRemoveNAColumns(famDF)

def combineFamDF(famFileList, prodID, prodMeta, tripMeta):
    '''
    Iterate through all family purchase files, creating a dataframe from each
    and appending to the combined dataframe.
    '''
    totalFamilies = len(famFileList)
    # Store number of families where unable to determine any switching
    # information from column
    NADict = {col : 0 for col in CATEGORICAL_VARS}

    combinedPurchaseDF = pd.DataFrame()
    for famFile in famFileList:
        famDF = famPurchToDF(prodID, famFile, prodMeta, tripMeta, NADict)
        combinedPurchaseDF = combinedPurchaseDF.append(famDF)

    combinedPurchaseDF = removeNAColumns(combinedPurchaseDF, NADict,
            totalFamilies)

    return combinedPurchaseDF.fillna(NA)
