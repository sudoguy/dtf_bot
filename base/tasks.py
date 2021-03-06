import logging
from datetime import timedelta

from celery import group
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from base.exceptions import InternalServiceError
from base.models import Comment, Entry, Skipped, User
from base.utils.dtf_helper import DTFHelper
from dtf_bot.celery import app


@app.task(
    autoretry_for=(InternalServiceError,), max_retries=20, retry_backoff=True, retry_backoff_max=30
)
def handle_comment(data: dict):
    entry_id = data["content"]["id"]

    try:
        entry = Entry.objects.get(id=entry_id)
    except ObjectDoesNotExist:
        update_entry(entry_id)
        entry = Entry.objects.get(id=entry_id)

    reply_to = data["reply_to"]["id"] if data["reply_to"] else None
    creator_id = data["creator"]["id"]

    time_threshold = timezone.now() - timedelta(days=7)
    need_to_update = User.objects.filter(id=creator_id, updated_at__lt=time_threshold).exists()
    if need_to_update:
        update_user.delay(creator_id)
    else:
        logging.info(f"User #{creator_id} was updated recently, skipped update")

    new_comment = Comment(
        id=data["id"], text=data["text"], reply_to=reply_to, last_response=data, entry=entry
    )
    new_comment.save()
    logging.info(f"Created comment #{data['id']}")


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


@app.task(
    autoretry_for=(InternalServiceError,),
    max_retries=20,
    retry_backoff=True,
    retry_backoff_max=30,
    rate_limit="5/s",
)
def update_user(user_id: int):
    dtf = DTFHelper()
    dtf.pull_user(user_id)


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
    run_every=(crontab(hour="*/4", minute="0")), name="task_update_all_entries", ignore_result=True
)
def task_update_all_entries():
    dtf = DTFHelper()
    last_id = dtf.last_entry_id()

    all_entries_ids = range(1, last_id)

    existed_entries = Entry.objects.filter(id__in=range(1, last_id)).values_list("id", flat=True)
    skipped_entries = Skipped.objects.filter(object_type="entry").values_list(
        "object_id", flat=True
    )

    not_existed_entries = set(all_entries_ids) - set(existed_entries) - set(skipped_entries)

    job = group([update_entry.s(entry_id) for entry_id in not_existed_entries][:500])

    job.apply_async()


@periodic_task(
    run_every=(crontab(hour="*/3", minute="0")), name="task_update_all_users", ignore_result=True
)
def task_update_all_users():
    last_id = User.objects.latest("id").id

    all_users_ids = range(1, last_id)

    existed_users = User.objects.filter(id__in=range(1, last_id)).values_list("id", flat=True)
    skipped_users = Skipped.objects.filter(object_type="user").values_list("object_id", flat=True)

    not_existed_users = set(all_users_ids) - set(existed_users) - set(skipped_users)

    job = group([update_user.s(user_id) for user_id in not_existed_users][:500])

    job.apply_async()


@periodic_task(
    run_every=(crontab(hour="*", minute="0")), name="task_check_skipped_users", ignore_result=True
)
def task_check_skipped_users():
    time_threshold = timezone.now() - timedelta(days=7)
    skipped_users = Skipped.objects.filter(
        object_type="user", updated_at__lt=time_threshold
    ).values_list("object_id", flat=True)

    job = group([update_user.s(user_id) for user_id in skipped_users][:500])

    job.apply_async()
