#!/bin/python3
#
# (c) 2022, Deich Geist
#
import requests
import json
import time
from   bs4 import BeautifulSoup

baseurl = 'https://die-maus-bremen.info/fileadmin/db_query'

RegisterList = [
    { 
        'type'  : 'Geburten',
        'query' : 'staamtreg_bremen-geb',
        'pages' : list()
    },

#    {
#        'type'  : 'Sterberegister',
#        'query' : 'staamtreg_bremen-sterbef',
#        'pages' : list()
#    },
#    {
#        'type'  : 'Trauunugen',
#        'query' : 'staamtreg_bremen-tr',
#        'pages' : list()
#    }
]

# Prepare a local counter for the number of webpages read: 
request_count = 0
t_start = time.time()


# Function to parse the person details from a geburten name page:
def parse_famname_details_geburten( session, url ) :
    global request_count
    personen = list()
    preq = session.get( url )
    request_count = request_count + 1
    if preq.status_code == 200 :
        phtml = BeautifulSoup( preq.content, 'html.parser')
        ptrs  = phtml.find_all('tr', class_=True)
        for ptr in ptrs :
            ptds  = ptr.find_all('td')
            if len(ptds) >= 4 :
                pname  = ptds[0].text.strip()
                pregnr = ptds[1].text
                pyear  = ptds[2].text
                psta   = ptds[3].text
                xurl   = ptds[0].select_one('a')['href']
                person = {
                    'name'  : pname,
                    'regnr' : pregnr,
                    'year'  : pyear,
                    'sta'   : psta,
                    'url'   : xurl,
                }
                # Add person to family names:
                personen.append( person )    
    return personen


# 1. Iterate through the 3 different types of registers:
for register in RegisterList :
    url        = baseurl + '/' + register['query'] + '/'
    print( "Start Crawling:", register['type'], url)
    session       = requests.Session()
    session.auth  = ('Maus', 'Maus')
    req           = session.get( url )
    request_count = request_count + 1
    if req.status_code == 200 :
        soup       = BeautifulSoup(req.content, 'html.parser')
        # Read the List of Verweise for alphabetic names as page list:
        verweise = soup.select('.verweis')
        for verweis in verweise :
            page = {
                'id'    : verweis.text,
                'url'   : url + verweis['href'],
                'names' : list()
            }
            # Read the Family Names from this Pages A-Z:
            print("    Crawling Page:", page)
            resp = session.get( page['url'])
            request_count = request_count + 1
            if resp.status_code == 200 :
                nhtml    = BeautifulSoup( resp.content, 'html.parser')
                nametags = nhtml.select('td[width="33%"] > a')
                for ntag in nametags :
                    fnurl   = url + ntag['href']
                    famname = {
                        'name'      : ntag.text,
                        'persons'   : list()
                    }
                    print("        ->", ntag.text)
                    # Now read the persons data for "family name" from the Name-Page:
                    # For the demo it is enough to only scroll all person details with Letter 'A'
                    if page['id'] == 'A' :
                        famname['persons'] = parse_famname_details_geburten( session, fnurl )
                    # Add family name to page
                    page['names'].append(famname)
            # Add Page Data to Register:
            register['pages'].append(page)
    else :
        print("Error reading page:", req)
    # Now we have read this register. 

# Set end time and calculate duration:
t_end   = time.time()
t_delta = t_end - t_start

# Convert Data structure to local json file:
with open("register.json", "w", encoding='utf8') as data_file:
    json.dump(RegisterList, data_file, indent=4, ensure_ascii=False)

# Print statistics:
print( "Webpages read:........", request_count)
print( "Duration:.............", t_delta, '[sec]')
print( "Pages per second:.....", request_count / t_delta)
