import re

from bs4 import BeautifulSoup


def igromania(html):
    """ Парсим сайт Игромании. """
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find('div', id='uni_com_feed_cont').find_all(
        'div', class_='aubl_item')[:10]
    news_list = []
    for n in news:
        try:
            title = n.find('div', class_='aubli_data').find('a').text.strip()
        except:
            title = ''
        try:
            url = 'https://www.igromania.ru' + \
                n.find('div', class_='aubli_data').find('a').get('href')
        except:
            url = ''
        try:
            img = n.find('img').get('src')
        except:
            img = ''
        local_list = [title, url, img]
        news_list.append(local_list)

    return news_list


def lenta(html):
    """ Парсим сайт Лента.ру. """
    lenta = {}
    soup = BeautifulSoup(html, 'lxml')
    glavnoe = soup.find('h2').find('a').text.strip()
    glav_url = soup.find('h2').find('a').get('href')
    glav_url = 'https://lenta.ru' + glav_url
    glavnoe = re.sub(r'^\d{2}:\d{2}', '', glavnoe)
    glavnoe = '*{}*\n'.format(glavnoe)
    news = soup.find(
        'section', class_='b-top7-for-main').find_all('div', class_='item')
    for i in news:
        a = i.find('a').get('href')
        a = 'https://lenta.ru' + a
        text = i.find('a').text.strip()
        text = re.sub(r'^\d{2}:\d{2}', '', text)
        text = '`{}`'.format(text)
        lenta[text] = a
    news = None

    return lenta, glavnoe, glav_url


def dozhd(html):
    """ Парсим сайт ТВ Дождь. """
    links = {}
    imge = {}
    soup = BeautifulSoup(html, 'lxml')
    t=soup.find_all('div', class_ = 'newsline_tile__el')
    count = 0
    for i in t:
        if count < 10:
            a = i.find('a').get('href')
            domain = 'https://tvrain.ru'
            a = domain + a
            text = i.find('h3').find('a').text

            try:
                img = i.find('img').get('data-image')
                https = 'https:'
                img = https + img
            except:
                img = 'None'
            links[a]= text
            imge[a] = img
        count = count +1
        
    return links, imge