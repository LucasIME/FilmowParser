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