import type { ComponentType } from 'svelte';

import { ViewType } from '$lib/instance-views/schema.js';
import Audio from './elements/Audio.svelte';
import Code from './elements/Code.svelte';
import Image from './elements/Image.svelte';
import List from './elements/List.svelte';
import Markdown from './elements/Markdown.svelte';
import Message from './elements/Message.svelte';
import SeparatedValues from './elements/SeparatedValues.svelte';
import Text from './elements/Text.svelte';
import VStack from './elements/VStack.svelte';

export const elementMap: Record<string, ComponentType> = {
	[ViewType.text]: Text,
	[ViewType.vstack]: VStack,
	[ViewType.list]: List,
	[ViewType.markdown]: Markdown,
	[ViewType.image]: Image,
	[ViewType.audio]: Audio,
	[ViewType.code]: Code,
	[ViewType.message]: Message,
	[ViewType.separatedValues]: SeparatedValues
};

export function isComplexElement(type: string) {
	return ['vstack', 'list', 'image', 'audio', 'code', 'message'].includes(type);
}
