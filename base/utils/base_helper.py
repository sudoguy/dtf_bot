import logging
import os
from urllib.parse import urljoin

from base.exceptions import ObjectNotFound, InternalServiceError

import requests


class BaseHelper:
    headers = {"X-Device_Token": os.getenv("DTF_TOKEN")}
    base_url = "https://api.dtf.ru"

    def send_request(self, url: str):
        _url = urljoin(self.base_url, url)

        response = requests.get(_url, headers=self.headers)
        if response.status_code in (403, 404, 500):
            logging.info(f"Bad response - url: {_url}, status_code: {response.status_code}")
            raise ObjectNotFound
        if not response:
            raise InternalServiceError(
                f"Bad request. url: {_url}, status: {response.status_code}, body: {response.text}"
            )
        result = response.json()["result"]

        return result
