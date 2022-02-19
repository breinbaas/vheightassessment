from viktor.parametrization import Parametrization, OptionField, IntegerField


from ..lib.postgresdb import PostgresDB

class LeveeSectionParametrization(Parametrization):
    _postgres_db = PostgresDB()

    _levee_codes = _postgres_db.get_levee_codes()
    levee_code = OptionField('Levee code', options=_levee_codes, default=_levee_codes[0], autoselect_single_option=True)
    year_ahn3 = IntegerField('AHN3 jaar', min=2014, max=2018, step=1, default=2015)
    year_ahn4 = IntegerField('AHN4 jaar', min=2019, max=2021, step=1, default=2020)
    max_bgs = IntegerField('Limiet achtergrondzetting [mm/jaar]', min=1, max=100, default=20)
    year_analysis = IntegerField('Analyse jaar', min=2022, max=2052, step=1, default=2032)
    