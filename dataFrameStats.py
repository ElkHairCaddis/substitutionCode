#!/usr/bin/env python3

'''
Collect statistics on the raw and transformed data sets.
'''

from constants import (PVT_LABEL_LOW, PVT_LABEL_HIGH, CHANGE, SAME, NA)
import scipy.stats as stat
import collections

def getPercentNaN(df):
    '''
    Get percentage of missing values from dataframe.
    '''
    results = []
    totalRows = float((df.shape)[0])
    for col in list(df):
        naCount = df[col].isna().sum()
        percentNAN = round(float(naCount/totalRows * 100.00),2)
        results.append((col,percentNAN))
    return results


def getPercentNoSwitch(famDF):
    '''
    Percent of purchases that are favorite brand.
    '''
    favBrand = famDF['brandCode'].mode().iloc[0]
    favBrandNPurch = (famDF['brandCode'] == favBrand).sum()
    totalPurch = (famDF.shape)[0]

    return float(favBrandNPurch / totalPurch) * 100.00


def getPercentDealSwitch(famDF):
    '''
    Percent of cases where there is a switch '0' and also a deal flag set.
    '''
    switch = famDF['brandCode'] == CHANGE
    deal = famDF['deal'] == 1
    stay = famDF['brandCode'] == SAME

    nSwitch = (switch).sum()
    nStay = (stay).sum()
    nSwitchAndDeal = (switch & deal).sum()
    nStayAndDeal = (stay & deal).sum()

    percSwitchAndDeal = float(nSwitchAndDeal / nSwitch) * 100.00
    percStayAndDeal = float(nStayAndDeal / nStay) * 100.00

    return (percSwitchAndDeal, percStayAndDeal)


def getPercentPrivateLabel(famDF):
    '''
    Get the percentage of purchases that are private label.
    '''
    nPvtLabel = (famDF['private'] == 1).sum()
    total = float((famDF.shape)[0])

    return (nPvtLabel / total) * 100.00


def getPrivateLabelPriceData(famDF):
    priv = famDF['private'] == 1
    nonPriv = famDF['private'] == 0
    privRows = famDF.index[priv].tolist()
    nonPrivRows = famDF.index[nonPriv].tolist()


    privPrice = (famDF.loc[privRows,'unitCost']).values.mean()
    nonPrivPrice = (famDF.loc[nonPrivRows,'unitCost']).values.mean()

    return (privPrice, nonPrivPrice)


def getUnitCostData(famDF, loyalRow, otherRow):
    '''
    Test the mean prices between favorite and switching brand purchases.
    '''
    loyalPrices = (famDF.loc[loyalRow, 'unitCost']).values
    otherPrices = (famDF.loc[otherRow, 'unitCost']).values

    avgLoyal = loyalPrices.mean()
    avgOther = otherPrices.mean()

    tTest = stat.ttest_ind(loyalPrices, otherPrices, equal_var=False)
    tStatistic = tTest[0]
    pVal = tTest[1]
    if not pVal or not tStatistic:
        print('No data from this tTest')

    return [avgLoyal, avgOther, tStatistic, pVal]


def getOrigCostData(famDF, loyalRow, otherRow):
    '''
    Test the mean prices between favorite and switching brand purchases.
    '''
    loyalPrices = (famDF.loc[loyalRow, 'origUnitCost']).values
    otherPrices = (famDF.loc[otherRow, 'origUnitCost']).values

    avgLoyal = loyalPrices.mean()
    avgOther = otherPrices.mean()

    tTest = stat.ttest_ind(loyalPrices, otherPrices, equal_var=False)
    tStatistic = abs(tTest[0])
    pVal = tTest[1]
    if not pVal or not tStatistic:
        print('No data from this tTest')

    return [avgLoyal, avgOther, tStatistic, pVal]


