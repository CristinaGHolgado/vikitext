import setuptools
from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Retrieve article links and text from Vikidia and their equivalents in Wikipedia'
LONG_DESCRIPTION = 'A packgage to build a parallel corpus with articles from Vikidia and Wikipedia only for research purposes (e.g. readability analysis, text simplification). Only Vikidia articles with Wikipedia equivalents are downloaded.'

setup(
	name = 'vikitext',
	version = '0.0.3',
	author = 'Cristina Garcia Holgado',
	author_email = 'cristina.garcia-holgado@etu.unistra.fr',
	description = DESCRIPTION,
	install_requires = ['beautifulsoup4','requests','numpy','pandas'],
	license = 'MIT',
	keywords = ['corpus','vikidia','wikicommons','wikipedia'],
	url = 'https://github.com/CristinaGHolgado/vikitext',
	classifiers = [
		"Programming Language :: Python :: 3",
		"Operating System :: Microsoft :: Windows"],
    packages=['vikitext'],
    package_data={'vikitext': [r'data/*.txt']},
    python_requires=">=3.6",
    zip_safe=False
	)