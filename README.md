## **Installation**

`pip install vikitext`

## **Overview**
This package allows to easily build a parallel corpus with Vikidia and Wikipedia articles. In other words, a parallel corpus of simple and complex texts. It is mainly designed for research purposes such as readability analysis or text simplification.

## **Quickstart**

A sample script can be found in the repository *example_vikitext.py*


```python

import vikitext
from vikitext import hyperlinks, article_links, get_text
```


- Function `get_src_links()` retrieve a list of links from each page of Vikidia's alphabetical index (Note that the following link
 hides the redirects and namespace). This list of links is later used to obtain the links for the articles.
```python
viki_link "https://fr.vikidia.org//w//index.php?title=Sp%C3%A9cial%3AIndex&prefix=&namespace=0&hideredirects=1"
src_links = hyperlinks.get_src_links(viki_link)
```


- `get_article_links()` returns the links to every article found
```python
txt_links = article_links.get_article_links("vikidia_src_links.txt") # file generated with src_links
```


- The text content of each article can be retrieved using `content()`. A basic cleaning is performed to remove text from non-relevant sections of the article.
```python
text = get_text.content('fullset_urls.tsv','texts') # file generated with txt_links | output file custon name
```
  
  
#### **Preview**
|  | TITLE      | URL              | URL_WIKIPEDIA                              | URL_VIKIDIA                          | vikidia_text                     |                                         |
|----|------------|------------------|--------------------------------------------|--------------------------------------|----------------------------------|-----------------------------------------|
| 0  | 'Pataph... | /wiki/%27Pata... | https://fr.wikipedia.org/wiki/%27Pat...    | https://fr.vikidia.org/wiki/%27Pa... | La ’pataphysique est une sci...  | La ’Pataphysique apparaît dans ...      |
| 1   | Belenos    | /wiki/Bele...    | https://fr.wikipedia.org/wiki/(11284)_B... | https://fr.vikidia.org/wiki/(112... | Belenos est un astéroïde ...     | Belenos, désignation internat... |