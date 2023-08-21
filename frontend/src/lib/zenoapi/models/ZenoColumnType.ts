/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Enumeration of possible column types in Zeno.
 *
 * Attributes:
 * DATA: Input data instance. Either raw data or filename.
 * LABEL: Ground truth label.
 * OUTPUT: Model output.
 * FEATURE: Metadata feature for an input data instance.
 * EMBEDDING: Vector embedding representing a data instance or output.
 */
export enum ZenoColumnType {
	DATA = 'DATA',
	LABEL = 'LABEL',
	OUTPUT = 'OUTPUT',
	FEATURE = 'FEATURE',
	EMBEDDING = 'EMBEDDING'
}
