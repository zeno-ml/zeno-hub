<script lang="ts">
	import Markdown from '$lib/components/general/Markdown.svelte';
	import type { ReportElement } from '$lib/zenoapi';
	import purify from 'isomorphic-dompurify';
	import { parse } from 'marked';

	export let element: ReportElement;

	let renderedInput = element.data ? purify.sanitize(parse(element.data)) : '';
</script>

<article class="max-w-3xl">
	<Markdown renderedText={renderedInput} />
</article>
