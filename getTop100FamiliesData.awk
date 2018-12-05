#!/bin/bash

# Have a list of the most active families in the Nielsen consumer data set according to number of trips
# and dollars spent. Would like to subset the "XXXX_trips.tsv' and 'XXXX_purchases.csv' files to 
# create one merged file for each family. 

# Define input/output directories and files 
inDataDir='/scratch/enma222/panel'
outDataDir='/scratch/enma222/panel/allFamData'
topFamFile='/scratch/enma222/panel/metaData_eamonn/householdIDCounts.tsv'

#Retain only IDs of top 100 families 
cut -f1 ${topFamFile} | head -101 | tail -100 > ${outDataDir}/topIDList.tmp
topFamIDFile=${outDataDir}/topIDList.tmp

# Parse through the XXXX_trips.tsv and XXXX_purchases.tsv for each year.
# We first want to extract the tripIDs related to any family. 
# Then parse through the purchases file and output any line having a matching tripID 

for yr in {2004..2016}; do
	purchFile=${inDataDir}/${yr}/Annual_Files/purchases_${yr}.tsv
	tripFile=${inDataDir}/${yr}/Annual_Files/trips_${yr}.tsv
	outFile=${outDataDir}/${yr}_100FamilyPurchases.tmp
	outDatesFile=${outDataDir}/${yr}_tripIDWithDates.tmp

	awk 'BEGIN { 
		# Get family IDs
		while (getline < "'"$topFamIDFile"'")
		{
			ids[$1];
		}
		close("'"$topFamIDFile"'")
		print "Got family IDs from file, searching trips..."			

		# Search for family IDs in trip file,
		# Store trip IDs WITH FAM ID AS KEY in array
       	# Also, print tripID - date to file 
		while (getline < "'"$tripFile"'")  
		{
			if ($2 in ids) 
			{ 
				trips[$1] = $2; 
				print $1"\t"$3 > "'"$outDatesFile"'"
			}
		}
		close("'"$tripFile"'")
		print "Stored trip IDs in array, searching purchases..."

		# Search for trip IDs in purchases file,
		# redirect matching lines to outfile
		while (getline < "'"$purchFile"'") 
		{
			if ($1 in trips) {
				famID=trips[$1];
				print $0"\t"famID > "'"$outFile"'";
			}
		}
		close("'"$purchFile"'")
		close("'"$outfile"'")

		print "'"$purchFile"'"
		print "Finished parsing"
		}'

	# Get rid of the ^M character inserted by awk
	sed -i 's/\r//g' ${outFile}
	echo "^M character removed"
done


#-----------------------------------------------------------------------------------------------------------------------------------------------------#
# Obtain all unique UPCs from the master purchases file. Collect meta data on these items from the master_products file
# (supplied by Nielsen).
 
masterPurchaseFile='/scratch/enma222/panel/allFamData/100FamilyPurchases_master.tsv'
UPCFile='/scratch/enma222/panel/allFamData/100FamilyUPCs.txt'
cut -f2 ${masterPurchaseFile} | sort | uniq > ${UPCFile}
echo "Collected unique UPCs... ready to search master product file"

masterProductFile='/scratch/enma222/panel/Master_Files/Latest/products.tsv'
UPCMetaDataFile='/scratch/enma222/panel/allFamData/100Family_UPCMetaData.tmp'
awk 'BEGIN {
	# Get UPCs from file, store in array 
	while (getline < "'"$UPCFile"'")
	{
		upcs[$1];
	}
	close("'"$UPCFile"'")
	print "Collected UPCs..."

	# Parse master products file; return lines 
	# with matching UPCs
	while (getline < "'"$masterProductFile"'")
	{
		if ($1 in upcs) print $0 > "'"$UPCMetaDataFile"'";
	}
	close("'"$masterProductFile"'")
	close("'"$UPCMetaDataFile"'")
	print "Finished scraping master product file"
	}'

# Only keep the upc, product_module_code, product_group_code, department_code, and brand_code from the meta data file
cutMetaData='/scratch/enma222/panel/allFamData/100Family_UPCMetaData_cut.tsv'
cut -f1,4,6,8,10 ${UPCMetaDataFile} > ${cutMetaData}
echo "Finished cutting meta data file... process complete"


#-----------------------------------------------------------------------------------------------------------------------------------------------------#
# Run python script to add product meta data to master family purchases file 
#
inDir='/scratch/enma222/panel/allFamData'
upc=${inDir}/cut_UPCMetaData_100Family.tsv
trips=${inDir}/tripIDWithDates_100Family.tsv
purchases=${inDir}/purchases_Master_100Family.tsv
./appendDateAndCategoryToPurchase.py ${upc} ${trips} ${purchases}


#-----------------------------------------------------------------------------------------------------------------------------------------------------#
# Concatenate all of the XXXX_purchase.tmp files into one master list. 
# Grep each family ID to output a list of all purchases from 2004-2016. 
cd /scratch/enma222/panel/allFamData
master=completeData/purchases_Master_100Family_addPurchaseMetaData.tsv
famIDFile=completeData/famIDList_100Family.txt

awk 'BEGIN {
	while (getline < "'"$famIDFile"'")
	{
		famID[$1];
	}
	close("'"$famFile"'")

	for ( id in famID)
	{
		ofname=id"_allPurchases.tsv";
		while (getline < "'"$master"'")
		{
			if ($8 == id) print $0 > ofname;
		}
		close("'"$master"'")
		print id" Finished..."	
	}
	}'


#-----------------------------------------------------------------------------------------------------------------------------------------------------#
# Finally, cut the individual purchase files of each family to only keep necessary information.
# Add header line  
# Then sort by purchase date.
cd /scratch/enma222/panel/allFamData
ls famPartitionedData/ > fileList.txt

while read line; do 
	sort -k13 famPartitionedData/${line} > ${line}.sort
	echo '$line done'	
done < fileList.txt
