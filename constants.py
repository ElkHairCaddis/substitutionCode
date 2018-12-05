#!/usr/bin/env python3

"""
Definition of global constants.
"""

START_DIR = '/scratch/enma222/famPartitionedData/'

# Metadata files
TRIP_METADATA = START_DIR + 'metaData/tripWithStoreInfo_date.tsv'
EXTRA_PRODUCT_METADATA = START_DIR + 'metaData/focusProducts.tsv.cut'
UPC_METADATA = START_DIR + 'metaData/UPCandBrand_100Family.tsv'
NAME_MAP = START_DIR + '/metaData/productNames.txt'

# Family purchase and candidate product files
PURCHASE_DATA_DIR = START_DIR + 'inputData/'
CANDIDATE_PRODUCT_DIR = START_DIR + 'results/candProducts/'
DOT_FILE_OUT_DIR = START_DIR + 'results/dTreePics/'

# Private Label brand code
PVT_LABEL_LOW = 536746
PVT_LABEL_HIGH = 536876

# We have a deviation from normal purchasing behavior
CHANGE = 0

# Purchase behavior consistent with favorite brand.
SAME = 1

# Remaining NA values
NA = 10

# Data stored in the dataframe for each purchase.
COLUMN_NAMES = [
        'private',
        'origUnitCost',
        'unitCost',
        'coupVal',
        'percOff',
        'deal',
        'brandCode',
        'flavor',
        'form',
        'formula',
        'container',
        'salt',
        'style',
        'type',
        'product',
        'variety',
        'organic',
        'strength',
        'scent',
        'dosage',
        'gender',
        'sizeCode',
        'sizeAmount',
        'sizeUnit',
        'retailCode',
        'dayOfWeek',
        'date'
        ]


# Only categorical variable names.
CATEGORICAL_VARS = [
        'flavor',
        'form',
        'formula',
        'container',
        'salt',
        'style',
        'type',
        'product',
        'variety',
        'organic',
        'strength',
        'scent',
        'dosage',
        'gender',
        'sizeCode',
        'sizeAmount',
        'sizeUnit',
        'retailCode',
        'dayOfWeek'
        ]


waterContainer = {
        'ASEPTIC':'ASEPTIC',
        'BOTTLE IN BOX':'BOTTLE',
        'BOX':'BOTTLE',
        'CAN':'CAN',
        'CARTON':'CARTON',
        'NON REFILLABLE BOTTLE PLS':'BOTTLE',
        'NON REFILLABLE BOTTLES':'BOTTLE',
        'NON REFILLABLE BOTTLES PLS':'BOTTLE',
        'POUCH':'POUCH',
        'REFILLABLE BOTTLES PLS':'BOTTLE'
        }

waterFlav = {
	'BLACK & BLUE BERRY':'BLACK AND BLUE BERRY',
	'KIWI STRAWBERRY':'KIWI/STRAWBERRY',
	'PEACH & MANGO':'PEACH/MANGO'
	}


