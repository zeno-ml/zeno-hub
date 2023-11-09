<script lang="ts">
	export let type: string;
	export let message: string | undefined;
</script>

<div class="flex flex-col overflow-auto text-red">
	<span class="font-bold">{type}</span>
	{#if message}
		<pre>
{message}
		</pre>
	{/if}
</div>
