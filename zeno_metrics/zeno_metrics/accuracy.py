"""Provides the accuracy metric for Zeno."""
from typing import Any

import psycopg
from psycopg import sql
from util import Metric, MetricReturn, MetricType, column_id_from_name_and_model


class Accuracy(Metric):
    """Calculating system accuracy.

    Calculated either on a column that indicates correctness or on input/output columns.

    Attributes:
        correct_column (str | None): name of column that indicates system correctnes.
    """

    correct_column: str | None

    def __init__(
        self,
        name: str = "accuracy",
        correct_column: str | None = None,
    ):
        """Create an acurracy metric for use in Zeno.

        Args:
            name (str): the name of the metric to be shown. Defaults to "accuracy".
            correct_column (str | None, optional): if this is specified, calculate
                accuracy based on this column. Needs to be a boolean column.
                Defaults to None.
        """
        self.name = name
        self.type = MetricType.ACCURACY
        self.correct_column = correct_column

    def evaluate(
        self, db_cursor: psycopg.Cursor[tuple[Any, ...]], model: str, project: str
    ) -> MetricReturn:
        """Evaluate the metric given a database curser.

        Args:
            db_cursor (psycopg.Cursor[tuple[Any, ...]]): the curser to issue database
                operations on.
            model (str): the model for which to evaluate the metric.
            project (str): the project for which to evaluate the metric.

        Returns:
            MetricReturn: the metric and instance count value for the evaluated metric.
        """
        if self.correct_column is not None:
            return self.calculate_from_correct(db_cursor, model, project)
        return self.calculate_from_label_output(db_cursor, model, project)

    def calculate_from_label_output(
        self, db_cursor: psycopg.Cursor[tuple[Any, ...]], model: str, project: str
    ) -> MetricReturn:
        """Calculate the accuracy from a label and output column.

        Args:
            db_cursor (psycopg.Cursor[tuple[Any, ...]]): the curser to issue database
                operations on.
            model (str): the model for which to evaluate the metric.
            project (str): the project for which to evaluate the metric.

        Returns:
            MetricReturn: the metric and instance count value for the evaluated metric.
        """
        output_column_id = column_id_from_name_and_model(
            db_cursor, project, "output", model
        )
        correct_query = sql.SQL("SELECT COUNT(*) FROM {} WHERE {} = label").format(
            sql.Identifier(project), sql.Identifier(output_column_id)
        )
        db_cursor.execute(
            correct_query
            if filter is None
            else correct_query + sql.SQL(" AND ") + filter,
        )
        num_correct = db_cursor.fetchone()
        total_query = sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(project))
        db_cursor.execute(
            total_query
            if filter is None
            else total_query + sql.SQL(" WHERE ") + filter,
        )
        num_total = db_cursor.fetchone()
        return (
            (
                MetricReturn(
                    metric=100 * num_correct[0] / num_total[0], size=num_total[0]
                )
                if num_total[0] != 0
                else MetricReturn(metric=0, size=0)
            )
            if num_correct is not None
            and isinstance(num_correct[0], int)
            and num_total is not None
            and isinstance(num_total[0], int)
            else MetricReturn(metric=None, size=0)
        )

    def calculate_from_correct(
        self,
        db_cursor: psycopg.Cursor[tuple[Any, ...]],
        model: str,
        project: str,
    ) -> MetricReturn:
        """Calculate the accuracy from a correctness column.

        Args:
            db_cursor (psycopg.Cursor[tuple[Any, ...]]): the curser to issue database
                operations on.
            model (str): the model for which to evaluate the metric.
            project (str): the project for which to evaluate the metric.

        Returns:
            MetricReturn: the metric and instance count value for the evaluated metric.
        """
        if self.correct_column is None:
            return MetricReturn(metric=None, size=0)
        correct_column_id = column_id_from_name_and_model(
            db_cursor, project, self.correct_column, model
        )
        correct_query = sql.SQL("SELECT COUNT(*) FROM {} WHERE {} IS TRUE").format(
            sql.Identifier(project), sql.Identifier(correct_column_id)
        )
        db_cursor.execute(
            correct_query
            if filter is None
            else correct_query + sql.SQL(" AND ") + filter,
        )
        num_correct = db_cursor.fetchone()
        total_query = sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(project))
        db_cursor.execute(
            total_query
            if filter is None
            else total_query + sql.SQL(" WHERE ") + filter,
        )
        num_total = db_cursor.fetchone()
        return (
            (
                MetricReturn(
                    metric=100 * num_correct[0] / num_total[0], size=num_total[0]
                )
                if num_total[0] != 0
                else MetricReturn(metric=0, size=0)
            )
            if num_correct is not None
            and isinstance(num_correct[0], int)
            and num_total is not None
            and isinstance(num_total[0], int)
            else MetricReturn(metric=None, size=0)
        )
