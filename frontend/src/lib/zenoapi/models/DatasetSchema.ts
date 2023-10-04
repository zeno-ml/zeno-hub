/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Metadata for dataset columns.
 *
 * Attributes:
 * project_uuid (str): unique identifier of the project.
 * columns (list[str]): list of column names.
 * id_column (str): column name of the unique identifier.
 * label_column (str): column name of the ground truth label.
 * data_column (str): column name of the raw input data instance.
 */
export type DatasetSchema = {
	projectUuid: string;
	columns: Array<string>;
	idColumn: string;
	labelColumn?: string;
	dataColumn?: string;
};
