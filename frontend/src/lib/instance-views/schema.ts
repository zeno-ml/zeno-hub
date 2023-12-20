export enum ViewType {
	// direct data renderers
	'text' = 'text',
	'image' = 'image',
	'audio' = 'audio',
	'code' = 'code',
	'markdown' = 'markdown',
	'3D' = '3D',
	// data containers
	'list' = 'list',
	'vstack' = 'vstack',
	'message' = 'message',
	'separatedValues' = 'separatedValues'
}

export enum DisplayType {
	'table' = 'table'
}

export type ViewUnion = View | Text | Image | List | Message | VStack | SeparatedValues;

export interface View {
	type: ViewType;
}

export interface Text extends View {
	type: ViewType.text;
	label?: string;
}

export interface Image extends View {
	type: ViewType.image;
	maxWidth?: 'small' | 'medium' | 'large' | 'full';
}

export interface List extends View {
	type: ViewType.list;
	elements: ViewUnion;
	horizontal?: boolean;
	collapsible?: string;
	border?: boolean;
	pad?: boolean;
}

export interface Message extends View {
	type: ViewType.message;
	content: ViewUnion;
	plain?: boolean;
	role?: string;
	ownMessage?: boolean;
	highlight?: boolean;
}

export interface VStack extends View {
	type: ViewType.vstack;
	keys: Record<string, ViewUnion>;
	collapsible?: string;
	border?: boolean;
	pad?: boolean;
}

export interface SeparatedValues extends View {
	type: ViewType.separatedValues;
	header?: string;
	separator?: string;
	highlight?: boolean;
}

export interface ViewSchema {
	data?: ViewUnion;
	label?: ViewUnion;
	output?: ViewUnion;
	displayType?: DisplayType;
	size?: 'medium' | 'large';
}
