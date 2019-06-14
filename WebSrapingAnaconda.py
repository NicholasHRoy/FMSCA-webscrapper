# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 13:36:46 2019

@author: Nicholas Roy
"""
#Import Libraries
import urllib.request
from bs4 import BeautifulSoup
import csv

"""

This is the data that is unique to the FMSCA database.
Prior to using this utility, the user should be familiar with the html file for the webpage they are scraping.
    and should adjust the following variables:
        sitelist : Dictionary of sites where data is being extracted from formatted to change for each obs.
        htmlvardict : dictionary of desired extracted html variables
        observations : Serves as a list of observation keys and the text changing in the URL for each observation
"""
#Dictionary of variables defined by a list containing their html element equivalent id and type
htmlvardictMAIN = {
        
        'usdot_num' : ["dot-num-li","li"] ,
        'carrier_name' : ["basicInfo","div"],
        'address' : ["basicInfo","div"],
        'citystatezip' : ["basicInfo","div"],
        'numberofvehicles' : ["basicInfo","div"],
        'numberofdrivers' : ["basicInfo","div"],
        'numberofinspections' : ["basicInfo","div"],
        'safetyratingdate' : ["SafetyRating", "div"],
        'VehicleOOSr' : ["SafetyRating", "div"],
        'DriverOOSr' : ["SafetyRating", "div"],
        'BASICstatusdate' : ["BASICs", "section"],
        'mostrecentinvestigation' : ["SummaryOfActivities", "section"]
        }

htmlvardictSAFETY = {
        'unsafedrivingmeasure' : ["resultData", "div"]
        }   
htmlvardictSERVICE = {
        'hoursofservcomp' : ["resultData", "div"]
        }
htmlvardictMAINTENANCE = {
        'vehiclemaintenancemeasure' : ["resultData", "div"]
        }
#Site(s) to extract data from
sitelist = {'FMSCA_main' : ["https://ai.fmcsa.dot.gov/SMS/Carrier/%s/Overview.aspx?FirstView=True", htmlvardictMAIN],
            'FMSCA_safety' : ["https://ai.fmcsa.dot.gov/SMS/Carrier/%s/BASIC/UnsafeDriving.aspx", htmlvardictSAFETY],
            'FMSCA_service' : ["https://ai.fmcsa.dot.gov/SMS/Carrier/%s/BASIC/HOSCompliance.aspx", htmlvardictSERVICE],
            'FMSCA_maintenance' : ["https://ai.fmcsa.dot.gov/SMS/Carrier/%s/BASIC/VehicleMaint.aspx", htmlvardictMAINTENANCE]
            }

#Observations are the part of the url that will be changing for each observation
observations = [1593023,2545275,1958964,3060243,112044,2209354,716474,135530,213754,54283,1998297,2525629,983878,2594483,850888,369330,511412,149350,208073,185183,2534602,548880,21800,51518,2834333,2630581,2410313,1346846,53467,2475054,204935,28406,1077521,548880,2638517,121337,1591600,2581136,1933358,163421,587147,2594483,511412,1942407,843546,2565304,2914147,31706,2872789,80806,1861195,2944219,2270874,2786530,16130,120195,54283,3706,264184,2928169,511412,313891,165206,112044,428823,1848462,273818,121058,53467,2297576,135530,95610,95610,203287,434467,2801282,63585,73705,80806,548880,1252905,73705,1025678,1654367,2556034,1817188,265753,2416013,116195,247936,148817,54283,1896621,464352,79466,1206154,446997,313891,798227,46749,106289,1043105,241594,845505,84383,2989155,261728,264184,1758605,1062707,580685,2817545,182413,216939,375539,2078933,2541239,3021963,2204472,1077521,2351846,1444559,2786530,511412,548617,2450967,1146977,3176369,2826912,1758605,657569,3070574,2992572,2907322,264184,649914,16130,398991,28406,1023517,753551,166046,7276010,1147518,2536779,3201633,500737,3100962,264184,327574,146458,2981225,3100340,2801279,3072276,3171577,241572,1873432,1723326,2443231,156147,154712,3129577,612352,3160088,1638845,2373308,2424211,2938133,3206855,3706,3084193,3032372,96606,3706,2798993,65769,2164657,3327,2931587,3038416,3190876,105234,2554737,204935,2946610,2551995,8444428,511412,1346895,3138093,2458134,1580995,439471,591520,511412,580685]

type2obs = 0
type3obs = 0

"""

