#############################################################################
# Imports
#############################################################################
from services.arangoManager import get_works as get_works_from_db
from services.arangoManager import get_work_by_type as get_work_by_type_from_db
from services.arangoManager import get_number_of_works as get_number_of_works_from_db
from services.arangoManager import get_closest_works as get_closest_works_from_db


#############################################################################
# Works Management
#############################################################################

def get_works():
    works = get_works_from_db()
    return works, 200

def get_number_of_works():
    worksNum = get_number_of_works_from_db()
    return { "nbWorks" : worksNum}

LOCATION_LOUVRE_LONGITUDE = 2.337644
LOCATION_LOUVRE_LATITUDE = 48.860611
ARTWORK_NUMBER = 1

def get_closest_works():
    worksClosest = get_closest_works_from_db(LOCATION_LOUVRE_LONGITUDE, LOCATION_LOUVRE_LATITUDE, 0, ARTWORK_NUMBER)
    return worksClosest, 200

WORK_TYPE = "Painting"
def get_by_type():
    workByType = get_work_by_type_from_db(WORK_TYPE)
    return workByType

#def get_by_search():