from bs4 import BeautifulSoup
import requests

'''
module 1 : Return list of hyperlinks from the Vikidia alphabetical index
'''

_init_link = []
_clean_init_links = []

def source_hl(init_link):
	'''Scrap links from Vikidia alphabetical index
	
	Parameters
	----------
	init_link : str
		main link from the index

	Returns
	-------
		list
	'''
	
	x = requests.get(init_link)
	soup = BeautifulSoup(x.content, features='lxml')

	for div in soup.findAll('div', {'class': 'mw-prefixindex-nav'}):
		a = div.findAll('a', href=True)[0]
		_init_link.append(a)
		
		if len(a) >= 1:
			return True
		else:
			return False


def main_hl():
	'''
	start iteration from last item in list
	'''
	if type(_init_link) == list and len(_init_link) >= 1:
		init_link_src = str(_init_link[-1])
		init_link_src = init_link_src.split('"')
		init_link_src = "https://fr.vikidia.org" + str(''.join([''.join(item) for item in init_link_src if item.startswith("/w/index")]))
		_clean_init_links.append(init_link_src.replace("&amp;","&"))
	
	else:
		init_link_src = str(pass_init_link[-1]).split('"')
		init_link_src = [''.join(item) for item in init_link_src if item.startswith("/w/index")]
		_clean_init_links.append(init_link_src)


def list_hl():
	'''
	list all hyperlinks retrieved by iterating through the succeeding Vikidia Index pages starting from the source link
	'''
	while source_hl(_clean_init_links[-1]) == True:
		main_hl()
		print(_clean_init_links[-1])
	
	else:
		print("Finished")


def hl_to_txt(init_link):
	'''
	list of links to text file
	'''
	with open("vikidia_src_links.txt", 'w', encoding='utf8') as f:
		f.write(init_link + '\n')
		for item in _clean_init_links:
			f.write("%s\n" % item)
	print(f"{len(_clean_init_links)} links retrieved")

# main func
def get_hyperlinks(hl):
	'''Run retrieving
	
	Parameters
	----------
	hl : str
		Source link from Vikidia alphabetical index. Recommended to hide redirects.
		Use : https://fr.vikidia.org//w//index.php?title=Sp%C3%A9cial%3AIndex&prefix=&namespace=0&hideredirects=1
	'''
	source_hl(hl)
	main_hl()
	list_hl()
	hl_to_txt(hl)


