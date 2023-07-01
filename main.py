import argparse
import sys
from MovieScanner import movieFolderScan
from FirebaseUpload import sync_data, import_data


class MoviewCLI(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Welcome to Moview',
            usage='''moview <command> [<args>]

The most commonly used moview commands are:
   sync     Scan folder filled with movies and sync it
   upload   Upload new folder filled with movies
''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def sync(self):
        parser = argparse.ArgumentParser(
            description='Scan folder filled with movies and sync it')
        parser.add_argument('directory')
        args = parser.parse_args(sys.argv[2:])
        scanned_movies: list
        try:
            scanned_movies = movieFolderScan(args.directory)
        except:
            print('Invalid Path')
        if input("Do you want to sync the list with the database? y/n") == "y":
            sync_data(scanned_movies, 'movies_test')
        else:
            print('aborted')

    def upload(self):
        parser = argparse.ArgumentParser(
            description='Scan and upload a new folder filled with movies')
        parser.add_argument('directory')
        args = parser.parse_args(sys.argv[2:])
        scanned_movies: list
        try:
            scanned_movies = movieFolderScan(args.directory)
            if input("Do you want to upload the list in the database? y/n") == "y":
                import_data(scanned_movies, 'movies_test')
            else:
                print('aborted')
        except Exception as e:
            print('Invalid Path:', e)


if __name__ == '__main__':
    MoviewCLI()
