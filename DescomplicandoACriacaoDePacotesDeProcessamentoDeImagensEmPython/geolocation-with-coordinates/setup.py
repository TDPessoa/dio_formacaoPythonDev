"""
(PT-BR)
    Geolocalização e Georreferenciamento com poligonos
(EN-US)
    Geolocation and Georefferencing with polygons
Copyright (C) 2024 Thiago Daniel Pessoa

This program is free software: you can redistribute it and/or modify it _
under the terms of the GNU General Public License as published by the   _
Free Software Foundation, either version 3 of the License, or (at your  _
option) any later version.

This program is distributed in the hope that it will be useful, but     _
WITHOUT ANY WARRANTY; without even the implied warranty of              _
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU        _
General Public License for more details.

You should have received a copy of the GNU General Public License along _
with this program. If not, see <https://www.gnu.org/licenses/>.
"""


from setuptools import (
    setup, 
    find_packages
)

with open('README.md', 'r') as f:
    description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='geo_bound',
    version='0.0.1',
    author='TDPessoa',
    author_email='thiago.d.pessoa@gmail.com',
    description='Location of coordinates in geospatial maps.',
    long_description=description,
    long_description_content_type='text/markdown',
    url='', # TODO
    packages=find_packages(),
    requires=requirements
)
