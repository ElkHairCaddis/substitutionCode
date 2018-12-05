#!/usr/bin/env python3

# I want to focus on just a few families in the Booth 'Panel' data to
# get experience processing the data set and determine if we are able
# to detect any substitution actions.

import subprocess
import sys
import glob

'''
 Retrieve the 'trips_*.tsv' files from each year to get IDs.
'''
def getTripFileList():
	return glob.glob('/scratch/enma222/boothPanel/*/Annual_Files/trips_*.tsv')


'''
 Update the 'familyCountDict' in the getFamilyTripCount() function
 by process a line from a trip_****.tsv file.
'''
def updateFamilyCount(d, line):
	cols = line.strip('\n').split('\t')
	householdID = int(cols[1])
	dollarsSpent = float(cols[7])
	if householdID in d:
		d[householdID][0] += 1
		d[householdID][1] += dollarsSpent
	else:
		d[householdID] = [1, dollarsSpent]


'''
 Count the total number of trips and dollars spent for each family.
'''
def getFamilyTripCount(tripFileList):
	familyCountDict = {}
	for tripFile in tripFileList:
		with open(tripFile, 'r') as infile:
			next(infile) # Skip header row
			for line in infile:
				updateFamilyCount(familyCountDict, line)
		print('Finished processing ' + tripFile.strip('\n').split('/')[-1])
	return familyCountDict


'''
 Get top 3 household IDs by number of visits and dollars spent
 by processing dictionary returned by getFamilyTripCount().

 EDIT: Just print all data in one list  
'''
def printSorted(d):
	sorted_by_tripCount = sorted(d.items(), key=lambda kv: (kv[1])[0], reverse=True)

	print('householdID\ttotalTrips\tdollarsSpent\n')
	for tup in sorted_by_tripCount: 
		print(str(tup[0]) + '\t' + str((tup[1])[0]) + '\t' + str((tup[1])[1]))


'''
Main program.
'''
if __name__ == '__main__':
	tripFiles = getTripFileList()
	countDict = getFamilyTripCount(tripFiles)
	printSorted(countDict)

