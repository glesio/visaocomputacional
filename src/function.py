import os 

''' Retorna o caminho absoluto da imagem '''
def image_path(image_name = ''):    
    return os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'images', image_name))

''' Retorna o diretorio das imagens '''    
def data_path():
    return os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data', 'folhas.csv'))
