from config.init_config import get_config, ERROR_COLOR, DEBUG_COLOR
from utils.utils import clean_text
from termcolor import colored
from arango import ArangoClient, exceptions

db = None  # Wrapper for the Arango MuseumGo database

WORKS_COLLECTION_NAME = "works"


def setup():
    global db

    # Load config
    config = get_config()
    HOST = config["ARANGODB"]["HOST"]
    PORT = config["ARANGODB"]["PORT"]
    DATABASE = config["ARANGODB"]["DATABASE"]
    USER = config["ARANGODB"]["USER"]
    PASSWORD = config["ARANGODB"]["PASSWORD"]

    # Connect to ArangoDB
    print("\nConnecting to ArangoDB...")
    print(" - Initializing client")
    print(f"   - Host: {colored(HOST, DEBUG_COLOR)}")
    print(f"   - Port: {colored(PORT, DEBUG_COLOR)}")
    print(f"   - Database: {colored(DATABASE, DEBUG_COLOR)}")
    print(f"   - User: {colored(USER, DEBUG_COLOR)}")

    # Initialize the ArangoDB client.
    client = ArangoClient(hosts=f"http://{HOST}:{PORT}")

    # Connect to the MuseumGo database
    db = client.db(DATABASE, username=USER, password=PASSWORD)

    try:
        # Delete the collections if it exist
        db.delete_collection(WORKS_COLLECTION_NAME)
        # Create the collections if they don't exist
        if not db.has_collection(WORKS_COLLECTION_NAME):
            print(
                f" - Creating collection {colored(WORKS_COLLECTION_NAME, DEBUG_COLOR)}"
            )
            db.create_collection(WORKS_COLLECTION_NAME)
        #add_work({"name": "Allegoria de la Primavera","image": "https://upload.wikimedia.org/primavera","description": {"fr": "Le Printemps (Primavera en italien prononcé : [primaˈvɛra]) est une peinture allégorique de Sandro Botticelli, exécutée à tempera sur panneau de bois entre 1478 et 1482, période de la Première Renaissance. Elle a été décrite comme « l'une des peintures les plus commentées et les plus controversées au monde », et aussi « l'une des peintures les plus populaires de l'art occidental »","en": "Primavera (Italian pronunciation: [primaˈvɛːra], meaning 'Spring'), is a large panel painting in tempera paint by the Italian Renaissance painter Sandro Botticelli made in the late 1470s or early 1480s (datings vary). It has been described as 'one of the most written about, and most controversial paintings in the world', and also 'one of the most popular paintings in Western art'"},"location": {"coordinates": [40.01232, 50.02344],"name": "Musée des Offices"},"artists": ["Sandro Botticelli"],"type": {"fr": "Peinture","en": "Painting"},"creationPeriod": {"minDate": 1500,"maxDate": 1600},"wikiLink": "https://fr.wikipedia.org/wiki/Le_Printemps_(Botticelli)"})
        work_get_by_name("Allegoria de la Primavera")


    except exceptions.CollectionListError as e:
        print(colored(" - Error while creating collections", ERROR_COLOR))
        print(colored(e, ERROR_COLOR))
        exit(1)

    print(" - Connection established")


def dbMustBeSetup(func):
    def wrapper_dbMustBeSetup(*args, **kwargs):
        if db is None:
            raise Exception("Database not setup")
        return func(*args, **kwargs)

    return wrapper_dbMustBeSetup


@dbMustBeSetup
def get_number_of_works():
    # Get the number of works in the database
    return db.collection(WORKS_COLLECTION_NAME).count()


@dbMustBeSetup
def work_exists(work_id):
    

    # Check if a work exists in the database
    return db.collection(WORKS_COLLECTION_NAME).has(work_id)


@dbMustBeSetup
def add_work(doc):
    #This function is based of the document model: model.json
    # Check if the work already exists
    if work_get_by_name(doc["name"]):
        print(
            f"  Work {colored(work_name,ERROR_COLOR)} already exists in the \
database, skipping"
        )
        return

    # Add a work to the database

    res=db.collection(WORKS_COLLECTION_NAME).insert(doc, overwrite=True)
    #print(res)


@dbMustBeSetup
def get_works() -> list:
    # Get all the works in the database
    return list(db.collection(WORKS_COLLECTION_NAME).all())

@dbMustBeSetup
def get_work(work_id):
    return db.collection(WORKS_COLLECTION_NAME).get(work_id)

@dbMustBeSetup
def get_closest_works(longitude, latitude, _from, size) -> list:
    # Return the works near a location

    # Create the query
    query = f"""
FOR work IN {WORKS_COLLECTION_NAME}
LET distance = DISTANCE(
    work.location.coordinates[0],
    work.location.coordinates[1],
    {longitude},
    {latitude})
SORT distance ASC
LIMIT {_from}, {size}
RETURN {{work:work, distance,distance}}
    """

    # Execute the query
    cursor = db.aql.execute(query)

    # Merge the results with the distances
    results = []
    for result in cursor:
        result["work"]["distance"] = result["distance"]
        results.append(result["work"])

    # Return the results
    return results


@dbMustBeSetup
def delete_work(work_id) -> bool:
    # Delete a work from the database
    try:
        db.collection(WORKS_COLLECTION_NAME).delete(work_id)
        return True
    except exceptions.DocumentDeleteError:
        # The work doesn't exist
        return False

@dbMustBeSetup     
def work_get_by_name(work_name):
    query = f"""
FOR work IN {WORKS_COLLECTION_NAME}
FILTER work.name =={work_name}
RETURN work
    """
    cursor = db.aql.execute(query)
    for result in cursor:
        print(result)
        return result
