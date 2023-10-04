"""Types for Zeno projects."""

from zeno_backend.classes.base import CamelModel, ZenoColumn
from zeno_backend.classes.folder import Folder
from zeno_backend.classes.metric import Metric
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.tag import Tag


class Project(CamelModel):
    """Projects with datasets & models.

    Attributes:
        uuid (str): UUID of the task.
        name (str): name of the task.
        metrics (list[Metric]): metrics to calculate for the task.
        owner_name (str): name of the user who owns the task.
        view (str): name of the view to use for the task.
        data_url (Optional[str]): base URL from which to read data instances.
        editor (bool): whether the current user is an editor of the project.
        calculate_histogram_metrics (bool): whether to calculate histogram metrics.
            Default True.
        samples_per_page (int): number of datapoints to show per page. Default 10.
        public (bool): whether the task is public. Default False.
        description (str): description of the project. Default "".
    """

    uuid: str
    name: str
    metrics: list[Metric] = []
    owner_name: str
    view: str
    data_url: str | None
    editor: bool
    calculate_histogram_metrics: bool = True
    samples_per_page: int = 10
    public: bool = False
    description: str = ""


class ProjectStats(CamelModel):
    """Statistical numbers of a Zeno project.

    Attributes:
        num_instances (int): number of data instances in the project.
        num_charts (int): number of charts that have been created for the project.
        num_models (int): number of models associated with the project
    """

    num_instances: int
    num_charts: int
    num_models: int


class ProjectState(CamelModel):
    """State variables for a Zeno project.

    Attributes:
        project (Project): project object with project metadata.
        models (list[str]): names of the models in the project.
        metrics (list[Metric]): metrics to calculate for the project.
        columns (list[ZenoColumn]): columns in the project.
        slices (list[Slice]): slices in the project.
        tags (list[Tag]): tags in the project.
        folders (list[Folder]): folders in the project.
    """

    project: Project
    models: list[str]
    metrics: list[Metric]
    columns: list[ZenoColumn]
    slices: list[Slice]
    tags: list[Tag]
    folders: list[Folder]


class ProjectCopy(CamelModel):
    """Specification for copying a Zeno project.

    Attributes:
        name (str): name of the new project.
        data_url (str|None): base URL from which to read data instances.
        copy_data (bool): whether to copy the data instances.
        copy_systems (bool): whether to copy the systems.
        copy_slices (bool): whether to copy the slices.
        copy_charts (bool): whether to copy the charts.
    """

    name: str
    data_url: str | None
    copy_data: bool
    copy_systems: bool
    copy_slices: bool
    copy_charts: bool
