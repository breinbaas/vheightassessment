from viktor.core import ViktorController, ParamsFromFile
from .parametrization import LeveeSectionParametrization
from viktor.views import MapResult, MapView, MapPolyline
from viktor.geometry import GeoPolyline, GeoPoint
from munch import Munch
from ..lib.postgresdb import PostgresDB

class LeveeSectionController(ViktorController):
    viktor_convert_entity_field = True

    _postgres_db = PostgresDB()
    label = 'LeveeSection'
    parametrization = LeveeSectionParametrization

    @ParamsFromFile()
    def process_file(self, file, **kwargs):
        return {}

    @MapView('Map view', duration_guess=1)  # in seconds, if it is larger or equal to 3, the "update" button will appear
    def get_map_view(self, params: Munch, **kwargs) -> MapResult:  
        features = []  
        points = self._postgres_db.get_levee_referenceline(params.levee_code)
        geopoints = [GeoPoint.from_rd(p) for p in points]
        geoployline = GeoPolyline(*geopoints)
        features.append(MapPolyline.from_geo_polyline(geoployline))
        return MapResult(features)