"""
    Celery tasks. Some of them will be launched periodically from admin panel via django-celery-beat
"""

import time
from typing import Union, List, Optional, Dict

import telegram
from celery.utils.log import get_task_logger

from dtb.celery import app
from tgbot.handlers.broadcast_message.utils import _send_message, _from_celery_entities_to_entities, \
    _from_celery_markup_to_markup, _send_photo

logger = get_task_logger(__name__)


@app.task(ignore_result=True)
def broadcast_message(
        user_ids: List[Union[str, int]],
        text: str,
        entities: Optional[List[Dict]] = None,
        reply_markup: Optional[List[List[Dict]]] = None,
        sleep_between: float = 0.4,
        parse_mode=telegram.ParseMode.HTML,
) -> None:
    """ It's used to broadcast message to big amount of users """
    logger.info(f"Going to send message: '{text}' to {len(user_ids)} users")

    entities_ = _from_celery_entities_to_entities(entities)
    reply_markup_ = _from_celery_markup_to_markup(reply_markup)
    for user_id in user_ids:
        try:
            _send_message(
                user_id=user_id,
                text=text,
                entities=entities_,
                parse_mode=parse_mode,
                reply_markup=reply_markup_,
            )
            logger.info(f"Broadcast message was sent to {user_id}")
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}, reason: {e}")
        time.sleep(max(sleep_between, 0.1))

    logger.info("Broadcast finished!")


from datetime import datetime
from django.conf import settings
from hfspace.anime import to_anime, to_dragness, to_jojo


@app.task(ignore_result=True)
def animefy(user_id: int, image_path: str):
    file_timestamp = int(datetime.now().timestamp())
    out_put = f"{settings.MEDIA_ROOT}/image/output_anime_{file_timestamp}.png"
    to_anime(image_path, out_put)
    _send_message(
        user_id=user_id,
        text="Думаю какой ты анимешник")
    _send_photo(user_id=user_id,
                photo_path=f"{settings.MEDIA_ROOT}/image/output_anime_{file_timestamp}.png")


@app.task(ignore_result=True)
def dragnify(user_id: int, image_path: str):
    file_timestamp = int(datetime.now().timestamp())
    out_put = f"{settings.MEDIA_ROOT}/image/output_dragness_{file_timestamp}.png"
    to_dragness(image_path, out_put)
    _send_message(
        user_id=user_id,
        text="Думаю какая ты Dragness")
    _send_photo(user_id=user_id,
                photo_path=f"{settings.MEDIA_ROOT}/image/output_dragness_{file_timestamp}.png")


@app.task(ignore_result=True)
def jojofy(user_id: int, image_path: str):
    file_timestamp = int(datetime.now().timestamp())
    out_put = f"{settings.MEDIA_ROOT}/image/output_jojo_{file_timestamp}.png"
    to_jojo(image_path, out_put)
    _send_message(
        user_id=user_id,
        text="Думаю какой ты jojo")
    _send_photo(user_id=user_id,
                photo_path=f"{settings.MEDIA_ROOT}/image/output_jojo_{file_timestamp}.png")
