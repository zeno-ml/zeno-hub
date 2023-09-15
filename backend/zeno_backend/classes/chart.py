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
    metric: int
    models: list[str]
    color_channel: SlicesOrModels
    x_channel: SlicesOrModels

    def __hash__(self) -> int:
        """Hash the chart parameters.

        Returns:
            int: The hash of the chart parameters.
        """
        return hash(
            hash(tuple(self.slices))
            + hash(self.metric)
            + hash(tuple(self.models))
            + hash(self.color_channel)
            + hash(self.x_channel)
        )


class TableParameters(CamelModel):
    """Parameter specification for a tabular visualization."""

    metrics: list[int]
    slices: list[int]
    models: list[str]
    y_channel: SlicesOrModels
    x_channel: SlicesMetricsOrModels
    fixed_channel: SlicesMetricsOrModels

    def __hash__(self) -> int:
        """Hash the chart parameters.

        Returns:
            int: The hash of the chart parameters.
        """
        return hash(
            hash(tuple(self.metrics))
            + hash(tuple(self.slices))
            + hash(tuple(self.models))
            + hash(self.y_channel)
            + hash(self.x_channel)
            + hash(self.fixed_channel)
        )


class BeeswarmParameters(CamelModel):
    """Parameter specification for a beeswarm chart."""

    metrics: list[int]
    slices: list[int]
    models: list[str]
    y_channel: SlicesOrModels
    color_channel: SlicesOrModels
    fixed_dimension: str

    def __hash__(self):
        """Hash the chart parameters.

        Returns:
            int: The hash of the chart parameters.
        """
        return hash(
            hash(tuple(self.metrics))
            + hash(tuple(self.slices))
            + hash(tuple(self.models))
            + hash(self.y_channel)
            + hash(self.color_channel)
            + hash(self.fixed_dimension)
        )


class RadarParameters(CamelModel):
    """Parameter specification for a radar chart."""

    metrics: list[int]
    slices: list[int]
    models: list[str]
    axis_channel: SlicesMetricsOrModels
    layer_channel: SlicesOrModels
    fixed_channel: SlicesMetricsOrModels

    def __hash__(self):
        """Hash the chart parameters.

        Returns:
            int: The hash of the chart parameters.
        """
        return hash(
            hash(tuple(self.metrics))
            + hash(tuple(self.slices))
            + hash(tuple(self.models))
            + hash(self.axis_channel)
            + hash(self.layer_channel)
            + hash(self.fixed_channel)
        )


class HeatmapParameters(CamelModel):
    """Parameter specirication for a heatmap chart."""

    metric: int
    x_values: list[int | str]
    y_values: list[int | str]
    model: str
    y_channel: SlicesOrModels
    x_channel: SlicesOrModels

    def __hash__(self) -> int:
        """Hash the chart parameters.

        Returns:
            int: The hash of the chart parameters.
        """
        return hash(
            hash(self.metric)
            + hash(tuple(self.x_values))
            + hash(tuple(self.y_values))
            + hash(self.model)
            + hash(self.y_channel)
            + hash(self.x_channel)
        )


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
    project_uuid: str | None = None

    def __hash__(self) -> int:
        """Hash the chart parameters.

        Returns:
            int: The hash of the chart parameters.
        """
        return hash(
            hash(self.name)
            + hash(self.type)
            + hash(self.parameters)
            + hash(self.project_uuid)
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


class ChartResponse(CamelModel):
    """Chart specification and data.

    Parameters:
        chart (Chart): The chart specification.
        chart_data (str): The chart data in JSON string.
    """

    chart: Chart
    chart_data: str
