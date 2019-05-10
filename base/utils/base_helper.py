import os
from urllib.parse import urljoin

from base.exceptions import EntryNotFound, InternalServiceError

import requests


class BaseHelper:
    headers = {"X-Device_Token": os.getenv("DTF_TOKEN")}
    base_url = "https://api.dtf.ru"

    def send_request(self, url: str):
        _url = urljoin(self.base_url, url)

        response = requests.get(_url, headers=self.headers)
        if response.status_code == 404:
            raise EntryNotFound
        if not response:
            raise InternalServiceError(
                f"Bad request. url: {_url}, status: {response.status_code}, body: {response.text}"
            )
        result = response.json()["result"]

        return result