Cleaning methods will be a constant work in progress... 

This is a set of functions designed to extract each variable on a case-by-case basis.
Regular expressions would be the best option to make this a more robust and general form, 
    but for small amounts of variables this will suffice.
Less functions would be better.    
    
"""

#My Functions
    #Rinse Function

"""

The rinse function is a reoccuring process that is necessary due to the BeautifulSoup library.
It takes the unclean variable that is currently a list type object, 
    converts it into a string based on the location (stain) of the desired variable in the list,
    and devides the string into a list according to whichever delimiter is necessary.
    
The conversion from a list to a string and back to a list is used throughout the code.

It is used for each entry of each observation because the find all function, 
    from Beautiful soup, 
    extracts elements as a list."
    
Suggestions on a built in Python or Beautiful Soup function that serves the same purpose are welcome.
 
"""

def rinse(dirtyvar, delimiter, stain):
    #Convert 1 item list into string
    scrubbedvar = str(dirtyvar[stain])
    #Split up html lines
    if delimiter != '':
        rinsedvar = scrubbedvar.split(delimiter)
    else:
        rinsedvar = scrubbedvar.split()
    return(rinsedvar)

    #Headerpolish Function

"""

Headers are common html elements that must be extracted so a function to isolate the text within the header is provided

washedheader : is the rinsed and already pre cleaned header as seen in the 'carrier_name' variable that is extracted

"""

def headerpolish(washedheader):
    scrubbedheader = rinse(washedheader,'>',0)
    scrubbedheader = rinse(scrubbedheader,'<',1)
    polishedvar = str(scrubbedheader[0])
    return(polishedvar)

"""

concatenate appends a list of words together, with spaces inbetween each word, into one string .
listofwords : list of words

"""


def concatenate(listofwords):
    concatenation = ""
    for i in listofwords:
        if i != listofwords[-1]:
            concatenation += i + " "
        else:
            concatenation += i
    return concatenation

    #Variable Specific Cleaning Functions!
"""

Each variable will require a different cleaning method. 
Define the cleaning process for each variable in these functions depending on the html file for your data.

The extractelement function calls these functions depending on the variable extracted.
For these functions no docstrings will be provided, but the logic can be derived from looking at the html file.

(This is where regular expressions would be a really great idea to optimize this.)  

