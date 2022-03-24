from Anilibria.Dto.torrentLibria import TorrentLibria


class AnimeLibria:
    def __init__(self, id: int, name_ru: str, name: str, series: str,
                 poster: str, status: str, type: str, year: str, torrents: [TorrentLibria]):
        self.id = id
        self.name_ru = name_ru
        self.name = name
        self.series = series
        self.poster = poster
        self.status = status
        self.type = type
        self.year = year
        self.torrents = torrents
