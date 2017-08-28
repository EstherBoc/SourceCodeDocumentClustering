import pandas as pd
import numpy as np
from nltk.stem.snowball import SnowballStemmer
import xlwt
from heapq import *
import matplotlib.pyplot as plt
import csv

from EM import *


def extractsMostFrequentWords(dfTranspose, B):
    wordOccurrences =  dfTranspose.sum(0)
    wordOccurrences = wordOccurrences.nlargest(B)
    usedWords = list(wordOccurrences.index.values)
    data = dfTranspose.ix[:, usedWords]
    return data

def nullArticlesIndexes(Df):
    indexes = []  
    for i in range(len(Df)):
        #print sum(Df.ix[i,])
        if sum(Df.ix[i,]) == 0:
            #print "Null row"
            print (i)
            indexes.append(i)
    return indexes

def perc(row):
    lenDoc = sum(row)
    #print lenDoc
    if lenDoc == 0:
        print ("Warning: this document is inexistant")
    return [(u + (1/n))/ (float(lenDoc)+  B/n) for u in row]

B = 300
K = 30
thresholdConvergence = 1
epsilonForInitialization = .01
deltaInit = 0

df = pd.read_csv("NIPS_1987-2015.csv", sep=',', index_col = 0)
dfTranspose = df.transpose()
data = extractsMostFrequentWords(dfTranspose, B)
n = float(data.sum().sum())
indexes = nullArticlesIndexes(data)
data.drop(data.index[indexes], inplace = True)

csvfile = "initializationsLikelihoodShortRuns.csv"    
shortRuns = shortRunsEM(data.values, K, len(data), B, thresholdConvergence, epsilonForInitialization,  maxShortRunIterations = 15, numberOfRuns =500)

#Assuming res is a flat list
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(shortRuns[3])