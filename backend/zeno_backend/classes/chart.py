"""Type representations for chart data."""
import json
from enum import Enum

from zeno_backend.classes.base import CamelModel


class ChartType(str, Enum):
    """Enumeration of chart types available in Zeno."""

    BAR = "BAR"
    LINE = "LINE"
    TABLE = "TABLE"
    BEESWARM = "BEESWARM"
    RADAR = "RADAR"
    HEATMAP = "HEATMAP"


class SlicesOrModels(str, Enum):
    """Choice of chart encoding types between slices and models."""

    SLICES = "SLICES"
    MODELS = "MODELS"


class SlicesMetricsOrModels(str, Enum):
    """Choice of chart encoding types between slices, metrics, and models."""

    SLICES = "SLICES"
    MODELS = "MODELS"
    METRICS = "METRICS"


class XCParameters(CamelModel):
    """Parameter specification for the x and color channels of a chart."""

    slices: list[int]
    metric: str
    models: list[str]
    color_channel: SlicesOrModels
    x_channel: SlicesOrModels


class TableParameters(CamelModel):
    """Parameter specification for a tabular visualization."""

    metrics: list[str]
    slices: list[int]
    models: list[str]
    y_channel: SlicesOrModels
    x_channel: SlicesMetricsOrModels
    fixed_channel: SlicesMetricsOrModels


class BeeswarmParameters(CamelModel):
    """Parameter specification for a beeswarm chart."""

    metrics: list[str]
    slices: list[int]
    models: list[str]
    y_channel: SlicesOrModels
    color_channel: SlicesOrModels
    fixed_dimension: str


class RadarParameters(CamelModel):
    """Parameter specification for a radar chart."""

    metrics: list[str]
    slices: list[int]
    models: list[str]
    axis_channel: SlicesMetricsOrModels
    layer_channel: SlicesOrModels
    fixed_channel: SlicesMetricsOrModels


class HeatmapParameters(CamelModel):
    """Parameter specirication for a heatmap chart."""

    metric: str
    x_values: list[int | str]
    y_values: list[int | str]
    model: str
    y_channel: SlicesOrModels
    x_channel: SlicesOrModels


class Chart(CamelModel):
    """Generic chart specification with parameters for specific chart types."""

    id: int
    name: str
    type: ChartType
    parameters: (
        XCParameters
        | TableParameters
        | BeeswarmParameters
        | RadarParameters
        | HeatmapParameters
    )


class ParametersEncoder(json.JSONEncoder):
    """JSON encoder for chart parameter data."""

    def default(
        self,
        o: XCParameters
        | TableParameters
        | BeeswarmParameters
        | RadarParameters
        | HeatmapParameters,
    ):
        """Convert chart parameter data into JSON to be saved in the database.

        Args:
            o (Union[Any[ParameterType]]): The chart parameters to be
            converted.

        Returns:
            object: a dict to be encoded by a JSON encoder and saved into the database.
        """
        return o.__dict__
