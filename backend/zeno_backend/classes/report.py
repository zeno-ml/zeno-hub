"""Types for Zeno reports."""
from enum import Enum

from zeno_backend.classes.base import CamelModel
from zeno_backend.classes.project import Project


class ReportElementType(Enum):
    """Enumeration of possible report types in Zeno.

    Attributes:
        CHART: chart element for a report.
        TEXT: text element for a report.
        SLICE: slice of instances for a report.
    """

    CHART = "CHART"
    TEXT = "TEXT"
    SLICE = "SLICE"


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
    """

    id: int | None = None
    type: ReportElementType
    position: int
    data: str | None = None


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


class ReportDetails(CamelModel):
    """Report and details for homepage rendering.

    Attributes:
        report (Report): report object with report metadata.
        statistics (ReportStats): report statistics.
    """

    report: Report
    statistics: ReportStats


class SliceElementSpec(CamelModel):
    """Specification for slice element in a Zeno report."""

    slice_id: int
    model_name: str | None = None


class SliceElementOptions(CamelModel):
    """Necessary options to render a slice report element.

    Attributes:
        slice_name (str): name of the slice to render.
        slice_size (int): number of instances in the slice.
        view (str): name of the instance view.
        id_column (str): name of the column containing the instance id.
        data_column (str | None): name of the column containing the instance data.
        label_column (str | None): name of the column containing the instance label.
        model_column (str | None): name of the column containing the instance model.
    """

    project: Project
    slice_name: str
    slice_size: int
    id_column: str
    data_column: str | None = None
    label_column: str | None = None
    model_column: str | None = None
