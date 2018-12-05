#!/usr/bin/env python3

import pandas as pd
import numpy as np
from constants import (CHANGE, SAME, NA)
from constants import COLUMN_NAMES, CATEGORICAL_VARS


# Prepare individual dataframes per product per family.
# Record change versus preferred product.
# E.x. if most of the loyal brand purchases are some flavor but the others are
# not or if most of loyal are in one zip but others are not.
# Remove unnecessary data


def stringToNum(df):
    '''
    Convert string arguments to numeric types for appropriate columns like
    unitCost.
    '''
    df['deal'] = pd.to_numeric(df['deal'])
    df['brandCode'] = pd.to_numeric(df['brandCode'])
    df['unitCost'] = pd.to_numeric(df['unitCost'])
    df['coupVal'] = pd.to_numeric(df['coupVal'])
    df['percOff'] = pd.to_numeric(df['percOff'])

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)

def getLoyalProductIndices(df):
    '''
    Get row indices for purchases of favorite and not favorite products
    '''
    loyalProductID = df['brandCode'].mode().iloc[0]
    loyalRows = df.index[df['brandCode'] == loyalProductID].tolist()
    unLoyalRows = df.index[df['brandCode'] != loyalProductID].tolist()

    return (loyalRows, unLoyalRows)

def changeProdIDtoBinary(df, loyalRows, unLoyalRows):
    '''
    In the dataframe, make prodID of loyal rows '0' and unloyal rows '1'
    '''
    df.loc[loyalRows, 'brandCode'] = SAME
    df.loc[unLoyalRows, 'brandCode'] = CHANGE

def rawValToBinary(df, loyalRows, NADict, variables=CATEGORICAL_VARS):
    '''
    Instead of raw values for each column, look at whether there is a change
    versus the dominant brand. If the majority of columns are 'NA', set = 10
    and record this information. If too many families are lacking data in a
    particular column, we will remove them in the next function
    'removeNAColumns'
    '''
    def majorityNA(df, column, loyalRows):
        '''
        Determine if most entries in column for the most popular brand are NaN.
        '''
        loyalVals = df.loc[loyalRows,var]
        halfRows = int(len(loyalVals) * 0.5)
        if loyalVals.isna().sum() > halfRows:
            return True
        else:
            return False


    for var in variables:

        # Determine most popular value for favorite brand and change rows
        # accordingly.
        if not majorityNA(df, var, loyalRows) and var != 'dayOfWeek':
            favBrandChoice = df.loc[loyalRows,var].mode()
            favBrandChoice = favBrandChoice[0]

            consistentRetailPurchase = df.index[(df[var] == favBrandChoice) &
                (df[var].notna())].tolist()
            inconsistentRetailPurchase = df.index[(df[var] != favBrandChoice) &
                (df[var].notna())].tolist()

            df.loc[consistentRetailPurchase, var ] = SAME
            df.loc[inconsistentRetailPurchase, var] = CHANGE
            df[var].fillna(NA)

        # Cannot determine a favorite value for the loyal brand.
        # Increment family count for this column in NADict
        elif var == 'dayOfWeek':
            pass
        else:
            df.loc[:,var] = NA
            NADict[var] += 1


def individualRawValToBinary(df, loyalRows, variables=CATEGORICAL_VARS):
    '''
    Instead of raw values for each column, look at whether there is a change
    versus the dominant brand. If the majority of columns are 'NA', set = 10
    and record this information. If too many families are lacking data in a
    particular column, we will remove them in the next function
    'removeNAColumns'
    '''
    def majorityNA(df, column, loyalRows):
        '''
        Determine if most entries in column for the most popular brand are NaN.
        '''
        loyalVals = df.loc[loyalRows,var]
        halfRows = int(len(loyalVals) * 0.5)
        if loyalVals.isna().sum() > halfRows:
            return True
        else:
            return False


    for var in variables:

        # Determine most popular value for favorite brand and change rows
        # accordingly.
        if not majorityNA(df, var, loyalRows) and var != 'dayOfWeek':
            favBrandChoices = set(df.loc[loyalRows,var].values)
            try:
                favBrandChoices.remove(np.nan)
            except:
                pass

            consistentRetailPurchase = df.index[(df[var].isin(favBrandChoices)) &
                (df[var].notna())].tolist()
            inconsistentRetailPurchase = [x for x in df.index if x not in
                    consistentRetailPurchase]

            df.loc[consistentRetailPurchase, var ] = SAME
            df.loc[inconsistentRetailPurchase, var] = CHANGE
            df[var].fillna(NA)

        # Cannot determine a favorite value for the loyal brand.
        # Increment family count for this column in NADict
        elif var == 'dayOfWeek':
            pass
        else:
            df.loc[:,var] = NA


