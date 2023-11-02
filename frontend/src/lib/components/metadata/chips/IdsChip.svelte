<script lang="ts">
	import { TrailingIcon } from '@smui/chips';

	import { selectionIds } from '$lib/stores';
</script>

<div class="my width-fit mx-1 rounded border border-grey-lighter px-2.5 py-1">
	<span>Scatter Selection</span>
	<TrailingIcon class="remove material-icons" on:click={() => selectionIds.set([])}>
		cancel
	</TrailingIcon>
</div>
