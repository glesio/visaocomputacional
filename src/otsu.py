# -*- coding: utf-8 -*-
from function import image_path
from matplotlib import pyplot
from skimage import io
from skimage import filter
from skimage import exposure

class Otsu(object):

    def __init__(self, image_name = 'macrophyllum/l04.jpg'):
        self.__img_path = image_path(image_name)   

    def __transform(self):
        self.__img = io.imread(self.__img_path)
        self.__img_gray = io.imread(self.__img_path, True)

        self.__otsu = filter.threshold_otsu(self.__img_gray)

        self.__img_gray = self.__img_gray < self.__otsu

        # buscar função otsu  ou gerar nova imagem com for {0,1}
        self.__hist, self.__bins_center = exposure.histogram(self.__img_gray) # img < val | im

    def run(self):    

        self.__transform()        

        pyplot.figure(figsize=(9, 4))

        pyplot.subplot(131)
        pyplot.imshow(self.__img, cmap='gray', interpolation='nearest')
        pyplot.axis('off')

        pyplot.subplot(132)
        pyplot.imshow(self.__img_gray, cmap='gray', interpolation='nearest')
        pyplot.axis('off')

        pyplot.subplot(133)
        pyplot.plot(self.__bins_center, self.__hist, lw=2)
        pyplot.axvline(self.__otsu, color='k', ls='--')

        pyplot.show()
        

# Run Code
if __name__ == '__main__':
    Otsu().run()