"""Functionality to interact with the database."""
import os
from configparser import ConfigParser
from pathlib import Path
from typing import Any, LiteralString

import psycopg
from psycopg import sql


class Database:
    """Database representation to make SQL interaction simpler."""

    conn: psycopg.Connection[tuple[Any, ...]] | None = None
    cur: psycopg.Cursor[tuple[Any, ...]] | None = None

    def connect(self):
        """Connect to the running database.

        The connection can be specified in a configuration file.

        Raises:
            Exception: the connection to the database failed.
        """
        params = self.config()
        try:
            self.conn = psycopg.connect(**params)
            self.cur = self.conn.cursor()
        except (Exception, psycopg.DatabaseError) as error:
            raise Exception(error) from error

    def commit(self):
        """Commit a set of querys to the database."""
        if self.conn is not None:
            self.conn.commit()

    def disconnect(self):
        """Disconnect from the database."""
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
        self.cur = None
        self.conn = None

    def execute(
        self,
        query: LiteralString | sql.Composed,
        params: list[Any] | None = None,
    ):
        """Execute a query on the database.

        Args:
            query (Union[sql.LiteralString, sql.Composed]): the query to be executed.
            params (list[Any], optional): any parameters to be passed to the query.
            Defaults to None.

        Raises:
            Exception: the query failed to execute.
        """
        try:
            if self.cur is not None:
                self.cur.execute(query, params)
        except (Exception, psycopg.DatabaseError) as error:
            raise Exception(error) from error

    def connect_execute(
        self,
        query: LiteralString | sql.Composed,
        params: list[Any] | None = None,
    ):
        """Connect to the database and execute a query, then disconnect.

        Args:
            query (Union[LiteralString, sql.Composed]): the query to be executed.
            params (list[Any], optional): any parameters to be passed to the query.
            Defaults to None.

        Raises:
            Exception: the query failed to execute.
        """
        try:
            self.connect()
            self.execute(query, params)
            self.commit()
        except (Exception, psycopg.DatabaseError) as error:
            raise Exception(error) from error
        finally:
            self.disconnect()

    def execute_return(
        self,
        query: LiteralString | sql.Composed,
        params: list[Any] | None = None,
        return_all: bool = False,
    ):
        """Execute a query on the database and then return one or multiple results.

        Args:
            query (Union[LiteralString, sql.Composed]): the query to be executed.
            params (list[Any], optional): any parameters to be passed to the query.
            Defaults to None.
            return_all (bool, optional): whether to return all results instead of just
            the first. Defaults to False.

        Raises:
            Exception: the query failed to execute

        Returns:
            Any: the data as fetched by the query.
        """
        try:
            if self.cur is not None:
                self.cur.execute(query, params)
                return self.cur.fetchall() if return_all else self.cur.fetchone()
        except (Exception, psycopg.DatabaseError) as error:
            raise Exception(error) from error

    def connect_execute_return(
        self,
        query: LiteralString | sql.Composed,
        params: list[Any] | None = None,
        return_all: bool = False,
    ):
        """Connect, execute a query, return one or multiple results, and disconnect.

        Args:
            query (Union[sql.LiteralString, sql.Composed]): the query to be executed.
            params (list[Any], optional): any parameters to be passed to the query.
            Defaults to None.
            return_all (bool, optional): whether to return all results instead of just
            the first. Defaults to False.

        Raises:
            Exception: the query failed to execute

        Returns:
            Any: the data as fetched by the query.
        """
        try:
            self.connect()
            result = self.execute_return(query, params, return_all)
            self.commit()
            return result
        except (Exception, psycopg.DatabaseError) as error:
            raise Exception(error) from error
        finally:
            self.disconnect()

    def config(
        self,
        filename: str = "zeno_backend/database/database.ini",
        section: str = "postgresql",
    ) -> dict[str, Any]:
        """Get the configuration of the database.

        Args:
            filename (str, optional): the path to the database.ini.
            Defaults to "zeno_backend/database/database.ini".
            section (str, optional): which section in the database.ini to read.
            Defaults to "postgresql".

        Raises:
            Exception: reading the configuration failed.

        Returns:
            dict[str, Any]: the database configuration.
        """
        if Path(filename).exists():
            parser = ConfigParser()
            parser.read(filename)
            db: dict[str, Any] = {}
            if parser.has_section(section):
                params = parser.items(section)
                for param in params:
                    db[param[0]] = param[1]
            else:
                raise Exception(f"Section {section} not found in the {filename} file")
            return db
        else:
            db: dict[str, Any] = {}
            db["host"] = os.environ["DB_HOST"]
            db["port"] = os.environ["DB_PORT"]
            db["dbname"] = os.environ["DB_NAME"]
            db["user"] = os.environ["DB_USER"]
            db["password"] = os.environ["DB_PASSWORD"]
            return db
