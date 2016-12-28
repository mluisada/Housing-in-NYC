### Python project about housing in NYC ###

## Data comes from http://data.beta.nyc/dataset/inside-airbnb-data


### IMPORT LIBRARIES ###

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import re
import math

%matplotlib inline


### IMPORT DATA ###
data0 = pd.read_csv('listings.csv')


# list of all variables
data0.columns.values

nrow = len(data0.index)

data = data0[['name', 'neighbourhood_cleansed', 'city', 'zipcode', 'latitude', 'longitude', 'is_location_exact',
          'property_type', 'room_type', 'accommodates','bathrooms', 'bedrooms', 'beds', 'square_feet', 'price',
           'weekly_price', 'monthly_price', 'review_scores_value']]



#####################
### CLEANING DATA ###
#####################


day_price = []
for i in range(nrow):
    # remove commas ans $ sign, convert into float
    day_price.append((float(data.price[i].replace(',','')[1:])))

    
# there are null values for weekly / monthly prices
# use daily price to fill missing values

week_price, month_price = [], []    
for i in range(nrow):
    if pd.isnull(data.weekly_price[i]) == True :
        week_price.append(7*day_price[i])
    else :
        week_price.append(float(data.weekly_price[i].replace(',','')[1:]))
        
for i in range(nrow):
    if pd.isnull(data.monthly_price[i]) == True :
        month_price.append(30*day_price[i])
    else :
        month_price.append(float(data.monthly_price[i].replace(',','')[1:]))

# delete and add columns
data = data.drop(['price', 'weekly_price', 'monthly_price'], axis = 1)
data['day_price'] = day_price
data['week_price'] = week_price
data['month_price'] = month_price


## New variable : monthly price per square foot
price_sqft = []
for i in range(nrow):
    if pd.isnull(data.square_feet[i]) == False and data.square_feet[i] != 0:
        price_sqft.append(round(data.month_price[i]/data.square_feet[i], 2))
    else :
        price_sqft.append(None)

# add column
data['price_sqft'] = price_sqft


### AGGREGATE NEIBOURHOODS
len(set(data.neighbourhood_cleansed)) 
# 186 different values with duplicates sometimes


#There are too many different names of neighborhoods. 
#Sometimes, two names represent the same district. We rename them using the zipcodes. 
#This website gives the correspondence between zipcodes, districts and neighborhoods. 
#https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm


#We verify that there are not many missing values in the zipcode column less than 1%

# list of indices where zipcode is missing
non_missing_zip = [ind for ind in range(nrow) if pd.isnull(data.zipcode)[ind] == False] 
# get the proportion
len(non_missing_zip)/nrow 
# returns 0.994

data = data.ix[non_missing_zip,]
# reset indices
data = data.reset_index()


# update new number rows
nrow = len(data.index)



## CHANGE CITY COLUMN

manhattan_zip = ['10026' , '10027' , '10030' , '10037' , '10039' , 
                 '10001' , '10011' , '10018' , '10019' , '10020' , '10036' , 
                 '10029' , '10035' , 
                 '10010' , '10016' , '10017' , '10022' , 
                 '10012' , '10013' , '10014' , 
                 '10004' , '10005' , '10006' , '10007' , '10038' , '10280' , 
                 '10002' , '10003' , '10009' , 
                 '10021' , '10028' , '10044' , '10065' , '10075' , '10128' , 
                 '10023' , '10024' , '10025' , 
                 '10031' , '10032' , '10033' , '10034' , '10040']


brooklyn_zip = ['11212','11213','11216','11233','11238',
                '11209','11214','11228',
                '11204','11218','11219','11230',
                '11234','11236','11239',
                '11223','11224','11229','11235',
                '11201','11205','11215','11217','11231',
                '11203','11210','11225','11226',
                '11207','11208',
                '11211','11222',
                '11220','11232',
                '11206','11221','11237']

# DO THE SAME FOR QUEENS, BRONX
borough = []

for i in range(nrow):
    if data.zipcode[i] in manhattan_zip :
        borough.append("Manhattan")
    elif data.zipcode[i] in brooklyn_zip :
        borough.append("Brooklyn")
    else :
        borough.append("Other")


district = []

