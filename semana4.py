# -*- coding: utf-8 -*-
"""Semana4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nniwdlNOqYXqO-K8OF9OAqtNhVrlBw8v

<h1 align=center><font size = 6>Segmenting and Clustering</font></h1>

<h1 align=center><font size = 12>Neighborhoods in Toronto</font></h1>

# Peer-graded Assignment: Github_Segmenting and Clustering Neighborhoods in Toronto_Linda

#### In addion to the github repository with the full notebook, data set and html outputs of the maps, zipped: 


#### Here’s a link to the full notebook on Watson: 



# Table of Contents

Question 1: 

1.1. Notebook book created

1.2. Web page scraped

1.3. Data transformed into pandas dataframe 

#### 1.4. Dataframe cleaned and notebook annotate

## 1.5. Q1_notebook on Github repository. (10 marks)


Question 2: 

2.1. Used the Geocoder Package to get the coordinates of a few neighborhoods

#### 2.2. Used the csv file to create the requested dataframe 

## 2.2. Q2_ notebook on Github repository. (2 marks)

<h1 align=center><font size = 8>...</font></h1>

## Question 1: 

### 1.1. Notebook book created

with the basic dependencies.
"""

import numpy as np # library to handle data in a vectorized manner
import pandas as pd # library for data analsysis
import requests # Library for web scraping

print('Libraries imported.')

"""### 1.2. Web page scraped

About the Data, Wikipedia page, https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M, 
- is a list of postal codes in Canada where the first letter is M. Postal codes beginning with M are located within the city of Toronto in the province of Ontario. 

- Scraping table from HTML using BeautifulSoup, write a Python program similar to scrape.py,from:

##### Corey Schafer Python Programming Tutorial:
The code from this video can be found at: https://github.com/CoreyMSchafer/code...
"""

# To run this, you can install BeautifulSoup
# https://pypi.python.org/pypi/beautifulsoup4

# Or download the file
# http://beautiful-soup-4
# and unzip it in the same directory as this file
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import csv

print('BeautifulSoup  & csv imported.')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print('SSL certificate errors ignored.')

source = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text

soup = BeautifulSoup(source, 'lxml')

#print(soup.prettify())
print('soup ready')

table = soup.find('table',{'class':'wikitable sortable'})
#table

table_rows = table.find_all('tr')

#table_rows

data = []
for row in table_rows:
    data.append([t.text.strip() for t in row.find_all('td')])

df = pd.DataFrame(data, columns=['PostalCode', 'Borough', 'Neighbourhood'])
df = df[~df['PostalCode'].isnull()]  # to filter out bad rows

#print(df.head(5))
#print('***')
#print(df.tail(5))

"""### 1.3. Data transformed into pandas dataframe 

"""

df.info()

df.shape

"""### 1.4. Dataframe cleaned and notebook annotate

Only process the cells that have an assigned borough, we can ignore cells with 'Not assigned' boroughs, like in rows 1 & 2.
"""

import pandas
import requests
from bs4 import BeautifulSoup
website_text = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text
soup = BeautifulSoup(website_text,'lxml')

table = soup.find('table',{'class':'wikitable sortable'})
table_rows = table.find_all('tr')

data = []
for row in table_rows:
    data.append([t.text.strip() for t in row.find_all('td')])

df = pandas.DataFrame(data, columns=['PostalCode', 'Borough', 'Neighbourhood'])
df = df[~df['PostalCode'].isnull()]  # to filter out bad rows

#df.head(15)

df.drop(df[df['Borough']=="Not assigned"].index,axis=0, inplace=True)
#df.head()

"""The dataframe can be reindex as follows:"""

df1 = df.reset_index()
#df1.head()

df1.info()

df1.shape

"""More than one neighborhood can exist in one postal code area, M5A is listed twice and has two neighborhoods Harbourfront and Regent Park. These two rows will be combined into one row with the neighborhoods separated with a comma using groupby, see: 

https://pandas-docs.github.io/pandas-docs-travis/user_guide/groupby.html

"""

