from config import *
from FilmowParser import FilmowParser
import json
import time

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

    print(netflixVec)
    with open('netflix.json', 'w') as file:
        json.dump(netflixVec, file, sort_keys=True, indent=4, separators=(',',': '), ensure_ascii=False)

if __name__ == '__main__':
    main()
