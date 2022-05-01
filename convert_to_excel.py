#!/bin/phython3
#
# (c) 2022, Deich Geist
#


from itertools import count
import pandas as pd
import json

jsonfilename  = 'register.json'
excelfilename = 'register.xlsx'

register = ['Geburten', 'Trauungen', 'Sterberegister']
statcols = ['Standesamt','Register','Anzahl']

print(' 1.0 Loading JSON Data from file: ', jsonfilename)
with open(jsonfilename, encoding='utf-8') as json_file:
    json_data = json.load(json_file)
    json_file.close

xlswriter = pd.ExcelWriter(excelfilename, engine='xlsxwriter', options={'strings_to_urls': False})
totalstat = pd.DataFrame( columns=register  )
totalstat.index.name = 'Standesamt'

for register in json_data :
    allPersones = list()
    typ = register['type']
    print("Typ:", typ )
    for page in register['pages'] :
        for famname in page['names'] :
            for p in famname['persons'] :
                p['FamilienName']    = famname['name']
                allPersones.append(p)
    reg = pd.DataFrame(allPersones)
    reg['Vorname']  = reg.apply(lambda x: x['name'].replace( str(x['FamilienName']), ''), axis=1)
    reg['Register'] = typ
    reg.to_excel(xlswriter, sheet_name=typ, index=False, encoding="utf-8")
    print(reg)
    # Make a simple statistics about number of records per Standesamt:
    stat = reg.groupby(['sta']).count()
    stat.index.name = 'Standesamt'
    #print(stat)
    totalstat[typ] = stat['Register']

print(totalstat)
totalstat.to_excel(xlswriter, sheet_name='Standesämter', encoding='utf-8')
xlswriter.save()
