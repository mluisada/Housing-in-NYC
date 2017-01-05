# Housing prices in NYC and their relation with crime.

The city of New York faces several issues, among which are high housing prices and a high crime rate. 

This project aims at visualizing rental prices for each borough and neighborhood in NYC and compare them to each other. 
In addition, it provides a nice way of visualizing prices, the volume of appartments and the number of crimes for all neighborhoods.

The data has been extracted from 3 sources :
- Airbnb's data in January 2015 : http://data.beta.nyc/dataset/inside-airbnb-data 
- New York Police Department data in 2014 : http://data.beta.nyc/dataset/compstat/resource/21a30a06-01a4-4339-9469-1588779f57c2
- Department of Health, zipcodes and neighborhoods (web-scraping) : https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm

Here are the steps we followed :

![alt tag](https://github.com/mluisada/Housing-in-NYC/blob/master/Workflow.png)

- Downloading the first 2 datasets and webscraping the 3rd one.
- Cleaning the data, formatting some variables and adding new columns.
- Data exploration, building graphs (using seaborn and matplotlib)
- Map of NYC using Bokeh
- Building a "search engine" where the user is asked for what type of information she is looking for. The output is a summary of the housing and crime situations in NYC (per borough or neighborhood).
