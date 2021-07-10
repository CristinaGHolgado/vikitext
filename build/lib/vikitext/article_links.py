"""
Module 1 : Collecte des liens des articles à partir de la liste d'hyperliens de l'index alphabétique de Vikidia.
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



def make_linkset(inputfile, output_name):
	"""Retourne un fichier texte avec les liens de chaque article du domaine wiki (/wiki/[nom article])

	Parameters :
	------------
		inputfile : str
			Nom du fichier texte qui va contenit les hyperliens de chaque page de l'index de Vikidia. Ces hyperliens contiennent un ensemble de liens vers differents articles
		output_name : str
			Nom du fichier de sortie. Il regroupe les liens directs de tous les articles
	"""
	links_of_links = [] # liste des liens directs vers les articles (/wiki/[nom]) valables pour Wikipedia et Vikidia, extratis a partir des hyperliens de l'index alphabetique de Vikidia

	def get_links():
		with open(inputfile, 'r', encoding='utf-8') as f:
			urls = f.readlines()
			liens_to_dataframe2 = {'links of links': [line.strip('\n') for line in urls]}
			df = pd.DataFrame(liens_to_dataframe2, columns=['links of links'])
			print(f"Aperçu des hyperliens en entrée : {df.head()}")
			liens2 = [line.strip('\n') for line in urls]
			for item in liens2:
				page = requests.get(item)
				data = page.text
				soup = BeautifulSoup(data, features="lxml")
				for link in soup.find_all('a'):
					all_links = link.get('href')
					links_of_links.append(all_links)

	print()

	links_articles = []
	
	def filter_links():
		"""Premier filtrage des liens.
		- Liens de navigation du site : ignorer ceux ne commençant pas par /wiki/
		- Liens avec du texte et chiffres : ils renvoient souvent a des articles similaires (Airbus A220, Airbus A300, Airbus A380, A5, A33, A7...)
		- Liens qui renvoient principalement a des articles biographiques et des acronymes, pour reduire de la taille finale du corpus.
		"""
		print(f">> Nb brut de liens : {len(links_of_links)}")
		print(f"appercu :\n{links_of_links[0:10]}\n")
		filtered = [links_articles.append(l) for l in links_of_links if re.search(r'^/wiki/(?!Sp%C3%A|Vikidia:|Aide:|Fichier:|Portail:|.*[A-Z].*[0-9]|.*\..*|[A-Z].*_.*[A-Z])', str(l))]
		print(">> Nb de liens apres filtrage : ", len(links_articles))
		print(f"apercu :\n{links_articles[0:10]}\n\n")

	def links_to_df():
		"""Deuxième filtrage. Passer la liste d'articles dans un tableau.
		"""
		raw_data = {'Liens': [l for l in links_articles if len(l.split('/')[2]) >= 4]} # Sélectionner les liens où le nom de l'article est égal ou supérieur à 4 lettres
		df = pd.DataFrame(raw_data, columns = ['Liens'], dtype=object)
		print("Apercu : \n", df.loc[0:100])
		print("Nombre de liens apres la premiere selection : ",len(df))
		print()
		
		df = df[~df['Liens'].str.contains("(homonymie)")] # liens finissant par "homonymie" renvoient à des listes qui n'apportent pas de contenu
		df = df.drop_duplicates(subset=None, keep='first', inplace=False) # supprimer liens répétés
		df = df[~df.Liens.str.contains(r"/\d+$")] # articles /wiki/1945 /wiki/1887 /wiki/1988 ...
		df.loc[df['Liens'].str.contains(r".*_[a-z]"),'similaires'] = df['Liens'].apply(lambda x: '_'.join(x.replace("/wiki/","").split("_")[:2])[:-3]) ## supprimer articles similaires (acide_aspartique, acide_absorbique, etc. (acide_...) et conserver premier)
		df.loc[df['Liens'].str.contains(r".*-[a-z]"),'similaires'] = df['Liens'].apply(lambda x: '-'.join(x.replace("/wiki/","").split("-")[:2])[:-3])

		df.loc[df['similaires'].isna(),'similaires'] = df['Liens']
		df = df.drop_duplicates(subset="similaires", keep='first', inplace=False)
		del df['similaires']
		df = df.drop_duplicates()

		print("Nombre de liens apres la derniere selection : ", len(df))
		print(df.head(20))
		df.to_csv(output_name, sep = "\t", encoding='utf-8', index=False, header=None)
		print()
	
	get_links()
	filter_links()
	links_to_df()



def make_urls(out_file):
	"""Préparation des liens vers articles Vikidia et Wikipedia : nombre du domaine ["http://fr.wikipedia.org"]|["https://fr.vikidia.org"] + nombre article :"/wiki/Dune_littorale" )
	"""
	
	links_wiki = []
	links_viki = []

	with open(out_file, 'r', encoding='utf8') as f:
		read_f = f.readlines()	
		for line in read_f:
			string_wiki = "https://fr.wikipedia.org"
			links_wiki.append(string_wiki+line.replace('\n',''))
			
			string_viki = "https://fr.vikidia.org"
			links_viki.append(string_viki+line.replace('\n',''))
	
	print('Liens crées.')

	with open('liens_wikipedia.txt', 'w',encoding='utf8') as f:
		f.write(str("\n".join(links_wiki)))
		print("Fini - liens_wikipedia.txt")
	with open('liens_vikidia.txt', 'w',encoding='utf8') as f:
		f.write(str("\n".join(links_viki)))
		print("Fini - liens_wikipedia.txt")


def chunk_urls():
	"""Segmentation de la liste avec les liens dans des ensembles de 200 liens par fichier. 
	Cela évite des possibles problèmes de mémoire pendant l'extraction du texte des articles.
	"""

	# creer deux dossiers pour la sauvegarde des liens
	if os.path.exists('wiki_links_files') and os.path.exists('vikidia_links_files'):
		print('Creation dossier /wiki_links_files')
		shutil.rmtree('wiki_links_files')
		print('Creation dossier /wikidia_links_files')
		shutil.rmtree('vikidia_links_files')
	if not os.path.exists('wiki_links_files') or not os.path.exists('vikidia_links_files'):
		os.makedirs('wiki_links_files')
		os.makedirs('vikidia_links_files')
	
	print('Preparation des fichiers avec les liens Wikipedia')
	path = os.getcwd()
	os.chdir(path)
	dir_wiki = "wiki_links_files//wiki_"
	commande_wiki = f"split --verbose -l200 liens_wikipedia.txt {dir_wiki} --additional-suffix=.txt; exit"
	conv = ["bash", "-c", commande_wiki]
	subprocess.call(conv)
	print('Fini')

	print('Preparation des fichiers avec les liens Vikidia')
	dir_vikidia = "vikidia_links_files//vikidia_"
	commande_vikidia = f"split --verbose -l200 liens_vikidia.txt {dir_vikidia} --additional-suffix=.txt; exit"
	conv2 = ["bash", "-c", commande_vikidia]
	subprocess.call(conv2)
	print('Fini')

# main func
def get_links(infile, outfile):
	make_linkset(infile, outfile)
	make_urls(outfile)
	chunk_urls()