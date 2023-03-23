from math import ceil


def choice(item_id: int | str, prefix: str) -> dict:

    return {'inline_keyboard': [
        [
            {'text': 'Да', 'callback_data': f'{prefix}:del2:{item_id}'},
            {'text': 'Нет', 'callback_data': f'{prefix}:info:{item_id}'},
        ]
    ]}


def ref(ref: str) -> dict:

    return {'inline_keyboard': [
        [
            {'text': 'Назад', 'callback_data': f'reflist:1'},
            {'text': 'Удалить', 'callback_data': f'ref:del:{ref}'},
        ]
    ]}


def ref_list(refs: list, page: int=1) -> dict:

    pages = ceil(len(refs)/9) or 1

    return {'inline_keyboard': [
        *(
            [{'text': reflink, 'callback_data': f'ref:info:{reflink}'}]
            for reflink in refs[(page-1)*9:page*9]
        ),
        [
            {'text': '<-', 'callback_data': f'reflist:{page-1}'},
            {'text': f'{page}/{pages}', 'callback_data': 'none'},
            {'text': '->', 'callback_data': f'reflist:{page+1}'},
        ]
    ]}


def sponsors(sponsors: list) -> dict:

    return {'inline_keyboard': [
        *(
            [   
                {
                    'text': (
                        '🟢' if sponsor.is_active
                        else '⭕'
                    ),
                    'callback_data': f'sponsor:active:{sponsor.id}',
                },
                {
                    'text': (
                        (
                            '🤖 ' if sponsor.is_bot
                            else '💬 '
                        ) + sponsor.title
                    ), 
                    'url': sponsor.link,
                },
                {
                    'text': '%i/%s' % (
                        sponsor.visits, 
                        sponsor.limit or '∞',
                    ),
                    'callback_data': 'none',
                },
                {
                    'text': '🗑', 
                    'callback_data': f'sponsor:del:{sponsor.id}',
                },
            ]
            for sponsor in sponsors
        ),
        [
            {'text': 'Добавить', 'callback_data': 'sponsor:add'},
        ]
    ]}


def adverts(adverts: list) -> dict:

    return {'inline_keyboard': [
        *(
            [   
                {
                    'text': (
                        '🟢' if advert.is_active
                        else '⭕'
                    ),
                    'callback_data': f'ad:status:{advert.id}',
                },
                {
                    'text': advert.title,
                    'callback_data': 'none',
                },
                {
                    'text': '%i/%s' % (
                        advert.views, 
                        advert.target or '∞',
                    ),
                    'callback_data': 'none',
                },
                {
                    'text': '🗑', 
                    'callback_data': f'ad:del:{advert.id}',
                },
            ]
            for advert in adverts
        ),
        [
            {'text': 'Добавить', 'callback_data': 'ad:add'},
        ]
    ]}


DUMP = {'inline_keyboard': [
    [
        {'text': 'Всех', 'callback_data': 'dump:all'},
        {'text': 'Живых', 'callback_data': 'dump:alive'},
    ]
]}

CANCEL = {'inline_keyboard': [
    [
        {'text': 'Отмена', 'callback_data': 'cancel'},
    ]
]}

SPONSOR_CHOICE = {'inline_keyboard': [
    [
        {'text': 'Канал', 'callback_data': 'addsponsor:channel'},
        {'text': 'Бот', 'callback_data': 'addsponsor:bot'},
    ]
]}

STOPMAIL = {'inline_keyboard': [
    [
        {'text': 'Остановить рассылку', 'callback_data': 'stopmail'},
    ]
]}
