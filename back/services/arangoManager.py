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
        # Delete the collections if they exist
        # if db.has_collection(WORKS_COLLECTION_NAME):
        #     print(
        #         f" - Deleting collection {colored(WORKS_COLLECTION_NAME, DEBUG_COLOR)}"
        #     )
        #     db.delete_collection(WORKS_COLLECTION_NAME)

        # Insert few documents into the collection for testing purposes
        # add_work("Mona Lisa", [2.335, 48.861])
        # add_work("The Starry Night", [4.833, 52.367])
        # add_work("The Last Supper", [9.19, 45.464])
        # add_work("The Creation of Adam", [12.483, 41.898])
        # add_work("The Persistence of Memory", [-73.962, 40.781])
        # add_work("The Scream", [10.738, 59.913])
        # add_work("Guernica", [-2.988, 43.319])

        # Create the collections if they don't exist
        if not db.has_collection(WORKS_COLLECTION_NAME):
            print(
                f" - Creating collection {colored(WORKS_COLLECTION_NAME, DEBUG_COLOR)}"
            )
            db.create_collection(WORKS_COLLECTION_NAME)

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
def add_work(work_name, location: list):
    work_id = clean_text(work_name)
    # Check if the work already exists
    if work_exists(work_id):
        print(
            f"  Work {colored(work_name,ERROR_COLOR)} already exists in the \
database, skipping"
        )
        return

    # Add a work to the database
    document = {
        "_key": work_id,
        "name": work_name,
        "location": {
            "type": "Point",
            "coordinates": [location[0], location[1]],
        },
    }

    db.collection(WORKS_COLLECTION_NAME).insert(document, overwrite=True)


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
def get_works_in_range(longitude, latitude, range) -> list:
    # Return the works near a location

    # Create the query
    query = f"""
FOR work IN {WORKS_COLLECTION_NAME}
LET distance = DISTANCE(
    work.location.coordinates[0],
    work.location.coordinates[1],
    {longitude},
    {latitude})
FILTER distance < {range}
RETURN {{work:work, distance,distance}}
    """

    # Execute the query
    cursor = db.aql.execute(query)

    print(cursor)

    # Merge the results with the distances
    results = []
    for result in cursor:
        result["work"]["distance"] = result["distance"]
        results.append(result["work"])

    # Return the results
    return results


@dbMustBeSetup
def get_works_in_rectangle(
    bottomLeftLatitude, bottomLeftLongitude, topRightLatitude, topRightLongitude
) -> list:
    # Return the works in a rectangle

    # Create the query
    query = f"""
FOR work IN {WORKS_COLLECTION_NAME}
FILTER work.location.coordinates[0] >= {bottomLeftLongitude}
FILTER work.location.coordinates[0] <= {topRightLongitude}
FILTER work.location.coordinates[1] >= {bottomLeftLatitude}
FILTER work.location.coordinates[1] <= {topRightLatitude}
RETURN work
    """

    # Execute the query
    cursor = db.aql.execute(query)

    # Return the results
    return list(cursor)


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
