import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
from threading import Thread
import time
import queue

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

        q = queue.Queue()
        nThreads = 8

        def parsePage(pageUrl):
            wantToSeeCatalogueHTML = urllib.request.urlopen(urllib.request.Request(pageUrl, headers=hdr))
            catalogueSoup = BeautifulSoup(wantToSeeCatalogueHTML, 'html.parser')
            print(pageUrl)
            #looping through each movie in the current page
            for movieDiv in catalogueSoup.findAll('li', { 'class': 'span2 movie_list_item'}):
                divSoup = BeautifulSoup(str(movieDiv), 'html.parser')
                moviehref = str(divSoup.find("a")['href'])
                print(moviehref)
                movieURL = self.baseURL + moviehref
                q.put({'type':'movie', 'url':movieURL})
        
        def parseMovie(movieURL):
            movie  = {}
            moviePageHtml = urllib.request.urlopen(urllib.request.Request(movieURL, headers=hdr))
            moviePageSoup = BeautifulSoup(moviePageHtml, 'html.parser')
            movie['name'] = str(moviePageSoup.find('h2',{'class':'movie-original-title'}).string)
            movie['duration'] = str(moviePageSoup.find('span',{'class':'running_time'}).string)
            print(movie)
            moviesVec.append(movie)

        def worker():
            while True:
                work = q.get()
                if work == None:
                    break
                elif work['type'] == 'page':
                    parsePage(work['url'])
                elif work['type'] == 'movie':
                    parseMovie(work['url'])
                q.task_done()

        for i in range(nThreads):
            t = Thread(target = worker)
            #t.daemon = True
            t.start()
            threadList.append(t)

        for i in range(1, self.getWantToSeePages() + 1):
            pageUrl = searchURL + '?pagina=' + str(i)
            q.put({'type':'page', 'url':pageUrl})

        q.join()

        for i in range(nThreads):
            q.put(None)
        for t in threadList:
            t.join()

        return moviesVec
