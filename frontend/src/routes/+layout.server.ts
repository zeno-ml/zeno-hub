export const load = async ({ cookies }) => {
	const featureCookie = cookies.get('featureFlags');
	let features: Record<string, boolean> = {};
	if (featureCookie) {
		features = JSON.parse(featureCookie) as Record<string, boolean>;
	}
	return {
		features: features
	};
};
