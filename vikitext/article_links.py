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

'''
module 2 : Return each article link from Vikidia alphabetical index
'''


def make_linkset(inputfile, split_nb=None):
	"""Rreturns a text file with links to each article in the wiki domain (/wiki/[article title])

	Parameters :
	------------
		inputfile : str
			File listing main links from Vikidia alphabetical index
		
		split_nb : int (optional)
			If used, split output file containing all article links into n number of links per file

	"""
	raw_urls_articles = [] # liste des liens directs vers les articles (/wiki/[nom]) valables pour Wikipedia et Vikidia, extratis a partir des hyperliens de l'index alphabetique de Vikidia
	titles_articles = []

	def get_links():
		
		with open(inputfile, 'r', encoding='utf-8') as f:

			hyperurls = f.readlines()
			hyperurls_to_df = {'hyperurls': [line.strip('\n') for line in hyperurls]}

			df = pd.DataFrame(hyperurls_to_df, columns=['hyperurls'])

			print(f"List of collected hyperurls from Vikidia :\n{df.head()}")
		
			for item in df.hyperurls.to_list():
				page = requests.get(item)
				data = page.text
				soup = BeautifulSoup(data, features="lxml")
				for link in soup.find_all('a'):
					print(f"Retrieving link for article : {link.get('title')}")
					titles_articles.append(link.get('title'))
					raw_urls_articles.append(link.get('href'))

	get_links()

	df_articles = pd.concat([pd.DataFrame(titles_articles, columns=['TITLE']),
							pd.DataFrame(raw_urls_articles, columns=['URL'])], axis=1)

	# Exclude irrelevant/empty urls
	df_articles = df_articles.dropna()
	df_articles = df_articles[~df_articles.TITLE.str.contains("Spécial:Index") & ~df_articles.TITLE.str.contains("Vikidia:")]
	# df_articles = df_articles[~df_articles.TITLE.str.contains("Vikidia:")]

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
			
			print('Splitting links ...')
			
			path = os.getcwd()
			os.chdir(path)
			dir_folder_split = "splitted_urls//"
			commande_wiki = f"split --verbose -l{split_nb} fullset_urls.tsv {dir_folder_split} --additional-suffix=.tsv; exit"
			conv = ["bash", "-c", commande_wiki]
			subprocess.call(conv)
			print('\n\nFinished. Files saved in `splitted_urls/`')
		else:
			print("Argument `split_nb` must be an integer")
	else:
		print("No `split_nb` selected")



make_linkset("vikidia_hyperlinks.txt")