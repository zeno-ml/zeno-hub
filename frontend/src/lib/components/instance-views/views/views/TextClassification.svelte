<script lang="ts">
	// Objects with keys corresponding to the following props.
	export let entry: Record<string, string | number | boolean>;
	// Key for model outputs.
	export let modelColumn: string;

	$: textData = entry['data'] as string;
</script>

<div class="box">
	<span>{textData}</span>
	<br />
	<span class="label">label: </span><span class="value">
		{entry['label']}
	</span>
	{#if modelColumn && entry[modelColumn] !== undefined}
		<br />
		<span class="label">output: </span>
		<span class="value">{entry[modelColumn]} </span>
	{/if}
</div>

<style>
	.label {
		font-size: 12px;
		color: rgba(0, 0, 0, 0.5);
		font-variant: small-caps;
	}
	.value {
		font-size: 12px;
	}
	.box {
		padding: 10px;
		border: 0.5px solid rgb(224, 224, 224);
	}
</style>
