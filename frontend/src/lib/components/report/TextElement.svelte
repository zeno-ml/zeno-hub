<script lang="ts">
	import type { ReportElement } from '$lib/zenoapi';
	import purify from 'isomorphic-dompurify';
	import { parse } from 'marked';
	import Markdown from '../general/Markdown.svelte';

	export let element: ReportElement;

	let renderedInput = element.data ? purify.sanitize(parse(element.data)) : '';
</script>

<article class="max-w-3xl">
	<Markdown renderedText={renderedInput} />
</article>
