"""Classes for fetching homepage data."""

from enum import Enum

from zeno_backend.classes.base import CamelModel
from zeno_backend.classes.project import Project, ProjectStats
from zeno_backend.classes.report import Report, ReportStats


class HomeTypeFilter(str, Enum):
    """Type of entry to filter by."""

    ALL = "ALL"
    PROJECT = "PROJECT"
    REPORT = "REPORT"


class HomeSort(str, Enum):
    """Sort order for entries."""

    POPULAR = "POPULAR"
    RECENT = "RECENT"


class HomeRequest(CamelModel):
    """Request for homepage entries.

    Attributes:
        user_name: Username of user to get entries for. If None, get public entries.
        offset: Offset of entries to return
        limit: Limit of entries to return
        search_string: String to search for in entries
        type_filter: Type of entry to filter by
        sort: Sort order for entries
    """

    user_name: str | None = None
    offset: int = 0
    limit: int | None = None
    search_string: str = ""
    type_filter: HomeTypeFilter = HomeTypeFilter.ALL
    sort: HomeSort = HomeSort.POPULAR


class HomeEntry(CamelModel):
    """Entry for homepage.

    Attributes:
        entry: Project or Report
        stats: ProjectStats or ReportStats
    """

    entry: Project | Report
    stats: ProjectStats | ReportStats