waterType = {
        'ALPINE SPRING WATER':'SPRING',
        'ARTESIAN DRINKING WATER':'ARTESIAN',
        'ARTESIAN WATER':'ARTESIAN',
        'COCONUT WATER':'COCONUT',
        'DIETERS WATER':'FITNESS',
        'DISTILLED BABY WATER':'BABY',
        'DISTILLED DRINKING WATER':'DRINKING',
        'DISTILLED WATER':'DRINKING',
        'DRINKING & DISTILLED WATER':'DRINKING',
        'DRINKING WATER':'DRINKING',
        'ENERGY WATER':'FITNESS',
        'ENHANCED WATER':'ENHANCED',
        'EXTRA FANCY':'EXTA FANCY',
        'FITNESS WATER':'FITNESS',
        'MINERAL WATER':'MINERAL',
        'MNT SPRING WATER':'SPRING',
        'NONCARBONATED SOFT DRINK':'SOFT',
        'NT ARTESIAN DRINKING WATER':'ARTESIAN',
        'NT ARTESIAN WATER':'ARTESIAN',
        'NT DRINKING WATER':'DRINKING',
        'NT MINERAL WATER':'MINERAL',
        'NT MNT SPRING WATER':'SPRING',
        'NT SPARK MINERAL WATER':'SPARKLING MIN',
        'NT SPRING WATER':'SPRING',
        'PRM DRINKING WATER':'DRINKING',
        'PRM MNT SPRING WATER':'SPRING',
        'PROTEIN WATER':'FITNESS',
        'PURE DISTILLED WATER':'DRINKING',
        'PURE DRINKING WATER':'PURIFIED',
        'PURE MNT SPRING WATER':'SPRING',
        'PURE NT SPRING WATER':'SPRING',
        'PURE SPRING WATER':'SPRING',
        'PURIFIED BABY WATER':'BABY',
        'PURIFIED DISTILLED WATER':'DRINKING',
        'PURIFIED DRINKING WATER':'DRINKING',
        'PURIFIED INFANT TODDLER WATER':'BABY',
        'PURIFIED SPRING WATER':'SPRING',
        'PURIFIED WATER':'DRINKING',
        'PURIFIED WATER BEVERAGE':'DRINKING',
        'SPARKLING SPRING WATER':'SPARKLING',
        'SPARK MINERAL WATER':'SPARKLING MIN',
        'SPARK WATER':'SPARKLING',
        'SPORTS WATER':'FITNESS',
        'SPRING WATER':'SPRING',
        'ULTRA PRM DRINKING WATER':'DRINKING',
        'VITAMIN SPRING WATER':'FITNESS',
        'VITAMIN WATER':'FITNESS',
        'WATER BEVERAGE':'DRINKING'
        }


iceCreamFormula = {
        'DIET':'REDUCED FAT',
        'DIET FAT FREE':'FAT FREE',
        'FAT FREE':'FAT FREE',
        'FAT FREE LIF':'FAT FREE',
        'HALF THE FAT':'REDUCED FAT',
        'LACTOSE FREE':'LACTOSE FREE',
        'LACTOSE REDUCED':'LACTOSE REDUCED',
        'LESS CALORIE LESS FAT':'REDUCED FAT',
        'LESS CALORIE REDUCED FAT':'REDUCED FAT',
        'LESS FAT':'REDUCED FAT',
        'LESS FAT REDUCED FAT':'REDUCE FAT',
        'LESS FAT REDUCED FAT LFRE':'REDUCED FAT',
        'LFRE':'REDUCED FAT',
        'LIGHT':'REDUCED FAT',
        'LIGHT HALF THE FAT':'REDUCED FAT',
        'LIGHT LESS FAT':'REDUCED FAT',
        'LIGHT REDUCED FAT':'REDUCED FAT',
        'LITE LESS FAT':'REDUCED FAT',
        'LOW FAT':'REDUCED FAT',
        'REDUCED CALORIE REDUCED FAT':'REDUCED FAT',
        'REDUCED FAT':'REDUCED FAT',
        'REGULAR':'REGULAR'
        }


iceCreamOrganic = {
        'CALIFORNIA CRTFD ORG FARMERS':'ORGANIC',
        'CRTFD ORG BY CCOF ORG':'ORGANIC',
        'M/ORG CANE SGR':'ORGANIC',
        'ORG':'ORGANIC'
        }

iceCreamProduct = {
        'DESSERT':'',
        'ICE CREAM':''
        }

iceCreamVar = {
        'ROUND TOP':''
        }

milkForm = {'LIQUID':''}


milkOrganic = {
        'CERTIFIED ORGANIC BY QAI':'ORGANIC',
        'C-O':'ORGANIC',
        'COBOT ORGANIC':'ORGANIC',
        'COBQAI ORGANIC':'ORGANIC',
        'C-O BY QCS ORGANIC':'ORGANIC',
        'C-O ORGANIC':'ORGANIC',
        'CRTFD ORGANIC':'ORGANIC',
        'ORGANIC':'ORGANIC',
        'OR TILTH C-O ORGANIC':'ORGANIC'
        }


