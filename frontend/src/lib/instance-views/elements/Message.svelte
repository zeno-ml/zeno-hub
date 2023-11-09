<script lang="ts">
	import { elementMap } from '$lib/instance-views/resolve.js';
	import type { MessageView } from '$lib/instance-views/schema.js';
	import Error from '../Error.svelte';

	export let data: string;
	export let spec: MessageView;

	const type = elementMap[spec.content.type as string];

	let role: string | undefined = undefined;
	let content = '';
	let ownMessage = false;
	let errorMessage: string | undefined = undefined;

	if (spec.plain) {
		ownMessage = spec.ownMessage === undefined ? role === 'user' : spec.ownMessage;
		content = data;
	} else {
		try {
			const jsonData = JSON.parse(data);
			role = jsonData['role'];
			ownMessage =
				jsonData['ownMessage'] === undefined ? role === 'user' : jsonData['ownMessage'] === true;
			content = jsonData['content'];
			if (typeof content === 'object') content = JSON.stringify(content);
			errorMessage = undefined;
		} catch (error) {
			errorMessage = error as string;
		}
	}

	const iconPath = role === undefined ? undefined : getIcon(role);

	function getIcon(role: string): string | undefined {
		switch (role) {
			case 'user':
				// Person Icon
				return 'M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H418.3c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304H178.3z';
			case 'assistant':
				// Robot Icon
				return 'M320 0c17.7 0 32 14.3 32 32V96H472c39.8 0 72 32.2 72 72V440c0 39.8-32.2 72-72 72H168c-39.8 0-72-32.2-72-72V168c0-39.8 32.2-72 72-72H288V32c0-17.7 14.3-32 32-32zM208 384c-8.8 0-16 7.2-16 16s7.2 16 16 16h32c8.8 0 16-7.2 16-16s-7.2-16-16-16H208zm96 0c-8.8 0-16 7.2-16 16s7.2 16 16 16h32c8.8 0 16-7.2 16-16s-7.2-16-16-16H304zm96 0c-8.8 0-16 7.2-16 16s7.2 16 16 16h32c8.8 0 16-7.2 16-16s-7.2-16-16-16H400zM264 256a40 40 0 1 0 -80 0 40 40 0 1 0 80 0zm152 40a40 40 0 1 0 0-80 40 40 0 1 0 0 80zM48 224H64V416H48c-26.5 0-48-21.5-48-48V272c0-26.5 21.5-48 48-48zm544 0c26.5 0 48 21.5 48 48v96c0 26.5-21.5 48-48 48H576V224h16z';
			default:
				return undefined;
		}
	}
</script>

{#if errorMessage !== undefined}
	<Error type="Incorrect Data" message={errorMessage} />
{:else if role === 'system'}
	<p class="m-0">
		<b>System:</b>
		<svelte:component this={type} spec={spec.content} data={content} />
	</p>
{:else if ownMessage}
	<div class="relative my-1 flex items-end justify-end">
		<p
			class="relative m-0 max-w-[70%] self-start rounded border border-grey-darker bg-background p-2.5 before:absolute before:-right-2.5 before:bottom-0 before:-z-[1] before:h-6 before:w-5 before:rounded-bl-2xl before:bg-grey-darker before:content-[''] after:absolute after:-right-2.5 after:bottom-0 after:-z-[1] after:h-6 after:w-2.5 after:rounded-bl-xl after:bg-background after:content-[''] {spec.highlight
				? 'border border-primary before:bg-primary'
				: 'border border-grey-darker'}"
		>
			<svelte:component this={type} spec={spec.content} data={content} />
		</p>
		{#if iconPath !== undefined}
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 448 512"
				class="ml-2.5 mt-2 w-3.5 {spec.highlight ? 'fill-primary' : 'fill-grey-darker'}"
			>
				<path d={iconPath} />
			</svg>
		{:else if role !== undefined}
			{role}
		{/if}
	</div>
{:else}
	<div class="relative my-1 flex items-end">
		{#if iconPath !== undefined}
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 640 512"
				class={`${spec.highlight ? 'fill-primary' : 'fill-grey-darker'} mr-2.5 mt-2 w-6`}
			>
				<path d={iconPath} />
			</svg>
		{:else if role !== undefined}
			{role}
		{/if}
		<p
			class="relative m-0 max-w-[70%] self-start rounded bg-background p-2.5 before:absolute before:-left-2.5 before:bottom-0 before:-z-[1] before:h-6 before:w-5 before:rounded-br-2xl before:bg-grey-darker before:content-[''] after:absolute after:-left-2.5 after:bottom-0 after:-z-[1] after:h-6 after:w-2.5 after:rounded-br-xl after:bg-background after:content-[''] {spec.highlight
				? 'border border-primary before:bg-primary'
				: 'border border-grey-darker'}"
		>
			<svelte:component this={type} spec={spec.content} data={content} />
		</p>
	</div>
{/if}
