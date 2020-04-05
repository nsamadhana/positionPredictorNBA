import math
import csv 
import sys 
import statistics as stat


def standardize(x,mean,std):
    return (abs(x-mean))/std 

def findDistance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )

def percentError(expected, actual):
    errors = 0 
    for i in range(len(expected)):
        if expected[i] != actual[i]:
            errors += 1 
    return((errors,errors/len(actual)))

def predict(trainData, testData, hMean, hSTD, wMean, wSTD, flag):
    output = [] 
    train = [] 
    test = [] 
    for each in trainData:
        if flag:  
            train.append((int(each["Height"]), int(each["Weight"]), each["Position"]))
        else: 
            h = standardize(int(each["Height"]), hMean, hSTD)
            w = standardize(int(each["Weight"]), wMean, wSTD)
            train.append((h, w, each["Position"]))
    for each in testData: 
        if flag:
            test.append((int(each["Height"]), int(each["Weight"])))
        else: 
            h = standardize(int(each["Height"]), hMean, hSTD)
            w = standardize(int(each["Weight"]), wMean, wSTD)
            test.append((h, w))

    for i in test: 
        min = sys.maxsize 
        p1 = i 
        for j in train:
            p2 = (j[0],j[1])
            distance = findDistance(p1,p2)
            if distance <= min:
                min = distance 
                position = j[2]
        output.append(position)
    return output


trainingData = [] #training data 
heights = [] 
weights = []
with open("train.csv", newline = "") as trainFile:
    reader = csv.DictReader(trainFile)
    for row in reader:
        trainingData.append(row)
        heights.append(int(row["Height"]))
        weights.append(int(row["Weight"]))
hMean = stat.mean(heights)
hSTD = stat.stdev(heights)
wMean = stat.mean(weights)
wSTD = stat.stdev(weights)
print(hMean,hSTD,wMean,wSTD)
print("test for height: ", standardize(73,hMean,hSTD))
print("test for weight: ", standardize(180,wMean,wSTD))


actual = [] 
testingData = []
with open("test.csv", newline = "") as testFile: 
    reader = csv.DictReader(testFile)
    for row in reader:
        actual.append(row["Position"]) 
        testingData.append(row)

#Non standardized result
notStandardized = predict(trainingData,testingData, hMean, hSTD, wMean, wSTD, True)
print("Non-standardized: ", percentError(notStandardized, actual))

#Standardized result
standardized = predict(trainingData,testingData, hMean, hSTD, wMean, wSTD, False)
print("Standardized: ", percentError(standardized, actual))