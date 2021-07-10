import setuptools
from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Extract article links and text from Wikicommons'
LONG_DESCRIPTION = 'a packgage to build a corpus with articles from Vikidia'

setup(
	name = 'vikitext',
	version = '0.0.1',
	author = 'Cristina Garcia Holgado',
	author_email = 'cristina.garcia-holgado@etu.unistra.fr',
	description = DESCRIPTION,
	install_requires = ['beautifulsoup4','requests','numpy','pandas'],
	license = 'MIT',
	keywords = ['corpus','vikidia','wikicommons'],
	url = 'https://github.com/CristinaGHolgado/vikitext',
	classifiers = [
		"Programming Language :: Python :: 3",
		"Operating System :: Microsoft :: Windows"],
    packages=['vikitext'],
    python_requires=">=3.6",
    zip_safe=False
	)