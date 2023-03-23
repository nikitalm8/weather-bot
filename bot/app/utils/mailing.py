import time
import asyncio

from contextlib import suppress
from abc import ABCMeta, abstractmethod, abstractstaticmethod

from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError, TelegramRetryAfter


class IMailer(metaclass=ABCMeta):

    @abstractmethod
    async def start_mailing(self, *args, **kwargs) -> None:
        '''
        Method to be implemented in child class.
        '''

    @abstractstaticmethod
    def get_instance() -> 'IMailer':
        '''
        Method to be implemented in child class.
        '''


class MailerSingleton(IMailer):

    DEFAULT_DELAY = 1/25
    __instance = None


    def __init__(self, delay: int | float=None) -> None:
        """
        Creator of MailerSingleton. Raises an exception if an instance already exists.

        :param int | float delay: Delay between messages, optional.
        :raises Exception: If an instance already exists.
        """

        if MailerSingleton.__instance is not None:

            raise Exception('MailingSingleton is a singleton!')

        self.delay = delay or self.DEFAULT_DELAY
        MailerSingleton.__instance = self


    @staticmethod
    def get_instance() -> 'MailerSingleton':
        """
        Get an instance of MailerSingleton.

        :return MailerSingleton: Already existing / newly created instance.
        """

        if MailerSingleton.__instance is None:

            MailerSingleton()

        return MailerSingleton.__instance


    @staticmethod
    def pretty_time(seconds: float) -> str:
        """
        Get a pretty time string.

        :param float seconds: UNIX timestamp.
        :return str: Time in hunan-readable format.
        """

        seconds = int(seconds)

        return '%0d:%0d:%0d' % (
            seconds // 3600,
            seconds % 3600 // 60,
            seconds % 60
        )


    @classmethod
    def get_text(cls, scope: list[int], sent: int, delay: float) -> str:
        """
        Get an ETA message.

        :param list[int] scope: Scope of users.
        :param int sent: Progress of mailing.
        :param float delay: Delay between messages.
        :return str: Ready message.
        """

        progress = int(sent / len(scope) * 25)
        progress_bar = ('=' * progress) + (' ' * (25 - progress))

        return "<code>[%s]</code> %s/%s (ETA: %s)" % (
            progress_bar,
            sent,
            len(scope),
            cls.pretty_time((len(scope) - sent) * delay)
        )


    async def start_mailing(self, message: Message, scope: list[int], cancel_keyboard: dict) -> None:
        """
        Start the process of mailing.

        :param Message message: Message in admin chat, which will be copied.
        :param list[int] scope: Scope of users receiving the message.
        :param dict cancel_keyboard: Keyboard to cancel mailing.
        """

        self.TIME_STARTED = time.monotonic()

        time_started = self.TIME_STARTED
        blocked = 0
        delay = self.delay

        msg = await message.answer(
            self.get_text(
                scope, 1, delay,
            ),
            reply_markup=cancel_keyboard,
        )
        self.last_update = self.TIME_STARTED

        for sent, user_id in enumerate(scope, 1):

            if self.TIME_STARTED != time_started:

                break

            if time.monotonic() - self.last_update > 2:

                self.last_update = time.monotonic()

                with suppress(TelegramAPIError):
                    
                    await msg.edit_text(
                        self.get_text(
                            scope, sent, delay,
                        ),
                        reply_markup=cancel_keyboard,
                    )

            try:

                await message.copy_to(
                    user_id,
                    reply_markup=message.reply_markup,
                )

            except TelegramRetryAfter as exc:

                delay *= 2
                await asyncio.sleep(exc.retry_after)

            except TelegramAPIError:

                blocked += 1

            await asyncio.sleep(delay)

        with suppress(TelegramAPIError):

            await msg.edit_text(
                self.get_text(
                    scope, len(scope), delay,
                )
            )

        await msg.answer(
            'Рассылка завершена. Успешно: %s. Бот заблокирован: %s' % (
                (len(scope) - blocked), 
                blocked,
            )
        )


    def stop_mailing(self) -> bool:
        """
        Stops mailing. Returns True on success.

        :return bool: True on successful stop.
        """

        if self.TIME_STARTED == 0:

            return False

        self.TIME_STARTED = 0

        return True


    @property
    def is_mailing(self) -> bool:
        """
        Check if mailing is in progress.

        :return bool: True if mailing is in progress.
        """

        return self.TIME_STARTED != 0
