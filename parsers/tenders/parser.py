import json
from deep_translator import GoogleTranslator
from openpyxl import Workbook
import requests
import math
from datetime import datetime, timedelta
import ttkbootstrap as tb
from tkinter import *
from parsers.tenders.data import cookies, headers, json_data

translator = GoogleTranslator(source='auto', target='ru')
read = "https://gov.e-tender.ua/api/services/etender/readTender/GetTenders"
get = "https://gov.e-tender.ua/api/services/etender/getTender/GetTender"

#Функция для выполнения запросов
def data_request(type, cookies, headers, json_data):
    response = requests.post(
        type,
        cookies=cookies,
        headers=headers,
        json=json_data
    )
    return response


def cpvs(class_var, search_var):
    with open('parsers/tenders/classificators.json', 'r', encoding="utf-8") as file:
        dirr = json.load(file)

    match class_var:
        case 0:
            cpvs_list = dirr[search_var]
            json_data["TenderSearchFilter"]["Cpvs"] = cpvs_list 
        case 1:
            json_data["TenderSearchFilter"]["Title"] = search_var
        

#Функция выбора и ввода периода выгрузки
def date_choice(date_type: int, date_chosed: list):
    match date_type:
        case 0: 
            date1 = datetime.strptime(date_chosed[0], '%d.%m.%Y')
            date2 = date_chosed[0].split('.')
            date1 = str(date1 - timedelta(1)).split(' ')[0].split('-')
            json_data["TenderSearchFilter"]["tenderCreationTimeFrom"] = f'{date1[0]}-{date1[1]}-{date1[2]}T17:00:00.000Z'
            json_data["TenderSearchFilter"]["tenderCreationTimeTo"] = f'{date2[2]}-{date2[1]}-{date2[0]}T17:00:00.000Z'
        case 1:
            date = date_chosed[0].split(".")
            json_data["TenderSearchFilter"]["tenderCreationTimeFrom"] = f'{date[2]}-{date[1]}-{date[0]}T00:00:01.000Z'
            date = date_chosed[1].split(".")
            json_data["TenderSearchFilter"]["tenderCreationTimeTo"] = f'{date[2]}-{date[1]}-{date[0]}T23:59:59.000Z'
        case 2:
            pass

#Функция получения ссылок на тендеры
def get_links(type, tender):
    links = []
    if type == 1:
        json_data["TenderSearchFilter"]["ProcurementMethod"] = ["limited"]
        json_data["TenderSearchFilter"]["statuses"] = ['active', 'unsuccessful', 'complete', 'cancelled']
    elif type == 2:
        json_data["TenderSearchFilter"]["ProcurementMethod"] = ['open', 'selective']
        json_data["TenderSearchFilter"]["statuses"] = ['active.enquiries', 'active.tendering',
                                                      'active.pre-qualification',
                                                      'active.pre-qualification.stand-still',
                                                      'active.stage2.pending',
                                                      'active.stage2.waiting', 'active.auction',
                                                      'active.qualification',
                                                      'active.qualification.stand-still', 'active.awarded',
                                                      'unsuccessful', 'complete', 'cancelled']

    response = data_request(read, cookies, headers, json_data)
    page = response.json()
    print(page)
    records = page["result"]["countAllRecords"]
    tender.config(text=f"{tender.cget("text").replace("_", str(records))}")
    page_count = math.ceil(records / 20)

    for i in range(page_count):
        json_data["Page"] = i + 1
        response = data_request(read, cookies, headers, json_data)
        page = response.json()
        keys = [x for x in page["result"]["tender"]]
        for j in keys:
            links.append(j["url"])
    return links

