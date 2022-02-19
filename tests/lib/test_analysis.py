import pytest

from app.lib.analysis import Analysis, AnalysisError
from app.lib.route import Route
  
def test_set_valid_route():
    a = Analysis()
    a.set_route("A120")
    assert(a.route is not None)

def test_set_invalid_route():
    a = Analysis()
    with pytest.raises(AnalysisError):
        a.set_route("NoWayIExist")

def test_execute():    
    a = Analysis()
    a.route = Route(name="test", rd_points=[(123456,456789), (123466,456789)])
    year = 2030
    ahn3year = 2015
    ahn4year = 2020
    max_bgs = 0.02
    a.execute(year, ahn3year, ahn4year, max_bgs)
    assert(len(a.zpred)>0)