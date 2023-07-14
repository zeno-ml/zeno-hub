"""Functions to insert new data into Connex's database."""
import uuid

from connex.classes.endpoint import Endpoint
from connex.classes.project import Project
from connex.classes.user import User
from connex.database.database import Database


def insert_user(user: User):
    """Add a new user to the database.

    Args:
        user (User): the user to be added.
    """
    db = Database()
    db.connect_execute(
        'INSERT INTO account ("user_name","email","secret") values(%s,%s,%s)',
        [user.name, user.email, user.secret],
    )


def insert_endpoint(endpoint: Endpoint):
    """Add a new backend endpoint to the database.

    Args:
        endpoint (Endpoint): the endpoint to be added.
    """
    db = Database()
    db.connect_execute(
        'INSERT INTO endpoint ("name","url") values(%s,%s)',
        [endpoint.name, endpoint.url],
    )


def insert_project(project: Project):
    """Add a new project to Connex.

    Args:
        project (Project): the project to be added.
    """
    db = Database()
    db.connect_execute(
        'INSERT INTO project ("uuid","name","endpoint_id") values(%s,%s,%s)',
        [uuid.uuid4(), project.name, project.endpoint_id],
    )
