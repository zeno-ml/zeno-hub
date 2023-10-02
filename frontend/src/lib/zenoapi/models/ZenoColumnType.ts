/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Enumeration of possible column types in Zeno.
 *
 * Attributes:
 * ID: unique identifier.
 * DATA: raw input data instance.
 * LABEL: ground truth label.
 * OUTPUT: model output.
 * FEATURE: metadata feature for data instance.
 * EMBEDDING: vector embedding representing a data instance or output.
 */
export enum ZenoColumnType {
	ID = 'ID',
	DATA = 'DATA',
	LABEL = 'LABEL',
	OUTPUT = 'OUTPUT',
	FEATURE = 'FEATURE',
	EMBEDDING = 'EMBEDDING'
}
