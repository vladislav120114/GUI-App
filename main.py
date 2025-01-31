from tkinter import *
from tkinter import filedialog
from parsers.tenders.parser import tender_parser
from parsers.UCM.UCM_Parser import ucm_parser
from parsers.overpass.overpass import over
from parsers.della.della import della_parser
from parsers.firemap.firemap_parser import firemap
from parsers.energy_map.energy_parser import energymap
import ttkbootstrap as tb
import json
import threading
import webbrowser

def one_day():
    label_1.config(text="2. Выберите дату выгрузки")
    label_1_1.pack_forget()
    date_entry_0.pack(side=LEFT, padx=10)
    date_entry_1.pack_forget()

def few_days():
    label_1.config(text="2. Выберите даты выгрузки")
    label_1_1.pack_forget()
    date_entry_0.pack(side=LEFT, padx=10)
    date_entry_1.pack(side=LEFT, padx=10)
    
def all_days():
    label_1_1.pack(side=TOP)
    date_entry_0.pack_forget()
    date_entry_1.pack_forget()

def entry_class():
    label_3.config(text="4. Введите ключевое слово")
    class_combo.pack_forget()
    class_entry.pack()

def combobox_class():
    label_3.config(text="4. Выберите классификатор выгрузки")
    class_entry.pack_forget()
    class_combo.pack()

def tenders():
    button_start.config(state=DISABLED)
    for row in tree.get_children():
        tree.delete(row)
    tender_uncomp.config(text="Кол-во неконкурентных тендеров: _")
    tender_comp.config(text="Кол-во конкурентных тендеров: _")
    tree_label.pack_forget()
    date_arr = []
    search_var = ""
    match date_var.get():
        case 0:
            date_arr = [str(date_entry_0.entry.get())]
        case 1:
            date_arr = [str(date_entry_0.entry.get()), str(date_entry_1.entry.get())]
        case 2:
            date_arr = []
    match class_var.get():
        case 0:
            search_var = class_combo.get()
        case 1:
            search_var = class_entry.get()
    print(date_var, date_arr, class_var, search_var, tree)
    thread_parser = threading.Thread(target=tender_parser, args=(date_var.get(), date_arr, class_var.get(), search_var, tree, tree_label, tender_uncomp, tender_comp, button_start))
    thread_parser.start()

def get_path():
    filepath = filedialog.askopenfilename(filetypes=(("kml files", "*.kml"), ("all files", "*.*")))
    ucm_path.config(text=f'{filepath}')

def ucm():
    ucm_button_2.config(state=DISABLED)
    for row in ucm_tree.get_children():
        ucm_tree.delete(row)
    ucm_tree_label.pack_forget()
    path = ucm_path.cget("text")
    thread_ucm = threading.Thread(target=ucm_parser, args=(path, ucm_tree, ucm_tree_label, ucm_button_2))
    thread_ucm.start()

def callback(url):
    webbrowser.open_new(url)

def overpass_building():
    overpass_button_1.config(state=DISABLED)
    overpass_button_2.config(state=DISABLED)
    for row in overpass_tree.get_children():
        overpass_tree.delete(row)
    overpass_tree_label.pack_forget()
    key = overpass_entry_1.get()
    value = overpass_entry_2.get()
    name = overpass_entry_3.get()
    overpass_tree_label.config(text=f"Данные сохранены в файле {overpass_entry_3.get()}.xlsx в папке Результаты")
    thread_overpass = threading.Thread(target=over, args=(key, value, name, overpass_tree, overpass_tree_label, overpass_button_1, overpass_button_2, "buidings"))
    thread_overpass.start()

def overpass_roads():
    overpass_button_1.config(state=DISABLED)
    overpass_button_2.config(state=DISABLED)
    for row in overpass_tree.get_children():
        overpass_tree.delete(row)
    overpass_tree_label.pack_forget()
    key = overpass_entry_1.get()
    value = overpass_entry_2.get()
    name = overpass_entry_3.get()
    overpass_tree_label.config(text=f"Данные сохранены в файле {overpass_entry_3.get()}.xlsx в папке Результаты")
    thread_overpass = threading.Thread(target=over, args=(key, value, name, overpass_tree, overpass_tree_label, overpass_button_1, overpass_button_2, "roads"))
    thread_overpass.start()

