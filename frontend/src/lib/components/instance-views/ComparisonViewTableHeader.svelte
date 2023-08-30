<script lang="ts">
	import { compareSort, comparisonColumn } from '$lib/stores';
	import { Icon } from '@smui/button';

	export let header: string | undefined;
	export let sortModel: string;
</script>

<div style="display: flex; align-items:center;">
	<div>
		<div>{header ? header : 'difference'}</div>
		<div class="font-normal text-grey-dark">{$comparisonColumn?.name}</div>
	</div>
	{#if sortModel === header}
		<Icon class="material-icons" style="font-size: 25px; padding-top:3px;">
			{#if $compareSort[0] && $compareSort[1]}
				arrow_drop_up
			{:else if $compareSort[0]}
				arrow_drop_down
			{/if}
		</Icon>
	{/if}
</div>
