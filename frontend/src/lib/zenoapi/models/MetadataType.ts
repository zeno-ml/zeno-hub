/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Enumeration of possible metadata types in Zeno.
 *
 * Attributes:
 * NOMINAL: Nominal metadata type, e.g. string or small cardinality number.
 * CONTINUOUS: Continuous metadata type, e.g. large cardinality number.
 * BOOLEAN: Boolean metadata type, e.g. True or False.
 * DATETIME: Datetime metadata type, e.g. 2021-01-01 00:00:00.
 * OTHER: Any other metadata type, e.g. strings.
 */
export enum MetadataType {
	NOMINAL = 'NOMINAL',
	CONTINUOUS = 'CONTINUOUS',
	BOOLEAN = 'BOOLEAN',
	DATETIME = 'DATETIME',
	OTHER = 'OTHER'
}
