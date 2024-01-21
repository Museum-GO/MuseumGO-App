import csv, copy,requests
from bs4 import BeautifulSoup
model={"name": "TO CHANGE","image": "TO CHANGE","description": {"fr": "Il n'y a pas de description"},"location": {"type": "Point","coordinates": [48.860611, 2.337644],"name": "musee du louvre"},"artists": [],"type": {"fr": "Peinture","en": "Painting"},"minDate": 0}
model_list=[]
with open('Louvre.csv', newline='') as csvfile:
    
    reader = csv.reader(csvfile,delimiter=";")
    print(type(reader))
    #We skip the header to get our data directly
    next(reader,None)
    for row in reader:
        print(row)
    #We analys the current art work
        base_url="https://collections.louvre.fr/ark:/53355/"
        current_model=copy.deepcopy(model)
        current_model["name"]=row[1]
        #Decompose the artist name the ; is to remove ; France
        artist_name=row[2].split(";")[0].split(",")
        artist_toadd=artist_name[0]
        if(len(artist_name)>1):
            artist_toadd=artist_name[1]+" "+artist_toadd

        current_model["artists"].append(artist_toadd)
        date=row[3].split("/")
        current_model["minDate"]=date[0].replace(' ','')
        if(len(date)>1):
            current_model["maxDate"]=(date[1])[0:5].replace(' ','')
        # this part webscrap the Louvre website
        page=requests.get(base_url+row[0])
        soup = BeautifulSoup(page.content, "html.parser")
        result_dom=soup.find_all("picture")
        for current_class in result_dom:
            pic_parameter=current_class.find("img")
            if(pic_parameter.get("src",False)):
                current_model["image"]="https://collections.louvre.fr"+pic_parameter["src"]
        #We should get the description parameter
        history_entries=soup.find_all("div",class_="notice__mnr")
        for entry in history_entries:
            result=entry.find("span",class_="lbl_10")
            current_model["description"]["fr"]=result.text
        model_list.append(current_model)
    for m in model_list:
            print(m["artists"])


        

        #print(row)
        