def della_eu():
    della_button_1.config(state=DISABLED)
    della_button_2.config(state=DISABLED)
    for row in della_tree.get_children():
        della_tree.delete(row)
    della_tree_label.pack_forget()
    della_tree_label.config(text="Данные сохранены в файле della_eu.xlsx в папке Результаты")
    thread_overpass = threading.Thread(target=della_parser, args=(della_tree, della_tree_label, "eu", della_button_1, della_button_2))
    thread_overpass.start()

def della_ua():
    della_button_1.config(state=DISABLED)
    della_button_2.config(state=DISABLED)
    for row in della_tree.get_children():
        della_tree.delete(row)
    della_tree_label.pack_forget()
    della_tree_label.config(text="Данные сохранены в файле della_ua.xlsx в папке Результаты")
    thread_overpass = threading.Thread(target=della_parser, args=(della_tree, della_tree_label, "ua", della_button_1, della_button_2))
    thread_overpass.start()

def firemap_24h():
    firemap_button_1.config(state=DISABLED)
    firemap_button_2.config(state=DISABLED)
    firemap_button_3.config(state=DISABLED)
    for row in firemap_tree.get_children():
        firemap_tree.delete(row)
    firemap_tree_label.pack_forget()
    thread_overpass = threading.Thread(target=firemap, args=("24h", firemap_tree, firemap_tree_label, firemap_button_1, firemap_button_2, firemap_button_3))
    thread_overpass.start()

def firemap_48h():
    firemap_button_1.config(state=DISABLED)
    firemap_button_2.config(state=DISABLED)
    firemap_button_3.config(state=DISABLED)
    for row in firemap_tree.get_children():
        firemap_tree.delete(row)
    firemap_tree_label.pack_forget()
    thread_overpass = threading.Thread(target=firemap, args=("48h", firemap_tree, firemap_tree_label, firemap_button_1, firemap_button_2, firemap_button_3))
    thread_overpass.start()

def firemap_7d():
    firemap_button_1.config(state=DISABLED)
    firemap_button_2.config(state=DISABLED)
    firemap_button_3.config(state=DISABLED)
    for row in firemap_tree.get_children():
        firemap_tree.delete(row)
    firemap_tree_label.pack_forget()
    thread_overpass = threading.Thread(target=firemap, args=("7d", firemap_tree, firemap_tree_label, firemap_button_1, firemap_button_2, firemap_button_3))
    thread_overpass.start()

def energymap_parser():
    energymap_button_1.config(state=DISABLED)
    for row in firemap_tree.get_children():
        firemap_tree.delete(row)
    csrftoken = energymap_entry_1.get()
    sessionid = energymap_entry_2.get()
    thread_overpass = threading.Thread(target=energymap, args=(csrftoken, sessionid, energymap_tree, energymap_button_1))
    thread_overpass.start()

window = tb.Window(themename="darkly")
window.title("Ultimate Parser")
window.geometry("960x540")
window.maxsize(960, 540)
window.minsize(960, 540)

date_var = IntVar()
date_var.set(0)

class_var = IntVar()
class_var.set(0)

with open("parsers/tenders/classificators.json", "r", encoding="utf-8") as file:
    cl = json.load(file)

arr = []

for i in cl:
    arr.append(i)

notebook = tb.Notebook(window)

tab_1 = tb.Frame(notebook)
tab_2 = tb.Frame(notebook)
tab_3 = tb.Frame(notebook)
tab_4 = tb.Frame(notebook)
tab_5 = tb.Frame(notebook)
tab_6 = tb.Frame(notebook)

notebook.add(tab_1, text="E-tender")
notebook.add(tab_2, text="Ukraine Control Map")
notebook.add(tab_3, text="Overpass Turbo")
notebook.add(tab_4, text="Della")
notebook.add(tab_5, text="Fire Map")
notebook.add(tab_6, text="Energy Map")
notebook.pack(expand=True, fill="both")

