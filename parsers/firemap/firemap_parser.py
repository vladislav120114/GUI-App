import requests
from openpyxl import Workbook
from tkinter import *

cookies = {
    '_osm_totp_token': '311324',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'cookie': '_osm_totp_token=311324',
    'priority': 'u=1, i',
    'referer': 'https://nominatim.openstreetmap.org/ui/reverse.html?lat=0&lon=0&zoom=8',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

params = {
    'lat': '0',
    'lon': '0',
    'zoom': '8',
    'format': 'jsonv2',
}

fin_arr = [['№', 'Широта', 'Долгота', 'Область', 'Район', 'Дата появления', 'Время появления']]

def main(url, count, tb_tree):
    try:
        file = requests.get(url)
    except:
        main(url, count, tb_tree)

    content = str(file.content)
    arr = content.split('\\n')
    end = []
    for el in arr:
        end.append(el.split(','))
    end[0][0] = end[0][0][2:]
    end = end[:-1]
    print(len(end[1:]))

    for i in end[1:]:
        
        headers['referer'] = f'https://nominatim.openstreetmap.org/ui/reverse.html?lat={i[0]}&lon={i[1]}&zoom=8'
        params['lat'] = f'{i[0]}'
        params['lon'] = f'{i[1]}'
        try:
            response = requests.get('https://nominatim.openstreetmap.org/reverse.php', params=params, cookies=cookies, headers=headers).json()
            if response['address']['country'] == "Украина" and response['address']['state'] != "Республика Крым":
                fin_arr.append([
                    count,
                    i[0],
                    i[1],
                    response['address']['state'],
                    response['address']['district'],
                    i[5],
                    f'{end[1][6][:2]}:{end[1][6][2:]}'
                ])
                tb_tree.insert('', "end", values=[i[0], i[1], response['address']['state'], i[5]])
                tb_tree.yview_moveto(1)
                print(fin_arr[-1])
                count += 1
        except Exception as e:
            print(e)
            continue

def firemap(time, tb_tree, tree_label, button_1, button_2, button_3):
    try:
        urls = [
            f'https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_Europe_{time}.csv',
            f'https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Europe_{time}.csv',
            f'https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_Europe_{time}.csv',
            f'https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-21-viirs-c2/csv/J2_VIIRS_C2_Europe_{time}.csv'
        ]

        for url in urls:
            print(url.split('/')[-1])
            main(url, 1, tb_tree)

        wb = Workbook()
        ws = wb.active
        for i in fin_arr:
            ws.append(i)
        wb.save(f"Результаты/fire_map.xlsx")
        tree_label.pack(padx=10)
        button_1.config(state=NORMAL)
        button_2.config(state=NORMAL)
        button_3.config(state=NORMAL)
    except:
        button_1.config(state=NORMAL)
        button_2.config(state=NORMAL)
        button_3.config(state=NORMAL)