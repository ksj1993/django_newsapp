import urllib, urllib2, shutil, shutil, uuid, sys, requests
from cookielib import CookieJar
from bs4 import BeautifulSoup
from django.conf import settings as djangoSettings
from .models import Article
from urlparse import urlparse

class Scraper:

	def __init__(self, url_page):
		try:
			self.url_page = url_page
			cj = CookieJar()
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
			self.webpage = opener.open(url_page)
			self.soup = BeautifulSoup(self.webpage)
		except:
			raise

	def scrapeImage(self):
		tag = self.soup.find( "meta", {"property": "og:image"})
		if tag is not None:
			image_url = tag['content']
			return self.downloadImage(image_url)

		tag = self.soup.find('img')
		if tag is not None:
			image_url = tag['src']
			return self.downloadImage(image_url)

		# webpage doesnt have image, use default
		return ("default.png", "default.png")

	def downloadImage(self, image_url):
		article = Article.objects.filter(image_url = image_url).first()
		if article is None:
			try:
				response = requests.get(image_url, stream=True)
				extension = image_url.rsplit(".", 1)[-1]
				image_name = str(uuid.uuid4())
				print >> sys.stderr, image_name

				image_path = djangoSettings.MEDIA_ROOT + "/" + image_name
				with open(image_path, 'wb') as out_file:
					shutil.copyfileobj(response.raw, out_file)
				del response
				return (image_name, image_url)
			except:
				return ("default.png", "default.png")
		else:
			# image already exists
			return (article.image.name, image_url)

	def scrapeTitle(self):
		tag = self.soup.find( "meta", {"property": "og:title"})
		if tag is not None:
			return tag['content']

		tag = self.soup.find("title")
		if tag is not None:
			return tag.string

		return ""

	def scrapeSitename(self):
		tag = self.soup.find("meta", {"property": "og:site_name"})
		if tag is not None:
			return tag['content']
		else:
			try:
				cleaner = urlparse(self.url_page)
				return cleaner.netloc
			except:
				return ""

	def scrapeDescr(self):
		tag = self.soup.find("meta", {"property": "og:description"})
		if tag is not None:
			return tag['content']
		else:
			# TODO 
			return ""





	

