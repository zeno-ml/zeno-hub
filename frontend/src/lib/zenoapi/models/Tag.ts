/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Specification of the tag type in Zeno.
 *
 * Attributes:
 * id (int): The id of the tag.
 * tag_name (str): The name of the tag.
 * data_ids (list[str]): The ids of the data belonging to the tag.
 * folder_id (Optiona[int]): The id of the folder the tag belongs to. Default None.
 *
 */
export type Tag = {
	id: number;
	tagName: string;
	dataIds: Array<string>;
	folderId?: number | null;
};
