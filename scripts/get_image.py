import csv, copy,requests
from bs4 import BeautifulSoup
model={"name": "TO CHANGE","image": "TO CHANGE","description": {"fr": "Il n'y a pas de description"},"location": {"type": "Point","coordinates": [48.860611, 2.337644],"name": "musee du louvre"},"artists": [],"type": {"fr": "Peinture","en": "Painting"},"minDate": 0}
model_list=[]

        # this part webscrap the Louvre website
page=requests.get("http://www.purl.org/inha/agorha/003/28751")
soup = BeautifulSoup(page.content, "html.parser")
result_dom=soup.find_all('img')
for current_class in result_dom:
        if("https://agorha" in current_class.get("src")):
                print(current_class["src"])