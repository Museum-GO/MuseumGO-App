import requests,copy
from bs4 import BeautifulSoup
r=requests.get("https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/base-joconde-extrait/records?where=lien_inha%20is%20not%20null&limit=100")
data=r.json()
my_docs=list()
model={
  "name": "",
  "image": "",
  "description": {
    "fr": "Pas de description"
  },
  "location": {
    "coordinates": [0, 0],
    "name": ""
  },
  "artists": [],
  "type": {
    "fr": "",

  },
  "creationPeriod": {
    "minDate": 0
  }
}
for artwork in data["results"]:
    current_model=copy.deepcopy(model)
    current_model["name"]=artwork["titre"]
    ###############################################
    image=artwork["lien_inha"]
    page=requests.get("http://www.purl.org/inha/agorha/003/28751")
    soup = BeautifulSoup(page.content, "html.parser")
    result_dom=soup.find_all('img')
    for current_class in result_dom:
        if("https://agorha" in current_class.get("src")):
            current_model["image"]=current_class["src"]

    current_model["description"]["fr"]=artwork["description"]
    coordinates=list()
    coordinates.append(artwork["coordonnees"]["lon"])
    coordinates.append(artwork["coordonnees"]["lat"])
    current_model["location"]["coordinates"]=coordinates
    current_model["location"]["name"]=artwork["nom_officiel_musee"]
    current_model["type"]["fr"]=artwork["denomination"]
    current_model["creationPeriod"]["minDate"]=artwork["periode_de_creation"]


    my_docs.append(current_model)

for doc in my_docs:
    print(doc)
  

