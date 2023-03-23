from aiogram.types import BotCommand


user_commands = [
    BotCommand(
        command="start", 
        description="Запустить бота"
    ),    
    BotCommand(
        command='popular',
        description='Получить погоду в популярных городах',
    ),
    BotCommand(
        command='weather',
        description='Получить погоду',
    ),  
    BotCommand(
        command='popular',
        description='Получить погоду в популярных городах',
    ),
    BotCommand(
        command='location',
        description='Установить локацию',
    ),
]
