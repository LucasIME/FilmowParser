import queue
from threading import Thread
import urllib.request, urllib.error, urllib.parse

class ThreadPool:
    def __init__(self, n, workerFunc):
        self.nThreads = n
        self.queue = queue.Queue()
        self.workerFunc = workerFunc

    def startWorking(self):
        self.spawnThreads()

    def worker(self):
        while True:
            work = self.queue.get()
            self.workerFunc(work)
            self.queue.task_done()

    def spawnThreads(self):
        for i in range(self.nThreads):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

    def end(self):
        self.queue.join()

    def putInQueue(self, arg):
        self.queue.put(arg)

class FilmowParser():
    def __init__(self, baseURL, username):
        self.baseURL = baseURL
        self.username = username

    def getWantToSeePages(self):
        return 6

        moviesVec = []

        threadList = []

        q = queue.Queue()
        nThreads = 8

        def parsePage(pageUrl):
            wantToSeeCatalogueHTML = urllib.request.urlopen(urllib.request.Request(pageUrl, headers=hdr))
            catalogueSoup = BeautifulSoup(wantToSeeCatalogueHTML, 'html.parser')
            print(pageUrl)
            # looping through each movie in the current page
            for movieDiv in catalogueSoup.findAll('li', {'class': 'span2 movie_list_item'}):
                divSoup = BeautifulSoup(str(movieDiv), 'html.parser')
                moviehref = str(divSoup.find("a")['href'])
                print(moviehref)
                movieURL = self.baseURL + moviehref
                q.put({'type': 'movie', 'url': movieURL})


        def worker(work):
            if work['type'] == 'page':
                parsePage(work['url'])
            elif work['type'] == 'movie':
                parseMovie(work['url'])



        # block until all tasks are done
        q.join()

        return moviesVec
