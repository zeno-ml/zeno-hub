<script lang="ts">
	import type { ReportElement } from '$lib/zenoapi';
	import purify from 'isomorphic-dompurify';
	import { parse } from 'marked';

	export let element: ReportElement;

	let renderedInput = element.data ? purify.sanitize(parse(element.data)) : '';
</script>

<article class="prose">
	<!-- eslint-disable-next-line svelte/no-at-html-tags -->
	{@html renderedInput}
</article>
