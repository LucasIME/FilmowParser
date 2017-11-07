import urllib.request, urllib.error, urllib.parse
import json
import os

class NetflixWrapper:
    def __init__(self):
        self.baseURL = "http://netflixroulette.net/api/api.php?title="
        self.hdr = {
            "X-Mashape-Key": os.environ['MASHAPE_KEY'],
            "Accept": "application/json"
        }
    def isTitleInNetflix(self, title):
        try:
            response = urllib.request.urlopen(urllib.request.Request("https://utelly-tv-shows-and-movies-availability-v1.p.mashape.com/lookup?country=us&term={0}".format(title), headers=self.hdr))
        except:
            return (False, {"errorcode":404,"message":"Sorry! We couldn\'t find a movie with that title!"})
        else:
            jsonResponse= json.loads(response.read().decode())
            print(jsonResponse)
            for movie_obj in jsonResponse['results']:
                if movie_obj['name'] == title:
                    for location in movie_obj['locations']:
                        if "Netflix" in location['name']:
                            print("{0} is in Netflix!".format(title))
                            return (True, {'title': title, 'url': location['url']})

            return (False, {"errorcode":404,"message":"Sorry! We couldn\'t find a movie with that title!"})