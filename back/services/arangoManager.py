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
        #db.delete_collection(WORKS_COLLECTION_NAME)
        if db.has_collection(WORKS_COLLECTION_NAME):
            db.delete_collection(WORKS_COLLECTION_NAME)
        # Create the collections if they don't exist
        if not db.has_collection(WORKS_COLLECTION_NAME):
            print(
                f" - Creating collection {colored(WORKS_COLLECTION_NAME, DEBUG_COLOR)}"
            )
            db.create_collection(WORKS_COLLECTION_NAME)

        # Insert few documents into the collection for testing purposes
        add_work({"name": "Autoportrait à la palette","image": "https://collections.louvre.fr/media/cache/small/0000000021/0000054940/0000797482_OG.JPG","description": {"fr": "Œuvre récupérée à la fin de la Seconde Guerre mondiale, déposée par l'office des biens et intérêts privés (OBIP); en attente de sa restitution à ses légitimes propriétaires. Consulter la base de données ministérielle Rose Valland consacrée aux œuvres dites MNR (Musées nationaux récupération). "},"location": {"type": "Point","coordinates": [48.860611, 2.337644],"name": "musee du louvre"},"artists": ["François-André Vincent"],"style": {"id": 1,"name": {"fr": "Peinture","en": "Painting"}},"minDate": 1769 ,"maxDate": 1770})
        add_work({"name": "Paysage avec chute d'eau","image": "https://collections.louvre.fr/media/cache/small/0000000021/0000055427/0000767624_OG.JPG","description": {"fr": " Pendant de INV 3220. Ancienne collection de Louis XVI, provient de Fontainebleau. Dépôt à Maisons-Laffitte en 1912 (?); retour au musée du Louvre le 18 avril 1944; dépôt au ministère des Affaires étrangères le 9 novembre 1944; retour au Louvre le 15 novembre 1944; dépôt à Maisons-Laffitte en 1948; retour au Louvre le 18 octobre 1989; dépôt à l'Hôtel Marigny le 4 décembre 1997; retour au musée du Louvre 14 décembre 2017"},"location": {"type": "Point","coordinates": [48.860611, 2.337644],"name": "musee du louvre"},"artists": ["Claude Louis Chatelet"],"style": {"id": 1,"name": {"fr": "Peinture","en": "Painting"}},"minDate": 1781})
        add_work({"name": "Le Christ en croix","image": "https://collections.louvre.fr/media/cache/small/0000000021/0000056784/0001136914_OG.JPG","description": {"fr": "Pas de description"},"location": {"type": "Point","coordinates": [48.8526049229,2.33466199468],"name": "musee eugene delacroix"},"artists": ["Eugene Delacroix"],"style": {"id": 1,"name": {"fr": "Peinture","en": "Painting"}},"minDate": 1800,"maxDate": 1900})
        add_work({"name": "Mort de Sardanapale","image": "https://collections.louvre.fr/media/cache/small/0000000021/0000059166/0001136918_OG.JPG","description": {"fr": "Peint en 1844, copie de la répétion réduite exécutée par Delacroix en 1844 (coll. McIlhenny, Philadelphie) de sa composition du Salon de 1827 (Louvre, R.F. 2346); acheté à Paris, à l'hôtel Drouot (étude Ader), en 1962 (vente non identifiée) "},"location": {"type": "Point","coordinates": [48.8526049229,2.33466199468],"name": "musee eugene delacroix"},"artists": ["Frédéric Villot"],"style": {"id": 1,"name": {"fr": "Peinture","en": "Painting"}},"minDate": 1844})
        add_work({"name": "PA_177","image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Space_Invader_-_Rue_du_29_Juillet%2C_Paris_1_November_2013.jpg/220px-Space_Invader_-_Rue_du_29_Juillet%2C_Paris_1_November_2013.jpg","description": {"fr": "Oeuvre réalisé en 1999, elle représente une créature du jeu space invader"},"location": {"type": "Point","coordinates": [48.865486327298036, 2.330770955848266],"name": "Space Invader"},"artists": ["Invader"],"style": {"id": 2,"name": {"fr": "Mosaique","en": "Mosaic"}},"minDate": 1999})




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
def work_exists(work_name):
    work_id = clean_text(work_name)

    # Check if a work exists in the database
    return db.collection(WORKS_COLLECTION_NAME).has(work_id)


@dbMustBeSetup
def add_work(doc):
    #This function is based of the document model: model.json
    work_id = doc["name"]
    # Check if the work already exists
    if work_exists(work_id):
        print(
            f"  Work {colored(work_name,ERROR_COLOR)} already exists in the \
database, skipping"
        )
        return

    # Add a work to the database
    document = doc
    db.collection(WORKS_COLLECTION_NAME).insert(doc, overwrite=True)


@dbMustBeSetup
def get_works() -> list:
    # Get all the works in the database
    return list(db.collection(WORKS_COLLECTION_NAME).all())


@dbMustBeSetup
def get_work(work_name):
    work_id = clean_text(work_name)
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
def delete_work(work_name) -> bool:
    work_id = clean_text(work_name)
    # Delete a work from the database
    try:
        db.collection(WORKS_COLLECTION_NAME).delete(work_id)
        return True
    except exceptions.DocumentDeleteError:
        # The work doesn't exist
        return False
