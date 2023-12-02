"""Type representations for chart data."""
import json
from enum import Enum

from zeno_backend.classes.base import CamelModel


class ChartType(str, Enum):
    """Enumeration of chart types available in Zeno.

    Attributes:
        BAR: bar chart.
        LINE: line chart.
        TABLE: table.
        BEESWARM: beeswarm chart.
        RADAR: radar chart.
        HEATMAP: heatmap chart.
    """

    BAR = "BAR"
    LINE = "LINE"
    TABLE = "TABLE"
    BEESWARM = "BEESWARM"
    RADAR = "RADAR"
    HEATMAP = "HEATMAP"


class SlicesOrModels(str, Enum):
    """Choice of chart encoding types between slices and models.

    Attributes:
        SLICES: slices.
        MODELS: models.
    """

    SLICES = "SLICES"
    MODELS = "MODELS"


class SlicesMetricsOrModels(str, Enum):
    """Choice of chart encoding types between slices, metrics, and models.

    Attributes:
        SLICES: slices.
        MODELS: models.
        METRICS: metrics.
    """

    SLICES = "SLICES"
    MODELS = "MODELS"
    METRICS = "METRICS"


class XCParameters(CamelModel):
    """Parameter specification for the x and color channels of a chart.

    Attributes:
        slices (list[int]): slices to be used in the chart.
        metric (int): metric to be used in the chart.
        models (list[str]): models to be used in the chart.
        color_channel (SlicesOrModels): type of the color channel.
        x_channel (SlicesOrModels): type of the x channel.
    """

    slices: list[int]
    metric: int
    models: list[str]
    color_channel: SlicesOrModels
    x_channel: SlicesOrModels

    def __hash__(self) -> int:
        """Hash the chart parameters.

        Returns:
            int: hash of the chart parameters.
        """
        return hash(
            hash(tuple(self.slices))
            + hash(self.metric)
            + hash(tuple(self.models))
            + hash(self.color_channel)
            + hash(self.x_channel)
        )


class TableParameters(CamelModel):
    """Parameter specification for a tabular visualization.

    Attributes:
        metrics (list[int]): metrics to be used in the chart.
        slices (list[int]): slices to be used in the chart.
        models (list[str]): models to be used in the chart.
        y_channel (SlicesOrModels): type of the y channel.
        x_channel (SlicesMetricsOrModels): type of the x channel.
        fixed_channel (SlicesMetricsOrModels): type of the fixed channel.
    """

    metrics: list[int]
    slices: list[int]
    models: list[str]
    y_channel: SlicesOrModels
    x_channel: SlicesMetricsOrModels
    fixed_channel: SlicesMetricsOrModels

    def __hash__(self) -> int:
        """Hash the chart parameters.

        Returns:
            int: hash of the chart parameters.
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
    """Parameter specification for a beeswarm chart.

    Attributes:
        metrics (list[int]): metrics to be used in the chart.
        slices (list[int]): slices to be used in the chart.
        models (list[str]): models to be used in the chart.
        y_channel (SlicesOrModels): type of the y channel.
        color_channel (SlicesOrModels): type of the color channel.
        fixed_dimension (str): fixed dimension of the chart.
    """

    metrics: list[int]
    slices: list[int]
    models: list[str]
    y_channel: SlicesOrModels
    color_channel: SlicesOrModels
    fixed_dimension: str

    def __hash__(self):
        """Hash the chart parameters.

        Returns:
            int: hash of the chart parameters.
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
    """Parameter specification for a radar chart.

    Attributes:
        metrics (list[int]): metrics to be used in the chart.
        slices (list[int]): slices to be used in the chart.
        models (list[str]): models to be used in the chart.
        axis_channel (SlicesMetricsOrModels): type of the axis channel.
        layer_channel (SlicesOrModels): type of the layer channel.
        fixed_channel (SlicesMetricsOrModels): type of the fixed channel.
    """

    metrics: list[int]
    slices: list[int]
    models: list[str]
    axis_channel: SlicesMetricsOrModels
    layer_channel: SlicesOrModels
    fixed_channel: SlicesMetricsOrModels

    def __hash__(self):
        """Hash the chart parameters.

        Returns:
            int: hash of the chart parameters.
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
    """Parameter specirication for a heatmap chart.

    Attributes:
        metric (int): metric to be used in the chart.
        x_values (list[int | str]): x values to be used in the chart.
        y_values (list[int | str]): y values to be used in the chart.
        model (str): model to be used in the chart.
        y_channel (SlicesOrModels): type of the y channel.
        x_channel (SlicesOrModels): type of the x channel.
    """

    metric: int
    x_values: list[int | str]
    y_values: list[int | str]
    model: str
    y_channel: SlicesOrModels
    x_channel: SlicesOrModels

    def __hash__(self) -> int:
        """Hash the chart parameters.

        Returns:
            int: hash of the chart parameters.
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
    """Generic chart specification with parameters for specific chart types.

    Attributes:
        id (int): the id of the chart.
        name (str): the name of the chart.
        project_uuid (str): the project uuid of the chart.
        type (ChartType): the type of the chart.
        parameters (XCParameters | TableParameters | BeeswarmParameters |
            RadarParameters | HeatmapParameters): the parameters of the chart.
        data (str): the JSON string data of the chart.
    """

    id: int
    name: str
    project_uuid: str
    type: ChartType
    parameters: (
        XCParameters
        | TableParameters
        | BeeswarmParameters
        | RadarParameters
        | HeatmapParameters
    )
    data: str | None = None


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
            o (Union[Any[ParameterType]]): chart parameters to be converted.

        Returns:
            object: a dict to be encoded by a JSON encoder and saved into the database.
        """
        return o.__dict__


class ChartResponse(CamelModel):
    """Chart specification and data.

    Parameters:
        chart (Chart): chart specification.
        chart_data (str): chart data in a JSON string.
    """

    chart: Chart
    chart_data: str
