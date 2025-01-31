import xml.etree.ElementTree as ET
import requests
from openpyxl import Workbook
from tkinter import *
cookies = {
    '_pk_ref.1.cf09': '%5B%22%22%2C%22%22%2C1711449710%2C%22https%3A%2F%2Fopeninframap.org%2F%22%5D',
    '_pk_id.1.cf09': 'a800cfd961ff0b27.1710848097.',
    '_osm_location': '30.57151|50.39838|19|M',
    '_osm_session': 'ff12a5d7f765f56d4fcd0775f50543b0',
    '_pk_ses.1.cf09': '1',
    '_osm_totp_token': '676799',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://overpass-turbo.eu/',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://overpass-turbo.eu',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
}

def toFixed(num, dig=0):
    return f"{num:.{dig}f}"

def check(key, value, tb_tree, load_type):

    data = f'data=area(id%3A3600060199)-%3E.searchArea%3B%0Anwr%5B%22{key}%22%3D%22{value}%22%5D(area.searchArea)%3B%0Aout%3B'

    response = requests.post('https://overpass-api.de/api/interpreter', headers=headers, data=data).text
    tree = ET.fromstring(response)

    arr = []
    for node in tree.findall("node"):
        n = []
        lat = node.attrib["lat"]
        lon = node.attrib["lon"]
        n.append(lat)
        n.append(lon)
        for tag in node.findall("tag"):
            n.append(f"{tag.attrib['k']} = {tag.attrib['v']}")
        arr.append(n)
        tb_tree.insert('', "end", values=[lat, lon])
        tb_tree.yview_moveto(1)
        print(n)
    match load_type:
        case "roads":
            for way in tree.findall('way'):
                n = []
                way_resp = requests.get('https://www.openstreetmap.org/api/0.6/way/'+way.attrib["id"]+'/full', headers=headers, cookies=cookies).text
                way_point = ET.fromstring(way_resp)
                nodes = way_point.findall('node')
                for i in nodes:
                    n.append(f'{i.attrib['lat']}; {i.attrib['lon']}')
                for tag in way.findall("tag"):
                    n.append(f"{tag.attrib['k']} = {tag.attrib['v']}")
                tb_tree.insert('', "end", values=[way_point.findall('node')[0].attrib['lat'], way_point.findall('node')[0].attrib['lon']])
                tb_tree.yview_moveto(1)  
                arr.append(n)
                print(n)

        case "buidings":
            for way in tree.findall('way'):
                n = []
                way_resp = requests.get(f'https://www.openstreetmap.org/api/0.6/way/{way.attrib["id"]}/full', headers=headers, cookies=cookies).text
                way_point = ET.fromstring(way_resp)
                n.append(way_point.findall('node')[0].attrib['lat'])
                n.append(way_point.findall('node')[0].attrib['lon'])
                for tag in way.findall("tag"):
                    n.append(f"{tag.attrib['k']} = {tag.attrib['v']}")
                tb_tree.insert('', "end", values=[way_point.findall('node')[0].attrib['lat'], way_point.findall('node')[0].attrib['lon']])
                tb_tree.yview_moveto(1)    
                arr.append(n)
                print(n)
    return arr

def over(key, value, name, tb_tree, tree_label, button_1, button_2, load_type):
    #try:
    arr = check(key, value, tb_tree, load_type)
    wb = Workbook()
    ws = wb.active
    for i in arr:
        try:
            ws.append(i)
        except:
            ws.append(["Ошибка"])

    wb.save(f"Результаты/{name}.xlsx")
    tree_label.pack(padx=10)
    button_1.config(state=NORMAL)
    button_2.config(state=NORMAL)
    #except:
        #button_1.config(state=NORMAL)
        #button_2.config(state=NORMAL)