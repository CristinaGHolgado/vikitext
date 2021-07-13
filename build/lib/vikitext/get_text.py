"""
Module 2 : Collecte du texte des articles Wikipedia et Vikidia.
"""
from bs4 import BeautifulSoup, SoupStrainer
import numpy as np
import bs4
import requests
import csv
import re
import pandas as pd
import os
import subprocess
import pathlib
import shutil
import glob

def get_content(f, outname):
	"""Extraire le contenu des liens des articles
	
	Parameters :
	------------
	f : str
		csv file containing article urls
	outname : str
		output name
	"""
	if not os.path.exists('corpus'):
		os.makedirs('corpus')
	else:
		pass

	df = pd.read_csv(f, sep='\t', encoding='utf8', names=['title','url','wiki_url','viki_url'], quoting=csv.QUOTE_NONE)
	print(f'Columns content in input file : TITLE | URL | WIKIPEDIA_URL | VIKIDIA_URL\n')
		
	print("Extracting article text content from Vikidia ...")
	df['vikidia_text'] = df['viki_url'].apply(lambda x: BeautifulSoup(requests.get(x).text, features="lxml").text.strip())

	print("Extracting article text content from Wikipedia ...")
	df['wikipedia_text'] = df['wiki_url'].apply(lambda x: BeautifulSoup(requests.get(x).text, features="lxml").text.strip())
	
	output_name = "corpus/" + outname + ".tsv"
	df.to_csv(output_name, sep='\t', encoding='utf8')
	
	print("File save in /corpus")


#get_content("fullset_urls.tsv", "fullset_text")
