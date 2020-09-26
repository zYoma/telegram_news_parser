import os
import json

from dotenv import load_dotenv
import aiohttp

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


class Api(object):
    URL = 'https://api.telegram.org/bot'+ TELEGRAM_TOKEN + '/%s'

    async def _request(self, method, answer):
        """ Асинхронно выполняем POST запрос к серверу телеграм. """
        headers = {
            'Content-Type': 'application/json'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.URL % (method),
                                    data=json.dumps(answer),
                                    headers=headers) as resp:
                try:
                    assert resp.status == 200
                except:
                    print(f'Ошибка - {resp.status}')

    async def sendMessage(self, chat_id, text, blog_url):
        """ Метод отправляет сообщение с клавиатурой и ссылкой сайт новости. """
        kb_markup = {'inline_keyboard': [[{
            'text': 'Читать дальше', 
            'url': blog_url, 
            'callback_data': 'var1',
        }]]}
        answer = {
            'chat_id': chat_id,
            'text': text,
            'reply_markup': kb_markup, 
            'parse_mode': 'Markdown',
        }
        await self._request('sendMessage', answer)

    async def send_Photo(self, chat_id, text, img, blog_url):
        """ Метод отправляет картинку с подписью и сслку на сайт. """
        kb_markup = {'inline_keyboard': [[{
            'text': 'Читать дальше', 
            'url': blog_url, 
            'callback_data': 'blog_url',
        }]]}
        answer = {
            'chat_id': chat_id, 
            'caption': text, 
            'photo': img,
            'reply_markup': kb_markup, 
            'parse_mode': 'Markdown',
        }
        await self._request('sendPhoto', answer)

