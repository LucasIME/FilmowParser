import queue
from threading import Thread
import urllib.request, urllib.error, urllib.parse

class ThreadPool:
    def __init__(self, n):
        self.nThreads = n
        self.queue = queue.Queue()

    def startWorking(self):
        self.spawnThreads()

    def worker(self):
        while True:
            work, args = self.queue.get()
            work(**args)
            self.queue.task_done()

    def spawnThreads(self):
        for i in range(self.nThreads):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

    def end(self):
        self.queue.join()

    def putInQueue(self, func, args_dict):
        self.queue.put((func, args_dict))