milkType = {
        '1% LOWFAT':'1%',
        '1% LOWFAT LIGHT VITAMIN A/D':'1%',
        '1% LOWFAT V-AP/D3':'1%',
        '1% LOWFAT VITAMIN A/C/D':'1%',
        '1% LOWFAT VITAMIN A/D':'1%',
        '1% LOWFAT VITAMIN A/D3':'1%',
        '1% LOWFAT VITAMIN A/D/D3':'1%',
        '1% LOWFAT VITAMIN A/D/E':'1%',
        '1% LOWFAT VITAMIN A/D LC-F':'1%',
        '1% LOWFAT VITAMIN A/D LR':'1%',
        '1% LOWFAT VITAMIN A/D L-R':'1%',
        '1% LOWFAT VITAMIN A/D S-A':'1%',
        '1% LOWFAT VITAMIN D3':'1%',
        '1% LOWFAT VITAMIN E':'1%',
        '2% LOWFAT VITAMIN A/D':'2%',
        '2% RD FAT':'2%',
        '2% RD FAT AC':'2%',
        '2% RD FAT VITAMIN A':'2%',
        '2% RD FAT VITAMIN A/C/D':'2%',
        '2% RD FAT VITAMIN A/D':'2%',
        '2% RD FAT VITAMIN A/D3':'2%',
        '2% RD FAT VITAMIN A/D LC-F':'2%',
        '2% RD FAT VITAMIN A/D LC-F CE':'2%',
        '2% RD FAT VITAMIN D':'2%',
        '2% RD FAT VTMN D LC-F':'2%',
        '2% REDUCED FAT VITAMIN A/D':'2%',
        '.5% LOWFAT VITAMIN A/D':'1%',
        'FF':'SKIM',
        'FF SKIM':'SKIM',
        'FF SKIM DLX VITAMIN A/D':'SKIM',
        'FF SKIM SPM VITAMIN A/D':'SKIM',
        'FF SKIM VITAMIN A':'SKIM',
        'FF SKIM VITAMIN A/C/D':'SKIM',
        'FF SKIM VITAMIN A/D':'SKIM',
        'FF SKIM VITAMIN A/D CE':'SKIM',
        'FF SKIM VITAMIN A/D/D3':'SKIM',
        'FF SKIM VITAMIN A/D LC-F':'SKIM',
        'FF SKM+ VITAMIN A/D':'SKIM',
        'FF SP SKM':'SKIM',
        'FF VITAMIN A/C/D':'SKIM',
        'FF VITAMIN A/C/D/E':'SKIM',
        'FF VITAMIN A/D':'SKIM',
        'FF VITAMIN A/D LC-F':'SKIM',
        'FF VITAMIN A/D LC-F CE':'SKIM',
        'FF VITAMIN D':'SKIM',
        'GOAT 1% LOWFAT VITAMIN A/D':'1%',
        'LOWFAT VITAMIN A/D':'1%',
        'LOWFAT VITAMIN A/D LC-F':'1%',
        'NF SKIM VITAMIN A/D':'SKIM',
        'NF VITAMIN A/D':'SKIM',
        'NF VITAMIN A/D LC-F':'SKIM',
        'NF VITAMIN A/D LR':'SKIM',
        'PURE GRADE A':'PURE GRADE',
        'RD FAT VITAMIN A/D':'1%',
        'SKIM VITAMIN A/D':'SKIM',
        'SKIM VITAMIN A/D/E':'SKIM',
        'SKIM VITAMIN A/D L-C':'SKIM',
        'SKIM VITAMIN A/D LR':'SKIM',
        'SKIM VITAMIN D':'SKIM',
        'SKIM VITAMIN E LC-F':'SKIM',
        'SKIM VITAMINS A D B6 B12 C E':'SKIM',
        'SKM+ VITAMIN A/D':'SKIM',
        'WHOLE KOSHER VITAMIN D':'KOSHER',
        'WHOLE LC-F VITAMIN D':'WHOLE',
        'WHOLE VITAMIN A/C/D':'WHOLE',
        'WHOLE VITAMIN A/D':'WHOLE',
        'WHOLE VITAMIN A/D LC-F':'WHOLE',
        'WHOLE VITAMIN C/D':'WHOLE',
        'WHOLE VITAMIN D':'WHOLE',
        'WHOLE VITAMIN D/E':'WHOLE',
        'WHOLE VITAMIN D KOSHER':'WHOLE',
        'WHOLE VITAMIN D LC-F':'WHOLE',
        'WHOLE VITAMIN D LC-F CE':'WHOLE'
        }


