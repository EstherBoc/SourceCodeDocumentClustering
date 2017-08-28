
import random
import numpy as np
import matplotlib.pyplot as plt
from math import *
from scipy.stats import nanmean
from nltk.stem.snowball import SnowballStemmer



def extractsMostFrequentWords(dfTranspose, B):
    '''dfTranspose - transpose of the initial df i.e. columns
    correspond to the dictionary of words and rows correspond to the article labels

    B - the number of bins wanted for the EM. By default, we take the most frequent words.'''
    wordOccurrences =  dfTranspose.sum(0)
    wordOccurrences = wordOccurrences.nlargest(B)
    usedWords = list(wordOccurrences.index.values)
    data = dfTranspose.ix[:, usedWords]
    return data


def extractSubDictionary(dfTranspose, B, R):
    """R : number of most frequent words to retire from data 
    B : once most frequent words cancelled, number of words to consider in the final dictionary 
    dfTranspose : columns = words, rows = articles"""
    wordOccurrences =  dfTranspose.sum(0)
    tooFrequentWords = wordOccurrences.nlargest(R)
    tooFrequentWords = tooFrequentWords.index.values.tolist()
    setWithoutFrequentWords = set(list(dfTranspose)) - set(tooFrequentWords)
    setWithoutFrequentWords = {x for x in setWithoutFrequentWords if x==x}
    dfTransposeWithoutFrequentWords = dfTranspose[list(setWithoutFrequentWords)]
    wordOccurrencesWithoutFrequentWords =  dfTransposeWithoutFrequentWords.sum(0)
    wordOccurrencesWithoutFrequentWords = wordOccurrencesWithoutFrequentWords.nlargest(B)
    usedWords = list(wordOccurrencesWithoutFrequentWords.index.values)
    data = dfTransposeWithoutFrequentWords[usedWords]
    return data


def extractSubDictionaryBasedOnProportions(dfTranspose, B):
    """This method removes most frequent words and most rare words based on the proportion of
    documents in which they appear. If a word appears in less than 10 perc or in more than 80 perc
    of the documents, it is removed from the dictionary. Then the B words that occur most compose the dictionary.

    dfTranspose : columns = words, rows = articles
    B : number of words to consider in the final dictionary"""
    nbDoc = len(dfTranspose)
    dictionary = list(dfTranspose)
    usedWords = []
    for word in dictionary:
        proportion = len(dfTranspose[dfTranspose[word]>0])/float(nbDoc)
        #print (word, proportion)
        if proportion >0.1 and proportion <0.7:
            #print("Good proportion ", word, proportion)
            usedWords.append(word)
    dfTranspose2 = dfTranspose[usedWords]
    wordOccurrences2 =  dfTranspose2.sum(0)
    wordOccurrences2 = wordOccurrences2.nlargest(B)
    finalWords = wordOccurrences2.index.values.tolist()
    return dfTranspose2[finalWords]



def stemWordsFromInitialDictionary(dfTranspose):
    dicDf = dfTranspose.to_dict(orient = 'list')
    stemmer = SnowballStemmer("english")
    stemDf = {}
    for key in dicDf.keys():
        if type(key) == str:
            #print "Key is not nan"
            stemWord = str(stemmer.stem(key))
            #print "Stemmed word! " + stemWord
            if stemWord not in stemDf.keys():
                stemDf[stemWord] = dicDf[key]
            elif stemWord in stemDf.keys():
                #print "Key already in new dictionary"
                #print "Last values in dicDf: " + str(dicDf[key])
                #print "Last values in stemDf: " + str(stemDf[stemWord])
                stemDf[stemWord] = list(np.array(stemDf[stemWord]) + np.array(dicDf[key]) )
                #print "New values in stemDf: " + str(stemDf[stemWord])
    Df = pd.DataFrame.from_dict(stemDf)
    Df.index = dfTranspose.index.tolist()
    dfTranspose = Df
    return dfTranspose


def nullArticlesIndexes(Df):
    indexes = []  
    for i in range(len(Df)):
        #print sum(Df.ix[i,])
        if sum(Df.ix[i,]) == 0:
            #print "Null row"
            print (i)
            indexes.append(i)
    return indexes

def dropVoidArticles(data):
    indexes = nullArticlesIndexes(data)
    data.drop(data.index[indexes], inplace = True)
    return data

def perc(row):
    lenDoc = sum(row)
    #print lenDoc
    if lenDoc == 0:
        print ("Warning: this document is inexistant")
    return [(u + (1/n))/ (float(lenDoc)+  B/n) for u in row]