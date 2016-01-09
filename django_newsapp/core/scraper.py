import urllib2
from bs4 import BeautifulSoup
import shutil
import requests
from django.conf import settings as djangoSettings
import uuid

class Scraper:

	def __init__(self, url_page):
		
		self.webpage = urllib2.urlopen(url_page)
		self.soup = BeautifulSoup(self.webpage)
	

	def scrapeImage(self):
		tag = self.soup.find( "meta", {"property": "og:image"})
		if tag is not None:
			image_url = tag['content']
			response = requests.get(image_url, stream=True)

			# TODO rel path
			image_name = djangoSettings.MEDIA_ROOT + str(uuid.uuid4())
			with open(image_name, 'wb') as out_file:
				shutil.copyfileobj(response.raw, out_file)
			del response
			return image_name

		else:
			# TODO choose first image
			return ""



	def scrapeSitename(self):
		tag = self.soup.find("meta", {"property": "og:site_name"})
		if tag is not None:
			return tag['content']
		else:
			# TODO 
			return ""

	def scrapeDescr(self):
		tag = self.soup.find("meta", {"property": "og:description"})
		if tag is not None:
			return tag['content']
		else:
			# TODO 
			return ""





	

