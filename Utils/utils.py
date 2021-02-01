import datetime


class Utils:
    @staticmethod
    def get_value_in_dict(d: dict, key: str):
        return d.get(key)

    @staticmethod
    def chunkify(items, chunk_size):
        for i in range(0, len(items), chunk_size):
            yield items[i:i + chunk_size]

    @staticmethod
    def get_date_now_sec() -> str:
        return str(datetime.datetime.now())
