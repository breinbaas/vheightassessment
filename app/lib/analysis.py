from pydantic import BaseModel
import numpy as np
from typing import List

from ..lib.route import Route
from ..lib.ahnextractor import AhnExtractor, AhnVersion

class AnalysisError(Exception):
    """Raised when an error in the analysis is found"""
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return f'{self.message}'

class Analysis(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    route: Route = None   
    dl: List[float] = []
    dz: List[float] = []
    ahn3: List[float] = []
    ahn4: List[float] = []
    zpred: List[float] = []
    
    def execute(self, year: int, ahn3year: int, ahn4year: int, max_bgs: float, allow_swell=False):
        ahn3extractor = AhnExtractor(version=AhnVersion.AHN3)
        ahn4extractor = AhnExtractor(version=AhnVersion.AHN4)
        
        ahn3 = ahn3extractor.get(*self.route.rd_points)
        ahn4 = ahn4extractor.get(*self.route.rd_points)
        
        nd3 = np.array([p.z for p in ahn3])
        nd4 = np.array([p.z for p in ahn4])
        dz = (nd4 - nd3) / (ahn4year - ahn3year)
        dz[dz<-max_bgs] = -max_bgs

        if not allow_swell:
            dz[dz > 0] = 0.0

        zpred = nd4 + dz * (year - ahn4year)

        # save the outcome that we want to use in the view in the properties of the analysis
        self.dl = [p.l for p in ahn3]
        self.ahn3 = [p.z for p in ahn3]
        self.ahn4 = [p.z for p in ahn4]
        self.zpred = list(zpred)
        self.dz = list(dz) 

    def set_route(self, levee_code: str):
        self.route = None
        try:
            self.route = Route.from_database(levee_code)
        except Exception as e:
            raise AnalysisError(f"Could not set analysis route with error '{e}'")
        
        

