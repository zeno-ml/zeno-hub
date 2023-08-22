/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MetadataType } from './MetadataType';
import type { ZenoColumnType } from './ZenoColumnType';

/**
 * Representation of a column in a Zeno project.
 *
 * Attributes:
 * id (str): The ID of the column.
 * name (str): The name of the column.
 * column_type (ZenoColumnType): The type of the column.
 * data_type (MetadataType): The data type of the column.
 * model (str | None): The name of the model that produced the column.
 *
 */
export type ZenoColumn = {
	id: string;
	name: string;
	columnType: ZenoColumnType;
	dataType: MetadataType;
	model?: string | null;
};
