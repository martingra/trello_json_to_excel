#!/usr/bin/env python3
import json
import os
import argparse
import pandas as pd

print("Que archivo desea convertir?")
inputFile = input("Archivo: ")
print("Desea obtener solo excel (1) o excel y json (2)?")
excelJson = input("Ingrese 1 o 2: ")

with open(os.path.abspath(inputFile)) as f:
    data = json.load(f)

print("Se encontraron {} cards en {} lists.".format(len(data['cards']), len(data['lists'])))
print("Parsing...")

lists = {l['id']: l['name'] for l in data['lists']}
users = {u['id']: u['fullName'] for u in data['members']}
labels = {l['id']: l['name'] for l in data['labels']}

parsed_cards = [{
    "name": c['name'],
    "list": lists[c['idList']],
    "description": c['desc'],
    "members": [u for k, u in users.items() if k in c['idMembers']],
    "labels": [l for k, l in labels.items() if k in c['idLabels']]
} for c in data['cards']]

output = {
    "board_data": {
        "name": data['name'],
        "url": data['shortUrl']
    },
    "cards": parsed_cards
}

if excelJson == '2':
	with open(os.path.abspath('resultado.json'), 'w') as f:
		json.dump(output, f, indent=4)

df = pd.DataFrame(output["cards"])
df.to_excel('resultado.xls', columns=['list', 'name', 'description', 'members'])	
	
print("Archivos generados con exito con el nombre de resultado")