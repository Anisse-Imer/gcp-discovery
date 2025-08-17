import json

class Movie:
    imdb:str
    title:str
    year:int
    rank:int
    actors:list[str]
    aka:str

    __imdb_url:str
    __imdb_iv:str
    __img_poster:str
    __photo_width:int
    __photo_height:int

    def __init__(self, dict:dict={}):
        self.title = dict.get("#TITLE", None)
        self.year = dict.get("#YEAR", None)
        self.imdb = dict.get("#IMDB_ID", None)
        self.rank = dict.get("#RANK", None)
        self.aka = dict.get("#AKA", None)

        self.actors = dict.get("#ACTORS", "").split(", ")

        self.__imdb_url = dict.get("#IMDB_URL", None)
        self.__imdb_iv = dict.get("#IMDB_IV", None)
        self.__img_poster = dict.get("#IMG_POSTER", None)
        self.__photo_width = dict.get("photo_width", None)
        self.__photo_height = dict.get("photo_height", None)

    def to_dict(self) ->  dict:
        return {
            "imdb" : self.imdb,
            "title" : self.title,
            "year" : self.year,
            "rank" : self.rank,
            "aka" : self.aka,
            "actors" : self.actors,

            "imdb_url" : self.__imdb_url,
            "imdb_iv" : self.__imdb_iv,
            "img_poster" : self.__img_poster,

            "photo_width" : self.__photo_width,
            "photo_height" : self.__photo_height,
        }

    def __str__(self):
        return json.dumps(self.to_dict(), indent=2)
    
    def __repr__(self):
        return json.dumps(self.to_dict(), indent=2)
