from viktor.parametrization import Parametrization, OptionField


from ..lib.postgresdb import PostgresDB

class LeveeSectionParametrization(Parametrization):
    _postgres_db = PostgresDB()

    _levee_codes = _postgres_db.get_levee_codes()
    levee_code = OptionField('Levee code', options=_levee_codes, default=_levee_codes[0], autoselect_single_option=True)

    