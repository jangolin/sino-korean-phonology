'''
Created on 2022. 3. 6.

@author: 82108
'''

import os 
import pandas as pd
import json
import hanja

import requests
from bs4 import BeautifulSoup

import ndic

data_in = pd.read_excel('korean501.xlsx')

eng = []
for i in data_in.index:
    print(i, data_in['kor'][i])
    p = ndic.search(data_in['kor'][i])
    q = ndic.search(data_in['kor'][i], 2)
    r = {'eng' : " | [2] ".join([p, q])}
    print(i, r)
    eng.append(r)
eng = pd.DataFrame(eng)

data_out = pd.concat([data_in, eng], axis=1)
print(data_out)

data_out.to_csv('korean501_out.csv')
