import csv
model={"name": "TO CHANGE","image": "TO CHANGE","description": {"fr": "To Change"},"location": {"type": "Point","coordinates": [48.860611, 2.337644],"name": "musee du louvre"},"artists": [],"style": {"id": 1,"name": {"fr": "Peinture","en": "Painting"}},"minDate": 0,"maxDate": 0}
with open('Louvre.csv', newline='') as csvfile:
    
    reader = csv.reader(csvfile,delimiter=";")
    print(type(reader))
    #We skip the header to get our data directly
    next(reader,None)
    for row in reader:
        print(row)
    print(type(reader))