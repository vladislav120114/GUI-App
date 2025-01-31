import pandas as pd
import networkx as nx
import netwulf as nw

data = pd.read_excel('C:/Users/User/Desktop/GUI App/Результаты/della_ua.xlsx')

G = nx.Graph()
arr = {}
for index, row in data.iterrows():
    start = row['Место загрузки (перевод)']
    end = row['Место разгрузки (перевод)']
    if start not in arr:
        arr[start] = []
        if end not in arr[start]:
            arr[start].append(end)
    else:
        if end not in arr[start]:
            arr[start].append(end)
    
for i in arr:
    for j in arr[i]:
        G.add_edge(i, j)

network, config = nw.visualize(G, config={'zoom': 3})

fig, ax = nw.draw_netwulf(network, draw_nodes=False)
