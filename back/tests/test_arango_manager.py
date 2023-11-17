from services.arangoManager import (
    setup,
    add_work,
    get_number_of_works,
    delete_work,
    get_works,
    get_work,
    get_closest_works,
)
import pytest

original_number_of_works = None


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # This code will run before the first test
    setup()

    # Delete the works if they exist
    delete_work("test_work_1")
    delete_work("test_work_2")
    delete_work("test_work_3")


def test_get_number_of_works():
    global original_number_of_works
    # Get the current number of works
    original_number_of_works = get_number_of_works()
    assert type(original_number_of_works) is int


def test_add_works():
    # Insert some works
    add_work("test_work_1", [1, 1])
    add_work("test_work_2", [2, 2])
    add_work("test_work_3", [3, 3])

    # Check that the number of works has increased
    assert get_number_of_works() == original_number_of_works + 3


def check_that_dict_is_a_work(work):
    assert type(work) is dict
    assert "_id" in work
    assert "name" in work
    assert "location" in work

    assert type(work["_id"]) is str
    assert type(work["name"]) is str
    assert type(work["location"]) is dict

    assert type(work["location"]["type"]) is str
    assert type(work["location"]["coordinates"]) is list
    assert type(work["location"]["coordinates"][0]) in (int, float)
    assert type(work["location"]["coordinates"][1]) in (int, float)

    assert work["location"]["type"] == "Point"


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
    assert any(work["name"] == "test_work_1" for work in works)
    assert any(work["name"] == "test_work_2" for work in works)
    assert any(work["name"] == "test_work_3" for work in works)


def test_get_work():
    # Get a work
    work = get_work("test_work_1")
    assert type(work) is dict

    # Check that the work is correct
    check_that_dict_is_a_work(work)

    assert work["name"] == "test_work_1"
    assert work["location"]["type"] == "Point"
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
    assert closest_works[0]["name"] == "test_work_3"
    assert closest_works[1]["name"] == "test_work_2"
    assert closest_works[2]["name"] == "test_work_1"


def test_delete_works():
    # Delete the inserted works
    assert delete_work("test_work_1")
    assert delete_work("test_work_2")
    assert delete_work("test_work_3")

    # Check that the number of works is back to normal
    assert get_number_of_works() == original_number_of_works

    # Try to get the deleted works
    assert get_work("test_work_1") is None
    assert get_work("test_work_2") is None
    assert get_work("test_work_3") is None
