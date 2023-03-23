from aiogram.types import BotCommand

admin_commands = [
    BotCommand(
        command="start", 
        description="Запустить бота"
    ),
    BotCommand(
        command="stats", 
        description="Статистика"
    ),
    BotCommand(
        command="dump", 
        description="Выгрузка"
    ),
    BotCommand(
        command="mailing", 
        description="Рассылка"
    ),
    BotCommand(
        command="referrals", 
        description="Рефералы"
    ),
    BotCommand(
        command="sponsors", 
        description="Спонсоры"
    ),
    BotCommand(
        command="adverts", 
        description="Реклама"
    ),
]