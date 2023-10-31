<script lang="ts">
	import type { Project, ProjectStats, Report, ReportStats, User } from '$lib/zenoapi';
	import ProjectComponent from '../project/Project.svelte';
	import ReportComponent from '../report/Report.svelte';

	export let entry: Project | Report;
	export let stats: ProjectStats | ReportStats;
	export let user: User | null;

	let project: Project;
	let projectStats: ProjectStats;

	let report: Report;
	let reportStats: ReportStats;

	if ('uuid' in entry) {
		project = entry as unknown as Project;
		projectStats = stats as unknown as ProjectStats;
	} else {
		report = entry as unknown as Report;
		reportStats = stats as unknown as ReportStats;
	}
</script>

{#if 'uuid' in entry}
	<ProjectComponent {project} stats={projectStats} {user} />
{:else}
	<ReportComponent {report} stats={reportStats} {user} />
{/if}
