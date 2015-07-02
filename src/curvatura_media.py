# -*- coding: utf-8 -*-
from function import image_path
from skimage import io
from matplotlib import pyplot
from skimage import filter
from skimage import measure
from skimage import morphology
import numpy as np
import math


class CurvaturaMedia(object):
    
    def __init__(self, image_name = 'macrophyllum/l04.jpg'):
        self.image_path = image_path(image_name)   

    def __transform(self):
        img_gray = io.imread(self.image_path, True)
        #Aplicar otsu para binarizar a imagem
        img_otsu = filter.threshold_otsu(img_gray) 
        self.__img = img_gray < img_otsu

        # Procura contornos da imagem binarizada
        self.__contours = measure.find_contours(self.__img, 0.5)
        
        arclen=0.0
        for n, contour in enumerate(self.__contours):
            arclenTemp=0.0
            for indice, valor in enumerate(contour):
                if indice > 0:
                    d1 = math.fabs(round(valor[0]) - round(contour[indice-1,0]))
                    d2 = math.fabs(round(valor[1]) - round(contour[indice-1,1]))
                    if d1+d2>1.0:
                        arclenTemp+=math.sqrt(2)
                    elif d1+d2 == 1:
                        arclenTemp+=1
            if arclenTemp > arclen:
                arclen = arclenTemp
                bestn = n
        
        #Transforma a lista contours[bestn] em uma matriz[n,2]
        aux = np.asarray(self.__contours[bestn])

        #---------------------------  Curvatura --------------
        vetor = [] #vetor que irá receber as curvaturas k(t)
        
        for i in range(len(aux)-2):    #Percorrer ate -2 para não pegar elementos inexistentes
            #---------------------------  Curvatura --------------
            #Inverter as posições em relação a fórmula pois o x esta no lugar do y
            b1 =  ( (aux[i-2,1]+aux[i+2,1]) + (2*(aux[i-1,1] + aux[i+1,1])) - (6*aux[i,1]) ) / 12
            b2 = ( (aux[i-2,0]+aux[i+2,0]) + (2*(aux[i-1,0] + aux[i+1,0])) - (6*aux[i,0]) ) / 12
            c1 =  ( (aux[i+2,1]-aux[i-2,1]) + (4*(aux[i+1,1] - aux[i-1,1])) ) / 12
            c2 = ( (aux[i+2,0]-aux[i-2,0]) + (4*(aux[i+1,0] - aux[i-1,0])) ) / 12

            k =  (2*(c1*b1 - c2*b2)) / ((c1**2 + c2**2)**(3/2))

            vetor.append(k) #append: insere objeto no final da lista

        self.__media_curvatura = np.mean(np.abs(vetor))
        self.__comprimento_arco = arclen
        self.__area = np.sum(self.__img)
        self.__esqueleto_pixel = np.sum(morphology.medial_axis(self.__img))
        self.__bestn = bestn

    def run(self):

        self.__transform()
        
        pyplot.annotate('Media da curvatura: ' + "{:.4f}".format(self.__media_curvatura) , xy=(10, -180), color='black')
        pyplot.annotate('Comprimento de Arco: ' + "{:.4f}".format(self.__comprimento_arco) , xy=(10, -130), color='black')
        pyplot.annotate('Area: ' + str(self.__area) , xy=(10, -90), color='black')
        pyplot.annotate('Numero de pixels do esqueleto: ' + str(self.__esqueleto_pixel) , xy=(10, -50), color='black')
        pyplot.annotate('Posicao do melhor array: ' + str(self.__bestn) , xy=(10, -10), color='black')
        
        pyplot.imshow(self.__img, interpolation='nearest', cmap=pyplot.cm.gray)

        for contour in self.__contours:
            pyplot.plot(contour[:, 1], contour[:, 0], linewidth=2)

        pyplot.axis('off')
        pyplot.show()


if __name__  == '__main__':
    CurvaturaMedia().run()
