from config import *
from FilmowParser import FilmowParser

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

if __name__ == '__main__':
    main()
