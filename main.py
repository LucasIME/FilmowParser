from config import *
from FilmowParser import FilmowParser
import json

def durationStrToInt(input):
    durationStr = input['duration']
    durationInt = int(durationStr.split(' ')[0])
    return durationInt

def main():
    print(config)
    filmowparser = FilmowParser(config['filmowURL'], config['filmowUsername'])
    moviesVec = filmowparser.getWantToSeeMovies()
    moviesVec.sort(key=durationStrToInt)
    print(moviesVec)
    with open('movies.json', 'w') as file:
        json.dump(moviesVec, file, sort_keys=True, indent=4, separators=(',',': '), ensure_ascii=False)

if __name__ == '__main__':
    main()
