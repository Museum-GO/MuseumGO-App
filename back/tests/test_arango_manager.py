from services.arangoManager import (
    setup,
    add_work,
    get_number_of_works,
    delete_work,
    get_works,
    get_work,
    get_closest_works,
    get_works_in_range,
    get_works_in_rectangle,
    delete_collection_by_name,
    create_collection_by_name,
    setup_works_collection_name,
)
import pytest

test_doc_id_1 = None
test_doc_id_2 = None
test_doc_id_3 = None
original_number_of_works = None
artwork_test_collection = "artwork_test"


# The scope module is define to use the setup database function for all tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # This code will run before the first test
    setup()
    # Define a specific collection to isolate our tests from the default collection
    setup_works_collection_name("artwork_test")

    # Delete the collection and create it again for test purposes
    delete_collection_by_name(artwork_test_collection)
    create_collection_by_name(artwork_test_collection)

    # At the end of the tests, delete the collection
    yield

    delete_collection_by_name(artwork_test_collection)


def test_get_number_of_works():
    global original_number_of_works
    # Get the current number of works
    original_number_of_works = get_number_of_works()
    assert type(original_number_of_works) is int


def test_add_works():
    global test_doc_id_1, test_doc_id_2, test_doc_id_3
    # Insert some works
    test_doc_id_1 = add_work(
        {
            "name": "Artwork-1",
            "image": "https://upload.wikimedia.org/primavera",
            "location": {
                "coordinates": [1, 1],
                "name": "Museum name",
            },
            "artists": ["Artist"],
            "type": {"en": "Painting"},
            "creationPeriod": {"minDate": 1500, "maxDate": 1600},
            "wikiLink": "https://fr.wikipedia.org/wiki/Le_Printemps_(Botticelli)",
        }
    )
    test_doc_id_2 = add_work(
        {
            "name": "Artwork-2",
            "image": "https://upload.wikimedia.org/primavera",
            "location": {
                "coordinates": [2, 2],
                "name": "Museum name",
            },
            "artists": ["Artist"],
            "type": {"en": "Painting"},
            "creationPeriod": {"minDate": 1500, "maxDate": 1600},
            "wikiLink": "https://fr.wikipedia.org/wiki/Le_Printemps_(Botticelli)",
        }
    )
    test_doc_id_3 = add_work(
        {
            "name": "Artwork-3",
            "image": "https://upload.wikimedia.org/primavera",
            "location": {
                "coordinates": [3, 3],
                "name": "Museum name",
            },
            "artists": ["Artist"],
            "type": {"en": "Painting"},
            "creationPeriod": {"minDate": 1500, "maxDate": 1600},
            "wikiLink": "https://fr.wikipedia.org/wiki/Le_Printemps_(Botticelli)",
        }
    )
    # Check that the number of works has increased
    assert get_number_of_works() == original_number_of_works + 3


def check_that_dict_is_a_work(work):
    assert type(work) is dict
    assert "name" in work
    assert "location" in work
    assert type(work["_id"]) is str
    assert type(work["name"]) is str
    assert type(work["location"]) is dict

    assert type(work["location"]["coordinates"]) is list
    assert type(work["location"]["coordinates"][0]) in (int, float)
    assert type(work["location"]["coordinates"][1]) in (int, float)


def test_get_works():
    # Test that we get the correct number of works and that they are correct
    # Get all the works
    works = get_works()
    assert type(works) is list
    assert len(works) == original_number_of_works + 3

    # Check that the works are correct
    for work in works:
        check_that_dict_is_a_work(work)

    # Check that the inserted works are in the list
    assert any(work["name"] == "Artwork-1" for work in works)
    assert any(work["name"] == "Artwork-2" for work in works)
    assert any(work["name"] == "Artwork-3" for work in works)


def test_get_work():
    # Get a work
    global test_doc_id_1
    work = get_work(test_doc_id_1)
    assert type(work) is dict

    # Check that the work is correct
    check_that_dict_is_a_work(work)

    assert work["name"] == "Artwork-1"
    assert work["location"]["coordinates"][0] == 1
    assert work["location"]["coordinates"][1] == 1


def test_get_closest_works():
    # Get the closest works
    closest_works = get_closest_works(3, 3, 0, 3)
    assert type(closest_works) is list
    assert len(closest_works) == 3

    # Check that the works are correct
    for work in closest_works:
        check_that_dict_is_a_work(work)

    # Check that the closest works are correct
    assert closest_works[0]["name"] == "Artwork-3"
    assert closest_works[1]["name"] == "Artwork-2"
    assert closest_works[2]["name"] == "Artwork-1"


def test_get_works_in_radius():
    # Get the works in a radius
    works_in_radius = get_works_in_range(3, 3, 1000)
    assert type(works_in_radius) is list
    assert len(works_in_radius) == 1

    works_in_radius = get_works_in_range(3, 3, 600000)
    assert type(works_in_radius) is list
    assert len(works_in_radius) == 3


def test_get_works_in_rectangle():
    # Get the works in a rectangle
    # bottomLeftLatitude, bottomLeftLongitude, topRightLatitude, topRightLongitude
    # add_work("Artwork_1", [1, 1])
    # add_work("Artwork_2", [2, 2])
    # add_work("Artwork_3", [3, 3])

    # A rectangle that contains all the works:
    works_in_rectangle = get_works_in_rectangle(0, 0, 4, 4)
    assert type(works_in_rectangle) is list
    assert len(works_in_rectangle) == 3

    # A rectangle that contains only one work:
    works_in_rectangle = get_works_in_rectangle(0, 0, 1.2, 1.2)
    assert type(works_in_rectangle) is list
    assert len(works_in_rectangle) == 1
    assert works_in_rectangle[0]["name"] == "Artwork-1"


def test_delete_works():
    # Delete the inserted works
    assert delete_work(test_doc_id_1)
    assert delete_work(test_doc_id_2)
    assert delete_work(test_doc_id_3)

    # Check that the number of works is back to normal
    assert get_number_of_works() == original_number_of_works

    # Try to get the deleted works
    assert get_work(test_doc_id_1) is None
    assert get_work(test_doc_id_2) is None
    assert get_work(test_doc_id_3) is None
