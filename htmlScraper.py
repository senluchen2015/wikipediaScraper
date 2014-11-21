from HTMLParser import HTMLParser 
import requests
import re
import os
import sys
class HtmlParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if(tag == 'a'):
			global linkArray
			link = attrs[0][1]
			print link
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
			pageText = get_main_category(page.text)
			if pageText == - 1:
				parser.feed(page.text)
			else:
				parser.feed(pageText) 

def get_main_category(text):
	start = text.find('<div id="mw-subcategories">')
	if start == -1:
		return False
	end = text.find('<noscript>')
	return text[start:end]

def get_main_body(text):
	start = text.find('<div id="mw-content-text" lang="en" dir="ltr" class="mw-content-ltr">')
	if start == -1:
		return False
	finish = text.find('<div class="printfooter">')
	return text[start:finish]

def remove_tags(text):
	return re.sub('<[^>]*>', '', text)

def main(argv):
	# page = requests.get('http://en.wikipedia.org/wiki/Category:Superheroes')
	global linkArray
	global categoryLinkArray
	entryCategory = argv[0]
	print entryCategory
	categoryLinkArray = [entryCategory]
	print categoryLinkArray
	linkArray = []

	parser = HtmlParser()
	host = 'http://en.wikipedia.org'
	numArticles = 10
	
	populate_link_array(parser, host, numArticles)	
	# print linkArray
	for i in range(1,(len(linkArray))):
		fullLink = make_full_html(host, linkArray[i])
		# print fullLink
		page = requests.get(fullLink)
		text = get_main_body(page.text)
		if text == False:
				continue
		text = remove_tags(page.text)
		nameArr = linkArray[i].split('/')
		filename = nameArr[2]

		filename = os.path.join('captain',filename)
		# print filename
		f = open(filename, 'w+')
		text = text.encode('utf-8')
		f.write(text)

if __name__ == "__main__":
	main(sys.argv[1:])