import json

from requests import Session

from Anilibria.Dto.animeLibria import AnimeLibria
from Anilibria.Dto.torrentLibria import TorrentLibria


class Anilibria:
    __BASE_URL = 'https://www.anilibria.tv'
    __SEARCH_URL = __BASE_URL + '/public/api/index.php'

    def __get_dto_from_str(self, res):
        animes = []

        for anime in res.get('data'):
            torrents = []
            for torrent in anime.get('torrents'):
                t = TorrentLibria(id=torrent.get('id'), quality=torrent.get('quality'), series=torrent.get('series'),
                                  url=self.__BASE_URL+torrent.get('url'))
                torrents.append(t)

            anime_r = AnimeLibria(id=anime.get('id'), name_ru=anime.get('names')[0], name=anime.get('names')[1],
                                series=anime.get('series'), poster=self.__BASE_URL+anime.get('poster'),
                                status=anime.get('status'), type=anime.get('type'), year=anime.get('year'),
                                torrents=torrents)
            animes.append(anime_r)
        return animes

    def get_search_anime(self, search: str, filters: str = None,
                         rm: str = None, page: int = 1, per_page: int = 15) -> list[AnimeLibria]:
        #if filters is None:
        #    filters = 'names, series, poster, status, type, year, torrents'
        ses = Session()

        params = {'query': 'search', 'search': search, 'filter': filters, 'rm': rm, 'page': page, 'perPage': per_page}
        req = ses.post(url=self.__SEARCH_URL, data=params)
        r = json.loads(req.text)
        animes = self.__get_dto_from_str(json.loads(req.text))
        return animes

