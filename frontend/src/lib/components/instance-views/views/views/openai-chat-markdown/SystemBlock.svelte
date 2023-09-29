<script lang="ts">
	import Markdown from '$lib/components/general/Markdown.svelte';
	import purify from 'isomorphic-dompurify';
	import { parse } from 'marked';

	export let input: string;

	let renderedInput = purify.sanitize(parse(input));
</script>

<p class="m-0">
	<b>System:</b>
	<span>
		<Markdown renderedText={renderedInput} />
	</span>
</p>
