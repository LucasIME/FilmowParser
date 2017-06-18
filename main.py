from config import *
from FilmowParser import FilmowParser
import json
import time

def durationStrToInt(input):
    durationStr = input['duration']
    durationInt = int(durationStr.split(' ')[0])
    return durationInt

def netflixStrToInt(input):
    durationStr = input['runtime']
    durationInt = 0
    if durationStr != "N/A":
        durationInt = int(durationStr.split(' ')[0])
    return durationInt

def filterNetflix(moviesVec):
    return [ {'runtime' : movie['runtime'], 'Title' : movie['show_title'], 'rating':movie['rating']} for movie in moviesVec]

def main():
    filmowparser = FilmowParser(config['filmowURL'], config['filmowUsername'])

    print ('Started time tracking')
    timeStart = time.time()

    result = filmowparser.getWantToSeeMovies()
    moviesVec = result[0]
    netflixVec = result[1]

    timeEnd = time.time()
    print('Elapsed time: {}'.format(timeEnd - timeStart))

    moviesVec.sort(key=durationStrToInt)
    print(moviesVec)
    with open('movies.json', 'w') as file:
        json.dump(moviesVec, file, sort_keys=True, indent=4, separators=(',',': '), ensure_ascii=False)

    print("\n\n")

    netflixVec.sort(key=netflixStrToInt)
    print(netflixVec)
    netflixVec = filterNetflix(netflixVec)
    with open('netflix.json', 'w') as file:
        json.dump(netflixVec, file, sort_keys=True, indent=4, separators=(',',': '), ensure_ascii=False)

if __name__ == '__main__':
    main()
