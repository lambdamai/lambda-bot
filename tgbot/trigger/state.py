from tgbot.trigger.tg import TelegramTrigger


class BaseState:
    def __init__(self):
        self.back = "⬅️ Назад"

    def __str__(self):
        """
            Название класса
        :return: Название класса
        """
        return '.'.join([self.__class__.__module__, self.__class__.__name__])

    def on_enter(self, trigger: TelegramTrigger):
        """
            Срабатывает при переходе пользователя
        :param trigger:
        :return:
        """
        pass

    def on_trigger(self, trigger: TelegramTrigger):
        """
            Срабатывает при отправке сообщения пользователем
        :param trigger:
        :return:
        """
        pass

    def on_exit(self, trigger: TelegramTrigger):
        pass
