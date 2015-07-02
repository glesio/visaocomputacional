# -*- coding: utf-8 -*-
from function import image_path
from skimage import io
import numpy as np
from matplotlib import pyplot
import math
from skimage import filter
from skimage import measure


class Contorno(object):
    
    def __init__(self, image_name = 'macrophyllum/l04.jpg'):
        self.__img_path = image_path(image_name)   

    def __transform(self):
        self.__img_gray = io.imread(self.__img_path, True)

        self.__otsu = filter.threshold_otsu(self.__img_gray) #Aplicar otsu para binarizar a imagem
        self.__img_gray = self.__img_gray < self.__otsu

        # Find contours at a constant value of 0.5
        self.__contours = measure.find_contours(self.__img_gray, 0.5)

        self.__arclen = 0.0
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

            if arclenTemp > self.__arclen:
                self.__arclen = arclenTemp
                self.__bestn = n
        #self.__bestn = 0
        print self.__contours[0]
    def run(self):

        self.__transform()
        

        #print "\nExtração Paramétrica do contorno"
        #print self.__contours[contorno['bestn']]

        pyplot.annotate('Tamanho do array do contorno: ' + str(np.shape(self.__contours[self.__bestn])[0]), xy=(0, -150)) 
        pyplot.annotate('Comprimento de Arco: ' + str(self.__arclen), xy=(0, -100))
        pyplot.annotate('Area: ' + str(np.sum(self.__img_gray)), xy=(0, -50))

        pyplot.imshow(self.__img_gray, interpolation='nearest', cmap=pyplot.cm.gray)

        for contour in self.__contours:
            pyplot.plot(contour[:, 1], contour[:, 0], linewidth=2)

        pyplot.axis('off')
        pyplot.show()


# Run Code
if __name__ == '__main__':     
     Contorno().run()