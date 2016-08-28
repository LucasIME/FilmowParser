from config import *
from FilmowParser import FilmowParser
import json

def movieCmp(movie1, movie2):
    duration1 = int(movie1['duration'].split(' ')[0])
    duration2 = int(movie2['duration'].split(' ')[0])
    if duration1 < duration2:
        return -1
    elif duration1 > duration2:
        return 1
    else:
        return 0

def main():
    print config
    filmowparser = FilmowParser(config['filmowURL'], config['filmowUsername'])
    moviesVec = filmowparser.getWantToSeeMovies()
    moviesVec.sort(cmp=movieCmp)
    print moviesVec
    with open('movies.json', 'w') as file:
        json.dump(moviesVec, file, sort_keys=True, indent=4, separators=(',',': '))

if __name__ == '__main__':
    main()
