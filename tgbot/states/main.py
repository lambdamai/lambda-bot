from datetime import datetime

from django.conf import settings

from tgbot.tasks import animefy, dragnify, jojofy
from tgbot.trigger.state import BaseState as State
from tgbot.trigger.tg import TelegramTrigger


class BootStrapState(State):

    def on_trigger(self, trigger):
        if not trigger.check_user_exist():
            trigger.send_message("Привет, это телеграм бот Lambda МАИ")
        return MainMenu()


class MainMenu(State):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.keyboards = ["AnimeGANv2",
                          "Dragness",
                          "JoJoGAN"
                          ]

    def on_enter(self, trigger):
        trigger.send_keyboard("""️Выберите, чтобы вы хотели бы сделать?""",
                              self.keyboards)

    def on_trigger(self, trigger: TelegramTrigger):
        if trigger.text == self.keyboards[0]:
            return AnimeGanV2()
        elif trigger.text == self.keyboards[1]:
            return Dragness()
        elif trigger.text == self.keyboards[2]:
            return JoJoGAN()


class AnimeGanV2(State):
    def __init__(self):
        super(AnimeGanV2, self).__init__()
        self.keyboards = ["Назад", ]

    def on_enter(self, trigger: TelegramTrigger):
        trigger.send_keyboard("Загрузи изображение для анимефикации", self.keyboards)

    def on_trigger(self, trigger: TelegramTrigger):
        if trigger.message.photo:
            file = trigger.client.getFile(trigger.message.photo[-1].file_id)
            upload_filename = f'{settings.MEDIA_ROOT}/image/animeganv2_{datetime.now().timestamp()}.jpg'
            file.download(custom_path=upload_filename)
            trigger.send_message("Подожди пару секунд, фото обрабатывается")
            animefy.delay(user_id=trigger.user_id, image_path=upload_filename)
        if trigger.text == self.keyboards[0]:
            return MainMenu()
        else:
            return AnimeGanV2()


class Dragness(State):
    def __init__(self):
        super(Dragness, self).__init__()
        self.keyboards = ["Назад", ]

    def on_enter(self, trigger: TelegramTrigger):
        trigger.send_keyboard("Загрузи изображение для Dragness", self.keyboards)

    def on_trigger(self, trigger: TelegramTrigger):
        if trigger.message.photo:
            file = trigger.client.getFile(trigger.message.photo[-1].file_id)
            upload_filename = f'{settings.MEDIA_ROOT}/image/drageness{datetime.now().timestamp()}.jpg'
            file.download(custom_path=upload_filename)
            trigger.send_message("Подожди пару секунд, фото обрабатывается")
            dragnify.delay(user_id=trigger.user_id, image_path=upload_filename)
        elif trigger.text == self.keyboards[0]:
            return MainMenu()
        else:
            return Dragness()


class JoJoGAN(State):
    def __init__(self):
        super(JoJoGAN, self).__init__()
        self.keyboards = ["Назад", ]

    def on_enter(self, trigger: TelegramTrigger):
        trigger.send_keyboard("Загрузи изображение для Dragness", self.keyboards)

    def on_trigger(self, trigger: TelegramTrigger):
        if trigger.message.photo:
            file = trigger.client.getFile(trigger.message.photo[-1].file_id)
            upload_filename = f'{settings.MEDIA_ROOT}/image/JoJo{datetime.now().timestamp()}.jpg'
            file.download(custom_path=upload_filename)
            trigger.send_message("Подожди пару секунд, фото обрабатывается")
            jojofy.delay(user_id=trigger.user_id, image_path=upload_filename)
        elif trigger.text == self.keyboards[0]:
            return MainMenu()
        else:
            return JoJoGAN()
