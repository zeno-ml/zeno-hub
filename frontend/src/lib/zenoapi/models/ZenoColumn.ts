/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MetadataType } from './MetadataType';
import type { ZenoColumnType } from './ZenoColumnType';

/**
 * Representation of a column in Zeno's project data.
 */
export type ZenoColumn = {
	id: string;
	columnType: ZenoColumnType;
	name: string;
	dataType: MetadataType;
	model?: string | null;
};
