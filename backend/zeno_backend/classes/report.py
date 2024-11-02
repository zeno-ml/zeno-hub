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
        TAG: tag element for a report.
    """

    CHART = "CHART"
    TEXT = "TEXT"
    SLICE = "SLICE"
    TAG = "TAG"


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
        created_at (str): ISO-format string time the report was created. Default "".
        updated_at (str): ISO-format string time the report was last updated.
            Default "".
    """

    id: int
    name: str
    owner_name: str
    linked_projects: list[str]
    editor: bool
    public: bool = False
    description: str = ""
    created_at: str = ""
    updated_at: str = ""


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
        num_likes (int): number of likes the report has.
        user_liked (bool): whether the current user has liked the report.
    """

    report: Report
    report_elements: list[ReportElement]
    num_likes: int
    user_liked: bool


class ReportStats(CamelModel):
    """Statistical numbers of a Zeno report.

    Attributes:
        num_projects (int): number of projects that are linked to the report.
        num_elements (int): number of elements in the report.
        num_likes (int): number of likes the report has.
        user_liked (bool): whether the current user has liked the report.
    """

    num_projects: int
    num_elements: int
    num_likes: int
    user_liked: bool


class SliceElementSpec(CamelModel):
    """Specification for slice element in a Zeno report."""

    slice_id: int
    system_name: str | None = None


class TagElementSpec(CamelModel):
    """Specification for tag element in a Zeno report."""

    tag_id: int
    system_name: str | None = None


class SliceElementOptions(CamelModel):
    """Necessary options to render a slice report element.

    Attributes:
        slice_name (str): name of the slice to render.
        slice_size (int): number of instances in the slice.
        view (str): name of the instance view.
        id_column (str): name of the column containing the instance id.
        data_column (str | None): name of the column containing the instance data.
        label_column (str | None): name of the column containing the instance label.
        system_column (str | None): name of the column containing the instance model.
    """

    project: Project
    slice_name: str
    slice_size: int
    id_column: str
    data_column: str | None = None
    label_column: str | None = None
    system_column: str | None = None


class TagElementOptions(CamelModel):
    """Necessary options to render a tag report element.

    Attributes:
        tag_name (str): name of the tag to render.
        tag_size (int): number of instances in the tag.
        view (str): name of the instance view.
        id_column (str): name of the column containing the instance id.
        data_column (str | None): name of the column containing the instance data.
        label_column (str | None): name of the column containing the instance label.
        system_column (str | None): name of the column containing the instance model.
    """

    project: Project
    tag_name: str
    tag_size: int
    id_column: str
    data_column: str | None = None
    label_column: str | None = None
    system_column: str | None = None
