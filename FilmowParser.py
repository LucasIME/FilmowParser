import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
from threading import Thread
import time

class FilmowParser():
    def __init__(self, baseURL, username):
        self.baseURL = baseURL
        self.username = username

    def getWantToSeePages(self):
        return 6

    def getWantToSeeMovies(self):
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        searchURL = self.baseURL + '/usuario/' + self.username + '/quero-ver/';

        moviesVec = []

        threadList = []

        def parsePage(i):
            wantToSeeCatalogueHTML = urllib.request.urlopen(urllib.request.Request(searchURL + '?pagina=' + str(i) , headers=hdr))
            catalogueSoup = BeautifulSoup(wantToSeeCatalogueHTML)
            print(searchURL + '?pagina=' + str(i))
            #looping through each movie in the current page
            for movieDiv in catalogueSoup.findAll('li', { 'class': 'span2 movie_list_item'}):
                divSoup = BeautifulSoup(str(movieDiv))
                moviehref = str(divSoup.find("a")['href'])
                print(moviehref)
                movieURL = self.baseURL + moviehref
                movie  = {}
                moviePageHtml = urllib.request.urlopen(urllib.request.Request(movieURL, headers=hdr))
                moviePageSoup = BeautifulSoup(moviePageHtml)
                movie['name'] = str(moviePageSoup.find('h2',{'class':'movie-original-title'}).string)
                movie['duration'] = str(moviePageSoup.find('span',{'class':'running_time'}).string)
                print(movie)
                moviesVec.append(movie)

        #looping through all the pages of 'want to see' movies
        for i in range(1, self.getWantToSeePages() +1):

            thread = Thread(target=parsePage, args=(i,))
            thread.start()
            time.sleep(0.1)
            threadList.append(thread)

        for thread in threadList:
            thread.join()

        return moviesVec
