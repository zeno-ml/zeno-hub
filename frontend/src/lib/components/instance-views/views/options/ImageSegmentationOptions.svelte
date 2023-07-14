<script lang="ts">
	import Button, { Group } from '@smui/button';

	export let options: Record<string, unknown>;

	let choices = ['Label', 'Model'];
	let selected = ['Label'];

	$: options = { mask: selected };
</script>

<div>
	<Group>
		{#each choices as choice}
			<Button
				variant={selected.includes(choice) ? 'raised' : 'outlined'}
				on:click={() => {
					if (selected.includes(choice)) {
						selected = selected.filter((c) => c !== choice);
					} else {
						selected = [...selected, choice];
					}
				}}>{choice}</Button
			>
		{/each}
	</Group>
</div>
