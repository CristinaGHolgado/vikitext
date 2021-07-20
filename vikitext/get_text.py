# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, SoupStrainer
import bs4
import requests
import csv
import pandas as pd
import os
import re
"""
Module 3 : retrieve text from each article & basic preprocess
"""

ignore_sents = ['Les associations Vikidia', 'Répondre au sondage', 'Aller à :',
				'Récupérée de « https', 'Accédez aux articles', 'Catégorie :',
				'Le contenu est disponible sous licence', 'Sur d’autres projets',
				'Imprimer / exporter', 'Créer un livre', 'Vikidia, l’encyclopédie',
				'Attention, à ne pas confondre', 'Cet article est à compléter', '(Aide)',
				'Pages liées', 'À propos de Vikidia', 'Pages liées', 'Espaces de noms',
				'PageDiscussion', 'LireModifierModifier', 'AccueilPages par thèmes',
				'Article au hasardBanque d’imagesLe SavantDemander un article', 
				'Modifications récentesCommunautéBavardagesAide', 'Vikidia a besoin de toi',
				'Pour rester indépendant, nous refusons' ,'Tu peux soutenir Vikidia',
				'Tu peux également financer gratuitement', 'Dernière modification de cette page',
				'Non connectéDiscussion', 'Notes et références', '↑ Table', 'Voir aussi[',
				'Portail de la littérature  —', 'Pour aller plus loin[', 'Portail des sciences —',
				'Vikiliens[', 'Lien interne[', 'Lien externe[', '• modifier',
				'Soit vous avez mal écrit le titre', "L'article a peut-être été supprimé",
				"Il peut aussi avoir été renommé sans création", 'Si vous avez récemment créé cet article',
				'Créer le wikicode', 'dans les autres articles (aide)',
				'Consultez la liste des articles dont le titre', "Cherchez d'autres pages de Wikipédia",
				"Wikipédia ne possède pas d'article", 'Cet article est une ébauche',
				'Vous pouvez partager vos connaissances en ']

ignore_single_items = ['Confidentialité', 'Avertissements', 'Version mobile', 'Plus', 'Chercher',
						'Navigation', 'Contribuer', 'Espaces de noms', 'PageDiscussion',
						'Variantes', 'Affichages', 'Menu de navigation', 'Outils personnels',
						'Vikidia', 'Wikipédia', 'Outils', 'Notes pour les rédacteurs :',
						'Commons (images et médias)', 'Wikivoyage (guides de voyage)',
						'Wikidata (base de données)']

ignore_single_items_wiki = ['Aller au contenu', 'Rechercher', 'Imprimer / exporter', 'Modifier les liens',
							'Outils personnels', 'Menu de navigation', 'Navigation', 'Contribuer', 'Outils', 'Espaces de noms', 'Variantes',
							'Affichages', 'Liens externes', 'Politique de confidentialité', "À propos de Wikipédia",
							"Contact", "Développeurs", 'Statistiques', 'Déclaration sur les témoins (cookies)',
							'Précédé par', 'Suivi par', 'Références', 'modifier', 'Lien externe', 'Voir aussi']

ignore_sents_wiki = ['Aragonés | ', 'Un article de Wikipédia', 'AccueilPortails', 'Débuter sur Wikipédia', 'Dans d’autres projets',
						'Pour les articles homonymes, voir', 'Wikimedia Commons', 'Afficher / masquer', 'EsperantoEspañol',
						'EnglishEspañol', 'EnglishEsperanto', 'Vous lisez un « bon article »', 'Bahasa Indonesia', 'La dernière modification de cette page', 'Dans d’autres projets', 'Wikimedia CommonsWikiquote', 'ArticleDiscussion',
							'— Wikipédia', 'Non connectéDiscussion', 'Pages liéesSuivi des pages', 'Créer un livre',
							'LireModifier', 'Ce document provient de «', 'Catégories cachées : Pages', "Droit d'auteur : les",
							"Voyez les conditions d’utilisation pour plus", 'marque déposée de la Wikimedia Foundation',
							'organisation de bienfaisance régie par le paragraphe', 'Cette section est vide, insuffisamment',
							'(voir la liste des auteurs)', '(comparer avec la version actuelle)', 'Pour toute information complémentaire,',
							'/Articles liés']



