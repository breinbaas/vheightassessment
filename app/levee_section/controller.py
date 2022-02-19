from cProfile import label
from viktor.core import ViktorController, ParamsFromFile
from .parametrization import LeveeSectionParametrization
from viktor.views import MapResult, MapView, MapPolyline, MapPoint, PlotlyView, PlotlyResult
from viktor.geometry import RDWGSConverter
from munch import Munch
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import numpy as np

from ..lib.analysis import Analysis

pio.templates.default = "simple_white"

class LeveeSectionController(ViktorController):
    viktor_convert_entity_field = True

    _points = []
    _analysis = Analysis()
    label = 'LeveeSection'
    parametrization = LeveeSectionParametrization(width=20)
    

    @ParamsFromFile()
    def process_file(self, file, **kwargs):
        return {}

    @MapView('Map view', duration_guess=1)  # in seconds, if it is larger or equal to 3, the "update" button will appear
    def get_map_view(self, params: Munch, **kwargs) -> MapResult:  
        features = []  

        if self._analysis.route is None:
            self._analysis.set_route(params.levee_code)
        
        features.append(MapPolyline(*self._analysis.route.mappoints))
        return MapResult(features)

    @PlotlyView("Plotly view", duration_guess=999)
    def get_plotly_view(self, params, **kwargs):
        if self._analysis.route is None:
            self._analysis.set_route(params.levee_code) 

        self._analysis.execute(
            year=params.year_analysis,
            ahn3year=params.year_ahn3,
            ahn4year=params.year_ahn4,
            max_bgs=params.max_bgs / 1e3, # from m to mm
        )
        
        fig = go.Figure()
        fig = make_subplots(rows=2, cols=1)

        fig.add_trace(go.Scatter(
            x=self._analysis.dl,
            y=self._analysis.ahn3,
            mode="lines+text",
            name="AHN3",            
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=self._analysis.dl,
            y=self._analysis.ahn4,
            mode="lines+text",
            name="AHN4",            
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=self._analysis.dl,
            y=self._analysis.zpred,
            mode="lines+text",
            name=f"Predicted height in {params.year_analysis}",            
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=self._analysis.dl,
            y=self._analysis.dz,
            mode="lines+markers+text",
            name="zetting [m per jaar]",                       
        ), row=2, col=1)

        fig.update_layout(
            title=f"Height assessment {params.levee_code}",
            xaxis_title="chainage [m]",
            yaxis_title="height [m NAP]",            
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='gray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gray')
        
        return PlotlyResult(fig.to_json())