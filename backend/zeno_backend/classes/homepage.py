"""Classes for fetching homepage data."""

from enum import Enum

from zeno_backend.classes.base import CamelModel
from zeno_backend.classes.project import Project, ProjectStats
from zeno_backend.classes.report import Report, ReportStats


class EntryTypeFilter(str, Enum):
    """Type of entry to filter by."""

    ALL = "ALL"
    PROJECT = "PROJECT"
    REPORT = "REPORT"


class EntrySort(str, Enum):
    """Sort order for entries."""

    POPULAR = "POPULAR"
    RECENT = "RECENT"


class HomeRequest(CamelModel):
    """Request for homepage entries.

    Attributes:
        user_name: Username of user to get entries for. If None, get public entries.
        project_offset: Offset of project entries already fetched
        report_offset: Offset of report entries already fetched
        limit: Limit of entries to return
        search_string: String to search for in entries
        type_filter: Type of entry to filter by
        sort: Sort order for entries
    """

    user_name: str | None = None
    project_offset: int = 0
    report_offset: int = 0
    limit: int | None = None
    search_string: str = ""
    type_filter: EntryTypeFilter = EntryTypeFilter.ALL
    sort: EntrySort = EntrySort.POPULAR


class HomeEntry(CamelModel):
    """Entry for homepage.

    Attributes:
        entry: Project or Report
        stats: ProjectStats or ReportStats
    """

    entry: Project | Report
    stats: ProjectStats | ReportStats
