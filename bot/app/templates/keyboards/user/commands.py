from aiogram.types import BotCommand


user_commands = [
    BotCommand(
        command='start', 
        description='Перезапустить бота 🤖'
    ),        
    BotCommand(
        command='weather',
        description='Получить погоду в установленном местоположении ⛅',
    ),  
    BotCommand(
        command='popular',
        description='Получить погоду в популярных городах 🌆',
    ),
]
