/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Enumeration of possible metadata types in Zeno.
 *
 * Attributes:
 * NOMINAL: nominal metadata type, e.g. string or small cardinality number.
 * CONTINUOUS: continuous metadata type, e.g. large cardinality number.
 * BOOLEAN: boolean metadata type, e.g. True or False.
 * DATETIME: datetime metadata type, e.g. 2021-01-01 00:00:00.
 * EMBEDDING: vector embedding representing a data instance or output.
 * OTHER: any other metadata type, e.g. strings.
 */
export enum MetadataType {
	NOMINAL = 'NOMINAL',
	CONTINUOUS = 'CONTINUOUS',
	BOOLEAN = 'BOOLEAN',
	DATETIME = 'DATETIME',
	EMBEDDING = 'EMBEDDING',
	OTHER = 'OTHER'
}
