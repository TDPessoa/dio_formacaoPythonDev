from skimage.io import (
    imread,
    imsave
)

def ler_imagem(caminho, tom_de_cinza=False):
    return imread(caminho, as_gray=tom_de_cinza)

def salvar_imagem(imagem, caminho):
    imsave(caminho, imagem)
