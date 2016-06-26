from config import *
from FilmowParser import FilmowParser

def main():
    print config
    filmowparser = FilmowParser(config['filmowURL'], config['filmowUsername'])
    print filmowparser.getWantToSeeMovies()

if __name__ == '__main__':
    main()
