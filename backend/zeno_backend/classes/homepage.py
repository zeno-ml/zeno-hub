"""Classes for homepage data."""

from zeno_backend.classes.base import CamelModel
from zeno_backend.classes.project import Project
from zeno_backend.classes.report import Report


class HomepageData(CamelModel):
    """Projects, reports, and metadata for homepage rendering.

    Attributes:
        projects (list[Project]): the projects to be displayed.
        reports (list[Report]): the reports to be displayed.
        num_projects (int): the number of projects.
        num_reports (int): the number of reports.
    """

    projects: list[Project]
    reports: list[Report]
    num_projects: int
    num_reports: int
