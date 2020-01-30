import logging

from base.models import Entry, Skipped, User
from base.exceptions import ObjectNotFound

from .base_helper import BaseHelper


class DTFHelper(BaseHelper):
    base_url = "https://api.dtf.ru/v1.8/"

    def last_entry_id(self):
        url = "timeline/index/recent?count=1"
        result = self.send_request(url)
        last_id = result[0]["id"]

        return last_id

    def pull_entry(self, entry_id: int, entry: dict = None):
        url = f"entry/{entry_id}"
        try:
            if not entry:
                entry = self.send_request(url)
        except ObjectNotFound:
            Skipped.objects.update_or_create(object_type="entry", object_id=entry_id)
            logging.info(f"Entry #{entry_id} not found, skipped")

            return

        entry_id = entry["id"]
        title = entry["title"]
        intro = entry["intro"]

        defaults = {"title": title, "intro": intro, "last_response": entry}
        _, created = Entry.objects.update_or_create(id=entry_id, defaults=defaults)

        action = "Created" if created else "Updated"
        logging.info(f"{action} entry #{entry_id}")

    def pull_user(self, user_id: int):
        url = f"user/{user_id}"
        try:
            user = self.send_request(url)
        except ObjectNotFound:
            Skipped.objects.update_or_create(object_type="user", object_id=user_id)
            logging.info(f"user #{user_id} not found, skipped")

            return
        user_id = user["id"]
        name = user["name"]
        url = user["url"]
        avatar_url = user["avatar_url"]

        defaults = {"name": name, "url": url, "avatar_url": avatar_url, "last_response": user}
        _, created = User.objects.update_or_create(id=user_id, defaults=defaults)

        action = "Created" if created else "Updated"
        logging.info(f"{action} user #{user_id}")
