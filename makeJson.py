import json

def generateJSON(grade: int, sdict: dict):
    with open(f'./file/scores{grade}.json', 'w', encoding='UTF-8') as f:
        json.dump(sdict, f)