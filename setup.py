import requests
import urllib.request
import time
from bs4 import BeautifulSoup	


def _getMoviesByPage(page):
	links = []
	response = requests.get("https://filmesnomega.info/page/" + str(page))
	soup = BeautifulSoup(response.text, "html.parser")
	posts = soup.findAll("a", {"class": "readmore"})

	for post in posts:
		links.append(post['href'])

	return links

def _getMovieUrl(link):
	response = requests.get(link)
	soup = BeautifulSoup(response.text, "html.parser")
	detail = soup.findAll("div", {"class": "separator"})
	
	try:
		link = str(detail[2]).split('href="')
		name = str(soup.findAll("span")[2]).split('Titulo Original: </b>')[1].replace("</span>", "")
		return {"url": link[1].split('"')[0], "name": name}
	except:
		return "" 
		  	
downloads = []
 	
for page in range(1, 10):
	links = _getMoviesByPage(page)

	for movie in links:
		url = _getMovieUrl(movie)
		if (url != ""):
			downloads.append(url)

for downloadMovieUrl in downloads:
		print(downloadMovieUrl)