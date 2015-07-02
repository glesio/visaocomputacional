# -*- coding: utf-8 -*-
from function import image_path
from skimage import io
from matplotlib import pyplot
from skimage import filter
from skimage import measure
import numpy as np
import math

class Curvatura(object):

    def __init__(self, image_name = 'macrophyllum/l04.jpg'):
        self.__img_path = image_path(image_name)   

    def __transform(self):
        # Transformar em escala de cinza para reduzir a dimensionalidade
        self.__img_gray = io.imread(self.__img_path, True) 
        #Aplicar otsu para binarizar a imagem
        self.__img_otsu = filter.threshold_otsu(self.__img_gray) 

        self.__img_gray = self.__img_gray < self.__img_otsu 

        # Procura contornos da imagem binarizada
        self.__contours = measure.find_contours(self.__img_gray, 0.5)

        arclen=0.0
        for n, contour in enumerate(self.__contours):
            arclenTemp=0.0
            for indice, valor in enumerate(contour):
                if indice > 0:
                    d1 = math.fabs(round(valor[0]) - round(contour[indice-1,0]))
                    d2 = math.fabs(round(valor[1]) - round(contour[indice-1,1]))
                    if d1+d2 > 1.0:
                        arclenTemp += math.sqrt(2)
                    elif d1+d2 == 1:
                        arclenTemp+= 1

            if arclenTemp > arclen:
                arclen = arclenTemp
                bestn = n

        #Transforma a lista contours[bestn] em uma matriz aux[n,2]
        aux = np.asarray(self.__contours[bestn])
        #Transforma os valores da matriz em inteiros        
        aux = aux.astype(int)

        vetor = [] #vetor que irá receber as curvaturas k(t)

        # Inverter as posições em relação a fórmula pois o x esta no lugar do y
        for i in range(len(aux)-2):
            b1 = ( (aux[i-2,1]+aux[i+2,1]) + (2*(aux[i-1,1] + aux[i+1,1])) - (6*aux[i,1]) ) / 12
            b2 = ( (aux[i-2,0]+aux[i+2,0]) + (2*(aux[i-1,0] + aux[i+1,0])) - (6*aux[i,0]) ) / 12
            c1 = ( (aux[i+2,1]-aux[i-2,1]) + (4*(aux[i+1,1] - aux[i-1,1])) ) / 12
            c2 = ( (aux[i+2,0]-aux[i-2,0]) + (4*(aux[i+1,0] - aux[i-1,0])) ) / 12
            k = (2*(c1*b1 - c2*b2)) / ((c1**2 + c2**2)**(3/2))

            vetor.append(k) #append: insere objeto no final da lista

        self.__dimensao = np.shape(vetor)
        self.__media = np.mean(vetor)
        self.__bestn = bestn

    def run(self):

        self.__transform()

        pyplot.annotate('Posicao do melhor array: ' + str(self.__bestn), xy=(10, -150), color='black')
        pyplot.annotate('Dimensao do vetor de curvaturas: ' + str(self.__dimensao), xy=(10, -100), color='black')
        pyplot.annotate('Media local: ' + str(self.__media), xy=(10, -50), color='black')
        pyplot.imshow(self.__img_gray, interpolation='nearest', cmap=pyplot.cm.gray)

        for contour in self.__contours:
            pyplot.plot(contour[:, 1], contour[:, 0], linewidth=2)

        pyplot.axis('off')
        pyplot.show()


# Run Code
if __name__ == '__main__':
    Curvatura().run()