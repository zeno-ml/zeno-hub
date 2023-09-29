<script lang="ts">
	import { resolveDataPoint } from '$lib/util/util';
	import CircularProgress from '@smui/circular-progress';

	export let entry: Record<string, number | string | boolean | { role: string; content: string }[]>;
	export let modelColumn: string;

	// Split each column by newlines then spaces.
	$: fetchData = (async () => {
		let response = await resolveDataPoint(entry);
		if (response instanceof Response) {
			response = await response.text();
		}
		return response.split('\n').map((x) => x.split(' '));
	})();
	$: labelEntries = (entry['label'] + '').split('\n').map((x) => x.split(' '));
	$: modelEntries = (entry[modelColumn] + '').split('\n').map((x) => x.split(' '));
</script>

{#await fetchData}
	<CircularProgress style="height: 32px; width: 32px; margin-right:20px" indeterminate />
{:then data}
	<table id="example_table">
		<tbody>
			{#each data as entry}
				<tr>
					<th>Data: </th>
					{#each entry as cell}
						<td>{cell}</td>
					{/each}
				</tr>
			{/each}
			{#each labelEntries as entry}
				<tr class="label">
					<th>Label: </th>
					{#each entry as cell}
						<td>{cell}</td>
					{/each}
				</tr>
			{/each}
			{#if modelColumn}
				{#each modelEntries as entry}
					<tr>
						<th>Output: </th>
						{#each entry as cell}
							<td>{cell}</td>
						{/each}
					</tr>
				{/each}
			{/if}
		</tbody>
	</table>
{/await}

<style>
	#example_table {
		margin: 2.5px;
		border: 1px solid rgb(224, 224, 224);
		min-width: 350px;
		font-family: Arial, Helvetica, sans-serif;
		border-collapse: collapse;
		width: 100%;
	}

	#example_table td,
	#example_table th {
		border: 1px solid #ddd;
		padding: 8px;
	}

	#example_table tr.label {
		background-color: #f2f2f2;
	}
</style>
