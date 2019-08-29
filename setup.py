import requests
import urllib.request
import time
import json
from bs4 import BeautifulSoup

TITLE = 'Titulo Original: </b>'
MOVIE_URI = "https://filmesnomega.info/page/"
API_KEY = "PlzBanMe"
OMDB_URI = "http://www.omdbapi.com/?t="


def getMoviesByPage(page):
    links = []
    response = requests.get(MOVIE_URI + str(page))
    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.findAll("a", {"class": "readmore"})

    for post in posts:
        links.append(post['href'])

    return links


def getMovieUrl(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    detail = soup.findAll("div", {"class": "separator"})

    try:
        link = str(detail[2]).split('href="')
        name = str(soup.findAll("span")[2]).split(TITLE)[1].replace('</span>', '')
        return {"url": link[1].split('"')[0], "name": name, "imdb": _imdbSearch(name)}
    except:
        return ""


def _imdbSearch(movieName):
    response = requests.get(OMDB_URI + movieName + "&apikey=" + API_KEY)
    imdbResult = json.loads(response.text)
    return imdbResult['imdbID']



downloads = []

for page in range(1, 10):
    links = getMoviesByPage(page)

    for movie in links:
        url = getMovieUrl(movie)
        if url != "":
            downloads.append(url)

for downloadMovieUrl in downloads:
    print(downloadMovieUrl)



