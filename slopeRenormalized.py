import pandas as pd
import numpy as np
from nltk.stem.snowball import SnowballStemmer
import xlwt
from heapq import *
import matplotlib.pyplot as plt
import time
import pickle


from EMrenormalized import *
from cleaningData import *

def serialize(object,fichier):
    pickle.dump(object, file(fichier,'w'))

def deserialize(fichier):
    return pickle.load(file(fichier))


B = 300
thresholdConvergence = 1
epsilonForInitialization = .01


df = pd.read_csv("NIPS_1987-2015.csv", sep=',', index_col = 0)
dfTranspose = df.transpose()
#print(dfTranspose)

data = extractSubDictionaryBasedOnProportions(dfTranspose, B)
n = float(data.sum().sum())
print(n)

indexes = nullArticlesIndexes(data)
data.drop(data.index[indexes], inplace = True)
dataClean = data.values


dateActuelle = time.localtime()
dateActuelle = time.strftime("%d %b %Y %H-%M-%S", dateActuelle)


style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')
style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

wb = xlwt.Workbook()
ws = wb.add_sheet('EM on multinomials')

ws.write(0, 0, "model")
ws.write(0, 1, "pen shape")
ws.write(0, 2, "model complexity")
ws.write(0, 3, "contrast")

logKClusters = []
modelNumber = 1
KClusters = []

for k in range(1,200,5):


    print ("NEW NUMBER OF CLUSTERS : " ,k)
    P,Pi,Rpost,logScore,logScores = expectationMaximisation2(dataClean, k, len(data), B, thresholdConvergence,epsilonForInitialization, 200)
    K, P, Pi, Rpost,logScore,logScores = readjustEM(dataClean, len(data), B, P, Pi,Rpost, logScore, logScores, thresholdConvergence, epsilonForInitialization, 200)

    dicToPickle = {}
    dicToPickle['K'] = K
    dicToPickle['P'] = P
    dicToPickle['Pi'] = Pi
    dicToPickle['logScore'] = logScore

    serialize(dicToPickle,"parametersWith" + str(K) + "Clusters" + str(k) + ".pickle")

    
    

    #ws.write(modelNumber, 0, "K = " + str(K))
    #ws.write(modelNumber, 1, K*B -1 )
    #ws.write(modelNumber, 2, K*B -1 )
    #if len(logKClusters) == 0: 
    #    ws.write(modelNumber, 3, - logScore)
    #else:
    #    if K > KClusters[len(KClusters) - 1]:
    #        ws.write(modelNumber, 3, - max(logScore, max(logKClusters)))
    #    else:
    #        ws.write(modelNumber, 3, - logScore)
    logKClusters.append(logScore)
    KClusters.append(K)


KClustersSorted = sorted(KClusters)


for i in range(len(KClustersSorted)):
    ws.write(modelNumber, 0, "K = " + str(KClustersSorted[i]))
    ws.write(modelNumber, 1, KClustersSorted[i]*B -1 )
    ws.write(modelNumber, 2, KClustersSorted[i]*B -1 )
    if i == 0:
        ws.write(modelNumber, 3, - logKClusters[i])
    else:
        ws.write(modelNumber, 3, - max(logKClusters[i], max(logKClusters[0:i])) )

    wb.save('Slope 3 Adjusted - Model Selection via CAPUSHE - ' + dateActuelle + '.xls')

    modelNumber +=1


