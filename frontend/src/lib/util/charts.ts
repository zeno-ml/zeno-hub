import BarChart from '$lib/components/chart/chart-types/bar-chart/BarChart.svelte';
import BeeswarmChart from '$lib/components/chart/chart-types/beeswarm-chart/BeeswarmChart.svelte';
import HeatMap from '$lib/components/chart/chart-types/heatmap-chart/HeatMap.svelte';
import LineChart from '$lib/components/chart/chart-types/line-chart/LineChart.svelte';
import RadarChart from '$lib/components/chart/chart-types/radar-chart/RadarChart.svelte';
import Table from '$lib/components/chart/chart-types/table/Table.svelte';
import { metrics, models } from '$lib/stores';
import {
	ChartType,
	SlicesMetricsOrModels,
	SlicesOrModels,
	type BeeswarmParameters,
	type Chart,
	type HeatmapParameters,
	type RadarParameters,
	type TableParameters,
	type XCParameters
} from '$lib/zenoapi';
import type { ComponentType } from 'svelte';
import { get } from 'svelte/store';

export function chartDefaults(
	name: string,
	id: number,
	project_uuid: string,
	type: ChartType
): Chart {
	switch (type) {
		case ChartType.BAR:
		case ChartType.LINE:
			return {
				id: id,
				name: name,
				type: type,
				projectUuid: project_uuid,
				parameters: <XCParameters>{
					slices: [-1],
					metric: -1,
					models: get(models),
					xChannel: SlicesOrModels.SLICES,
					colorChannel: SlicesOrModels.MODELS
				}
			};
		case ChartType.TABLE:
			return {
				id: id,
				name: name,
				projectUuid: project_uuid,
				type: ChartType.TABLE,
				parameters: <TableParameters>{
					models: get(models),
					slices: [-1],
					metrics: [-1],
					xChannel: SlicesMetricsOrModels.MODELS,
					yChannel: SlicesOrModels.SLICES,
					fixedChannel: SlicesMetricsOrModels.METRICS
				}
			};
		case ChartType.BEESWARM:
			return {
				id: id,
				name: name,
				projectUuid: project_uuid,
				type: ChartType.BEESWARM,
				parameters: <BeeswarmParameters>{
					models: [get(models)[0]],
					slices: [-1],
					metrics: get(metrics).map((m) => m.id),
					yChannel: SlicesOrModels.MODELS,
					colorChannel: SlicesOrModels.SLICES,
					fixedDimension: 'y'
				}
			};
		case ChartType.RADAR:
			return {
				id: id,
				name: name,
				projectUuid: project_uuid,
				type: ChartType.RADAR,
				parameters: <RadarParameters>{
					models: [get(models)[0]],
					slices: [-1],
					metrics: [...get(metrics).map((m) => m.id), -1],
					axisChannel: SlicesMetricsOrModels.METRICS,
					fixedChannel: SlicesMetricsOrModels.MODELS,
					layerChannel: SlicesOrModels.SLICES
				}
			};
		case ChartType.HEATMAP:
			return {
				id: id,
				name: name,
				projectUuid: project_uuid,
				type: ChartType.HEATMAP,
				parameters: <HeatmapParameters>{
					xValues: [-1],
					yValues: get(models),
					metric: -1,
					model: get(models)[0],
					xChannel: SlicesOrModels.SLICES,
					yChannel: SlicesOrModels.MODELS
				}
			};
	}
}

export const chartMap: Record<string, ComponentType> = {
	[ChartType.BAR]: BarChart,
	[ChartType.LINE]: LineChart,
	[ChartType.TABLE]: Table,
	[ChartType.BEESWARM]: BeeswarmChart,
	[ChartType.RADAR]: RadarChart,
	[ChartType.HEATMAP]: HeatMap
};
