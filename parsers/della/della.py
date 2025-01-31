from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook
from deep_translator import GoogleTranslator
from tkinter import *
import math
import re
import json
import pycountry


# ЕВРОПА - УКРАИНА

def della_parser(tb_tree, tree_label, load_type, button_1, button_2):
    try:
        with open('C:/Users/User/Desktop/GUI App/parsers/della/della_db.json', encoding="utf-8") as f:
            db = json.load(f)

        match load_type:
            case "eu":
                link = "https://della.eu/search/abd204efloh0ilk0m1r.html"
            case "ua":
                link = "https://della.eu/search/a204bd204eflolz64h0ilk0m1.html"
        translator = GoogleTranslator(source='auto', target='ru')
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--enable-unsafe-swiftshader')
        driver = webdriver.Chrome(options=options)
        driver.get(link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "requests_count_all")))

        days_chose = driver.find_elements(By.CLASS_NAME, "selectric-wrapper")[0]
        days_chose.click()
        days_chose.find_elements(By.TAG_NAME,"li")[4].click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "requests_count_all")))

        days_chose = driver.find_elements(By.CLASS_NAME, "selectric-wrapper")[1]
        days_chose.click()
        days_chose.find_elements(By.TAG_NAME,"li")[2].click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "requests_count_all")))

        count_block = driver.find_element(By.CLASS_NAME, "requests_count_all")
        blocks_count = count_block.find_element(By.CLASS_NAME, "bold").text
        blocks_on_page = count_block.find_element(By.CLASS_NAME, "semibold").text
        pages_count = math.ceil(int(blocks_count.replace(' ', '')) / int(blocks_on_page))
        print(blocks_count, blocks_on_page, pages_count)

        trans = {
            "tautliner": "Таутлайнер",
            "covered truck": "Крытый грузовик",
            "refrigerator truck": "Грузовик-холодильник",
            "Cherkas’ka obl.": "Черкасская область",
            "Chernihivs’ka obl.": "Черниговская область",
            "Chernivets’ka obl.": "Черновицкая область",
            "Dnipropetrovs’ka obl.": "Днепропетровская область",
            "Donets'ka obl.": "Донецкая область",
            "Ivano-Frankivs’ka obl.": "Ивано-Франковская область",
            "Kharkivs’ka obl.": "Харьковская область",
            "Khersons’ka obl.": "Херсонская область",
            "Khmel’nyts’ka obl.": "Хмельницкая область",
            "Kirovohrads’ka obl.": "Кировоградская область",
            "Kyivs’ka obl.": "Киевская область",
            "L’vivs’ka obl.": "Львовская область",
            "Luhans’ka obl.": "Луганская область",
            "Mykolayivs’ka obl.": "Николаевская область",
            "Odes’ka obl.": "Одесская область",
            "Poltavs’ka obl.": "Полтавская область",
            "Sumsca obl.": "Сумская область",
            "Ternopilska obl.": "Тернопольская область",
            "Vinnyts’ka obl.": "Винницкая область",
            "Volyns’ka obl.": "Волынская область",
            "Zakarpats’ka obl.": "Закарпатская область",
            "Zaporiz'ka obl.": "Запорожская область",
            "Zhytomyrs’ka obl.": "Житомирская область"
        }

        count = 0
        final_arr = [["Дата объявления", "Cтрана загрузки", "Область загрузки", "Город загрузки", "Город загрузки (Перевод)", "Cтрана разрузки", "Область разгрузки", "Город разгрузки", "Город разгрузки (Перевод)", "Дистанция", "Груз", "Груз (Перевод)", "Тип груза", "Вес", "Транспорт", "Кол-во транспорта", "Стоимость"]]
        b = False
        for page in range(pages_count):
            blocks = driver.find_elements(By.CLASS_NAME, "is_search")
            for block in blocks:
                if "день" in block.find_element(By.CLASS_NAME, "time_string").text:
                    b = True
                    break
                try:
                    # Дата объявления (или загрузки, тут хз)
                    date_add = block.find_element(By.CLASS_NAME, "date_add").text

                    # Маршрут (нужен для определения мест загрузки и разгрузки)
                    route = block.find_element(By.CLASS_NAME, "request_distance").text
                    start_obl = block.find_element(By.CLASS_NAME, "request_distance").find_elements(By.TAG_NAME, "span")[0].get_attribute("title")
                    end_obl = block.find_element(By.CLASS_NAME, "request_distance").find_elements(By.TAG_NAME, "span")[2].get_attribute("title")
                    if start_obl in trans:
                        start_obl = trans[start_obl]
                    if end_obl in trans:
                        end_obl = trans[end_obl]
                    # Место загрузки
                    start_point = route.split(' — ')[0]
                    start_point = start_point.split(', ')
                    point = start_point[0].split(' ')
                    start_city = ' '.join(point[:-1]).strip()
                    start_country_code = point[-1][1:-1]
                    start_country = translator.translate(pycountry.countries.get(alpha_2=start_country_code).name)
                    if start_city not in db:
                        db[start_city] = {"translated_name": translator.translate(start_city)}
                        t_start_city = db[start_city]["translated_name"]
                    else:
                        t_start_city = db[start_city]["translated_name"]

                    # Место разгрузки
                    end_point = route.split(' — ')[1]
                    end_point = end_point.split(', ')
                    point = end_point[0].split(' ')
                    end_city = ' '.join(point[:-1]).strip()
                    end_country_code = point[-1][1:-1]
                    end_country = translator.translate(pycountry.countries.get(alpha_2=end_country_code).name)
                    if end_city not in db:
                        db[end_city] = {"translated_name": translator.translate(end_city)}
                        t_end_city = db[end_city]["translated_name"]
                    else:
                        t_end_city = db[end_city]["translated_name"]

                    # Расстояние
                    try:
                        distance = block.find_element(By.CLASS_NAME, "distance").text
                    except:
                        distance = "Нет данных"

                    # Груз
                    cargo_type = block.find_element(By.CLASS_NAME, "cargo_type").text
                    if cargo_type not in trans:
                        trans[cargo_type] = translator.translate(cargo_type)
                        t_cargo_type = trans[cargo_type]
                    else:
                        t_cargo_type = trans[cargo_type]

                    try: # Вес груза
                        weight = float(block.find_element(By.CLASS_NAME, "weight").text.split(" ")[0].replace(",","."))
                    except:
                        weight = 0.0
                    # Тип груза (гуманитара или нет)
                    try:
                        hum = translator.translate(block.find_element(By.CLASS_NAME, "gps_label").text)
                    except:
                        hum = "Обычный груз"

                    # Транспорт
                    truck_type = block.find_element(By.CLASS_NAME, "truck_type").text

                    # Тип транспорта
                    try:
                        truck_num = int(block.find_element(By.CLASS_NAME, "request_text").find_element(By.CLASS_NAME, "value").text)
                    except Exception as e:
                        truck_num = 1
                    if truck_type not in trans:
                        trans[truck_type] = translator.translate(truck_type)
                        truck_type = trans[truck_type]
                    else:
                        truck_type = trans[truck_type]

                    # Стоимость
                    try:
                        price = block.find_element(By.CLASS_NAME, "price_main").text.replace('\n', '').replace(' ', '')
                        alphabets = re.findall(r"[a-zA-Z]+", price)
                        numbers = re.findall(r"[0-9]+", price)
                        price = f"{numbers[0]} {alphabets[0]}"
                    except:
                        price = "Нет данных"

                    count += 1
                    row = [
                        date_add,
                        start_country,
                        start_obl,
                        start_city,
                        t_start_city,
                        end_country,
                        end_obl,
                        end_city,
                        t_end_city,
                        distance,
                        cargo_type,
                        t_cargo_type,
                        hum,
                        weight,
                        truck_type,
                        truck_num,
                        price,
                    ]
                    print(row)
                    tb_tree.insert('', "end", values=[cargo_type, start_city, end_city])
                    tb_tree.yview_moveto(1)
                    if row not in final_arr:
                        final_arr.append(row)

                except Exception as e:
                    print(e)

            if b: break

            if page != pages_count - 1:
                next_page = driver.find_elements(By.CLASS_NAME, "end")[0]
                driver.execute_script(f"arguments[0].scrollIntoView();", next_page)
                next_page.click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "requests_count_all")))
        count_arr = [["№"]]
        for i in range(len(final_arr[1:])):
            count_arr.append([f"{i+1}"])
        arr = []
        for i in range(len(count_arr)):
            arr.append(count_arr[i]+final_arr[i])
        wb = Workbook()
        ws = wb.active
        for i in arr:
            ws.append(i)
        wb.save(f"Результаты/della_{load_type}.xlsx")
        tree_label.pack(padx=10)
        print(f"Результаты сохранены в файле Грузоперевозки.xlsx")
        button_1.config(state=NORMAL)
        button_2.config(state=NORMAL)
    except:
        
        button_1.config(state=NORMAL)
        button_2.config(state=NORMAL)