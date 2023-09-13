<script lang="ts">
	import type { ReportElement } from '$lib/zenoapi';
	import purify from 'dompurify';
	import { parse } from 'marked';

	export let element: ReportElement;

	let renderedInput = element.data ? purify.sanitize(parse(element.data)) : '';
</script>

<div>
	{@html renderedInput}
</div>
