#############################################################################
# Imports
#############################################################################
from services.arangoManager import get_works as get_works_from_db

#############################################################################
# Works Management
#############################################################################


def get_works():
    works = get_works_from_db()
    return works, 200