# 1 - E-Tender

column_0 = tb.Frame(tab_1, width=480, height=540)
column_1 = tb.Frame(tab_1, width=480, height=540)
column_0.pack(side=LEFT, fill=Y, expand=True)
column_1.pack(side=RIGHT, fill=Y, expand=True)

column_0_c = tb.Frame(column_0)
column_0_l = tb.Label(column_0, text="Настройки выгрузки\n(Перед работой обязательно включить VPN)", font=("Jost", 16), bootstyle="warning", justify='center')
column_0_l.place(relx=.5, rely=.1, anchor=CENTER)
column_0_c.place(relx=.5, rely=.55, anchor=CENTER)

row_0_0 = tb.Frame(column_0_c)
label_0 = tb.Label(row_0_0, text="1. Выберите период выгрузки", font=("Jost"))
date_radio_0 = tb.Radiobutton(row_0_0, bootstyle="warning", variable=date_var, text="За один день", value=0, command=one_day)
date_radio_1 = tb.Radiobutton(row_0_0, bootstyle="warning", variable=date_var, text="За несколько дней", value=1, command=few_days)
date_radio_2 = tb.Radiobutton(row_0_0, bootstyle="warning", variable=date_var, text="За все время", value=2, command=all_days)

row_0_0.pack()
label_0.pack(side=TOP, pady=10)
date_radio_0.pack(side=LEFT, padx=10)
date_radio_1.pack(side=LEFT, padx=10)
date_radio_2.pack(side=LEFT, padx=10)

row_0_1 = tb.Frame(column_0_c)
label_1 = tb.Label(row_0_1, text="2. Введите дату выгрузки", font="Jost")
label_1_1 = tb.Label(row_0_1, text="Выбрана выгрузка за все время", font="Jost", bootstyle="warning")
date_entry_0 = tb.DateEntry(row_0_1, bootstyle="warning")
date_entry_1 = tb.DateEntry(row_0_1, bootstyle="warning")

row_0_1.pack()
label_1.pack(side=TOP, pady=10)
date_entry_0.pack(side=LEFT, padx=10)

row_0_2 = tb.Frame(column_0_c)
label_2 = tb.Label(row_0_2, text="3. Выберите тип выгрузки", font="Jost")
class_radio_0 = tb.Radiobutton(row_0_2, bootstyle="warning", variable=class_var, text="По классификаторам", value=0, command=combobox_class)
class_radio_1 = tb.Radiobutton(row_0_2, bootstyle="warning", variable=class_var, text="По ключевому слову", value=1, command=entry_class)

row_0_2.pack()
label_2.pack(side=TOP, pady=10)
class_radio_0.pack(side=LEFT, padx=10)
class_radio_1.pack(side=LEFT, padx=10)

row_0_3 = tb.Frame(column_0_c)
label_3 = tb.Label(row_0_3, text="4. Выберите классификатор выгрузки", font="Jost")
class_combo = tb.Combobox(row_0_3, bootstyle="warning", values=arr, font="Jost")
class_entry = tb.Entry(row_0_3, bootstyle="warning", font="Jost")
class_combo.current(0)

row_0_3.pack()
label_3.pack(side=TOP, pady=10)
class_combo.pack()

row_0_4 = tb.Frame(column_0_c)
label_4 = tb.Label(row_0_4, text="5. Начните выгрузку", font="Jost")
button_start = tb.Button(row_0_4, text="Старт", bootstyle="warning", width=15, command=tenders)

row_0_4.pack()
label_4.pack(side=TOP, pady=10)
button_start.pack()

column_1_c = tb.Frame(column_1)
column_1_l = tb.Label(column_1, text="Вывод результатов", font=("Jost", 16), bootstyle="warning")
column_1_l.place(relx=.5, rely=.1, anchor=CENTER)
column_1_c.place(relx=.5, rely=.55, anchor=CENTER)

