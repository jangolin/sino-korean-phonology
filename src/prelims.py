'''
Created on 2022. 2. 18.

@author: Joshua M Zhang

Basic Hanja dataset obtained from project 'hanja-graph' by Pablo Estrada
Hanja characters scraped from Naver. 
https://github.com/pabloem/hanja-graph/
'''

import os 
import pandas as pd
import json

h = open('data/basic_hanjas.json')
hbasic = pd.DataFrame({'hanja': json.load(h)})

h.close()

'''
Code to pull hangul, pinyin, romanization etc. to synthesize into data frame below

1. Hangul data generated using 'hanja' package by Sumin Byeon (https://pypi.org/project/hanja/)
2. Romanization data from 'hangul-romanize' package by Jeong Yun Won (https://pypi.org/project/hangul-romanize/)
3. Pinyin data generated using 'pinyin' package by Lxyu (https://pypi.org/project/pinyin/)
4. Jyutping data generated using 'jyutping' package by Ivor Zhou (https://pypi.org/project/jyutping/)

Turn these into functions later and just make this whole thing a package to use in future analsyes??? :0
'''

import pinyin
import jyutping
import hanja
import hangul_romanize

mando = []
for i in hbasic.index:
    p = {'pinyin' : pinyin.get(hbasic['hanja'][i], format="numerical")}
    mando.append(p)
mando = pd.DataFrame(mando)

canto = []
for i in hbasic.index:
    p = jyutping.get(hbasic['hanja'][i])
    canto.append(p)
canto = pd.DataFrame(canto, columns=['canto'])

hangul = []
for i in hbasic.index:
    p = {'hangul' : hanja.translate(hbasic['hanja'][i], 'substitution')}
    hangul.append(p)
hangul = pd.DataFrame(hangul)

from hangul_romanize import Transliter
from hangul_romanize.rule import academic
transliter = Transliter(academic)

rom = []
for i in hangul.index:
    p = {'rom' : transliter.translit(hangul['hangul'][i])}
    rom.append(p)
rom = pd.DataFrame(rom)

'''
Compile the whole data frame
'''

df = pd.concat([hbasic, hangul, rom, mando, canto], axis=1)
print(df)
import openpyxl
df.to_excel('data/df_raw.xlsx')
df.to_json('data/df_raw.json', orient="index")

df1 = pd.concat([hbasic, hangul, rom, mando], axis=1)
df1.to_excel('data/df_mando.xlsx')
df1.to_json('data/df_mando.json', orient="index")
