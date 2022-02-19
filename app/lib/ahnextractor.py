"""
Copyright (c) 2022 VIKTOR B.V. / Breinbaas
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

VIKTOR B.V. / Breinbaas PROVIDES THIS SOFTWARE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pydantic import BaseModel
from enum import IntEnum
from typing import List, Union
import urllib
from urllib.request import urlopen
import json
import numpy as np
import math

class AhnPoint(BaseModel):
    l: float
    x: float
    y: float
    z: float

class AhnVersion(IntEnum):
    #AHN2 = 2
    AHN3 = 3
    AHN4 = 4

AhnProfileName = {
    #AhnVersion.AHN2:"Profile_AHN2",
    AhnVersion.AHN3:"Profile_AHN3",  
    AhnVersion.AHN4:"Profile_AHN4",    
}

GRIDSIZE_AHN = 0.5

class AhnExtractor(BaseModel):
    version: AhnVersion = AhnVersion.AHN4

    def get(self, *points) -> List[AhnPoint]:
        result = [] # l, x, y, z
        l = 0

        steps = list(np.arange(0, len(points), 50)) + [len(points)]
        if steps[-1] == steps[-2]:
            steps.pop()
        
        for i in range(1, len(steps)):
            iresult = self._get(points[steps[i-1]:steps[i]])
            for j in range(len(iresult)):
                x = iresult[j][0]                
                y = iresult[j][1]
                z = iresult[j][2]

                if len(result) == 0:
                    result.append(AhnPoint(l=l, x=x, y=y, z=z))
                else:
                    px = result[-1].x
                    py = result[-1].y
                    l += math.hypot(x-px, y-py)
                    result.append(AhnPoint(l=l, x=x, y=y, z=z))
        
        return result    
            
    def _get(self, points) -> List[Union[float, float]]:
        result = []

        spoints = [f"[{p[0]:.2f},{p[1]:.2f}]" for p in points]
        spoints = ",".join(spoints)

        sInputLineFeatures = """{
            "fields":[
                {
                    "name":"OID",
                    "type":"esriFieldTypeObjectID",
                    "alias":"OID"
                }
            ],
            "geometryType":"esriGeometryPolyline",
            "features":[
                {
                    "geometry":
                        {"paths":
                            [
                                [
                                    POINTS_PLACEHOLDER
                                ]
                            ],
                            "spatialReference":{"wkid":28992}
                        },
                    "attributes":{"OID":1}
                }
            ],
            "sr":{"wkid":28992}
        }""".replace(" ", "").replace("\n","").replace("POINTS_PLACEHOLDER", spoints)

        urlsafe = urllib.parse.quote_plus(sInputLineFeatures)

        url = f'https://ahn.arcgisonline.nl/arcgis/rest/services/Geoprocessing/{AhnProfileName[self.version]}/GPServer/Profile/execute?f=json&env:outSR=28992&InputLineFeatures={urlsafe}&ProfileIDField=OID&DEMResolution=FINEST&MaximumSampleDistance=0.5&MaximumSampleDistanceUnits=Meters&returnZ=true&returnM=true'

        try:
            response = urlopen(url)
            data = json.loads(response.read())
            return [(p[0], p[1], p[2], p[3]) for p in data['results'][0]['value']['features'][0]['geometry']['paths'][0]]
        except Exception as e:
            return []        
