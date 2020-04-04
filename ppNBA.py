import math
import csv 
import sys 
import statistics as stat


def standardize(h,mean,std):
    return (abs(h-mean))/std 

def findDistance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )

def percentError(expected, actual):
    errors = 0 
    for i in range(len(expected)):
        if expected[i] != actual[i]:
            errors += 1 
    return((errors,errors/len(actual)))

def predict(trainData,testData,flag):
    output = [] 
    train = [] 
    test = [] 
    for each in trainData: 
        train.append((int(each["Height"]), int(each["Weight"]), each["Position"]))
    for each in testData: 
        test.append((int(each["Height"]), int(each["Weight"])))
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

expected = [] 
actual = [] 
testingData = []
with open("test.csv", newline = "") as testFile: 
    reader = csv.DictReader(testFile)
    for row in reader:
        actual.append(row["Position"]) 
        testingData.append(row)

#Non standardized result
expected = predict(trainingData,testingData, True)
print("Percent error: ", percentError(expected, actual))