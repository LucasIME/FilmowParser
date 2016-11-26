from config import *
from FilmowParser import FilmowParser
import json
import time

def durationStrToInt(input):
    durationStr = input['duration']
    durationInt = int(durationStr.split(' ')[0])
    return durationInt

def main():
    filmowparser = FilmowParser(config['filmowURL'], config['filmowUsername'])

    print ('Started time tracking')
    timeStart = time.time()

    moviesVec = filmowparser.getWantToSeeMovies()

    timeEnd = time.time()
    print('Elapsed time: {}'.format(timeEnd - timeStart))

    moviesVec.sort(key=durationStrToInt)

    print(moviesVec)
    
    with open('movies.json', 'w') as file:
        json.dump(moviesVec, file, sort_keys=True, indent=4, separators=(',',': '), ensure_ascii=False)

if __name__ == '__main__':
    main()
