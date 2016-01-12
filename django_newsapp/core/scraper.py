import urllib, urllib2, shutil, shutil, uuid, sys, requests
from cookielib import CookieJar
from bs4 import BeautifulSoup
from django.conf import settings as djangoSettings
from .models import Article

class Scraper:

	def __init__(self, url_page):
		cj = CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		
		self.webpage = opener.open(url_page)
		self.soup = BeautifulSoup(self.webpage)

	def scrapeImage(self):
		tag = self.soup.find( "meta", {"property": "og:image"})
		if tag is not None:
			image_url = tag['content']
			print >> sys.stderr, image_url
			article = Article.objects.filter(image_url = image_url).first()
			if article is None:
				response = requests.get(image_url, stream=True)
				extension = image_url.rsplit(".", 1)[-1]
				image_name = str(uuid.uuid4())
				print >> sys.stderr, image_name
				# TODO rel path
				image_path = djangoSettings.MEDIA_ROOT + "/" + image_name
				with open(image_path, 'wb') as out_file:
					shutil.copyfileobj(response.raw, out_file)
				del response
				return (image_name, image_url)
			else:
				# image already exists
				return (article.image.name, image_url)
		else:
			# TODO choose first image, currently default
			return "default.png"

	def scrapeTitle(self):
		tag = self.soup.find( "meta", {"property": "og:title"})
		if tag is not None:
			return tag['content']
		else:
			#TODO
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





	

