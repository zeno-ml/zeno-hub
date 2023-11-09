<script lang="ts">
	import purify from 'isomorphic-dompurify';
	import { parse } from 'marked';

	export let data: string;

	const renderedText = purify.sanitize(parse(data));
</script>

<article class="[&_a]:break-word prose max-w-none [&_p]:whitespace-pre-wrap">
	<!-- eslint-disable-next-line svelte/no-at-html-tags -->
	{@html renderedText}
</article>
