

class MainCache:

    __CACHE = {}

    def add(self, key: str, value) -> None:
        self.__CACHE[key] = value

    def remove(self, key: str) -> None:
        self.__CACHE.pop(key)

    def get(self, key: str):
        return self.__CACHE.get(key)

    def clear_all(self):
        self.__CACHE = {}
