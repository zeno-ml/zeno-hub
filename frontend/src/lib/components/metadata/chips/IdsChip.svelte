<script lang="ts">
	import { TrailingIcon } from '@smui/chips';

	import { selectionIds } from '$lib/stores';
</script>

<div class="py-1 px-2.5 border border-grey-lighter my mx-1 rounded width-fit">
	<span>Scatter Selection</span>
	<TrailingIcon class="remove material-icons" on:click={() => selectionIds.set([])}>
		cancel
	</TrailingIcon>
</div>