for i in range(nrow):
    # Manhattan
    if data.zipcode[i] in ['10026' , '10027' , '10030' , '10037' , '10039']:
        district.append('Central Harlem')
    elif data.zipcode[i] in ['10001' , '10011' , '10018' , '10019' , '10020' , '10036']:
        district.append('Chelsea and Clinton')
    elif data.zipcode[i] in ['10029' , '10035']:
        district.append('East Harlem')
    elif data.zipcode[i] in ['10010' , '10016' , '10017' , '10022'] :
        district.append('Gramercy Park and Murray Hill')
    elif data.zipcode[i] in ['10012' , '10013' , '10014'] :
        district.append('Greenwich Village and Soho')
    elif data.zipcode[i] in ['10004' , '10005' , '10006' , '10007' , '10038' , '10280'] :
        district.append('Lower Manhattan')
    elif data.zipcode[i] in ['10002' , '10003' , '10009'] :
        district.append('Lower East Side')
    elif data.zipcode[i] in ['10021' , '10028' , '10044' , '10065' , '10075' , '10128'] :
        district.append('Upper East Side')
    elif data.zipcode[i] in ['10023' , '10024' , '10025'] :
        district.append('Upper West Side')
    elif data.zipcode[i] in ['10031' , '10032' , '10033' , '10034' , '10040'] :
        district.append('Inwood and Washington Heights')
    
    # Brooklyn, etc
    else :
        district.append('Other')
     
data = data.drop(['city', 'neighbourhood_cleansed'], axis = 1)
data['district'] = district
data['borough'] = borough


## AT THE MOMENT LET'S WORK ON MANHATTAN ONLY, TOO MANY NEIGHBOURHOODS
df = data.ix[[ind for ind in range(nrow) if data.zipcode[ind] in manhattan_zip],]
df = df.reset_index()

df = df.drop(['level_0','index'], axis = 1)



########################
### DATA EXPLORATION ###
########################

## Continous, categorical variables and coordinates
loc_var = ['latitude', 'longitude']
# categorical variables
categ_var = ['name', 'district', 'borough', 'zipcode', 'is_location_exact', 'property_type', 'room_type']
# continuous 
cont_var = [x for x in df.columns.values if x not in categ_var + loc_var]


## Summary on continuous variables
df[cont_var].describe()


## Price per day : global analysis
fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize = (10,5))
fig.subplots_adjust(wspace= 0.5)
# to adjust whitespace between subplots : plt.subplots_adjust(wspace=0.01,hspace=0.01)

# rectangular box plot
bplot1 = axes[0].boxplot(df.day_price, 0, 'b+', patch_artist = True)
# notch shape box plot (notch = 1)
bplot2 = axes[1].boxplot(df.day_price, 1, '',  patch_artist = True)

# adding horizontal grid lines
axes[0].set_xlabel('With outliers')
axes[1].set_xlabel('Without outliers')
for ax in axes:
    ax.set_ylabel('Price per day ($)')

# add x-tick labels
plt.setp(axes, xticks=[1], xticklabels=['price'])

plt.show()



## Price per district
### Example : daily price in Midtown versus Harlem versus Greenwich Village

df_UpperEast = df.ix[[ind for ind in list(df.index) if df.district[ind] == 'Upper East Side'],]
df_EastHarlem = df.ix[[ind for ind in list(df.index) if df.district[ind] == 'East Harlem'],]
df_Greenwich = df.ix[[ind for ind in list(df.index) if df.district[ind] == 'Greenwich Village and Soho'],]


fig, axes = plt.subplots(figsize=(10, 6))
all_data = [df_UpperEast.day_price, df_EastHarlem.day_price, df_Greenwich.day_price]
bplot = plt.boxplot(all_data, 0, '', # to remove outliers
                        vert=True,   # vertical box aligmnent
                        patch_artist=True)   # fill with color
# to display outliers : write instead : 'bD' (blue dots) or 'rD' (red dots) etc.


# fill with colors
colors = ['pink', 'lightblue', 'lightgreen']
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)


# adding horizontal grid lines
#for ax in axes:
    #ax.yaxis.grid(True)
    #ax.set_xticks([y+1 for y in range(len(all_data))], )
axes.set_xlabel('Districts')
axes.set_ylabel('Price per day ($)')

    
# add x-tick labels
plt.setp(axes, xticks=[y+1 for y in range(len(all_data))],
         xticklabels=['Upper East', 'East Harlem', 'Greenwich and Soho'])

plt.show()




## Number of appartments per district
import seaborn as sns
sns.set(style="whitegrid", color_codes=True)

fig, axes = plt.subplots(figsize=(18, 10))

sns.countplot(x="district", data=df, palette="Greens_d")

plt.xticks(rotation=40) 

plt.show()




