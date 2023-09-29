export async function load({ params }) {
	return {
		compare: params.page === 'compare'
	};
}
