from app.lib.postgresdb import PostgresDB

db = PostgresDB()

def test_get_levee_codes():
    levee_codes = db.get_levee_codes()
    assert(len(levee_codes)>0)

def test_get_levee_referenceline():
    pts = db.get_levee_referenceline('A120')
    assert(len(pts)>0)