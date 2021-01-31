#Author: Mo Kyn
import urllib.request, json 

def initdatabase():
    with urllib.request.urlopen("https://trefle.io/api/v1/plants?token=pFbl2RllF92awIAiWg2gFmvk1J8N_3CCq4mZXgRxf4U") as url:
        data = json.loads(url.read().decode())
        plants=data["data"]
        return plants

def search(term,plants):
    for plant in plants:
        if term==plant["common_name"]:
            return plant