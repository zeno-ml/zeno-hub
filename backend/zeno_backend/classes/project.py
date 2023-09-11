"""Types for Zeno projects."""

from zeno_backend.classes.base import CamelModel, ZenoColumn
from zeno_backend.classes.folder import Folder
from zeno_backend.classes.metric import Metric
from zeno_backend.classes.slice import Slice
from zeno_backend.classes.tag import Tag


class Project(CamelModel):
    """Projects with datasets & models.

    Attributes:
        uuid (str): The UUID of the task.
        name (str): The name of the task.
        metrics (list[Metric]): The metrics to calculate for the task.
        owner_name (str): The name of the user who owns the task.
        view (str): The name of the view to use for the task.
        data_url (Optional[str]): The base URL from which to read data instances.
        editor (bool): Whether the current user is an editor of the project.
        calculate_histogram_metrics (bool): Whether to calculate histogram metrics.
            Default True.
        samples_per_page (int): The number of datapoints to show per page. Default 10.
        public (bool): Whether the task is public. Default False.
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
        project (Project): The project object with project metadata.
        models (list[str]): The names of the models in the project.
        metrics (list[Metric]): The metrics to calculate for the project.
        columns (list[ZenoColumn]): The columns in the project.
        slices (list[Slice]): The slices in the project.
        tags (list[Tag]): The tags in the project.
        folders (list[Folder]): The folders in the project.
    """

    project: Project
    models: list[str]
    metrics: list[Metric]
    columns: list[ZenoColumn]
    slices: list[Slice]
    tags: list[Tag]
    folders: list[Folder]