paperTowelScent = {
        'FRAGRANCE FREE':'UNSCENTED',
        'FREE OF FRAGRANCES':'UNSCENTED',
        'LEMON FRESH':'LEMON',
        'NOT COLLECTED':'NA',
        'UNSCENTED':'UNSCENTED'
        }


chipForm = {
        'CRINKLE CUT':'CRINKLE',
        'CURLY WAVE':'WAVY',
        'GROOVY':'WAVY',
        'KRINKLE CUT':'CRINKLE',
        'LATTICE CUT':'WAFFLE',
        'MARCELLED':'MARCELLED',
        'REGULAR':'REGULAR',
        'RIDGED':'WAVY',
        'RIPPLE':'WAVY',
        'RIPPLE CUT':'WAVY',
        'WAFFLE CUT':'WAFLLE',
        'WAVE CUT':'WAVY',
        'WAVY':'WAVY'
        }


chipFormula = {
        'FAT FREE':'FAT FREE',
        'LESS FAT':'REDUCED FAT',
        'LIGHT R-F NO CHOLESTEROL':'REDUCED FAT',
        'LOW FAT':'REDUCED FAT',
        'LOW FAT NO CHOLESTEROL':'REDUCED FAT',
        'NO CHOLESTEROL':'REDUCED FAT',
        'REGULAR':'REGULAR',
        'R-F':'REDUCED FAT',
        'R-F NO CHOLESTEROL':'REDUCED FAT'
        }


chipOrganic = {
        'COBOT ORGANIC':'ORGANIC',
        'ORGANIC PURE ORGANIC PRFCTN':'ORGANIC'
        }


chipProduct = {
        'BAKING MIX':'CHIP',
        'POTATO CHIP':'CHIP',
        'POTATO CRISP':'CHIP',
        'POTATO SKIN SNACK CHIP':'SKIN',
        'SWEET POTATO CHIP':'SWEET',
        'SWEET POTATO CRISP':'SWEET'
        }


chipSalt = {
        'LIGHTLY SALTED':'LOW SALT',
        'LIGHT SALT':'LOW SALT',
        'LOW SODIUM':'LOW SALT',
        'SALTED':'SALTED',
        'UNSALTED':'UNSALTED'
        }


chipStyle = {'WITHOUT FROSTING':'NA'}


chipType = {
        'BAKED':'BAKED',
        'BAKED GOURMET':'BAKED',
        'BAKED POPPED':'BAKED',
        'BAKED THICK CUT':'BAKED THICK',
        'CAROLINA STYLE':'CAROLINA',
        'CRISPY':'CRISPY',
        'CRUNCHY EXTRA THICK':'CRISPY THICK',
        'DELI STYLE':'DELI',
        'EXTRA THICK':'THICK',
        'GOURMET HAND COOKED':'HAND COOKED',
        'GOURMET KC':'KC',
        'GOURMET NATURAL':'NATURAL',
        'GOURMET NATURAL KC':'KC',
        'GOURMET NATURAL KC D-R':'KC',
        'HAND COOKED':'HAND COOKED',
        'HAND COOKED NATURAL':'HAND COOKED',
        'HOME STYLE KC':'HOMESTYLE',
        'KC':'KC',
        'KC CRUNCHY EXTRA THICK':'THICK',
        'KC EXTRA THICK':'THICK',
        'KC HAND COOKED':'HAND COOKED',
        'KC KS':'KC',
        'KC NATURAL':'NATURAL',
        'KC NATURAL BAKED':'BAKED',
        'KC NATURALLY BAKED O-R':'BAKED',
        'KC THICK':'THICK',
        'KOSHER':'KOSHER',
        'KS':'KC',
        'NATURAL':'NATURAL',
        'NATURAL CRISP':'CRISPY',
        'NATURAL CRISPY':'CRISPY',
        'NATURAL HAND COOKED':'HAND COOKED',
        'NATURAL KC':'KC',
        'NATURAL KC OF':'KC',
        'NATURAL KC OF D-R':'KC',
        'NATURAL KS THICK SLICED':'THICK',
        'NATURALLY BAKED':'BAKED',
        'OF':'OF',
        'OLD FASHION':'OF',
        'POPPED':'POPPED',
        'REGULAR':'REGULAR',
        'THICK':'THICK',
        'THICK CUT':'THICK',
        'THICK KC':'THICK',
        'THIN':'BAKED'
        }


