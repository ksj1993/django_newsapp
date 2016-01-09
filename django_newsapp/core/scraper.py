import urllib2
from bs4 import BeautifulSoup

def scrape(url_page):

	scraped_content = {}

	url_page = urllib2.urlopen(new_article.url_link)
	soup = BeautifulSoup(url_page)

	tag = bs.find("meta", {"property": "og:image"})
	if tag is not None:
		scraped_content['image'] = tag['content']
	else:
		# TODO choose first image
		pass
		
	tag = bs.find("meta", {"property": "og:image"})
	if tag is not None:
		scraped_content['image'] = tag['content']


	

