from typing import Tuple
import psycopg2
from typing import List, Tuple
from pydantic import BaseModel

from ..secrets import *

class PostgresDB(BaseModel):
    _connection = None
    
    @property
    def connection(self):
        if self._connection is None:
            return  psycopg2.connect(
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=f"{DB_PORT}",
                database=DB_NAME
            )
        else:
            return self._connection
    
    def get_levee_codes(self):
        cur = self.connection.cursor()
        cur.execute("SELECT code FROM routes")
        rows = cur.fetchall()
        self.connection.close()
        return sorted([row[0] for row in rows])

    def get_levee_referenceline(self, levee_code: str) -> List[Tuple[float, float]]:
        cur = self.connection.cursor()
        cur.execute(f"SELECT ST_AsText(geom) FROM routes WHERE code='{levee_code}'")
        ls = cur.fetchone()[0].replace('LINESTRING(','').replace(')','')
        self.connection.close()

        pts = []
        for p in ls.split(','):
            args = p.split(' ')
            pts.append((float(args[0]), float(args[1])))
        
        return pts
    

    


    
