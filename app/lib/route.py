from pydantic import BaseModel
from typing import List, Union, Tuple
from viktor.geometry import RDWGSConverter
from viktor.views import MapPoint

from ..lib.postgresdb import PostgresDB

_postgresdb = PostgresDB()

class Route(BaseModel):  

    class Config:
        arbitrary_types_allowed = True
    name: str = ""
    rd_points: List[Union[Tuple, Tuple]] = [] 

    @classmethod
    def from_database(cls, levee_code):
        try:
            pts = _postgresdb.get_levee_referenceline(levee_code)        
        except Exception as e:
            raise ValueError(f"Error reading database, '{e}'") 
        return Route(name=levee_code, rd_points=pts)

    @property
    def mappoints(self):
        return [MapPoint(p[0], p[1]) for p in self.latlons]  

    @property
    def latlons(self):
         return [RDWGSConverter.from_rd_to_wgs((p[0], p[1])) for p in self.rd_points]    