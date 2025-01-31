from lxml import etree
from openpyxl import Workbook
from deep_translator import GoogleTranslator
from tkinter import *
import ttkbootstrap as tb
import os
import json
import datetime
import math

translator = GoogleTranslator(source='auto', target='ru')

today = str(datetime.date.today()).split('-')
today = f"{today[2]}.{today[1]}.{today[0]}"

def get_positions(file, tree):
    arr = [['Подразделение', 'Номер части', 'Краткие сведения', 'Предыдущие появления', 'Широта начальная', 'Долгота начальная', 'Широта конечная', 'Долгота конечная', 'Растояние', 'Дата последнего появления']]
    positions = {}
    units = {}
    if os.path.exists('C:/Users/User/Desktop/GUI App/parsers/UCM/positions.json'):
        with open('C:/Users/User/Desktop/GUI App/parsers/UCM/positions.json', encoding="utf-8") as f:
            positions = json.load(f)
    for pos in file:
        try: name = pos.xpath('kml:name/text()', namespaces={"kml":"http://www.opengis.net/kml/2.2"})[0]
        except: continue
        if name == "Holding Area for Russian Forces" or name == "Holding Area for Ukrainian Forces":
            break
        if name in units:
            continue
        else:
            units[name] = "checked"
        try: unit = pos.xpath('kml:ExtendedData/kml:Data[@name="Military Unit Number"]/kml:value/text()',
                              namespaces={"kml":"http://www.opengis.net/kml/2.2"})[0]
        except: unit = ""
        try: description = pos.xpath('kml:ExtendedData/kml:Data[@name="description"]/kml:value/text()',
                                     namespaces={"kml":"http://www.opengis.net/kml/2.2"})[0]
        except: description = ""
        try: geo = pos.xpath('kml:ExtendedData/kml:Data[@name="Older Geolocations"]/kml:value/text()',
                                     namespaces={"kml":"http://www.opengis.net/kml/2.2"})[0]
        except: geo = ""
        description = description.replace('\n', ' ').replace('\xa0', '')
        try: cords = pos.xpath('kml:Point/kml:coordinates/text()',
                               namespaces={"kml":"http://www.opengis.net/kml/2.2"})[0]
        except: cords = ""
        cords = cords.replace(' ', '').replace('\n', '').split(",")
        try: lat = cords[1]
        except: lat = ''
        try: lon = cords[0]
        except: lon = ''
        if name in positions:
            t_name = positions[name]["t_name"]
        else:
            try:
                positions[name] = {"t_name": translator.translate(name)}
                t_name = positions[name]["t_name"]
            except: continue
        if "unit" in positions[name]:
            unit = positions[name]["unit"]
        else:
            try:
                positions[name]["unit"] = translator.translate(unit)
                unit = positions[name]["unit"]
            except: pass
        if "description" in positions[name]:
            description = positions[name]["desc"]
        else:
            try:
                positions[name]["desc"] = translator.translate(description)
                description = positions[name]["desc"]
            except: pass

        lat = lat.replace(".", ",")
        lon = lon.replace(".", ",")
        if "old_lat" not in positions[name]:
            positions[name]["old_lat"] = lat
        if "old_lon" not in positions[name]:
            positions[name]["old_lon"] = lon
        if "old_date" not in positions[name]:
            positions[name]["old_date"] = today
        if positions[name]["old_lat"] != lat or positions[name]["old_lon"] != lon:
            if "new_lat" not in positions[name]:
                positions[name]["new_lat"] = lat
            else:
                positions[name]["old_lat"] = positions[name]["new_lat"]
                positions[name]["new_lat"] = lat
            if "new_lon" not in positions[name]:
                positions[name]["new_lon"] = lon
            else:
                positions[name]["old_lon"] = positions[name]["new_lon"]
                positions[name]["new_lon"] = lon
            if "new_date" not in positions[name]:
                positions[name]["new_date"] = today
            else:
                positions[name]["old_date"] = positions[name]["new_date"]
                positions[name]["new_date"] = today

        if "new_date" in positions[name]:
            rad_old_lat = math.radians(float(positions[name]["old_lat"].replace(",", ".")))
            rad_old_lon = math.radians(float(positions[name]["old_lon"].replace(",", ".")))
            rad_new_lat = math.radians(float(positions[name]["new_lat"].replace(",", ".")))
            rad_new_lon = math.radians(float(positions[name]["new_lon"].replace(",", ".")))
            first_block = math.pow(math.sin((rad_old_lat - rad_new_lat) / 2), 2)
            second_block = math.pow(math.sin((rad_old_lon - rad_new_lon) / 2), 2)
            third_block = math.cos(rad_old_lat) * math.cos(rad_new_lat)
            positions[name]["distance"] = str(2 * 6371 * math.asin(math.sqrt(first_block + second_block * third_block)))
        print(f"{t_name} | {unit} | {description} | {positions[name]['old_lat']} | {positions[name]['old_lon']}")
        tree.insert('', "end", values=[t_name, positions[name]['old_lat'], positions[name]['old_lon']])
        tree.yview_moveto(1)
        farr = [t_name, unit, description, geo, positions[name]['old_lat'], positions[name]['old_lon'], lat, lon]
        if "distance" in positions[name] and positions[name]["distance"] != "0.0":
            farr.append(str(round(float(positions[name]["distance"]), 3)).replace(".", ","))
            farr.append(positions[name]["old_date"])
        arr.append(farr)

    arr.pop(1)
    arr.pop()
    with open("C:/Users/User/Desktop/GUI App/parsers/UCM/positions.json", "w", encoding="utf-8") as f:
        json.dump(positions, f, ensure_ascii=False, indent=4)
    return arr


def make_file(name, arr):
    wb = Workbook()
    ws = wb.active
    for i in arr:
        try:
            ws.append(i)
        except:
            ws.append(["Ошибка"])
    wb.save(f"Результаты/{name}.xlsx")


def ucm_parser(path, tb_tree: tb.Treeview, tree_label, button):
    try:
        tree = etree.parse(path)
        u_positions = tree.xpath('//kml:Folder', namespaces={"kml":"http://www.opengis.net/kml/2.2"})[2]
        r_positions = tree.xpath('//kml:Folder', namespaces={"kml":"http://www.opengis.net/kml/2.2"})[3]

        u_positions = get_positions(u_positions, tb_tree)
        r_positions = get_positions(r_positions, tb_tree)

        make_file("Позиции Украина", u_positions)
        make_file("Позиции Россия", r_positions)

        tree_label.pack(padx=10)
        button.config(state=NORMAL)
    except:
        button.config(state=NORMAL)