import requests
import csv
import os
import json
from datetime import date
from bs4 import BeautifulSoup


def collect_data():
    videocards_data = []
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.3.852 Yowser/2.5 Safari/537.36'
    }

    chipsets = ['NVIDIA  GeForce RTX 3060', 'NVIDIA  GeForce RTX 3070TI', 'NVIDIA  GeForce RTX 3060Ti', 'NVIDIA  GeForce RTX 3070','NVIDIA  GeForce RTX 3080']

    page = 1

    print("Starting...")
    current_date = date.today()

    if not os.path.isdir("../out"):
        os.mkdir("../out")

    if not os.path.isdir("../out/csv"):
        os.mkdir("../out/csv")

    if not os.path.isdir("../out/json"):
        os.mkdir("../out/json")

    with open(f'../out/csv/{current_date}_videocards.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Название',
                'Цена',
                'Старая цена',
                'Скидка',
                'Ссылка'
            )
        )

    while True:
        url = f'https://www.citilink.ru/catalog/videokarty/?action=changeCity&space=dzj_cl:&p={page}'
        request = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(request.text, 'lxml')
        isThereAPage = ''
        try:
            isThereAPage = soup.find('div', class_='PaginationWidget__wrapper-pagination').find('a',
                                                                                                class_='PaginationWidget__page_next')
        except AttributeError:
            pass

        try:
            videocards = soup.find('div', class_='ProductCardCategoryList').find('div',
                                                                                 class_='ProductCardCategoryList__products-container').find(
                'div', class_='ProductCardCategoryList__grid-container').find('div',
                                                                              class_='ProductCardCategoryList__list').find(
                'section', class_='ProductGroupList').find_all('div', class_='product_data__gtm-js')
        except AttributeError:
            pass

        for item in videocards:
            chipset = item.find('div', class_='ProductCardHorizontal__description-block').find('span',
                                                                                               class_='ProductCardHorizontal__properties_value').text.strip()
            if chipset not in chipsets:
                continue

            try:
                availability = item.find('div', class_='ProductCardHorizontal__not-available-block')
            except AttributeError:
                pass

            if availability is not None:
                continue

            item_title = item.find('a', class_='ProductCardHorizontal__title').text
            item_url = item.find('a')['href']
            item_url = f'https://www.citilink.ru{item_url}'

            try:
                item_old_price = item.find('div', class_='ProductCardHorizontal__buy-block').find('div',
                                                                                                  class_='ProductPrice_old').find(
                    'span', class_='_current-price js--_current-price').text.strip().replace(' ', '')
                item_old_price = int(item_old_price)
            except AttributeError:
                item_old_price = '-'

            try:
                item_price = item.find('div', class_='ProductCardHorizontal__buy-block').find('div',
                                                                                              class_='ProductPrice_default').find(
                    'span', class_='ProductCardHorizontal__price_current-price').text.strip().replace(' ', '')
                item_price = int(item_price)
            except AttributeError:
                item_price = '-'

            if item_old_price != '-':
                discount = str(round(100 - ((item_price * 100) / item_old_price)))
                discount = f'{discount}%'
            else:
                discount = '-'

            with open(f'../out/csv/{current_date}_videocards.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        item_title,
                        item_price,
                        item_old_price,
                        discount,
                        item_url
                    )
                )

            videocards_data.append(
                {
                    'title': item_title,
                    'price': item_price,
                    'old_price': item_old_price,
                    'discount': discount,
                    'url': item_url
                }
            )

            with open("../out/json/result.json", "w", encoding="utf-8") as file:
                json.dump(videocards_data, file, indent=4, ensure_ascii=False)

        if isThereAPage is None:
            break

        print(f'[INFO]: {page} page is done!')
        page += 1

    print("Parsing was finished successfully")