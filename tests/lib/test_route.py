from multiprocessing.sharedctypes import Value
import pytest

from app.lib.route import Route

def test_properties():
    r = Route(name="test", rd_points=[(123456,456789), (123466,456789)])
    
    assert(len(r.latlons)==2)
    assert(len(r.mappoints)==2)

def test_from_database_valid():
    r = Route.from_database("A120")
    assert(r is not None)

def test_from_database_invalid():
    with pytest.raises(ValueError):
        r = Route.from_database("NoWayIExist")  