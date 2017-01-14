import os
from bs4 import BeautifulSoup as bs
import requests

mimic2wb = "https://www.physionet.org/physiobank/database/mimic2wdb/"
intermediate_levels = ['%s/' % i for i in range(31, 40)]

def getMimicFiles(html, levels):

    rec_files = dict()

    for lvl in levels:
        lvl_link = html+lvl
        soup = bs(requests.get(lvl_link).text, "lxml")
        records = [a['href'] for a in soup.find_all('a') if a['href'].startswith(lvl.split('/')[0])]

        print records[0], records[-1]


        for rec in records:
            rec_link = lvl_link+rec
            soup = bs(requests.get(rec_link).text, "lxml")
            files = [a['href'] for a in soup.find_all('a') if a['href'].startswith(lvl.split('/')[0])]

            rec_files[rec.split('/')[0]] = files

    return rec_files

import pickle
def saveMimicStructure(dict, name):
    with open(name+'.pkl', 'wb') as f:
        pickle.dump(dict, f, pickle.HIGHEST_PROTOCOL)

for i in intermediate_levels:
    files = getMimicFiles(mimic2wb, intermediate_levels)
    saveMimicStructure(files, i.split('/')[0])

print 'ok'

