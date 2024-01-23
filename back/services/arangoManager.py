from config.init_config import get_config, ERROR_COLOR, DEBUG_COLOR
from utils.utils import clean_text
from termcolor import colored
from arango import ArangoClient, exceptions

db = None  # Wrapper for the Arango MuseumGo database

WORKS_COLLECTION_NAME = "works"


def setup(default_collection="works"):
    global db,WORKS_COLLECTION_NAME
    print(default_collection)
    # Load config
    config = get_config()
    HOST = config["ARANGODB"]["HOST"]
    PORT = config["ARANGODB"]["PORT"]
    DATABASE = config["ARANGODB"]["DATABASE"]
    USER = config["ARANGODB"]["USER"]
    PASSWORD = config["ARANGODB"]["PASSWORD"]
    # Define WORKS_COLLECTION_NAME
    WORKS_COLLECTION_NAME=default_collection

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
    # This function is based of the document model: model.json it will return the document _id
    # Check if the work already exists
    work_name = doc["name"]
    chk_work = work_get_by_name(doc["name"])
    if chk_work:
        print(
            f"  Work {colored(work_name,ERROR_COLOR)} already exists in the \
database, skipping"
        )
        return chk_work["_id"]

    # Add a work to the database

    res = db.collection(WORKS_COLLECTION_NAME).insert(doc, overwrite=True)
    return res["_id"]


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
    FOR doc IN {WORKS_COLLECTION_NAME}
        FILTER doc.name == "{work_name}"
        RETURN doc
"""
    cursor = db.aql.execute(query)
    for result in cursor:
        return result


@dbMustBeSetup
def delete_collection_by_name(collection_name):
    if db.has_collection(collection_name):
        print(f" - Deleting collection {colored(collection_name, DEBUG_COLOR)}")
        db.delete_collection(collection_name)


@dbMustBeSetup
def create_collection_by_name(collection_name):
    if not db.has_collection(collection_name):
        print(f" - Creating collection {colored(collection_name, DEBUG_COLOR)}")
        db.create_collection(collection_name)
