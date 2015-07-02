# -*- coding: utf-8 -*-
from function import data_path
import csv
import random
import math
import operator

class KNN(object):

    def load_data(self, training, test, split):

        with open(data_path(), 'rb') as csvfile:
            lines = csv.reader(csvfile)
            dataset = list(lines)
            for x in range(len(dataset)-1):
                for y in range(4):
                    dataset[x][y] = float(dataset[x][y])

                if random.random() < split:
                    training.append(dataset[x])
                else:
                    test.append(dataset[x])


    def euclidean_distance(self, instance1, instance2, length):
        distance = 0
        for x in range(length):
            distance += pow((instance1[x] - instance2[x]), 2)
        
        return math.sqrt(distance)

    def neighbors(self, trainingSet, testInstance, k):
        distances = []
        length = len(testInstance)-1
        for x in range(len(trainingSet)):
            dist = self.euclidean_distance(testInstance, trainingSet[x], length)
            distances.append((trainingSet[x], dist))
        
        distances.sort(key=operator.itemgetter(1))	
        neighbors = []
        for x in range(k):
            neighbors.append(distances[x][0])

        return neighbors

    def response(self, neighbors):
        classVotes = {}
        for x in range(len(neighbors)):
            response = neighbors[x][-1]
            if response in classVotes:
                classVotes[response] += 1
            else:
			classVotes[response] = 1
       
        sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sortedVotes[0][0]
 
    def accuracy(self, testSet, predictions):
        correct = 0
        for x in range(len(testSet)):
            if testSet[x][-1] == predictions[x]:
			correct += 1
   
        return (correct/float(len(testSet))) * 100.0 
 
    def run(self, k = 3, split = 0.6):

        training_set = []
        test_set = []

        self.load_data(training_set, test_set, split)

        knn=[]

        print 'Classificação: '
        for x in range(len(test_set)):

            neighbors = self.neighbors(training_set, test_set[x], k)
            result = self.response(neighbors)

            knn.append(result)
            
            
            test = test_set[x][-1];
            print('[Classificado=' + str(result) + ', Classe=' + test + ']')

        accuracy = self.accuracy(test_set, knn)
        print '\n\n'
        print 'Total imagens para treinamento: ' + str(len(training_set))
        print 'Total imagens para teste: ' + str(len(test_set))
        print 'Taxa de Acerto: ' + "{:.2f}".format(accuracy) + '%'
             

# Run Code
if __name__ == '__main__':
    KNN().run(k=3, split=0.7)