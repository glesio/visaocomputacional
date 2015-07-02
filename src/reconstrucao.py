# -*- coding: utf-8 -*-
from function import image_path
from matplotlib import pyplot
from skimage import filter
from skimage import morphology
from skimage import io
from skimage.draw import circle_perimeter_aa

class Reconstrucao(object):

    def __init__(self, image_name = 'macrophyllum/l04.jpg'):
        self.__img_path = image_path(image_name)   

    def __transform(self):
        img_gray = io.imread(self.__img_path, True)
        
        thresh = filter.threshold_otsu(img_gray)
        data = img_gray < thresh
        s1, self.__distancia = morphology.medial_axis(data, return_distance=True)
        self.__s2 = s1

        for i in range(len(s1)):
            for j in range(len(s1)):
                if (s1[i,j] <> False): #Percorre o esqueleto da imagem
                    x, y,val = circle_perimeter_aa(i, j, int(self.__distancia[i,j]))

                    #desenha um circulo ao redor do pixel do esqueleto
                    #i,j coordenadas do centro  -- int(distance[i,j]=raio do circulo)
                    #x,y = índices dos pixels  ---- val = intensidade

                    #Define quais circulos devem ficar de acordo com o raio
                    if (int(self.__distancia[i,j]) > 0):
                        self.__s2[x, y] = True
                    else:
                        self.__s2[x, y] = False
                else:
                    self.__s2[i, j] = False        


    def run(self):
        self.__transform()

        fig, axes = pyplot.subplots(ncols=2)
        axes[0].imshow(self.__distancia, cmap=pyplot.cm.gray,interpolation='nearest')
        axes[1].imshow(self.__s2, cmap=pyplot.cm.gray,interpolation='nearest')
        
        pyplot.show()


# Run Code
if __name__ == '__main__':
    Reconstrucao().run()