columns = ("№", "Название тендера", "Кол-во", "Сумма в долларах")

tender_uncomp = tb.Label(column_1_c, text="Кол-во неконкурентных тендеров: _", font="Jost")
tender_comp = tb.Label(column_1_c, text="Кол-во конкурентных тендеров: _", font="Jost")
tree_top = tb.Label(column_1_c, text="Данные в таблице выводятся в сокращенном виде", font="Jost", bootstyle="warning")
tree_frame = tb.Frame(column_1_c)
tree = tb.Treeview(tree_frame, columns=columns, show="headings")
tree_label = tb.Label(column_1_c, text="Данные сохранены в файле tender.xlsx в папке Результаты", font="Jost", bootstyle="warning")

tender_uncomp.pack()
tender_comp.pack()
tree_top.pack(pady=20)
tree_frame.pack()
tree.pack(side=LEFT)

tree.heading("№", text="№", anchor=W)
tree.heading("Название тендера", text="Название тендера", anchor=W)
tree.heading("Кол-во", text="Кол-во техники", anchor=W)
tree.heading("Сумма в долларах", text="Сумма в долларах", anchor=W)

tree.column("#1", stretch=NO, width=30)
tree.column("#2", stretch=NO, width=120)
tree.column("#3", stretch=NO, width=100)
tree.column("#4", stretch=NO, width=120)

scrollbar = tb.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview, bootstyle="warning-round")
scrollbar.pack(side=LEFT, fill='y')
tree.configure(yscroll=scrollbar.set)

# 2 - Ukraine Control Map

column_2 = tb.Frame(tab_2, width=480, height=540)
column_3 = tb.Frame(tab_2, width=480, height=540)
column_2.pack(side=LEFT, fill="both", expand=True)
column_3.pack(side=LEFT, fill="both", expand=True)

column_2_c = tb.Frame(column_2)
column_3_c = tb.Frame(column_3)
column_2_l = tb.Label(column_2, text="Ввод файла выгрузки", font=("Jost", 16), bootstyle="warning", justify='center')
column_2_l.place(relx=.5, rely=.1, anchor=CENTER)
column_2_c.place(relx=.5, rely=.55, anchor=CENTER)
column_3_c.place(relx=.5, rely=.55, anchor=CENTER)
ucm_label_3 = tb.Label(column_3, text="Вывод результатов", font=("Jost", 16), bootstyle="warning")
ucm_label_3.place(relx=.5, rely=.1, anchor=CENTER)

ucm_label_start = tb.Label(column_2_c, text="1. Скачайте kml файл карты по ссылке", font="Jost")
ucm_label_link = tb.Label(column_2_c, text="[Ссылка по клику]", font="Jost", cursor="hand2", bootstyle="warning")
ucm_label = tb.Label(column_2_c, text="2. Выберите kml файл для выгрузки", font="Jost")
ucm_button = tb.Button(column_2_c, text="Выбор файла", bootstyle="warning", width=15, command=get_path)
ucm_path = tb.Label(column_2_c, text="[Здесь будет отображаться путь до файла]", font=("Jost", 12), bootstyle="warning")
ucm_label_start.pack()
ucm_label_link.pack(pady=10)
ucm_label_link.bind("<Button-1>", lambda e: callback("https://www.google.com/maps/d/u/0/viewer?mid=1xPxgT8LtUjuspSOGHJc2VzA5O5jWMTE"))
ucm_label.pack()
ucm_button.pack(pady=10)
ucm_path.pack()

ucm_label_2 = tb.Label(column_2_c, text="3. Начните выгрузку", font="Jost")
ucm_button_2 = tb.Button(column_2_c, text="Старт", bootstyle="warning", width=15, command=ucm)
ucm_label_2.pack()
ucm_button_2.pack(pady=10)

ucm_label_4 = tb.Label(column_2_c, text="Примечание. Файл сравнивает координаты подразделений\nс координатами полученными при предыдущей выгрузке.\n Если это первая выгрузка, сравнивать будет не с чем.", font="Jost", justify='center')
ucm_label_4.pack()

