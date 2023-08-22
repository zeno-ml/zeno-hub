"""Types for Zeno projects."""
from zeno_backend.classes.base import CamelModel


class Project(CamelModel):
    """Projects with datasets & models.

    Attributes:
        uuid (str): The UUID of the task.
        name (str): The name of the task.
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
