import json
from requests import Session


class GitHub:
    BASE_URL = 'https://api.github.com/'

    def get_commits(self, repo_name: str) -> list:
        s = Session()
        js = s.get(self.BASE_URL + 'repos/' + repo_name + '/commits')
        return json.loads(js.text)

    def get_info_about_commit(self, repo_name: str, sha_commit: str) -> dict:
        s = Session()
        js = s.get(self.BASE_URL + 'repos/' + repo_name + '/commits/' + sha_commit)
        return json.loads(js.text)

    def get_file_body(self, file_link: str) -> str:
        s = Session()
        content = s.get(file_link)
        return content.text
