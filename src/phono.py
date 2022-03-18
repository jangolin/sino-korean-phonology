'''
Created on 2022. 2. 19.

@author: Joshua M Zhang

Tone-independent analysis on Basic Hanja dataset, see prelims.py
Incorporate distinctive feature associations
'''

import os
import pandas as pd
import json
from _operator import index
from turtledemo.__main__ import font_sizes
from pickle import TRUE

os.chdir("..")
os.chdir("..")

d = open('data/df_mando.json')
data = pd.DataFrame(json.load(d))
data = data.T

d.close()

'''
Reorganising data for minimalistic effect
'''
pinyin = data['pinyin']

data = data.drop(['hangul'], axis=1)

for i in pinyin.index:
    data.at[i,'pinyin']=pinyin[i].rstrip("12345")

'''
Sort based by hanja with same pinyin
'''
df1 = data.sort_values(by=['pinyin', 'rom'])
print(df1)

edges = pd.concat([df1['pinyin'], df1['rom']], axis=1, ignore_index=False)
edges = edges.rename(columns={'pinyin': 'from', 'rom': 'to'})


edges2 = edges.groupby(edges.columns.tolist(),as_index=False).size()
'''print(edges2)'''


'''make this smaller to try out first'''

'''
edges2.to_excel('data/edges2.xlsx')

import networkx as nx
import matplotlib.pyplot as plt
import math

g = nx.from_pandas_edgelist(edges2, 
                            source='from',
                            target='to',
                            edge_attr='size')

pos = nx.spring_layout(g, k=5/math.sqrt(g.order()))
nx.draw(g, pos,
                 with_labels=True, 
                 node_size=20, 
                 font_size=8)
plt.savefig("path.png")
'''

'''Phoneme references'''



'''Syllabification'''

edges = edges.reset_index(inplace=False)

'''
edges.to_excel('data/edges.xlsx')
'''

import re

def syllabize(data, lang):

    c1 = []
    g1 = []
    v1 = []
    c2 = []
    
    ch_consonant = pd.Series(['b','p','m','f','d','t','n','l','g','k','h','j','q','x','zh','ch','sh','r','z','c','s'])
    ch_glide = pd.Series(['y','w','v'])
    ch_vowel = pd.Series(['i','a','o','e','u','ü','ɯ','ai','ao','ei','ou'])
    ch_final = pd.Series(['n','ng'])
    
    if lang == 'pinyin':
        for i in data.index:
            f = data[i]
            if "v" in f:
                f = f.replace('v','ü')
            else:
                pass
        
            if f.startswith(tuple(ch_consonant))==True:
                if f[1] == 'h':
                    c = f[0:2]
                    if "n" not in f[2:]:
                        v = f[2:]
                    else:
                        if "ng" in f[2:]:
                            v = f[2:-2]
                        else:
                            v = f[2:-1]
                    
                    if (f[2:].startswith('u') == True and len(f) > 3):
                        g = str('w')
                        if f[3] == 'n':
                            v = v.replace('u','e')
                        else:
                            v = v.lstrip('u')
                    else:
                        g = str('∅')
                    
                else:
                    c = f[0]
                    if "ng" in f[1:]:
                        v = f[1:-2]
                    elif "n" in f[1:]:
                        v = f[1:-1]
                    else:
                        v = f[1:]
        
                    if (f.startswith(tuple(['q','j','x'])) == True and f[1] == 'u') or (f.startswith('lü') == True):
                        if f[2:].startswith(tuple(ch_vowel)) == True:
                            g = str('v')
                            v = v.lstrip('uü')
                        else:
                            g = str('∅')
        
                    elif (f[1:].startswith('u') == True and len(f) > 2):
                        v = v.lstrip('u')
                        g = str('w')
                        if f[2] == 'n':
                            v = str('e')
                    elif (f[1:].startswith('i') == True and len(f) > 2 and f[2:].startswith(tuple(ch_vowel)) == True):
                        v = v.lstrip('i')
                        g = str('y')
                    else:
                        g = str('∅')
                        
            else:
                c = str('∅')
                if f.startswith(tuple(ch_glide)) == True:
                    g = f[0]
                    if "ng" in f:
                        v = f[1:-2]
                    elif "n" in f:
                        v = f[1:-1]
                    else:
                        v = f[1:]
                else:
                    g = str('∅')
                    if "n" not in f:
                        v = f
                    else:
                        v = f[:-1]
            
            if "ng" in f[1:]:
                m = str('ŋ')
            elif "n" in f[1:]:
                m = str('n')
            else:
                m = str('∅')
                
            if f.startswith(tuple(['si','ci','chi','shi','zhi'])) == True:
                v = str('ɯ')
            else:
                pass
            c2.append(m)
            v1.append(v)
            g1.append(g)
            c1.append(c)
        
        c1 = pd.Series(c1)
        g1 = pd.Series(g1)
        v1 = pd.Series(v1)
        c2 = pd.Series(c2)
        
        pinyin_syll = pd.concat([c1,g1,v1,c2], axis=1)
        pinyin_syll.columns = ['C1','G','V','C2']
        return pinyin_syll
    
    elif lang == 'hangul':
        print("under development")
    else:
        print("Please enter 'pinyin' or 'hangul'.")

'''
pinyin_syll.to_excel('data/pinyin_syll.xlsx')
'''

output = syllabize(edges['from'], 'pinyin')
print(output)

