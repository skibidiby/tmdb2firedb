import os
from tmdbv3api import TMDb, Movie
import json
tmdb = TMDb()
tmdb.api_key = ''


class Movie_Object:
    movies = []

    def newMovie(id: int, title: str, content: str, background: str, cover: str, rating: int, cast: list, trailer: str, pc: str, parent_directory: str, movie_folder: str, file_name: str, ):
        movie = {
            "id": id,
            "title": title,
            "content": content,
            "background": background,
            "cover": cover,
            "rating": rating,
            "cast": cast,
            "trailer": trailer,
            "pc": pc,
            "parent_directory": parent_directory,
            "movie_folder": movie_folder,
            "file_name": file_name,
        }
        return movie


# FETCHING MOVIE DATA AND CREATING OBJECT
def movieInfo(name: str, parent_directory: str, movie_folder: str, file_name: str,):
    id: int
    title: str
    content: str
    background: str
    cover: str
    rating: int
    cast_objects: list
    cast=[]
    pc = os.environ['COMPUTERNAME']
    movie = Movie()
    search = movie.search(name)
    if(search):
        id = search[0].id
        title = search[0].title
        content = search[0].overview
        background = search[0].backdrop_path
        cover = search[0].poster_path
        rating = search[0].vote_average
        cast_objects = movie.credits(id).cast[0:4]
        for i in cast_objects:
            actor = {
                "gender": i.gender,
                "id": i.id,
                "known_for_department": i.known_for_department,
                "name": i.name,
                "popularity": i.popularity,
                "profile_path": i.profile_path,
                "character": i.character,
                "cast_id": i.cast_id,
                "credit_id": i.credit_id,
                "order": i.order
            }
            cast.append(actor)
        trailer = movie.videos(id)[0].key
        movie_info = Movie_Object.newMovie(
            id, title, content, background, cover, rating, cast, trailer, pc, parent_directory, movie_folder, file_name,)
        jsonStr = json.dumps(movie_info, default=lambda o: o.__dict__,
                             sort_keys=True, indent=4)
        # print(jsonStr)
        Movie_Object.movies.append(movie_info)
    else:
        print(name, ' not found')


# SCAN FOLDER FOR MOVIES
def movieFolderScan(directory):
    extensions = ('.avi', '.mkv', '.wmv', '.mp4',
                  '.mpg', '.mpeg', '.mov', '.m4v')
    invaild_videos = ('sample', 'trailer')
    movie_folder: str
    file_name: str

    for name in os.listdir(directory):
        if os.path.isdir(directory+"/"+name):
            movie_folder = name
            name_arr = name.split('.')
            for file in os.listdir(directory + "/" + name):
                if file.endswith(extensions):
                    if not file.lower().startswith(invaild_videos):
                        file_name = file
            for i, c in enumerate(name_arr):
                if c.isdigit():
                    number_id = i
                    name_str = '+'.join(name_arr[0:i])
                    print(name)
                    movieInfo(name_str, directory, movie_folder, file_name)
                    break
    return Movie_Object.movies
