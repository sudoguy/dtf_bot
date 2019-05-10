import logging

from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery import group

from base.exceptions import InternalServiceError
from base.models import Entry, SkippedEntry
from base.utils.dtf_helper import DTFHelper
from dtf_bot.celery import app


@app.task(
    autoretry_for=(InternalServiceError,),
    max_retries=20,
    retry_backoff=True,
    retry_backoff_max=30,
    rate_limit="5/s",
)
def update_entry(entry_id: int):
    dtf = DTFHelper()
    dtf.pull_entry(entry_id)


@periodic_task(
    run_every=(crontab(minute="*/1")), name="task_update_last_entries", ignore_result=True
)
def task_update_last_entries():
    dtf = DTFHelper()
    last_id = dtf.last_entry_id()
    if Entry.objects.filter(id=last_id).exists():
        logging.info("New entries not found")
        return

    url = "timeline/index/recent"

    result = dtf.send_request(url)

    for entry in result:
        entry_id = entry["id"]

        dtf.pull_entry(entry_id, entry)


@periodic_task(
    run_every=(crontab(minute="*/5")), name="task_update_all_entries", ignore_result=True
)
def task_update_all_entries():
    dtf = DTFHelper()
    last_id = dtf.last_entry_id()

    all_entries_ids = range(1, last_id)

    existed_entries = Entry.objects.filter(id__in=range(1, last_id)).values_list("id", flat=True)
    skipped_entries = SkippedEntry.objects.values_list("id", flat=True)

    not_existed_entries = set(all_entries_ids) - set(existed_entries) - set(skipped_entries)

    job = group([update_entry.s(entry_id) for entry_id in not_existed_entries][:500])

    job.apply_async()
