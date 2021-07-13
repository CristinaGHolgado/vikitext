"""
Module 1 : Collecte des liens des articles à partir de la liste d'hyperliens de l'index alphabétique de Vikidia.
"""

from bs4 import BeautifulSoup, SoupStrainer
from  itertools import product
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



def make_urlset(inputfile, split_nb=None):
	"""Retourne un fichier texte avec les liens de chaque article du domaine wiki (/wiki/[nom article])

	Parameters :
	------------
		inputfile : str
			File contaning list of hyperlinks from which extract URLs to Wikipedia/Vikidia articles
		
		split_nb : int (optional)
			If used, split output file containing all article URLs into n number of URLs per file

	Returns
	-------
		Wikipedia/Vikidia csv article URLs

	"""
	raw_urls_articles = [] # liste des liens directs vers les articles (/wiki/[nom]) valables pour Wikipedia et Vikidia, extratis a partir des hyperliens de l'index alphabetique de Vikidia
	titles_articles = []

	def get_urls():
		
		with open(inputfile, 'r', encoding='utf-8') as f:

			hyperurls = f.readlines()
			hyperurls_to_df = {'hyperurls': [line.strip('\n') for line in hyperurls]}
			print(hyperurls_to_df)
			df = pd.DataFrame(hyperurls_to_df, columns=['hyperurls'])

			print(f"List of collected hyperurls from Vikidia :\n{df.head()}")
		
			for item in df.hyperurls.to_list():
				page = requests.get(item)
				data = page.text
				soup = BeautifulSoup(data, features="lxml")
				for link in soup.find_all('a'):
					titles_articles.append(link.get('title'))
					raw_urls_articles.append(link.get('href'))

	get_urls()

	df_articles = pd.concat([pd.DataFrame(titles_articles, columns=['TITLE']),
							pd.DataFrame(raw_urls_articles, columns=['URL'])], axis=1)

	# Exclude irrelevant/empty urls
	df_articles = df_articles.dropna()
	df_articles = df_articles[~df_articles.TITLE.str.contains("Spécial:Index")]
	df_articles = df_articles[~df_articles.TITLE.str.contains("Vikidia:")]

	# Add domain
	df_articles['URL_WIKIPEDIA'] = "https://fr.wikipedia.org" + df_articles['URL']
	df_articles['URL_VIKIDIA'] = "https://fr.vikidia.org" + df_articles['URL']

	df_articles.to_csv("fullset_urls.tsv", sep='\t', encoding='utf8', index=None, quoting=csv.QUOTE_NONE)

	print()

	if split_nb:
		if isinstance(split_nb, int):
			if os.path.exists('splitted_urls'):
				shutil.rmtree('splitted_urls')
			if not os.path.exists('splitted_urls'):
				os.makedirs('splitted_urls')
			
			print('Collecting article URLs ...')
			
			path = os.getcwd()
			os.chdir(path)
			dir_folder_split = "splitted_urls//"
			commande_wiki = f"split --verbose -l{split_nb} fullset_urls.tsv {dir_folder_split} --additional-suffix=.tsv; exit"
			conv = ["bash", "-c", commande_wiki]
			subprocess.call(conv)
			print('Finished. Files saved in `splitted_urls/`')
		else:
			print("Argument `split_nb` must be an integer")
	else:
		print("No `split_nb` selected")



