import asyncio
import random
import logging

import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import writer
from bd import Product, add_product, get_product_by_id, get_product_by_title, get_all_products
from writer import Writer

url = "https://www.producthunt.com/feed?category=technology"

writer = Writer()


async def get_news():
    headers = {
        "accept": "application/rss+xml;charset=UTF-8"
    }
    response = requests.get(url, headers, verify=True)

    with open("rss.xml", "w") as file:
        file.write(response.text)

    # Загружаем XML файл
    tree = ET.parse('rss.xml')
    root = tree.getroot()

    # Проход по каждому элементу entry и извлечение информации
    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        id = entry.find('{http://www.w3.org/2005/Atom}id').text
        published = entry.find('{http://www.w3.org/2005/Atom}published').text
        updated = entry.find('{http://www.w3.org/2005/Atom}updated').text
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        if get_product_by_title(title):
            continue
        content = entry.find('{http://www.w3.org/2005/Atom}content').text
        link_element = entry.find('{http://www.w3.org/2005/Atom}link')
        link_href = link_element.attrib.get('href') if link_element is not None else None

        content_soup = BeautifulSoup(content, 'html.parser')
        links = content_soup.find_all('a')
        content_links = [link['href'] for link in links]
        link_app = content_links[1]
        try:
            link_app = requests.get(link_app).request.url
            link_app = link_app.replace('?ref=producthunt', '')
        except Exception as e:
            print('Ошибка запроса ссылки')
            continue

        try:
            desc = get_desc(link_href)
            print(desc)
        except Exception as e:
            continue
            print('Ошибка получения описания')

        try:
            review = writer.get_post(desc)
        except Exception as e:
            review = None
            print('Ошибка написания обзора')

        try:
            img = get_img(link_href)
        except:
            img = None

        add_product(
            title=title,
            content=desc,
            review=review,
            linkPH=link_href,
            link=link_app,
            img=img
        )


def get_desc(app_url):
    # app_url = f'https://www.producthunt.com/posts/{app_slug}'

    app_info = {}
    response = requests.get(app_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # class ="styles_htmlText__eYPgj text-14 font-normal text-dark-gray text-gray-700"
    description_element = soup.find(class_="styles_htmlText__eYPgj text-14 font-normal text-dark-gray text-gray-700")
    if description_element:
        description = description_element.get_text(strip=True)
        app_info['description'] = description
        return app_info['description']


def get_img(app_url):
    response = requests.get(app_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    images = soup.find_all('img')
    img_links = [img['src'] for img in images if 'https://ph-files.imgix.net' and 'max' in img['src']]

    return random.choice(img_links).strip()

a = get_news()
