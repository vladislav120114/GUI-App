from bs4 import BeautifulSoup
import requests
import os
from tkinter import *

def energymap(csrftoken, sessionid, tb_tree, button):
    try:
        params = {
            'ordering': '-publication',
            'paginate_by': '20',
            'coverage_date_range_start': '',
            'coverage_date_range_end': '',
            'cost': '',
            'page': '1',
        }

        cookies = {
            'csrftoken': f'{csrftoken}',
            '_ga_RR6DR4QDC1': 'GS1.1.1726119829.10.1.1726121208.42.0.614750296',
            '_ga': 'GA1.1.503718087.1718024098',
            'metabase.DEVICE': '1c76a36b-0d4b-4f21-940b-46ffc7f946f6	',
            'sessionid': f'{sessionid}',
            '_ga_DD2ELLWT20': 'GS1.1.1716809233.1.1.1716809807.60.0.0',
            '_hjSessionUser_2334945': 'eyJpZCI6IjI5OGY1ZDM3LTA2OTQtNTRkYi05NWRhLTI5ZGQxNjNiZGIzNSIsImNyZWF0ZWQiOjE3MTY4MDkyMzU0ODIsImV4aXN0aW5nIjp0cnVlfQ==',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:126.0) Gecko/20100101 Firefox/126.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'https://map.ua-energy.org/en/resources/?ordering=-publication&paginate_by=20&coverage_date_range_start=&coverage_date_range_end=&cost=&page=2',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=1',
        }

        page = requests.get('https://map.ua-energy.org/en/resources/', params=params, cookies=cookies, headers=headers)

        soup = BeautifulSoup(page.text, "html.parser")

        pagination = soup.findAll('a', class_='pagination__item')
        print(len(pagination))
        page_count = int(pagination[4].get_text())

        for i in range(1, page_count+1):

            params['page'] = str(i)
            page = requests.get('https://map.ua-energy.org/en/resources/', params=params, cookies=cookies, headers=headers)
            soup = BeautifulSoup(page.text, 'html.parser')
            allCards = soup.find_all('div', class_='card')
            allCards.pop()
            for j in range(len(allCards)):
                link = allCards[j].find('a', class_='button button--primary')
                name = allCards[j].find('a', class_='card__title')
                print(name.getText().strip())
                info = allCards[j].find_all('span', class_='info-label__content')
                print(link.get("data-modal-form-url"))
                try:
                    page = requests.get(
                        f'https://map.ua-energy.org{link.get("data-modal-form-url")}',
                        cookies=cookies,
                        headers=headers,
                    )
                except: continue
                soup = BeautifulSoup(page.text, 'html.parser')
                token = soup.find('input')
                #print(token.get('value'))
                files = {
                    'csrfmiddlewaretoken': (None, token.get('value')),
                    'language': (None, 'en'),
                    'media_format': (None, 'xlsx'),
                }
                page = requests.post(
                    f'https://map.ua-energy.org{link.get("data-modal-form-url")}',
                    cookies=cookies,
                    headers=headers,
                    files=files,
                )
                url = page.json()
                #print(url["url"])
                response = requests.get(f'https://map.ua-energy.org{url["url"]}', cookies=cookies, headers=headers)
                date = f"{info[0].getText().strip()} ({info[1].getText().strip()})"
                tname = name.getText().strip().replace('/', ' ').replace('"', '')
                os.makedirs(f"Результаты/Выгрузка", exist_ok=True)
                with open(f"Результаты/Выгрузка/{date} {tname}.xlsx", 'wb') as file:
                    file.write(response.content)
                tb_tree.insert('', "end", values=[f"{date} {tname}.xlsx"])
                tb_tree.yview_moveto(1)
                print(f"{date} {tname}.xlsx")
        button.config(state=NORMAL)
    except:
        button.config(state=NORMAL)