df2= df1.groupby('PostalCode').agg(lambda x: ','.join(x))

#df2.head()

df2.info()

df2.shape

"""There are also cells that have an assigned neighbouhoods,like M7A, lets assign their boroughs as their neighbourhood, as follows:"""

df2.loc[df2['Neighbourhood']=="Not assigned",'Neighbourhood']=df2.loc[df2['Neighbourhood']=="Not assigned",'Borough']

#df2.head()

df3 = df2.reset_index()
#df3.head()

"""Now we can remove the duplicate boroughts as follows:"""

df3['Borough']= df3['Borough'].str.replace('nan|[{}\s]','').str.split(',').apply(set).str.join(',').str.strip(',').str.replace(",{2,}",",")

df3.head()

df3.info()

df3.shape

"""## 1.5. Q1_notebook on Github repository. (10 marks)

# Question 2: 

## 2.1. Used the Geocoder Package to get the coordinates of a few neighborhoods
"""

pip install geopy

from  geopy.geocoders import Nominatim
geolocator = Nominatim()
city ="London"
country ="Uk"
loc = geolocator.geocode(city+','+ country)
print("latitude is :-" ,loc.latitude,"\nlongtitude is:-" ,loc.longitude)

from  geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode("Toronto, North York, Parkwoods")

print(location.address)
print('')
print((location.latitude, location.longitude))
print('')
print(location.raw)

import pandas as pd
#df3.head()

import pandas as pd
df_geopy = pd.DataFrame({'PostalCode': ['M3A', 'M4A', 'M5A'],
                         'Borough': ['North York', 'North York', 'Downtown Toronto'],
                         'Neighbourhood': ['Parkwoods', 'Victoria Village', 'Harbourfront'],})

from geopy.geocoders import Nominatim
geolocator = Nominatim()

df_geopy1 = df3
#df_geopy1

from geopy.geocoders import Nominatim
geolocator = Nominatim()

df_geopy1['address'] = df3[['PostalCode', 'Borough', 'Neighbourhood']].apply(lambda x: ', '.join(x), axis=1 )
df_geopy1.head()

df_geopy1 = df3

df_geopy1.shape

df_geopy1.info()

df_geopy1.drop(df_geopy1[df_geopy1['Borough']=="Notassigned"].index,axis=0, inplace=True)
#df_geopy1
# code holds true up until i=102
df_geopy1.info()

#df_geopy1.head()

df_geopy1.shape

df_geopy1.to_csv('geopy1.csv')
# no data for location after row 75

"""Now let's test for location = 'M1G, Scarborough, Woburn'"""

from  geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode("M1G, Scarborough, Woburn")


#print(location.address)

#print((location.latitude, location.longitude))

#print(location.raw)

pip install geocoder

"""
 ####  Bonus _ Used Geopy & OpenStreetMap to create Dataframe
"""

df3.to_csv('geopy.csv')

import csv

