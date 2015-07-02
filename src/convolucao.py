# -*- coding: utf-8 -*-
from function import image_path
from skimage import filter
from skimage import io
from skimage.color import rgb2gray
from matplotlib import pyplot

class Convolucao(object):

    def __init__(self, blur = 8, image_name = 'macrophyllum/l04.jpg'):
        self.__blur = blur
        self.__img_path = image_path(image_name)

    def __transform(self):
        self.__img = io.imread(self.__img_path)
        self.__img_gaussian = filter.gaussian_filter(self.__img, self.__blur)
        self.__img_sobel = filter.sobel(rgb2gray(self.__img))

    def run(self):

        self.__transform()

        pyplot.subplot(131)
        pyplot.annotate('Imagem Original', xy=(10, 0), color='black') 
        pyplot.imshow(self.__img, vmin=0, vmax=1)

        pyplot.subplot(132)
        pyplot.annotate('Imagem Gaussiana P.B', xy=(10, 0), color='black')
        pyplot.imshow(self.__img_gaussian, vmin=0, vmax=1)

        pyplot.subplot(133)
        pyplot.annotate('Imagem Sobel P.A', xy=(10, 0), color='white')
        pyplot.imshow(self.__img_sobel, vmin=0, vmax=1, cmap='gray')

        pyplot.show()


# Run Code
if __name__ == '__main__':     
    Convolucao().run()