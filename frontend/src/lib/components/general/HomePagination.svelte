<script lang="ts">
	import { Pagination } from '@smui/data-table';
	import IconButton from '@smui/icon-button';

	export let ENTRIES_PER_PAGE = 6;
	export let currentPage = 0;
	export let totalEntries: number;

	let lastPage = Math.floor(totalEntries / ENTRIES_PER_PAGE);
</script>

<Pagination slot="paginate" class="pagination">
	<svelte:fragment slot="total">
		{Math.min(currentPage * ENTRIES_PER_PAGE + 1, totalEntries)} - {Math.min(
			(currentPage + 1) * ENTRIES_PER_PAGE,
			totalEntries
		)} of {totalEntries}
	</svelte:fragment>

	<IconButton
		class="material-icons"
		action="first-page"
		title="First page"
		on:click={() => (currentPage = 0)}
		disabled={currentPage === 0}>first_page</IconButton
	>
	<IconButton
		class="material-icons"
		action="prev-page"
		title="Prev page"
		on:click={() => currentPage--}
		disabled={currentPage === 0}>chevron_left</IconButton
	>
	<IconButton
		class="material-icons"
		action="next-page"
		title="Next page"
		on:click={() => currentPage++}
		disabled={currentPage >= lastPage}>chevron_right</IconButton
	>
	<IconButton
		class="material-icons"
		action="last-page"
		title="Last page"
		on:click={() => (currentPage = lastPage)}
		disabled={currentPage >= lastPage}>last_page</IconButton
	>
</Pagination>
