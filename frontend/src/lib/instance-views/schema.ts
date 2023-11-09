export enum ViewType {
	// direct data renderers
	'text' = 'text',
	'image' = 'image',
	'audio' = 'audio',
	'code' = 'code',
	'markdown' = 'markdown',
	// data containers
	'list' = 'list',
	'vstack' = 'vstack',
	'message' = 'message',
	'separatedValues' = 'separatedValues'
}

export enum DisplayType {
	'table' = 'table'
}

export type ViewUnion =
	| View
	| TextView
	| ImageView
	| ListView
	| MessageView
	| VStackView
	| SeparatedValuesView;

export interface View {
	type: ViewType;
}

export interface TextView extends View {
	type: ViewType.text;
	label?: string;
}

export interface ImageView extends View {
	type: ViewType.image;
	maxWidth?: 'small' | 'medium' | 'large' | 'full';
}

export interface ListView extends View {
	type: ViewType.list;
	elements: ViewUnion;
	horizontal?: boolean;
	collapsible?: string;
	border?: boolean;
	pad?: boolean;
}

export interface MessageView extends View {
	type: ViewType.message;
	content: ViewUnion;
	plain?: boolean;
	role?: string;
	ownMessage?: boolean;
	highlight?: boolean;
}

export interface VStackView extends View {
	type: ViewType.vstack;
	keys: Record<string, ViewUnion>;
	collapsible?: string;
	border?: boolean;
	pad?: boolean;
}

export interface SeparatedValuesView extends View {
	type: ViewType.separatedValues;
	header?: string;
	separator?: string;
	highlight?: boolean;
}

export interface ViewSchema {
	data: ViewUnion;
	label: ViewUnion;
	output: ViewUnion;
	displayType?: DisplayType;
}
