"""Functions to upload data to Zeno's backend."""
import io
import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from pycognito import Cognito


# TODO: Do not export the Project class, only make it available through the ZenoClient.
class ZenoProject:
    """Provides data upload functionality for a Zeno project.

    Attributes:
        user (Cognito): The user to authenticate uploads with.
        project_uuid (str): The ID of the project to add data to.
        endpoint (str): The base URL of the Zeno backend.
    """

    user: Cognito
    project_uuid: str
    endpoint: str

    def __init__(self, user: Cognito, project_uuid: str, endpoint: str) -> None:
        """Initialize the Project object for API upload calls.

        Args:
            user (Cognito): the user to authenticate uploads with.
            project_uuid (str): the ID of the project to add data to.
            endpoint (str): the base URL of the Zeno backend.
        """
        self.user = user
        self.project_uuid = project_uuid
        self.endpoint = endpoint

    def upload_dataset(
        self,
        df: pd.DataFrame,
        id_column: str,
        label_column: str | None = None,
        data_column: str | None = None,
    ):
        """Upload a dataset to a Zeno project.

        Args:
            df (pd.DataFrame): The dataset to upload.
            id_column (str): The name of the column containing the instance IDs.
            label_column (str | None, optional): The name of the column containing the
                instance labels. Defaults to None.
            data_column (str | None, optional): The name of the column containing the
                raw data. Only works for small text data. Defaults to None.
        """
        if len(id_column) == 0:
            raise Exception("ERROR: id_column name must be non-empty")

        b = io.BytesIO()
        df.to_feather(b)
        b.seek(0)
        response = requests.post(
            f"{self.endpoint}/api/dataset/{self.project_uuid}",
            data={
                "id_column": id_column,
                "label_column": label_column if label_column is not None else "",
                "data_column": data_column if data_column is not None else "",
            },
            files={"file": (b)},
            headers={"Authorization": "Bearer " + str(self.user.access_token)},
        )
        if response.status_code == 200:
            print("Successfully uploaded data")
        else:
            raise Exception(response.json()["detail"])

    def upload_system(
        self, system_name: str, df: pd.DataFrame, output_column: str, id_column: str
    ):
        """Upload a system to a Zeno project.

        Args:
            df (pd.DataFrame): The dataset to upload.
            system_name (str): The name of the system to upload.
            output_column (str): The name of the column containing the system output.
            id_column (str): The name of the column containing the instance IDs.
        """
        if len(system_name) == 0 or len(output_column) == 0:
            raise Exception("System_name and output_column must be non-empty.")

        b = io.BytesIO()
        df.to_feather(b)
        b.seek(0)
        response = requests.post(
            f"{self.endpoint}/api/system/{self.project_uuid}",
            data={
                "system_name": system_name,
                "output_column": output_column,
                "id_column": id_column,
            },
            files={"file": (b)},
            headers={"Authorization": "Bearer " + str(self.user.access_token)},
        )
        if response.status_code == 200:
            print("Successfully uploaded system")
        else:
            raise Exception(response.json()["detail"])


class ZenoClient:
    """Client class for data upload functionality to Zeno.

    Attributes:
        user (Cognito): The user to authenticate uploads with.
        username (str): The username of the user to authenticate with.
        endpoint (str): The base URL of the Zeno backend.
    """

    user: Cognito | None
    username: str
    endpoint: str

    def __init__(
        self, *, username, password, endpoint=os.environ["PUBLIC_BACKEND_ENDPOINT"]
    ) -> None:
        """Initialize the ZenoClient object for API upload calls.

        Args:
            username (str): the username of the user to authenticate with.
            password (str): the password of the user to authenticate with.
            endpoint (str, optional): the base URL of the Zeno backend.
                Defaults to os.environ["PUBLIC_BACKEND_ENDPOINT"].
        """
        # TODO: remove env vars loading.
        # load env vars for cognito if available
        env_path = Path("../../frontend/.env")
        if env_path.exists():
            load_dotenv(env_path)

        # TODO: Figure out how to package without providing env vars
        user = Cognito(
            os.environ["ZENO_USER_POOL_ID"],
            os.environ["ZENO_USER_POOL_CLIENT_ID"],
            username=username,
        )
        user.authenticate(password=password)

        self.user = user
        self.username = username
        self.endpoint = endpoint

    def create_project(
        self,
        name: str,
        view: str,
        data_url: str = "",
        calculate_histogram_metrics: bool = True,
        samples_per_page: int = 10,
        public: bool = False,
    ) -> ZenoProject:
        """Creates an empty project in Zeno's backend.

        Args:
            name (str): The name of the project to be created. The project will be
                created under the current user, e.g. username/name.
                project: str,
            view (str): The view to use for the project.
            metrics (list[str], optional): The metrics to calculate for the project.
                Defaults to [].
            data_url (str, optional): The URL to the data to use for the project.
                Defaults to "".
            calculate_histogram_metrics (bool, optional): Whether to calculate histogram
                metrics. Defaults to True.
            samples_per_page (int, optional): The number of samples to show per page.
                Defaults to 10.
            public (bool, optional): Whether the project is public. Defaults to False.


        Returns:
            ZenoProject | None: The created project object or None if the project could
                not be created.

        Raises:
            ValidationError: If the config does not match the ProjectConfig schema.
            HTTPError: If the project could not be created.
        """
        if self.user is None:
            raise Exception(
                "ERROR: User not authenticated. Please try creating the client again."
            )
        else:
            self.user.check_token()

        response = requests.post(
            f"{self.endpoint}/api/project",
            json={
                "uuid": "",
                "name": name,
                "view": view,
                "owner_name": self.username,
                "data_url": data_url,
                "calculate_histogram_metrics": calculate_histogram_metrics,
                "samplesPerPage": samples_per_page,
                "public": public,
                "editor": True,
            },
            headers={"Authorization": "Bearer " + str(self.user.access_token)},
        )
        if response.status_code == 200:
            print("Successfully created project", self.username + "/" + name)
            return ZenoProject(self.user, response.text[1:-1], self.endpoint)
        else:
            raise Exception(response.json()["detail"])

    def get_project(self, project_name: str) -> ZenoProject:
        """Get a project object by its name. Names are split into owner/project_name.

        If no slash is present, user is assumed to be the owner.

        Args:
            project_name (str): The owner/project_name of the project to get.


        Returns:
            Project | None: The project object or None if the project could not be
                found.


        Raises:
            Exception: If the user is not authenticated.
            HTTPError: If the project could not be found.
        """
        if self.user is None:
            print(
                "ERROR: User not authenticated. Please try creating the client again."
            )
            raise Exception(
                "User not authenticated. Please try creating the client again."
            )

        # Get owner and project name from project_name.
        # If no owner, assume current user.
        split_project_name = project_name.split("/")
        if len(split_project_name) == 1:
            user = self.username
            project_name = project_name
        else:
            user = split_project_name[0]
            project_name = split_project_name[1]

        response = requests.get(
            f"{self.endpoint}/api/project-uuid/{user}/{project_name}",
            headers={"Authorization": "Bearer " + str(self.user.access_token)},
        )
        if response.status_code == 200:
            return ZenoProject(self.user, response.text[1:-1], self.endpoint)
        else:
            raise Exception(response.json()["detail"])
