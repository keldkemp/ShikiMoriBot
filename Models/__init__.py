from Models.models import *

list_models = {
    Users().__str__(): Users(),
    AnimeTypes().__str__(): AnimeTypes(),
    AnimeStatus().__str__(): AnimeStatus(),
    Anime().__str__(): Anime(),
    Manga().__str__(): Manga(),
    UserRates().__str__(): UserRates(),
    SettingsListAnime().__str__(): SettingsListAnime()
    }
