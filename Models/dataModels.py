import datetime


class SettingsListAnime:
    def __init__(self, id: int = None, name: str = None):
        self.id = id
        self.name = name


class Users:
    def __init__(self, id: int = None, token: str = None, refresh_token: str = None, tg_id: int = None,
                list_settings: int = None, search: str = None, is_notify: int = None,
                filter_anime: int = None):
        self.id = id
        self.token = token
        self.refresh_token = refresh_token
        self.tg_id = tg_id
        self.list_settings = list_settings
        self.search = search
        self.is_notify = is_notify
        self.filter_anime = filter_anime


class AnimeTypes:
    def __init__(self, id: int = None, name: str = None):
        self.id = id
        self.name = name


class AnimeStatus:
    def __init__(self, id: int = None, name: str = None):
        self.id = id
        self.name = name


class Anime:
    def __init__(self, id: int = None, name: str = None, name_ru: str = None, name_jp: str = None,
                kind: str = None, score: str = None, status: str = None,
                episodes: int = None, episodes_aired: int = None, aired_on: datetime = None,
                released_on: datetime = None, rating: str = None, updated_at: datetime = None,
                next_episode_at: datetime = None, description: str = None, url: str = None,
                franchise: str = None):
        self.id = id
        self.name = name
        self.name_ru = name_ru
        self.name_jp = name_jp
        self.kind = kind
        self.score = score
        self.status = status
        self.episodes = episodes
        self.episodes_aired = episodes_aired
        self.aired_on = aired_on
        self.released_on = released_on
        self.rating = rating
        self.updated_at = updated_at
        self.next_episode_at = next_episode_at
        self.description = description
        self.url = url
        self.franchise = franchise


class Manga:
    def __init__(self, id: int = None, name: str = None, name_ru: str = None, name_jp: str = None,
                kind: str = None, score: str = None, status: str = None,
                volumes: int = None, chapters: int = None, aired_on: datetime = None,
                released_on: datetime = None, description: str = None, url: str = None,
                franchise: str = None):
        self.id = id
        self.name = name
        self.name_ru = name_ru
        self.name_jp = name_jp
        self.kind = kind
        self.score = score
        self.status = status
        self.volumes = volumes
        self.chapters = chapters
        self.aired_on = aired_on
        self.released_on = released_on
        self.description = description
        self.url = url
        self.franchise = franchise


class UserRates:
    def __init__(self, id: int = None, user_id: int = None, target_id: int = None, target_type: int = None,
                score: int = None, status: int = None, rewatches: int = None,
                episodes: int = None, volumes: int = None, chapters: int = None,
                text: str = None, created_at: datetime = None, updated_at: datetime = None,
              ):
        self.id = id
        self.user_id = user_id
        self.target_id = target_id
        self.target_type = target_type
        self.score = score
        self.status = status
        self.rewatches = rewatches
        self.episodes = episodes
        self.volumes = volumes
        self.chapters = chapters
        self.text = text
        self.created_at = created_at
        self.updated_at = updated_at
