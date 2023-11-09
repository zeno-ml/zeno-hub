import { browser } from '$app/environment';

export type URLParams = {
	sample: string | undefined;
};

export function setURLParameters(sample: string | undefined) {
	if (!browser) return;
	const params = {
		sample
	} as URLParams;
	window.history.replaceState(history.state, '', `?params=${btoa(JSON.stringify(params))}`);
}