ucm_columns = ("Подразделение", "Широта", "Долгота")

ucm_tree_top = tb.Label(column_3_c, text="Данные в таблице выводятся в сокращенном виде", font="Jost", bootstyle="warning")
ucm_tree_frame = tb.Frame(column_3_c)
ucm_tree = tb.Treeview(ucm_tree_frame, columns=ucm_columns, show="headings")

ucm_tree_top.pack(pady=10)
ucm_tree_frame.pack(pady=10)
ucm_tree.pack(side=LEFT)

ucm_scrollbar = tb.Scrollbar(ucm_tree_frame, orient=VERTICAL, command=tree.yview, bootstyle="warning-round")
ucm_scrollbar.pack(side=LEFT, fill='y')
ucm_tree.configure(yscroll=ucm_scrollbar.set)

ucm_tree.heading("Подразделение", text="Подразделение", anchor=W)
ucm_tree.heading("Широта", text="Широта", anchor=W)
ucm_tree.heading("Долгота", text="Долгота", anchor=W)

ucm_tree.column("#1", stretch=NO, width=200)
ucm_tree.column("#2", stretch=NO, width=100)
ucm_tree.column("#3", stretch=NO, width=100)

ucm_tree_label = tb.Label(column_3_c, text="Данные сохранены в файлах Позиции Украины.xlsx\nи Позиции России.xlsx в папке Результаты", font="Jost", bootstyle="warning", justify="center")

# 3 - Overpass

overpass_column_left = tb.Frame(tab_3, width=480, height=540)
overpass_column_right = tb.Frame(tab_3, width=480, height=540)
overpass_column_left.pack(side=LEFT, fill="both", expand=True)
overpass_column_right.pack(side=RIGHT, fill="both", expand=True)

overpass_inner_column_left = tb.Frame(overpass_column_left)
overpass_inner_column_right = tb.Frame(overpass_column_right)
overpass_label_column_left = tb.Label(overpass_column_left, text="Настройка выгрузки", font=("Jost", 16), bootstyle="warning", justify='center')
overpass_label_column_right = tb.Label(overpass_column_right, text="Вывод результатов", font=("Jost", 16), bootstyle="warning", justify='center')

overpass_inner_column_left.place(relx=.5, rely=.55, anchor=CENTER)
overpass_inner_column_right.place(relx=.5, rely=.55, anchor=CENTER)
overpass_label_column_left.place(relx=.5, rely=.1, anchor=CENTER)
overpass_label_column_right.place(relx=.5, rely=.1, anchor=CENTER)

overpass_label_1 = tb.Label(overpass_inner_column_left, text="1. Введите ключ и значение объекта поиска\nА также название файла для сохранения.\nВыгружаются объекты только на территории Украины.\nНайти ключи и их занчения можно на сайте\nwiki.openstreetmap.org", font="Jost", justify="center")
overpass_label_1.pack()

overpass_row_1 = tb.Frame(overpass_inner_column_left)
overpass_entry_1_label = tb.Label(overpass_row_1, text="Ключ", font="Jost", bootstyle="warning")
overpass_entry_1 = tb.Entry(overpass_row_1, bootstyle="warning", font="Jost")
overpass_row_1.pack(pady=10)
overpass_entry_1_label.pack(side=LEFT, padx=10)
overpass_entry_1.pack(side=LEFT)

overpass_row_2 = tb.Frame(overpass_inner_column_left)
overpass_entry_2_label = tb.Label(overpass_row_2, text="Значение", font="Jost", bootstyle="warning")
overpass_entry_2 = tb.Entry(overpass_row_2, bootstyle="warning", font="Jost")
overpass_row_2.pack()
overpass_entry_2_label.pack(side=LEFT, padx=10)
overpass_entry_2.pack(side=LEFT, pady=10)

