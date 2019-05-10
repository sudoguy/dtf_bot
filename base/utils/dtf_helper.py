import logging

from base.models import Entry, SkippedEntry
from base.exceptions import EntryNotFound

from .base_helper import BaseHelper


class DTFHelper(BaseHelper):
    base_url = "https://api.dtf.ru/v1.6/"

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
        except EntryNotFound:
            SkippedEntry.objects.update_or_create(id=entry_id)
            logging.info(f"Entry #{entry_id} not found, skipped")

            return

        entry_id = entry["id"]
        title = entry["title"]
        intro = entry["intro"]

        defaults = {"title": title, "intro": intro, "last_response": entry}
        saved_entry, created = Entry.objects.update_or_create(id=entry_id, defaults=defaults)

        action = "Created" if created else "Updated"
        logging.info(f"{action} entry #{entry_id}")
