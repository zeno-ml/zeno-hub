<script lang="ts">
	import Markdown from '$lib/components/general/Markdown.svelte';
	import purify from 'isomorphic-dompurify';
	import { parse } from 'marked';

	export let input: string;
	export let output = false;

	let renderedInput = purify.sanitize(parse(input));
</script>

<div class="my-1 flex justify-end items-end relative z-0">
	<div
		class="border border-grey-darker rounded m-0 p-2.5 relative self-start bg-background max-w-[70%]
		before:content-[''] before:-z-[1] before:h-6 before:bottom-0 before:absolute before:rounded-bl-2xl before:bg-grey-darker before:w-5 before:-right-2.5
		after:content-[''] after:-z-[1] after:h-6 after:bottom-0 after:absolute after:rounded-bl-xl after:bg-background after:w-2.5 after:-right-2.5 break-words"
	>
		<Markdown renderedText={renderedInput} />
	</div>
	<svg
		xmlns="http://www.w3.org/2000/svg"
		viewBox="0 0 448 512"
		class={`${output ? 'fill-primary' : 'fill-grey-darker'} w-3.5 ml-2.5 mt-2`}
	>
		<!-- Person Icon -->
		<path
			d="M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H418.3c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304H178.3z"
		/>
	</svg>
</div>
