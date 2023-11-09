<script lang="ts">
	import { HighlightAuto } from 'svelte-highlight';
	import github from 'svelte-highlight/styles/github';

	export let data: string;
</script>

<svelte:head>
	<!-- eslint-disable -->
	{@html github}
</svelte:head>

<HighlightAuto code={data} />
