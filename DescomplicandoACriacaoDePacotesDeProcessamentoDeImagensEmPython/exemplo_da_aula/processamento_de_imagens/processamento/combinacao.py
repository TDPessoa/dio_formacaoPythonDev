import numpy as np
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity

def find_difference(imagem1, imagem2):
    assert imagem1.shape == imagem2.shape, (
        'As imagens precisam ter as mesmas dimensões.'
    )
    imagem1_em_cinza = rgb2gray(imagem1)
    imagem2_em_cinza = rgb2gray(imagem2)
    (pontuacao, imagem_diferencial) = structural_similarity(
        imagem1_em_cinza, imagem2_em_cinza, full=True
    )
    print(f'A similaridade das imagens é de {(pontuacao*100):.1f}%.')
    imagem_diferencial_nomralizada = (
        (imagem_diferencial - np.min(imagem_diferencial))
      / (np.max(imagem_diferencial) - np.min(imagem_diferencial))
    )
    return imagem_diferencial_nomralizada

def transferir_histograma(imagem1, imagem2):
    imagem_equivalente = match_histograms(
        imagem1, imagem2, multichannel=True
    )
    return imagem_equivalente
