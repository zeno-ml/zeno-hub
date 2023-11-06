<script lang="ts">
	import { browser } from '$app/environment';
	import { page } from '$app/stores';
	import type { Report } from '$lib/zenoapi';
	import { Icon } from '@smui/button';
	import Paper, { Content } from '@smui/paper';

	export let showShare = false;
	export let container: HTMLDivElement;
	export let report: Report;
	export let printMode: boolean = false;

	async function toPDF() {
		var opt = {
			margin: 10,
			filename: `${report.name}.pdf`,
			image: { type: 'jpeg', quality: 1 },
			pagebreak: { mode: 'avoid-all' },
			html2canvas: {
				dpi: 192,
				scale: 4,
				letterRendering: true,
				useCORS: true
			},
			jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
		};
		if (browser) {
			const pdf = await import('html2pdf.js');
			printMode = true;
			await pdf.default(container, opt);
			printMode = false;
		}
	}
</script>

<div class="absolute right-0 top-0 z-30 mt-9 hover:bg-grey-lighter">
	<Paper style="padding: 3px 0px;" elevation={7}>
		<Content>
			<button
				class="py flex w-32 items-center px-2 hover:bg-grey-lighter"
				on:click={(e) => {
					e.stopPropagation();
					showShare = false;
					toPDF();
				}}
			>
				<Icon style="font-size: 18px;" class="material-icons">picture_as_pdf</Icon>&nbsp;
				<span class="text-xs">Export PDF</span>
			</button>
			<button
				class="py flex w-32 items-center px-2 hover:bg-grey-lighter"
				on:click={(e) => {
					e.stopPropagation();
					navigator.clipboard.writeText($page.url.href);
					showShare = false;
				}}
			>
				<Icon style="font-size: 18px;" class="material-icons">content_copy</Icon>&nbsp;
				<span class="text-xs">Copy URL</span>
			</button>
		</Content>
	</Paper>
</div>