with open('geopy.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     #for row in reader:
         #print(row['PostalCode'],row['Borough'], row['Neighbourhood'] )

from  geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode("M1B Scarborough Rouge,Malvern")

#print(location.address)

#print((location.latitude, location.longitude))

#print(location.raw)

from  geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode("Toronto, Highland Creek")

#print(location.address)

#print((location.latitude, location.longitude))

#print(location.raw)

#M1C Scarborough Highland Creek,Rouge Hill,Port Union = no address

from  geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode("Toronto, Morningside")

#print(location.address)

#print((location.latitude, location.longitude))

#print(location.raw)

#M1E Scarborough Guildwood,Morningside,West Hill = no address

"""#### Bonus how to create csv file. """

# The code was removed by Watson Studio for sharing.

# The code was removed by Watson Studio for sharing.

# The code was removed by Watson Studio for sharing.

"""
##  Retrieved coordinates with with lambda equation
"""

import pandas, os
#os.listdir()

df_geopy=df3
#df_geopy.head()

import geopy
#dir(geopy)

type(df_geopy)

df_geopy.info()

"""### Import GeoPy:"""

pip install geopy

from geopy.geocoders import Nominatim
print('Nominatim imported')

"""### Set connection to OpenStreeMap """

df_geopy['address']=df_geopy['PostalCode'] + ',' + df_geopy['Borough'] + ','+ df_geopy['Neighbourhood']
df_geopy.head()

nom = Nominatim()

n=nom.geocode('M1B, Scarborough, Rouge,Malvern')
n

n.latitude

type(n)

"""#### Watch out for None values"""

n2=nom.geocode('M1E Scarborough Guildwood,Morningside,West Hill')
print(n2)

"""### Use 'address' to get geocode coordinates:

Geocoding (Latitude/Longitude Lookup) Required parameters in a geocoding request: address — The street address that you want to geocode, in the format used by the national postal service of the country concerned. Additional address elements such as business names and unit, suite or floor numbers should be avoided.
"""

df_geopy['Coordinates'] =df_geopy['address'].apply(nom.geocode)
df_geopy.head()

"""### A few location objects created at 'Coordinates' 

"""

df_geopy.info()

df_geopy.Coordinates[0]

print(df_geopy.Coordinates[1])

df_geopy['latitude']=df_geopy['Coordinates'].apply(lambda x: x.latitude if x !=None else None)
df_geopy['longitude']=df_geopy['Coordinates'].apply(lambda x: x.longitude if x !=None else None)
df_geopy.head()

df_geopy.to_csv('geo_loc_py.csv')

"""#### As just 5 addresses were fruitful, we will go on to use the given geo-location csv."""

print('The latitude of', df_geopy.address[0],  'is', df_geopy.latitude[0], 'and its longitude is',df_geopy.longitude[0])

"""# 2.2. Used the csv file to create the requested dataframe """

# Load the Pandas libraries with alias 'pd' 
import pandas as pd 
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
data2 = pd.read_csv("geopy.csv") 
# Preview the first 5 lines of the loaded data 
data2.head()

data3 = pd.read_csv("Geospatial_Coordinates.csv") 
# Preview the first 5 lines of the loaded data 
data3.head()

"""- Rename 'Postal Code'"""

data3.rename(columns={'Postal Code': 'PostalCode'}, inplace=True)
#data3.head()

data1 = pd.merge(data3, data2, how='inner', on=None, left_on=None, right_on=None,
         left_index=False, right_index=False, sort=True,
         suffixes=('_x', '_y'), copy=True, indicator=False,
         validate=None)

data1.head()

data1.info()

"""- Rearrange columns and drop foreign key:"""

cols = data1.columns.tolist()
cols

new_column_order = ['PostalCode',
 'Borough',
 'Neighbourhood',
 'Latitude',
 'Longitude']
new_column_order

data1 = data1[new_column_order]
#data1.head()

"""- Sort dataframe to match example:"""

sorted_df = data1.sort_values([ 'Neighbourhood', 'Latitude'], ascending=[True, True])
#sorted_df.head()
# no idea how to get it exacly like the exqample :(

sorted_df.reset_index(inplace=True)
#sorted_df.head()

sorted_cols =sorted_df.columns.tolist()
#sorted_cols

new_column_order2 = ['PostalCode',
 'Borough',
 'Neighbourhood',
 'Latitude',
 'Longitude']
new_column_order2

sorted_dataframe = sorted_df[new_column_order]
sorted_dataframe.head()

"""## 2.6. Submit a link to your Notebook on your Github repository. (2 marks)"""

sorted_dataframe.to_csv('sorted_geoloc.csv')

"""This notebook is an assignment for a course on **Coursera** called *Applied Data Science Capstone*, you can take this course online by clicking [here](http://cocl.us/DP0701EN_Coursera_Week3_LAB2)."""