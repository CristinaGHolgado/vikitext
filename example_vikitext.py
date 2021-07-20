
#	sample

import vikitext
from vikitext import hyperlinks, article_links, get_text

# collect list of links containing articles links
src_links = hyperlinks.get_src_links("https://fr.vikidia.org//w//index.php?title=Sp%C3%A9cial%3AIndex&prefix=&namespace=0&hideredirects=1")

# collect direct links to articles
txt_links = article_links.get_article_links("vikidia_src_links.txt") # file generated with src_links

# retrieve text from articles
text = get_text.content('fullset_urls.tsv','texts') # file generated with txt_links | name for ouptul file
