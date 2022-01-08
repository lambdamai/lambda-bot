import logging

import telegram
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from telegram import ParseMode

from tgbot.models import User
from tgbot.trigger.base import BaseTrigger

logger = logging.getLogger(__name__)


class TelegramTrigger(BaseTrigger):
    """
        Телеграм триггер для State Machine
    """

    def send_keyboard(self, message: str, buttons: list, whom=None):
        """
            Отправка клавиатуры
        :param message: Текст для отправки
        :param buttons: Кнопки для отправки в формате массива
        :param whom: id чата для отправки
        :return: None
        """
        kb = []
        for button in buttons:
            kb.append([telegram.KeyboardButton(button)])
        kb_markup = telegram.ReplyKeyboardMarkup(kb)
        self.client.sendMessage(parse_mode=ParseMode.HTML,
                                chat_id=self.user_id,
                                text=message,
                                reply_markup=kb_markup)

    def send_message(self, message, whom=None):
        """
            Отправка сообщения
        :param message: текст сообщения
        :param whom: id чата для отпавки (необязательное)
        :return:
        """
        destination = whom or self.user_id
        self.client.sendMessage(destination, text=message, parse_mode=ParseMode.HTML)

    def send_message_inline_button(self, message, reply_markup, whom=None):
        """
            Отправка сообщения
        :param message: текст сообщения
        :param whom: id чата для отпавки (необязательное)
        :return:
        """
        destination = whom or self.user_id
        self.client.send_message(destination, text=message, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

    def send_photo(self, image_path):
        """
            Отправка фотографии
        :param image_path: Путь на самом сервере
        :return:
        """
        destination = self.user_id
        photo_path = "{}/{}".format(settings.MEDIA_ROOT, image_path)
        self.client.send_photo(chat_id=destination, photo=open(photo_path, 'rb'))

    def send_photo_with_caption(self, url_path, caption, reply_markup):
        destination = self.user_id
        self.client.send_photo(chat_id=destination, photo=open(url_path, 'rb'), caption=caption,
                               reply_markup=reply_markup)

    def send_media(self, images):
        destination = self.user_id
        self.client.send_media_group(chat_id=destination, media=images)

    def send_animation(self, url):
        self.client.send_animation(chat_id=self.user_id, animation=url)

    def check_user_exist(self):
        try:
            user = User.objects.get(user_id=self.user_id)
            return user
        except ObjectDoesNotExist as e:
            return None

    def get_user(self, whom=None):
        """
            Получение пользователя из базы данных
        :param whom: id пользователя
        :return: User объект пользователя
        """
        try:
            print("self.user_id", self.user_id)
            user = User.objects.get(user_id=self.user_id)
            return user
        except ObjectDoesNotExist as e:
            user = self.create_user()
            return user

    def create_user(self):
        """
            Создание пользователя
        :return: None
        """
        try:
            new_user = User.objects.create(user_id=self.user_id)
            new_user.save()
            return new_user
        except ObjectDoesNotExist as e:
            logger.error("Error on crete user: {}".format(e))
