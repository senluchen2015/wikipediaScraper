from HTMLParser import HTMLParser 
import requests
import re
import os

class HtmlParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if(tag == 'a'):
			global linkArray
			link = attrs[0][1]
			if(link.startswith("/wiki/")):
				if("Category:") in link: 
					categoryLinkArray.append(link)
				else:
					linkArray.append(link)

def make_full_html(host,path):
	return host+path

def populate_link_array(parser, host, numArticles):
	while(len(linkArray) < numArticles):
		if(len(categoryLinkArray)>0):
			categoryLink = categoryLinkArray.pop()
			fullLink = make_full_html(host, categoryLink)
			page = requests.get(fullLink)
			parser.feed(page.text) 

def get_main_body(text):
	start = text.find('<div id="mw-content-text" lang="en" dir="ltr" class="mw-content-ltr">')
	if start == -1:
		return False
	finish = text.find('<div class="printfooter">')
	return text[start:finish]

def remove_tags(text):
	return re.sub('<[^>]*>', '', text)

def main():
	# page = requests.get('http://en.wikipedia.org/wiki/Category:Superheroes')
	global linkArray
	global categoryLinkArray
	categoryLinkArray = ['/wiki/Category:Superheroes']
	linkArray = []

	parser = HtmlParser()
	host = 'http://en.wikipedia.org'
	numArticles = 50
	populate_link_array(parser, host, numArticles)	
	
	for i in range(1,(len(linkArray))):
		fullLink = make_full_html(host, linkArray[i])
		page = requests.get(fullLink)
		text = get_main_body(page.text)
		if text == False:
				continue
		text = remove_tags(page.text)
		nameArr = linkArray[i].split('/')
		filename = nameArr[2]
		filename = os.path.join("wikipediaSuperHero",filename)
		# print filename
		f = open(filename, 'w+')
		text = text.encode('utf-8')
		f.write(text)

if __name__ == "__main__":
	main()