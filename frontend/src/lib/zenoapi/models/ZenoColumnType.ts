/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Enumeration of possible column types in Zeno.
 *
 * Attributes:
 * DATA: input data instance. Either raw data or filename.
 * LABEL: ground truth label.
 * OUTPUT: model output.
 * FEATURE: metadata feature for an input data instance.
 * EMBEDDING: vector embedding representing a data instance or output.
 */
export enum ZenoColumnType {
	DATA = 'DATA',
	LABEL = 'LABEL',
	OUTPUT = 'OUTPUT',
	FEATURE = 'FEATURE',
	EMBEDDING = 'EMBEDDING'
}