#Функция получения данных из тендеров
def get_data(links, type, count, tree: tb.Treeview):
    arr = []
    for link in links:
        try:
            try:
                parts = link.split("/")
            except:
                continue

            json_data_get = {
                'id': None,
                'userName': None,
                'display': None,
                'url': parts[2],
                'categoryUrl': parts[1],
            }
            response = data_request(get, cookies, headers, json_data_get)

            page = response.json()
            quantity = 0
            count += 1
            value = 0
            startDate = ''
            endDate = ''
            title = page["result"]["title"]
            deliveryDate = page["result"]["lots"][0]["items"][0]["deliveryDate"]["endDate"].split("T")[0].split("-")
            deliveryDate = f"{deliveryDate[2]}.{deliveryDate[1]}.{deliveryDate[0]}"
            address = page["result"]["organization"]["address"]
            for j in page["result"]["lots"]:
                for q in j["items"]:
                    quantity += q["quantity"]
            p_name = 'Нет'
            o_name = 'Нет'
            try:
                value = page["result"]["value"]["amount"]
            except:
                pass
            try:
                p_name = page["result"]["organization"]["contactPoint"]["name"]
            except:
                pass
            try:
                o_name = page["result"]["organization"]["name"]
            except:
                pass

            if type == 1:
                startDate = page["result"]["creationTime"].split("T")[0].split("-")
                startDate = startDate[2] + "." + startDate[1] + "." + startDate[0]
                endDate = "Нет данных"
            elif type == 2:
                startDate = page["result"]["tenderPeriod"]["startDate"].split("T")[0].split("-")
                startDate = startDate[2] + "." + startDate[1] + "." + startDate[0]
                endDate = page["result"]["tenderPeriod"]["endDate"].split("T")[0].split("-")
                endDate = endDate[2] + "." + endDate[1] + "." + endDate[0]

            title = translator.translate(title)
            o_name = translator.translate(o_name)
            p_name = translator.translate(p_name)
            def holder(text):
                count = 0
                new_text = ''
                for char in range(len(text)):
                    if text[char] == "\"":
                        count += 1
                        if count % 2 == 1:
                            new_text += "«"
                        else:
                            new_text += "»"
                    else:
                        new_text += text[char]
                return new_text

            title = holder(title)
            o_name = holder(o_name)
            status = page["result"]["status"]
            if status == "unsuccessful":
                winner = "Закупка не состоялась"
                winner_place = ""
            elif status == "canceled":
                winner = "Закупка отменена"
                winner_place = ""
            elif status == "complete":
                winner = translator.translate(page["result"]["lots"][0]["awards"][0]["suppliers"][0]["name"])
                winner_place_country = page["result"]["lots"][0]["awards"][0]["suppliers"][0]["address"]["country"]["title"]
                winner_place_region = page["result"]["lots"][0]["awards"][0]["suppliers"][0]["address"]["region"]["title"]
                winner_place_city = page["result"]["lots"][0]["awards"][0]["suppliers"][0]["address"]["city"]["title"]
                winner_place_address = page["result"]["lots"][0]["awards"][0]["suppliers"][0]["address"]["addressStr"]
                winner_place = translator.translate(f"{winner_place_country}, {winner_place_region}, {winner_place_city}, {winner_place_address}")
            else:
                winner = "Закупка в процессе"
                winner_place = ""
            try:
                p_name = p_name.title()
            except:
                pass

            try:
                o_name = o_name.title()
            except:
                pass
            region = translator.translate(address["region"]["title"])
            city = translator.translate(f"{address['postIndex']}, {address['country']['title']}, {address['region']['title']}, {address['city']['title']}, {address['addressStr']}")
            arr.append([count,
                        title,
                        status,
                        quantity,
                        round(value, 2),
                        round(value * 0.025, 2),
                        startDate,
                        endDate,
                        deliveryDate,
                        region,
                        city,
                        p_name,
                        o_name,
                        winner,
                        winner_place])
            tree.insert('', "end", values=[arr[-1][0], arr[-1][1], arr[-1][3], arr[-1][5]])
            tree.yview_moveto(1)
        except Exception as e:
            print(e)
            continue
    return arr

#Функция сохрания файла
def save_tenders(tenders):
    wb = Workbook()
    ws = wb.active
    for i in tenders:
        ws.append(i)
    wb.save("Результаты/tender.xlsx")


def tender_parser(date_type: int, date_chosed: list, class_var: int, search_var: str, tree_sp: tb.Treeview, tree_label: tb.Label, tender_uncomp, tender_comp, button):

    print("Пошло говно")
    tenders = [["№", "Название тендера", "Статус", "Кол-во", "Сумма в гривнах", "Сумма в долларах", "Дата начала",
                "Дата завершения", "Дата доставки", "Область", "Адресс", "Контактное лицо", "Заказчик", "Победитель тендера", "Адресс победителя"]]
    date_choice(date_type, date_chosed)
    cpvs(class_var, search_var)
    tend1 = get_data(get_links(1, tender_uncomp), 1, 0, tree_sp)
    try: last_count = tend1[-1][0]
    except: last_count = 0
    tend2 = get_data(get_links(2, tender_comp), 2, last_count, tree_sp)
    tenders += tend1 + tend2
    tree_label.pack(pady=10)
    save_tenders(tenders)
    button.config(state=NORMAL)
