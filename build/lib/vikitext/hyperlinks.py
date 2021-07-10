from bs4 import BeautifulSoup
import requests

'''Extract hyperlinks from Vikidia (based on url: )
'''

_url = []
_clean_urls = []

def source_hl(url):
	'''Scrap over the site
	
	Parameters
	----------
	url : str
		Input site hyperlink

	Returns
	-------
		List
	'''
	
	x = requests.get(url)
	soup = BeautifulSoup(x.content, features='lxml')

	for div in soup.findAll('div', {'class': 'mw-prefixindex-nav'}):
		a = div.findAll('a', href=True)[0]
		_url.append(a)
		
		if len(a) >= 1:
			return True
		else:
			return False


def main_hl():
	'''List all found hyperlinks starting with the fist appended (referent) as reference
	to navigate to the next pages'''
	if type(_url) == list and len(_url) >= 1:
		url_src = str(_url[-1])
		url_src = url_src.split('"')
		url_src = "https://fr.vikidia.org"+str(''.join([''.join(item) for item in url_src if item.startswith("/w/index")]))
		_clean_urls.append(url_src.replace("&amp;","&"))
	else:
		url_src = str(pass_url[-1]).split('"')
		url_src = [''.join(item) for item in url_src if item.startswith("/w/index")]
		_clean_urls.append(url_src)


def list_hl():
	'''Iterate over the site index pages'''
	while source_hl(_clean_urls[-1]) == True:
		main_hl()
		print(_clean_urls[-1])
	else:
		print("Finished")


def hl_to_txt(url):
	'''Save collected urls into a plain text file'''
	with open("viki_hyperlinks.txt", 'w', encoding='utf8') as f:
		f.write(url+'\n')
		for item in _clean_urls:
			f.write("%s\n" % item)

# main func
def get_hl(hl):
	'''Generates a text file listing every hyperlink from the input site main hyperlink. Used to get links afterwards
	Parameters
	----------
	hl : str
		Hyperlink to Vikidia alphabetical index. Recommended to hide redirects. Use : https://fr.vikidia.org//w//index.php?title=Sp%C3%A9cial%3AIndex&prefix=&namespace=0&hideredirects=1
	'''
	source_hl(hl)
	main_hl()
	list_hl()
	hl_to_txt(hl)