def removeNAColumns(df, NACount, totalFamilies):
    '''
    Remove any columns from df where the majority of families offer no
    information on swapping behavior.
    '''
    emptyCols = []
    for var in CATEGORICAL_VARS:
        if NACount[var] > int(0.5 * totalFamilies):
            #print('Empty Col: ' + var + '. # NA: ' + str(NACount[var]))
            emptyCols.append(var)
    nonEmptyCols = [col for col in COLUMN_NAMES if col not in emptyCols]

    return df.loc[:,nonEmptyCols]


def individualRemoveNAColumns(df):
    '''
    For an individual family DF, remove cols where greater than 50% percent of
    the columns are NA.
    '''
    #print('Checking NA col count...')
    emptyCols = []
    totalRow = (df.shape)[0]
    for var in CATEGORICAL_VARS:
        NAcount = (df[var] == NA).sum()
        if NAcount > int(.5 * totalRow):
            emptyCols.append(var)
            #print('Col: ' + var + ' is mostly NA')
            #print('Count: ' + str(NAcount))
    nonEmptyCols = [col for col in COLUMN_NAMES if col not in emptyCols]

    return df.loc[:, nonEmptyCols]

def dateToDays(famDF):
    '''
    Turn date into number of days since first recorded purchase.
    '''
    earliestDate = famDF['date'].min()
    newCol = []
    for d in famDF['date']:
        nDays = (d - earliestDate).days
        newCol.append(nDays)

    famDF = famDF.assign(dayCount=pd.Series(newCol))
    famDF['dayCount'] = pd.to_numeric(famDF['dayCount'])

    return famDF

def addBrandSaturation(famDF):
    '''
    It is possible that after purchasing the same brand for a while, the
    consumer will simply switch brands out of boredom for the sake of variety.
    Here, we will attempt to quantify this loyal brand 'saturation'.
    '''
    def getFavPurchInARow(df, rowIndex, count, newList):
        '''
        Number of purchases of fav brand in a row
        '''
        if df.loc[rowIndex,'brandCode'] == 1:
            newList.append(count)
            return count + 1
        else:
            newList.append(count)
            return 0

    def daysSinceLastSwitch(df, rowIndex, lastSwitchDate, newList):
        '''
        Number of calendar days since last brand divergence.
        '''
        days = df.loc[rowIndex,'dayCount'] - lastSwitchDate
        newList.append(days)
        if df.loc[rowIndex, 'brandCode'] == 0:
            return df.loc[rowIndex,'dayCount']
        else:
            return lastSwitchDate

    def purchasesIn2Month(df, rowIndex, newList):
        '''
        Number of brand purchases made in 2 mo.
        '''
        date = df.loc[rowIndex,'dayCount']
        q1 = (date - df['dayCount']) > 0
        q2 = (date - df['dayCount']) < 60
        q3 = (df['brandCode'] == SAME)
        qFinal = (q1 & q2 & q3)

        within2Mo = qFinal.sum()
        newList.append(within2Mo)

    ######### Main function ##########
    inARow = []
    sinceLast = []
    per2Month = []

    count = 0
    lastSwitch = 0

    for purch in famDF.index:
        count = getFavPurchInARow(famDF, purch, count, inARow)
        lastSwitch = daysSinceLastSwitch(famDF, purch, lastSwitch, sinceLast)
        purchasesIn2Month(famDF, purch, per2Month)

    famDF = famDF.assign(row=pd.Series(inARow), dls=pd.Series(sinceLast),
            twoMo=pd.Series(per2Month))
    famDF['row'] = pd.to_numeric(famDF['row'])
    famDF['dls'] = pd.to_numeric(famDF['dls'])
    famDF['twoMo'] = pd.to_numeric(famDF['twoMo'])

    return famDF