def content(f, outname):
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

	df_content = pd.read_csv(f, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE)
	print(f'Columns content in input file : TITLE | URL | URL_WIKIPEDIA | URL_VIKIDIA\n')


	print("**This can take a while")
	print("Extracting article text content from Vikidia ...")
	df_content['vikidia_text'] = df_content['URL_VIKIDIA'].apply(lambda x: BeautifulSoup(requests.get(x).text, features="lxml").text.strip())
	
	print("Extracting article text content from Wikipedia ...")
	df_content['wikipedia_text'] = df_content['URL_WIKIPEDIA'].apply(lambda x: BeautifulSoup(requests.get(x).text, features="lxml").text.strip())

	
	def clean(col):
		'''basic preprocess specific to wiki data'''
		df_content[col] = df_content[col].apply(lambda x: re.sub(r'\n+', '__sent__', x).strip()) # remove succeeding line breaks
		df_content[col] = df_content[col].apply(lambda x: re.sub('\[.+?\]', '', x)) # remove items inside brackets
		df_content[col] = df_content[col].apply(lambda x: [sent for sent in x.split("__sent__") if len(sent) > 3]) # Ignore sent in article text is len < 3

		df_content[col] = df_content[col].apply(lambda x: [s for s in x if not any(item in s for item in ignore_sents)])
		df_content[col] = df_content[col].apply(lambda x: [item for item in x if item.strip() not in ignore_single_items])
		df_content[col] = df_content[col].apply(lambda x: [s for s in x if not any(item in s for item in ignore_sents_wiki)])
		df_content[col] = df_content[col].apply(lambda x: [item for item in x if item.strip() not in ignore_single_items_wiki])
		df_content[col] = df_content[col].apply(lambda x: x[1:] if 'langues' in x[0] else x[0:]) # ignore first item in list (12 langues, 34 langues...)

		if 'vikidia' in col:
			df_content[col] = df_content[col].apply(lambda x: x[1:]) # skip article title in position 0

		if 'wikipedia' in col:

			df_content[col] = df_content[col].apply(lambda x: x[1:] if x[0] == x[1] else x) # remove titles at the beginning ([Acacia, Acacia, Article text...])

			df_content[col] = df_content[col].apply(lambda x: [y.strip() for y in x]) # remove spaces at the begnning of sent
			df_content[col] = df_content[col].apply(lambda x: [y for y in x if not y.startswith('Portail d')]) # ignore items in list if starts with
		
		df_content[col] = df_content[col].apply(lambda x: [re.sub(r"(\w+[a-z])+([A-ZÂÊÎÔÛÄËÏÖÜÀÆÇÉÈŒÙ]\w+|[0-9])", r"\1 \2", y) for y in x]) # split overlapping words (wordWord)
		df_content[col] = df_content[col].apply(lambda x: [y for y in x if not y.startswith("↑ ")])
		df_content[col] = df_content[col].apply(lambda x: [y.replace("\xa0"," ") for y in x])
		df_content[col] = df_content[col].apply(lambda x: [y for y in x if len(y.split()) > 3]) # ignore items in list that only contain 3 words e.g.:  ['Ceinture de Kuiper', 'Cubewano', 'Plutino', 'Objet épars', ...]
		df_content[col] = df_content[col].apply(lambda x: [y for y in x if not y.startswith("v · m")])
	
	clean('vikidia_text')
	clean('wikipedia_text')

	
	output_name = "corpus/" + outname + ".tsv"
	df_content.to_csv(output_name, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE)
	
	print("File(s) saved in /corpus")

