from services.arangoManager import (
    setup,
    add_work,
    get_number_of_works,
    delete_work,
    get_works,
    get_work,
    work_get_by_name,
    get_closest_works,
    delete_collection_by_name,
    create_collection_by_name
)
import pytest

test_doc_id_1 = None
test_doc_id_2 = None
test_doc_id_3 = None
original_number_of_works = None


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # This code will run before the first test
    setup()

    # Delete the collection and create it again for test purposes
    delete_collection_by_name("works")
    create_collection_by_name("works")


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

            "name": "Allegoria de la Primaveraa",
            "image": "https://upload.wikimedia.org/primavera",
            "description": {
                "fr": "Le Printemps (Primavera en italien prononcé : [primaˈvɛra]) est une peinture allégorique de Sandro Botticelli, exécutée à tempera sur panneau de bois entre 1478 et 1482, période de la Première Renaissance. Elle a été décrite comme « l'une des peintures les plus commentées et les plus controversées au monde », et aussi « l'une des peintures les plus populaires de l'art occidental »",
                "en": "Primavera (Italian pronunciation: [primaˈvɛːra], meaning 'Spring'), is a large panel painting in tempera paint by the Italian Renaissance painter Sandro Botticelli made in the late 1470s or early 1480s (datings vary). It has been described as 'one of the most written about, and most controversial paintings in the world', and also 'one of the most popular paintings in Western art'",
            },
            "location": {
                "coordinates": [40.01232, 50.02344],
                "name": "Musée des Offices",
            },
            "artists": ["Sandro Botticelli"],
            "type": {"fr": "Peinture", "en": "Painting"},
            "creationPeriod": {"minDate": 1500, "maxDate": 1600},
            "wikiLink": "https://fr.wikipedia.org/wiki/Le_Printemps_(Botticelli)",
        }
    )
    test_doc_id_2=add_work({
            "name": "Allegoria de la Primaverab",
            "image": "https://upload.wikimedia.org/primavera",
            "description": {
                "fr": "Le Printemps (Primavera en italien prononcé : [primaˈvɛra]) est une peinture allégorique de Sandro Botticelli, exécutée à tempera sur panneau de bois entre 1478 et 1482, période de la Première Renaissance. Elle a été décrite comme « l'une des peintures les plus commentées et les plus controversées au monde », et aussi « l'une des peintures les plus populaires de l'art occidental »",
                "en": "Primavera (Italian pronunciation: [primaˈvɛːra], meaning 'Spring'), is a large panel painting in tempera paint by the Italian Renaissance painter Sandro Botticelli made in the late 1470s or early 1480s (datings vary). It has been described as 'one of the most written about, and most controversial paintings in the world', and also 'one of the most popular paintings in Western art'",
            },
            "location": {
                "coordinates": [40.01232, 50.02344],
                "name": "Musée des Offices",
            },
            "artists": ["Sandro Botticelli"],
            "type": {"fr": "Peinture", "en": "Painting"},
            "creationPeriod": {"minDate": 1500, "maxDate": 1600},
            "wikiLink": "https://fr.wikipedia.org/wiki/Le_Printemps_(Botticelli)",
        }
    )
    test_doc_id_3=add_work(
        {
            "name": "Allegoria de la Primaverac",
            "image": "https://upload.wikimedia.org/primavera",
            "description": {
                "fr": "Le Printemps (Primavera en italien prononcé : [primaˈvɛra]) est une peinture allégorique de Sandro Botticelli, exécutée à tempera sur panneau de bois entre 1478 et 1482, période de la Première Renaissance. Elle a été décrite comme « l'une des peintures les plus commentées et les plus controversées au monde », et aussi « l'une des peintures les plus populaires de l'art occidental »",
                "en": "Primavera (Italian pronunciation: [primaˈvɛːra], meaning 'Spring'), is a large panel painting in tempera paint by the Italian Renaissance painter Sandro Botticelli made in the late 1470s or early 1480s (datings vary). It has been described as 'one of the most written about, and most controversial paintings in the world', and also 'one of the most popular paintings in Western art'",
            },
            "location": {
                "coordinates": [40.01232, 50.02344],
                "name": "Musée des Offices",
            },
            "artists": ["Sandro Botticelli"],
            "type": {"fr": "Peinture", "en": "Painting"},
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
    assert any(work["name"] == "Allegoria de la Primavera-1" for work in works)
    assert any(work["name"] == "Allegoria de la Primavera-2" for work in works)
    assert any(work["name"] == "Allegoria de la Primavera-3" for work in works)


def test_get_work():
    # Get a work
    global test_doc_id_1
    work = get_work(test_doc_id_1)
    assert type(work) is dict

    # Check that the work is correct
    check_that_dict_is_a_work(work)

    assert work["name"] == "Allegoria de la Primavera-1"
    assert work["location"]["coordinates"][0] == 40.01232
    assert work["location"]["coordinates"][1] == 50.02344


def test_get_closest_works():
    # Get the closest works
    closest_works = get_closest_works(3, 3, 0, 3)
    assert type(closest_works) is list
    assert len(closest_works) == 3

    # Check that the works are correct
    for work in closest_works:
        check_that_dict_is_a_work(work)

    # Check that the closest works are correct
    assert closest_works[0]["name"] == "Allegoria de la Primavera-1"
    assert closest_works[1]["name"] == "Allegoria de la Primavera-2"
    assert closest_works[2]["name"] == "Allegoria de la Primavera-3"


def test_delete_works():
    # Delete the inserted works
    assert delete_work("74a9fe12-202d-4922-b6af-e3b3d48da1bd")
    assert delete_work("74a9fe13-202d-4922-b6af-e3b3d48da1bd")
    assert delete_work("74a9fe14-202d-4922-b6af-e3b3d48da1bd")

    # Check that the number of works is back to normal
    assert get_number_of_works() == original_number_of_works

    # Try to get the deleted works
    assert get_work("74a9fe12-202d-4922-b6af-e3b3d48da1bd") is None
    assert get_work("74a9fe13-202d-4922-b6af-e3b3d48da1bd") is None
    assert get_work("74a9fe14-202d-4922-b6af-e3b3d48da1bd") is None
