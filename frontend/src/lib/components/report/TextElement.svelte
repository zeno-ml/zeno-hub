<script lang="ts">
	import type { ReportElement } from '$lib/zenoapi';
	import purify from 'isomorphic-dompurify';
	import { parse } from 'marked';

	export let element: ReportElement;

	let renderedInput = element.data ? purify.sanitize(parse(element.data)) : '';
</script>

<div class="flex flex-wrap [&>p]:text-base w-full">
	<!-- eslint-disable-next-line svelte/no-at-html-tags -->
	{@html renderedInput}
</div>
