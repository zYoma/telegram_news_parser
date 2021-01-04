import asyncio
import multiprocessing
import re
from concurrent.futures import ThreadPoolExecutor
from parser import dozhd, igromania, lenta

from aiohttp import ClientSession, web
from api import TELEGRAM_TOKEN, Api

bot = Api()
routes = web.RouteTableDef()

async def create_app():
    """ Создаем экземпляр приложения. """
    app = web.Application()
    app.add_routes(routes)
    app.on_cleanup.append(on_shutdown)
    return app

async def on_shutdown(app):
    await app.shutdown()


async def get_html(url):
    """ Асинхронно получаем html страниц для парсинга. """
    async with ClientSession() as session:
        async with session.get(url) as response:
            html = await response.read()
    return html


def create_new_thread():
    """ Создание отдельных потоков для запуска синхронных функций. """
    pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
    loop = asyncio.get_event_loop()
    return pool, loop


@routes.post(f'/{TELEGRAM_TOKEN}/')
async def main(request):
    """ Слушаем что нам прислыоает Телеграм, парсим запрос,
        в зависимости от команды, запускаем соответсвующую функцию. """
    data = await request.json()
    if 'callback_query' in data:
        callback_data = data['callback_query']['data']
        callback_from_chat_id = data['callback_query']['message']['chat']['id']
        callback_message_id = data['callback_query']['message']['message_id']
        chat_id = callback_from_chat_id
        message_id = callback_message_id
        first_name = data['callback_query']['from']['first_name']
        caption = data['callback_query']['message']['caption']
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        first_name = data['message']['from']['first_name']
        message = data['message'].get('text')
        if message:
            if re.search(r'Игры', message):
                html = await get_html(url='https://www.igromania.ru/news/')

                pool, loop = create_new_thread()
                game_list = await loop.run_in_executor(pool, igromania, html)

                for news in game_list:
                    await bot.send_Photo(chat_id, news[0], news[2], news[1])

            elif re.search(r'Новости', message):
                html = await get_html(url='https://lenta.ru/')
                pool, loop = create_new_thread()
                news, glavnoe, glav_url = await loop.run_in_executor(pool, lenta, html)
                for key in news:
                    await bot.sendMessage(chat_id, key, news[key])
                await bot.sendMessage(chat_id, glavnoe, glav_url)

            elif re.search(r'дождь', message):
                html = await get_html(url='https://tvrain.ru/news/')

                pool, loop = create_new_thread()
                links_dozhd, img_dozhd = await loop.run_in_executor(pool, dozhd, html)
                for key in links_dozhd:
                    if img_dozhd[key] == 'None':
                        await bot.sendMessage(chat_id, links_dozhd[key], key)
                    else:
                        await bot.send_Photo(chat_id, links_dozhd[key], img_dozhd[key], key)
                

    return web.Response(status=200)