overpass_row_3 = tb.Frame(overpass_inner_column_left)
overpass_entry_3_label = tb.Label(overpass_row_3, text="Название файла", font="Jost", bootstyle="warning")
overpass_entry_3 = tb.Entry(overpass_row_3, bootstyle="warning", font="Jost")
overpass_row_3.pack()
overpass_entry_3_label.pack(side=LEFT, padx=10)
overpass_entry_3.pack(side=LEFT, pady=10)

overpass_label_2 = tb.Label(overpass_inner_column_left, text="2. Выберите и начните нужный формат выгрузки:\n"
                            "Объект - выгрузка первой координаты и всех характеристик\n"
                            "Путь - выгрузка всех координат и характеристик", font="Jost", justify="center")
overpass_row_4 = tb.Frame(overpass_inner_column_left)
overpass_button_1 = tb.Button(overpass_row_4, text="Объект", bootstyle="warning", width=15, command=overpass_building)
overpass_button_2 = tb.Button(overpass_row_4, text="Путь", bootstyle="warning", width=15, command=overpass_roads)

overpass_label_2.pack()
overpass_row_4.pack()
overpass_button_1.pack(pady=10, side=LEFT, padx=10)
overpass_button_2.pack(side=LEFT)

overpass_columns = ("Широта", "Долгота")

overpass_tree_top = tb.Label(overpass_inner_column_right, text="Данные в таблице выводятся в сокращенном виде", font="Jost", bootstyle="warning")
overpass_tree_frame = tb.Frame(overpass_inner_column_right)
overpass_tree = tb.Treeview(overpass_tree_frame, columns=overpass_columns, show="headings")

overpass_tree_top.pack(pady=10)
overpass_tree_frame.pack(pady=10)
overpass_tree.pack(side=LEFT)

overpass_scrollbar = tb.Scrollbar(overpass_tree_frame, orient=VERTICAL, command=tree.yview, bootstyle="warning-round")
overpass_scrollbar.pack(side=LEFT, fill='y')
overpass_tree.configure(yscroll=overpass_scrollbar.set)

overpass_tree.heading("Широта", text="Широта", anchor=W)
overpass_tree.heading("Долгота", text="Долгота", anchor=W)

overpass_tree.column("#1", stretch=NO, width=100)
overpass_tree.column("#2", stretch=NO, width=100)

overpass_tree_label = tb.Label(overpass_inner_column_right, text=f"Данные сохранены в файле .xlsx в папке Результаты", font="Jost", bootstyle="warning")

# 4 - Della

della_column = tb.Frame(tab_4)
della_column.pack(side=LEFT, fill="both", expand=True)

della_inner_column = tb.Frame(della_column)
della_label_column = tb.Label(della_column, text="Грузоперевозки Della", font=("Jost", 16), bootstyle="warning", justify='center')

della_inner_column.place(relx=.5, rely=.55, anchor=CENTER)
della_label_column.place(relx=.5, rely=.1, anchor=CENTER)

della_label_1 = tb.Label(della_inner_column, text="1. Выберите тип выгрузки", font="Jost", justify="center")
della_label_1.pack()

della_row_1 = tb.Frame(della_inner_column)
della_button_1 = tb.Button(della_row_1, text="Европа - Украина", bootstyle="warning", width=17, command=della_eu)
della_button_2 = tb.Button(della_row_1, text="Внутри Украины", bootstyle="warning", width=15, command=della_ua)

della_row_1.pack()
della_button_1.pack(pady=10, side=LEFT, padx=10)
della_button_2.pack(side=LEFT)

della_columns = ("Груз", "Место загрузки", "Место разгрузки")

della_tree_top = tb.Label(della_inner_column, text="Данные в таблице выводятся в сокращенном виде", font="Jost", bootstyle="warning")
della_tree_frame = tb.Frame(della_inner_column)
della_tree = tb.Treeview(della_tree_frame, columns=della_columns, show="headings")

della_tree_top.pack(pady=10)
della_tree_frame.pack(pady=10)
della_tree.pack(side=LEFT)

della_scrollbar = tb.Scrollbar(della_tree_frame, orient=VERTICAL, command=tree.yview, bootstyle="warning-round")
della_scrollbar.pack(side=LEFT, fill='y')
della_tree.configure(yscroll=della_scrollbar.set)

