# -*- coding: utf-8 -*-

from function import image_path
import skimage.filter  
import skimage.morphology  
import numpy as np  
from skimage import io
import matplotlib.pyplot as plt


class Esqueletizacao(object):
    
    def __init__(self, image_name = 'macrophyllum/l04.jpg'):
        self.img_path = image_path(image_name)   

    def __transform(self):
        img = io.imread(self.img_path, True)
        otsu = skimage.filter.threshold_otsu(img)  
        img = img < otsu # Threshold the image  

        self.__img_medial_axis = skimage.morphology.medial_axis(img)
    
    def run(self):    
        self.__transform()
        
        plt.annotate('Tamanho do array do contorno: ' + str(np.sum(self.__img_medial_axis)), xy=(10, 40), color='white') 
        plt.imshow(self.__img_medial_axis, interpolation='nearest', cmap = 'gray')
        plt.show()



# Run Code
if __name__ == '__main__':
    Esqueletizacao().run()