chipVariety = {'NON-MICROWAVE':'NA'}


dressingFormula = {
        'LIGHT':'LIGHT',
        'LIGHT REDUCED CALORIE':'LIGHT',
        'LITE':'LIGHT',
        'LITE REDUCED CALORIE':'LIGHT',
        'REDUCED CALORIE':'LIGHT',
        'REGULAR':'REGULAR'
        }


dressingOrganic = {
        'CRTFD ORG':'ORGANIC',
        'M/ORG X VRGN OIL':'ORGANIC',
        'ORG':'ORGANIC'
        }


dressingType = {
        'MICROWAVE':'NA',
        'REGULAR':'REGULAR'
        }


drinkContainer = {
        'CAN':'CAN',
        'NON REFILLABLE BOTTLES':'BOTTLE',
        'NON REFILLABLE BOTTLES ALUM':'ALUM',
        'NON REFILLABLE BOTTLES GL':'GLASS',
        'NON REFILLABLE BOTTLES GL CT':'GLASS',
        'NON REFILLABLE BOTTLES GOPLS':'PLAST',
        'NON REFILLABLE BOTTLES PLS':'PLAST',
        'NON REFILLABLE BOTTLES PLS CT':'PLAST',
        'REFILLABLE BOTTLES':'REFILL'
        }


drinkForm = {'CENTER CUT SLICED':'NA', 'ROLL':'NA'}


drinkFormula = {'LESS FAT':'DIET'}

drinkOrganic = {'COBOT OG':'Organic'}

drinkSalt = {'REGULAR':'NA'}

drinkScent = {'UNLABELED':'NA'}

drinkType = {
        'ARTESIAN SPRING WATER':'SPRING',
        'FRUIT BVRG':'FRUIT',
        'SELTZER':'SELTZER',
        'SOFT DRINK':'SOFT DRINK',
        'SPARKLING ARTESIAN WATER':'ARTESIAN',
        'SPARKLING BEVERAGE':'SPARKLING',
        'SPARKLING BVRG':'SPARKLING',
        'SPARKLING JUICE BVRG':'SPARKLING',
        'SPARKLING MINERAL WATER':'MINERAL',
        'SPARKLING M-S-W':'MINERAL',
        'SPARKLING SELTZER':'SELTZER',
        'SPARKLING SODA':'SPARKLING SODA',
        'SPARKLING SPRING WATER':'SPRING',
        'SPARKLING WATER':'SPARKLING',
        'SPARKLING WATER BVRG':'SPARKLING',
        'SPARK MINERAL WATER':'MINERAL',
        'TONIC':'TONIC',
        'WATER BVRG':'WATER'
        }


soupForm = {'WHOLE':'NA'}