della_tree.heading("Груз", text="Груз", anchor=W)
della_tree.heading("Место загрузки", text="Место загрузки", anchor=W)
della_tree.heading("Место разгрузки", text="Место разгрузки", anchor=W)

della_tree.column("#1", stretch=NO, width=100)
della_tree.column("#2", stretch=NO, width=150)
della_tree.column("#3", stretch=NO, width=150)

della_tree_label = tb.Label(della_inner_column, text="Данные сохранены в файле della.xlsx в папке Результаты", font="Jost", bootstyle="warning")

# 5 - Fire Map

firemap_column = tb.Frame(tab_5)
firemap_column.pack(side=LEFT, fill="both", expand=True)

firemap_inner_column = tb.Frame(firemap_column)
firemap_label_column = tb.Label(firemap_column, text="Карта пожаров NASA Fire Map", font=("Jost", 16), bootstyle="warning", justify='center')

firemap_inner_column.place(relx=.5, rely=.55, anchor=CENTER)
firemap_label_column.place(relx=.5, rely=.1, anchor=CENTER)

firemap_label_1 = tb.Label(firemap_inner_column, text="1. Выберите тип выгрузки", font="Jost", justify="center")
firemap_label_1.pack()

firemap_row_1 = tb.Frame(firemap_inner_column)
firemap_button_1 = tb.Button(firemap_row_1, text="1 День", bootstyle="warning", width=15, command=firemap_24h)
firemap_button_2 = tb.Button(firemap_row_1, text="2 Дня", bootstyle="warning", width=15, command=firemap_48h)
firemap_button_3 = tb.Button(firemap_row_1, text="7 Дней", bootstyle="warning", width=15, command=firemap_7d)

firemap_row_1.pack()
firemap_button_1.pack(pady=10, side=LEFT)
firemap_button_2.pack(side=LEFT, padx=10)
firemap_button_3.pack(side=LEFT)

firemap_columns = ("Широта", "Долгота", "Область", "Дата")

firemap_tree_top = tb.Label(firemap_inner_column, text="Данные в таблице выводятся в сокращенном виде", font="Jost", bootstyle="warning")
firemap_tree_frame = tb.Frame(firemap_inner_column)
firemap_tree = tb.Treeview(firemap_tree_frame, columns=firemap_columns, show="headings")

firemap_tree_top.pack(pady=10)
firemap_tree_frame.pack(pady=10)
firemap_tree.pack(side=LEFT)

firemap_scrollbar = tb.Scrollbar(firemap_tree_frame, orient=VERTICAL, command=tree.yview, bootstyle="warning-round")
firemap_scrollbar.pack(side=LEFT, fill='y')
firemap_tree.configure(yscroll=firemap_scrollbar.set)

firemap_tree.heading("Широта", text="Широта", anchor=W)
firemap_tree.heading("Долгота", text="Долгота", anchor=W)
firemap_tree.heading("Область", text="Область", anchor=W)
firemap_tree.heading("Дата", text="Дата", anchor=W)

firemap_tree.column("#1", stretch=NO, width=100)
firemap_tree.column("#2", stretch=NO, width=100)
firemap_tree.column("#3", stretch=NO, width=150)
firemap_tree.column("#4", stretch=NO, width=100)

firemap_tree_label = tb.Label(firemap_inner_column, text="Данные сохранены в файле fire_map.xlsx в папке Результаты", font="Jost", bootstyle="warning")

# 6 - Energy Map

energymap_column_left = tb.Frame(tab_6, width=480, height=540)
energymap_column_right = tb.Frame(tab_6, width=480, height=540)
energymap_column_left.pack(side=LEFT, fill="both", expand=True)
energymap_column_right.pack(side=RIGHT, fill="both", expand=True)

