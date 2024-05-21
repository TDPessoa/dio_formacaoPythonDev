from setuptools import setup, find_packages

with open('README.md', 'r') as arquivo:
    descricao = arquivo.read()

with open('requirements.txt', 'r') as arquivo:
    requerimentos = arquivo.read().splitlines()

setup(
    name='processamento_de_imagens',
    version='0.1',
    author='TDPessoa',
    author_email='thiago.d.pessoa@gmail.com',
    description='Processamento de Imagens Com Python',
    long_description=descricao,
    long_description_content_type='text/markdown',
    url='', # TODO
    packages=find_packages(),
    requires=requerimentos
)
