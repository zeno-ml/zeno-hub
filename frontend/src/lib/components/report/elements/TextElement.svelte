<script lang="ts">
	import Markdown from '$lib/components/general/Markdown.svelte';
	import type { ReportElement } from '$lib/zenoapi';
	import purify from 'isomorphic-dompurify';
	import { parse } from 'marked';

	export let element: ReportElement;

	$: renderedInput = element.data ? purify.sanitize(parse(element.data) as string) : '';
</script>

<article class="w-full overflow-hidden break-words">
	<Markdown renderedText={renderedInput} />
</article>
