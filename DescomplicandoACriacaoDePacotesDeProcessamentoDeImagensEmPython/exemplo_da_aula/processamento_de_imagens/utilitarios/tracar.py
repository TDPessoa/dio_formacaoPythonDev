import matplotlib.pyplot as plt

def tracar_imagem(imagem):
    plt.figure(figsize=(12, 4))
    plt.imshow(imagem, cmap='gray')
    plt.axis('off')
    plt.show

def tracar_resultado(*args):
    numero_de_imagens = len(args)
    figura, eixos = plt.subplots(
        nrows=1, ncols=numero_de_imagens, figsize=(12, 4)
    )
    lista_de_nomes = [
        'imagem {}'.format(i) for i in range(1, numero_de_imagens)
    ]
    for eixo, nome, imagem in zip(eixos, lista_de_nomes, args):
        eixo.set_title(nome)
        eixo.imshow(imagem, cmap='gray')
        eixo.axis('off')

    figura.tight_layout()
    plt.show()

def tracar_histograma(imagem):
    figura, eixo = plt.subplots(
        nrows=1, ncols=3, figsize=(12, 4), sharedx=True, sharey=True
    )
    lista_de_cores = ['red', 'green', 'blue']
    for indice, (eixo, cor) in enumerate(zip(eixo, lista_de_cores)):
        eixo.set_title('{} histograma'.format(cor.title()))
        eixo.hist(imagem[:, :, indice].ravel(), bins=256, color=cor, alpha=0.8)

    figura.tight_layout()
    plt.show()
