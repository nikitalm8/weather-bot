def subscription(sponsors: list) -> dict:

    return {'inline_keyboard': [
        *(
            [
                {
                    'text': sponsor.title,
                    'url': sponsor.link,
                },
            ]
            for sponsor in sponsors
        ),
        [
            {
                'text': 'Проверить подписку', 
                'callback_data': 'checksub'
            },
        ],
    ]}
    
    
def popular_places(places: list) -> dict:
    
    return {'inline_keyboard': [
        *(
            [
                {
                    'text': place['name'],
                    'callback_data': 'weather:%i' % id,
                },
            ]
            for id, place in enumerate(places)
        ),
    ]}
    
    
def back(place_id: int) -> dict:
    
    return {'inline_keyboard': [
        [
            {
                'text': 'Назад 🔙', 
                'callback_data': 'back',
            },
            {
                'text': 'Поделиться 📧', 
                'switch_inline_query': 'place:%i' % place_id,
            },
        ],
    ]}


WEATHER = {'inline_keyboard': [
    [
        {
            'text': 'Обновить ⟳', 
            'callback_data': 'myweather',
        },
        {
            'text': 'Поделиться 📧', 
            'switch_inline_query': 'share',
        },
    ],
]}
