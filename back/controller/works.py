#############################################################################
# Imports
#############################################################################

from services.arangoManager import (
    get_works as get_works_from_db,
    get_works_in_rectangle,
)

#############################################################################
# Works Management
#############################################################################


def get_works():
    works = get_works_from_db()
    return works, 200


def get_works_rect(bottomLeftLat, bottomLeftLon, topRightLat, topRightLon):
    works = get_works_in_rectangle(
        bottomLeftLat, bottomLeftLon, topRightLat, topRightLon
    )
    return works, 200
