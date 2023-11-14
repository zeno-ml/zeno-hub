/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Specification of the tag type in Zeno.
 *
 * Attributes:
 * id (int): id of the tag.
 * tag_name (str): name of the tag.
 * data_ids (list[str]): ids of the data belonging to the tag.
 * folder_id (Optiona[int]): id of the folder the tag belongs to. Default None.
 * project_uuid (Optional[str]): uuid of the project the tag belongs to.
 */
export type Tag = {
	id: number;
	tagName: string;
	dataIds: Array<string>;
	folderId?: number | null;
	projectUuid?: string | null;
};
