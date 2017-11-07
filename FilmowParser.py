import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
from threading import Thread
import time
import queue
from ThreadPool import ThreadPool
from NetflixWrapper import NetflixWrapper


class FilmowParser():
    def __init__(self, baseURL, username):
        self.baseURL = baseURL
        self.username = username
        self.hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

    def getWantToSeePages(self):
        want_to_see_url = self.baseURL + '/usuario/' + self.username + '/quero-ver/';
        wantToSeeCatalogueHTML = urllib.request.urlopen(urllib.request.Request(want_to_see_url, headers=self.hdr))
        catalogueSoup = BeautifulSoup(wantToSeeCatalogueHTML, 'html.parser')
        page_list = catalogueSoup.find('div', class_="pagination pagination-centered").find_all('a')
        last_page_index = 1
        for page in page_list:
            page_index = int(page['href'].split('=')[-1])
            last_page_index = max(page_index, last_page_index)
        return last_page_index

    def getWantToSeeMovies(self):

        searchURL = self.baseURL + '/usuario/' + self.username + '/quero-ver/';

        moviesVec = []
        netflixVec = []

        nThreads = 8
        threadPool = ThreadPool(nThreads)
        threadPool.startWorking()

        def parsePage(pageUrl):
            wantToSeeCatalogueHTML = urllib.request.urlopen(urllib.request.Request(pageUrl, headers=self.hdr))
            catalogueSoup = BeautifulSoup(wantToSeeCatalogueHTML, 'html.parser')
            print(pageUrl)
            #looping through each movie in the current page
            for movieDiv in catalogueSoup.findAll('li', { 'class': 'span2 movie_list_item'}):
                divSoup = BeautifulSoup(str(movieDiv), 'html.parser')
                moviehref = str(divSoup.find("a")['href'])
                print(moviehref)
                movieURL = self.baseURL + moviehref
                threadPool.putInQueue(parseMovie, {"movieURL": movieURL})
        
        def parseMovie(movieURL):
            movie = {}
            moviePageHtml = urllib.request.urlopen(urllib.request.Request(movieURL, headers=self.hdr))
            moviePageSoup = BeautifulSoup(moviePageHtml, 'html.parser')
            movie['name'] = str(moviePageSoup.find('h2',{'class':'movie-original-title'}).string)
            movie['duration'] = str(moviePageSoup.find('span',{'class':'running_time'}).string)
            print(movie)
            moviesVec.append(movie)
            threadPool.putInQueue(checkNetflix, {'title': movie['name']})

        def checkNetflix(title):
            netflixWrapper = NetflixWrapper()
            resp = netflixWrapper.isTitleInNetflix(title)
            if(resp[0]):
                netflixVec.append(resp[1])

        for i in range(1, self.getWantToSeePages() + 1):
            pageUrl = searchURL + '?pagina=' + str(i)
            threadPool.putInQueue(parsePage, {'pageUrl': pageUrl})
        
        #block until all tasks are done
        threadPool.end()

        return [moviesVec, netflixVec]
