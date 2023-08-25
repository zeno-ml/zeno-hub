/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MetadataType } from './MetadataType';

/**
 * Specification for a metadata feature in a Zeno project.
 *
 * Attributes:
 * data_id (int | str): The ID of the associated data instance.
 * col_name (str): The name of the associated column.
 * type (MetadataType): The type of the metadata feature.
 * value (Any): The value of the metadata feature. Default None.
 * model (str | None): The name of the model associated with the
 * metadata feature.
 */
export type FeatureSpec = {
	dataId: number | string;
	colName: string;
	type: MetadataType;
	value?: any;
	model?: string | null;
};
