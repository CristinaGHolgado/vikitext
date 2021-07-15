"""
Module 3 : retrieve text from each article
"""
from bs4 import BeautifulSoup, SoupStrainer
import bs4
import requests
import csv
import pandas as pd

def get_content(f, outname):
	"""retrieve text from each article
	
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
	
	print("File(s) saved in /corpus")

