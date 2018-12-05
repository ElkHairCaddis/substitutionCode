#!/usr/bin/env python3

import glob
import pandas as pd

CANDIDATE_FILES_DIR = '/home/enma222/marketingCode/analyzeCombinedFamilies/data/loyalFamList/'

# For the trip metadata. If purchase was made on weekday, assign value of 1. If
# purchase made on Fri, Sat, or Sun, assign value of 2.
WEEKDAY = 1
WEEKEND = 2

'''
1) Read in list of candidate files for each family.
2) Store all needed metadata in dictionaries for quick mapping.
'''

def getLoyalFamilies(fname):
    '''
    For a given product, read list of loyal family purchase files.
    '''
    familyFiles = []
    with open(fname, 'r') as infile:
        for line in infile:
            famFile = line.strip('\n') + '_allPurchases.tsv'
            familyFiles.append(famFile)

    return familyFiles


def getCandidateProductFileList():
    '''
    Read in the list of candidate products from file.
    '''
    return glob.glob(CANDIDATE_FILES_DIR + '*_loyalFamilies.txt')


def getTripMetaData(fname):
    '''
    Store mapping from tripID to store data in a dictionary.
    We will only include the retail identifier (e.x. Walmart versus WholeFoods)
    for this analysis
    '''
    tripDict = {}
    with open(fname, 'r') as infile:
        next(infile)
        for line in infile:
            fields = line.strip('\n').split('\t')
            date = pd.to_datetime(fields[-1])
            dayOfWeek = pd.Timestamp.weekday(date)
            if dayOfWeek < 4:
                tripDict[fields[0]] = [fields[1], WEEKDAY, fields[-1]]
            else:
                tripDict[fields[0]] = [fields[1], WEEKEND, fields[-1]]

    return tripDict


def getExtraPurchaseInfo(fname):
    '''
    Store mapping fro UPC to product information in dictionary.
    '''
    extraDict = {}
    with open(fname, 'r') as infile:
        for line in infile:
            fields = line.strip('\n').split('\t')
            extraDict[fields[0]] = fields[1:]
    return extraDict

def getUPCInfo(fname):
    '''
    Store mapping from UPC to brand name dictionary.
    '''
    UPCDict = {}
    with open(fname, 'r') as infile:
        for line in infile:
            fields = line.strip('\n').split('\t')
            UPCDict[fields[0]] = fields[1:]
    return UPCDict

def getProductName(fname):
    '''
    Map product code to description.
    '''
    nameDict = {}
    with open(fname,'r') as infile:
        for line in infile:
            fields = line.strip('\n').split('\t')
            productName = fields[1]
            # Replace spaces, /, and -
            for char in [' ','/','-']:
                productName.replace(char,'_')
            nameDict[fields[0]] = productName

    return nameDict

def getAllMetaData(tripFile, extraPurchFile, UPCFile, nameFile):
    '''
    One function to return all dictionaries.
    '''
    tripDict = getTripMetaData(tripFile)
    print('Read trip metadata...')
    extraDict = getExtraPurchaseInfo(extraPurchFile)
    print('Read product metadata...')
    upcDict = getUPCInfo(UPCFile)
    print('Read upc -> brand metadata...')
    nameDict = getProductName(nameFile)
    print('Got product descriptions...')

    return (tripDict, extraDict, upcDict, nameDict)