energymap_inner_column_left = tb.Frame(energymap_column_left)
energymap_inner_column_right = tb.Frame(energymap_column_right)
energymap_label_column_left = tb.Label(energymap_column_left, text="Настройка выгрузки", font=("Jost", 16), bootstyle="warning", justify='center')
energymap_label_column_right = tb.Label(energymap_column_right, text="Вывод результатов", font=("Jost", 16), bootstyle="warning", justify='center')

energymap_inner_column_left.place(relx=.5, rely=.55, anchor=CENTER)
energymap_inner_column_right.place(relx=.5, rely=.55, anchor=CENTER)
energymap_label_column_left.place(relx=.5, rely=.1, anchor=CENTER)
energymap_label_column_right.place(relx=.5, rely=.1, anchor=CENTER)

energymap_label_1 = tb.Label(energymap_inner_column_left, text="1. Зарегистрируйтесь на сайте https://map.ua-energy.org/\nРекомендуется использовать временную почту\n(Обязательно используйте VPN)", font="Jost", justify="center")
energymap_label_1.pack()
energymap_label_2 = tb.Label(energymap_inner_column_left, text="2. Перейдите во вкладку 'data'\nВключите просмотр запросов сайта\n(ПКМ -> Посмотреть код -> Network)", font="Jost", justify="center")
energymap_label_2.pack()
energymap_label_3 = tb.Label(energymap_inner_column_left, text="3. Скачайте любой файл\nВ окне запросов найдите запрос modal\nОткройте вкладку cookies", font="Jost", justify="center")
energymap_label_3.pack()
energymap_label_4 = tb.Label(energymap_inner_column_left, text="4. Подставьте csrftoken и sessionid в поля программы", font="Jost", justify="center")
energymap_label_4.pack()

energymap_row_1 = tb.Frame(energymap_inner_column_left)
energymap_entry_1_label = tb.Label(energymap_row_1, text="csrftoken", font="Jost", bootstyle="warning")
energymap_entry_1 = tb.Entry(energymap_row_1, bootstyle="warning", font="Jost")
energymap_row_1.pack(pady=10)
energymap_entry_1_label.pack(side=LEFT, padx=10)
energymap_entry_1.pack(side=LEFT)

energymap_row_2 = tb.Frame(energymap_inner_column_left)
energymap_entry_2_label = tb.Label(energymap_row_2, text="sessionid", font="Jost", bootstyle="warning")
energymap_entry_2 = tb.Entry(energymap_row_2, bootstyle="warning", font="Jost")
energymap_row_2.pack()
energymap_entry_2_label.pack(side=LEFT, padx=10)
energymap_entry_2.pack(side=LEFT, pady=10)

energymap_label_2 = tb.Label(energymap_inner_column_left, text="5. Начните выгрузку", font="Jost", justify="center")
energymap_button_1 = tb.Button(energymap_inner_column_left, text="Старт", bootstyle="warning", width=15, command=energymap_parser)

energymap_label_2.pack()
energymap_button_1.pack(pady=10)

energymap_columns = ("Файл")

energymap_tree_top = tb.Label(energymap_inner_column_right, text="Данные в таблице выводятся в сокращенном виде", font="Jost", bootstyle="warning")
energymap_tree_frame = tb.Frame(energymap_inner_column_right)
energymap_tree = tb.Treeview(energymap_tree_frame, columns=energymap_columns, show="headings")

energymap_tree_top.pack(pady=10)
energymap_tree_frame.pack(pady=10)
energymap_tree.pack(side=LEFT)

energymap_scrollbar = tb.Scrollbar(energymap_tree_frame, orient=VERTICAL, command=tree.yview, bootstyle="warning-round")
energymap_scrollbar.pack(side=LEFT, fill='y')
energymap_tree.configure(yscroll=energymap_scrollbar.set)

energymap_tree.heading("Файл", text="Файл", anchor=W)

energymap_tree.column("#1", stretch=NO, width=400)

energymap_tree_label = tb.Label(energymap_inner_column_right, text=f"Файлы сохраняются в папке Результаты/Выгрузка", font="Jost", bootstyle="warning")
energymap_tree_label.pack(padx=10)

window.mainloop()