"""

def basicinfoclean(varname, dirtyvar):
    cleanervar = rinse(dirtyvar, '\n', 0)
    #print(cleanervar)
    #Pattern Lists
        #For a set of variables that reduces lines of code through list 
    patternvarlist1 = ['citystatezip', 'numberofvehicles', 'numberofdrivers', 'numberofinspections']
    #isolatevalue
    if varname == 'carrier_name':
        cleanestvar = headerpolish(cleanervar[2].split('\n'))
    elif varname == 'address':
        cleanestvar = str(concatenate(rinse(cleanervar,'',17)))
    
    #The pattern of these datapoints seperation demands a for loop
    
    elif varname in patternvarlist1:
        line = 19
        for patternvar in patternvarlist1:
            if patternvar == varname:
                cleanervar = rinse(cleanervar,'',line)
                if patternvar == 'citystatezip':
                    cleanestvar = (concatenate(cleanervar))
                else:    
                    cleanervar = (concatenate(cleanervar)).replace(",","")
                    cleanestvar = int(cleanervar)
            line += 6
        
    return cleanestvar


def basicinfoclean2(varname, dirtyvar):
    cleanervar = rinse(dirtyvar, '\n', 0)
    #print(cleanervar)
    #Pattern Lists
        #For a set of variables that reduces lines of code through list 
    patternvarlist1 = ['citystatezip', 'numberofvehicles', 'numberofdrivers', 'numberofinspections']
    #isolatevalue
    if varname == 'carrier_name':
        cleanestvar = headerpolish(cleanervar[2].split('\n'))
    elif varname == 'address':
        cleanestvar = str(concatenate(rinse(cleanervar,'',22)))
   
    #The pattern of these datapoints seperation demands a for loop
    
    elif varname in patternvarlist1:
        line = 24
        for patternvar in patternvarlist1:
            if patternvar == varname:
                cleanervar = rinse(cleanervar,'',line)
                if patternvar == 'citystatezip':
                    cleanestvar = (concatenate(cleanervar))
                else:    
                    cleanervar = (concatenate(cleanervar)).replace(",","")
                    cleanestvar = int(cleanervar)      
            line += 6
        
    return cleanestvar

def safetyratingclean(varname, dirtyvar):
    patternvarlist2 = ['VehicleOOSr','DriverOOSr']
    if varname == 'safetyratingdate':
        cleanervar = rinse(dirtyvar,'\n', 0)
        cleanestvar = str(rinse(cleanervar,'',3)[-2])
    elif varname in patternvarlist2:
        line = 21
        for patternvar in patternvarlist2:
            if patternvar == varname:
                 cleanervar = rinse(dirtyvar,'\n', 0)
                 cleanervar = rinse(cleanervar,'',line)
                 cleanestvar = float(headerpolish(cleanervar))
            line += 5
    
    return cleanestvar

def safetyratingclean2(varname, dirtyvar):
    patternvarlist2 = ['VehicleOOSr','DriverOOSr']
    line = 25
    for patternvar in patternvarlist2:
        if patternvar == varname:
             cleanervar = rinse(dirtyvar,'\n', 0)
             cleanervar = rinse(cleanervar,'',line)
             cleanestvar = float(headerpolish(cleanervar))
        line += 5
    
    return cleanestvar

def extractelement(varname,elementid,elementtype,elementsite):
    #Request page using urllib request
    Page = urllib.request.urlopen(elementsite)
    #Extract html file using Beautiful Soup
    mainsoup = BeautifulSoup(Page, "lxml")
    mainsoup.prettify
    global type2obs
    global type3obs
    #Extract Data
    #Extract USDOT number from page
    element = mainsoup.find_all(elementtype,id=elementid)
    if varname == 'usdot_num':  
        element = int((rinse(element,'\n', 0)[4]).split('\n')[-1])
    elif varname in ['carrier_name', 'address', 'citystatezip', 'numberofvehicles', 'numberofdrivers', 'numberofinspections'] and type2obs == 0:
        element = basicinfoclean(varname, element)
        if element == '<ul class="no-list">':
            element = mainsoup.find_all(elementtype,id=elementid)
            element = basicinfoclean2(varname,element)
            type2obs = 1
    elif varname in ['carrier_name', 'address', 'citystatezip', 'numberofvehicles', 'numberofdrivers', 'numberofinspections'] and type2obs == 1:
        element = basicinfoclean2(varname,element)
    elif varname in ['safetyratingdate','VehicleOOSr','DriverOOSr'] and type3obs == 1:
        element = safetyratingclean2(varname,element)
    elif varname in ['safetyratingdate','VehicleOOSr','DriverOOSr'] and type3obs == 0:
        try:
            element = safetyratingclean(varname, element)
        except:
            element = mainsoup.find_all(elementtype,id=elementid)
            element = safetyratingclean2(varname,element)
            type3obs = 1
    elif varname in ['unsafedrivingmeasure', 'hoursofservcomp', 'vehiclemaintenancemeasure']:
        element = float(rinse(element,'"',0)[1])
    elif varname == 'BASICstatusdate':
        element = concatenate((rinse(element,'\n',0)[23]).split()[6:9])
    elif varname == 'mostrecentinvestigation':
        element = ((rinse(element, '\n', 0)[11]).split())[0]
    return (varname, element)

"""

Main function that extracts data and exports it into a CSV file
        csvobservation : the output data for the csvobservation

"""

def main():
    data=[]
    global type2obs
    global type3obs
    varlist = ['usdotinput']
    for site in sitelist:
            for var in sitelist[site][1]:
                varlist.append(var)
    data.append(varlist)
    print(data)
    for i in range (0,len(observations)):
        USDOTID=str(observations[i])
        #Initalize CSV line
        csvobservation = [observations[i]]
        #Extract all given variables
        for site in sitelist:
            obswebpage = str(sitelist[site][0]%USDOTID)
            
            #SaveHTML File for data validation
            obshtmlfile = str('M:\DataScraping\HTML Files\June 14th, 2019\%s.html'%USDOTID)
            urllib.request.urlretrieve(obswebpage, obshtmlfile)
            
            for var in sitelist[site][1]:
                #Add variable to observations by extracting from HTMl file
                try:
                    value=extractelement(var,sitelist[site][1][var][0],sitelist[site][1][var][1],obswebpage)
                except:
                    value = [var, 'ERROR']
                csvobservation.append(value[1])
        print(csvobservation)
        data.append(csvobservation)
        type2obs = 0
        type3obs = 0
    with open('FMSCAdata.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data)
    csvFile.close()
    print("Done")
    
main()