def getPercOffData(famDF, loyalRow, otherRow):
    '''
    Test the mean prices between favorite and switching brand purchases.
    '''
    loyalOff = (famDF.loc[loyalRow, 'percOff']).values
    otherOff = (famDF.loc[otherRow, 'percOff']).values

    avgLoyal = loyalOff.mean()
    avgOther = otherOff.mean()

    tTest = stat.ttest_ind(loyalOff, otherOff, equal_var=False)
    tStatistic = abs(tTest[0])
    pVal = tTest[1]
    if not pVal or not tStatistic:
        print('No data from this tTest')

    return [avgLoyal, avgOther, tStatistic, pVal]


def getCoupValData(famDF, loyalRow, otherRow):
    '''
    Test the mean coupon value between favorite and switching brand purchases.
    '''
    loyalPrices = (famDF.loc[loyalRow, 'coupVal']).values
    otherPrices = (famDF.loc[otherRow, 'coupVal']).values

    avgLoyal = loyalPrices.mean()
    avgOther = otherPrices.mean()

    tTest = stat.ttest_ind(loyalPrices, otherPrices, equal_var=False)
    tStatistic = abs(tTest[0])
    pVal = tTest[1]

    return [avgLoyal, avgOther, tStatistic, pVal]


def getRetailerData(famDF, loyalRow, otherRow):
    '''
    Test the correlation between retailer and switching behavior.
    '''
    favRetail = famDF['retailCode'].mode().iloc[0]
    favRetailPurchTot = (famDF['retailCode'] == favRetail).sum()
    favRetailPurchLoy = (famDF.loc[loyalRow,'retailCode'] == favRetail).sum()
    favRetailPurchOth = (famDF.loc[otherRow,'retailCode'] == favRetail).sum()

    totalPurch = (famDF.shape)[0]
    percFav = float(favRetailPurchTot / totalPurch) * 100.00
    percFavLoy = float(favRetailPurchLoy / len(loyalRow)) * 100.00
    percFavOth = float(favRetailPurchOth / len(otherRow)) * 100.00

    return [percFav, percFavLoy, percFavOth]


def returnAllStatistics(pID, famID, famDF, loyalRow, otherRow, nan=True, deal=True,
        private=True, unit=True, coup=True, retail=True, loyal=True,
        origUnit=True, percOff=True):
    '''
    Return the results of all statistical tests described above.
    '''
    results = [pID, famID]
    if loyal:
        results.append(getPercentNoSwitch(famDF))
    if nan:
        results.append(getPercentNaN(famDF))
    if deal:
        results.extend([x for x in getPercentDealSwitch(famDF)])
    if percOff:
        results.extend([x for x in getPercOffData(famDF, loyalRow, otherRow)])
    if private:
        results.append(getPercentPrivateLabel(famDF))
    if origUnit:
        results.extend([x for x in getOrigCostData(famDF, loyalRow, otherRow)])
    if unit:
        results.extend([x for x in getUnitCostData(famDF, loyalRow, otherRow)])
    if coup:
        results.extend([x for x in getCoupValData(famDF, loyalRow, otherRow)])
    if retail:
        results.extend([x for x in getRetailerData(famDF, loyalRow, otherRow)])

    return results


def returnStatsFieldNames(nan=True, deal=True, private=True, unit=True,
        coup=True, retail=True, loyal=True, origUnit=True, percOff=True):
    '''
    Depending on which statistics we would like to look at, return the field
    names for header row of output csv.
    '''
    fields = ['prodID','famID']
    if loyal:
        fields.extend(['brandLoyalty'])
    if nan:
        fields.extend(['percNaN'])
    if deal:
        fields.extend(['switch&Deal','stay&deal'])
    if percOff:
        fields.extend(['loyalOff','otherOff','offTval','offPval'])
    if private:
        fields.extend(['privateLabel'])
    if unit:
        fields.extend(['loyalUC','otherUC','UCtval','UCpval'])
    if origUnit:
        fields.extend(['loyalOUC', 'otherOUC', 'OUCtval', 'OUCpval'])
    if coup:
        fields.extend(['loyalCoup','otherCoup','coupTval','coupPval'])
    if retail:
        fields.extend(['retailLoyal','stayRetailLoyal','switchRetailLoyal'])

    return fields 
