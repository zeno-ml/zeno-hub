import type { ChartConfig } from '$lib/zenoapi';

export function getConfig(chartConfig: ChartConfig) {
	return {
		axis: { labelFontSize: chartConfig.fontSize, titleFontSize: chartConfig.fontSize },
		legend: { labelFontSize: chartConfig.fontSize, titleFontSize: chartConfig.fontSize },
		header: { labelFontSize: chartConfig.fontSize, titleFontSize: chartConfig.fontSize },
		mark: { fontSize: 14 },
		title: { fontSize: chartConfig.fontSize, subtitleFontSize: chartConfig.fontSize },
		text: { fontSize: chartConfig.fontSize }
	};
}