soupFormula = {
        'ASSORTED':'ASSORTED',
        'C-F':'CF',
        'C-F FAT FREE':'CFFF',
        'C-F FAT FREE L-S':'CFFF',
        'C-F LOW FAT':'CFLF',
        'C-F LOW FAT RM':'CFLF',
        'C-F L-S':'CFLS',
        'FAT FREE':'FF',
        'FAT FREE L-S':'FFLS',
        'FAT FREE RM':'FF',
        'FAT FREE UNSALTED':'FFNS',
        'LC':'LC',
        'LC FAT FREE':'LCFF',
        'LC FAT FREE L-S':'LCFFLS',
        'LC LOWER SODIUM':'LCLS',
        'LC LOW FAT':'LCLF',
        'LC LOW FAT LOWER SODIUM':'LCLFLS',
        'LC LOW FAT L-S':'LCLFLS',
        'LC LOW FAT RM':'LCLF',
        'LC RM':'LC',
        'LESS SALT':'LS',
        'LESS SODIUM':'LS',
        'LIGHT':'LF',
        'LIGHT FAT FREE RM':'FF',
        'LIGHT LC':'LC',
        'LIGHT LC LOW FAT':'LCLF',
        'LIGHT LOW FAT':'LF',
        'LIGHT LOW FAT RM':'LF',
        'LIGHT RM':'LF',
        'LIGHT SODIUM':'LS',
        'LOW CALORIE':'LF',
        'LOW CALORIES N-C LOW FAT':'NCLF',
        'LOWER SODIUM':'LS',
        'LOW FAT':'LF',
        'LOW FAT LOWER SODIUM':'LFLS',
        'LOW FAT L-S':'LFLS',
        'LOW FAT RM':'LF',
        'L-S':'LS',
        'L-S RM':'LS',
        'NC-FF':'NCFF',
        'NC-FF L-S':'NCFF',
        'NO CHOLESTEROL':'NC',
        'REDUCED CHOLESTEROL':'LC',
        'REGULAR':'REGULAR',
        'RM':'RM',
        'UNSALTED':'NS'
        }


soupOrganic = {
        'C-O':'ORGANIC',
        'COBOT ORG':'ORGANIC',
        'C-OBPC ORG':'ORGANIC',
        'COBPCOS ORG':'ORGANIC',
        'COBQ':'ORGANIC',
        'COBQ ORG':'ORGANIC',
        'C-O BY OREGON TILTH ORG':'ORGANIC',
        'C-O BY WSDOA ORG':'ORGANIC',
        'C-O ORG':'ORGANIC',
        'CRTFD ORG BY OREGON TILTH ORG':'ORGANIC',
        'MWODC MWOGL MWOMD ORG':'ORGANIC',
        'ORG':'ORGANIC',
        'ORG COBQ':'ORGANIC'
        }


yogurtFormula = {
        'CERT ORG BY ORG CERTIFIERS M/O':'ORGANIC',
        'COBOC M/OC':'ORGANIC',
        'COBQAI':'ORGANIC',
        'COBQAI ORG':'ORGANIC',
        'COBQCS ORG':'ORGANIC',
        'M/ORG SOYMILK':'ORGANIC',
        'NATURALLY MILLED ORG SUGAR':'ORGANIC',
        'ORG':'ORGANIC'
        }


yogurtProduct = {
        'DAIRY SNACK':'DS',
        'NONDAIRY DAIRY SNACK':'ND',
        'NONDAIRY YOGURT':'ND',
        'SKYR':'NA',
        'YOGURT':'YOGURT',
        'YOGURT/ADDITIVE':'YOGURT'
        }


yogurtStyle = {
        'ALL NATURAL GREEK':'GREEK',
        'CUSTARD':'CUSTARD',
        'GREEK':'GREEK',
        'GREEK ORGANIC':'GREEK',
        'ORGANIC':'ORGANIC',
        'ORIGINAL':'REGULAR',
        'PREMIUM':'PREMIUM',
        'REGULAR':'REGULAR',
        'SWISS':'SWISS'
        }


yogurtType = {
        'FAT FREE':'FF',
        'FAT FREE NATURAL':'FF',
        'LACTOSE FREE':'LCF',
        'LIGHT':'LF',
        'LIGHT FAT FREE':'FF',
        'LIGHT LOW-FAT':'LF',
        'LIGHT NON-FAT':'FF',
        'LITE NON-FAT':'FF',
        'LOW FAT':'LF',
        'LOW-FAT':'LF',
        'LOW-FAT LACTOSE FREE':'LFLF',
        'LOW-FAT NATURAL':'LF',
        'NATURAL':'',
        'NONFAT':'FF',
        'NON-FAT':'FF',
        'NON-FAT NATURAL':'FF',
        'NON-FAT SKIM':'FF',
        'REGULAR':'REG',
        'SKIM':'FF',
        'WHOLE VITAMIN D':'WHOLE'
        }
