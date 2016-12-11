import urllib.request, urllib.error, urllib.parse
import json

class NetflixWrapper:
    def __init__(self):
        self.baseURL = "http://netflixroulette.net/api/api.php?title="
    def isTitleInNetflix(self, title):
        try:
            response = urllib.request.urlopen(urllib.request.Request("http://netflixroulette.net/api/api.php?title=" + str(title)))
        except:
            return (False, {"errorcode":404,"message":"Sorry! We couldn\'t find a movie with that title!"})
        else:
            jsonResponse= json.loads(response.read().decode())
            print("%s is in Netflix!" % title)
            return (True, jsonResponse)