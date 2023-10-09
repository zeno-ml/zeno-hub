"""Types for Zeno reports."""
from enum import Enum

from zeno_backend.classes.base import CamelModel


class ReportElementType(Enum):
    """Enumeration of possible report types in Zeno.

    Attributes:
        CHART: chart element for a report.
        TEXT: text element for a report.
        INSTANCES: list of instances element for a report.
    """

    CHART = "CHART"
    TEXT = "TEXT"
    INSTANCES = "INSTANCES"


class Report(CamelModel):
    """Representation of a report in Zeno.

    Attributes:
        id (int): ID of the report.
        name (str): name of the report.
        owner_name (str): name of the creater of the report
        linked_projects (list[str]): all projects that can be used with the report.
        editor (bool): whether the current user can edit the report.
        public (bool): whether the report is publically visible.
        description (str): description of the report. Default "".
    """

    id: int
    name: str
    owner_name: str
    linked_projects: list[str]
    editor: bool
    public: bool = False
    description: str = ""


class ReportElement(CamelModel):
    """Representation of an element of a Zeno report.

    Attributes:
        type (ReportElementType): what type of element this represents.
        data (str | None): any data that the element holds.
        chart_id (int | None): id of the chart this element is linked to.
    """

    id: int | None = None
    type: ReportElementType
    position: int
    data: str | None = None
    chart_id: int | None = None


class ReportResponse(CamelModel):
    """Response for a report in Zeno.

    Attributes:
        report (Report): the report itself.
        report_elements (list[ReportElement]): all elements of the report.
    """

    report: Report
    report_elements: list[ReportElement]


class ReportStats(CamelModel):
    """Statistical numbers of a Zeno report.

    Attributes:
        num_projects (int): number of projects that are linked to the report.
        num_elements (int): number of elements in the report.
    """

    num_projects: int
    num_elements: int


class InstancesElement(CamelModel):
    """Data for an instances element in a Zeno report."""

    slice_id: int
    model_name: str


class InstancesOptions(CamelModel):
    """Necessary options to render an instances report element."""

    view: str
    id_column: str
    data_column: str | None = None
    label_column: str | None = None
    model_column: str | None = None
