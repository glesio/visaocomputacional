# -*- coding: utf-8 -*-
from function import image_path
from skimage import io
from skimage.util import random_noise
from scipy.signal import wiener
from matplotlib import pyplot


class Filtro(object):

    def __init__(self, image_name = 'macrophyllum/l04.jpg'):
        self.__img_path = image_path(image_name)   

    def __transform(self):
        self.__img_gray = io.imread(self.__img_path, True)
        self.__img_noise = random_noise(self.__img_gray, mode='gaussian')
        self.__img_wiener = wiener(self.__img_noise, (5,5))

    def run(self):

        self.__transform()

        pyplot.subplot(131)
        pyplot.imshow(self.__img_gray, vmin=0, vmax=1, cmap='gray')

        pyplot.subplot(132)
        pyplot.imshow(self.__img_noise, vmin=0, vmax=1, cmap='gray')

        pyplot.subplot(133)
        pyplot.imshow(self.__img_wiener, vmin=0, vmax=1, cmap='gray')

        pyplot.show()
        

# Run Code
if __name__ == '__main__':
    Filtro().run()