import { tooltipState } from '$lib/stores';

export function tooltip(node: HTMLElement, params: { text: string }) {
	const handleFocus = function (e: MouseEvent) {
		tooltipState.set({
			hover: true,
			mousePos: { x: e.clientX, y: e.clientY },
			text: params.text
		});
		node.addEventListener('mouseleave', handleBlur);
		node.addEventListener('mousemove', handleMove);
	};

	const handleMove = function (e: MouseEvent) {
		tooltipState.set({
			hover: true,
			mousePos: { x: e.clientX, y: e.clientY },
			text: params.text
		});
	};

	const handleBlur = function () {
		node.removeEventListener('mouseleave', handleBlur);
		node.removeEventListener('mousemove', handleMove);
		tooltipState.set({ hover: false, mousePos: { x: 0, y: 0 }, text: undefined });
	};

	node.addEventListener('mouseenter', handleFocus);

	return {
		update(newParams: { text: string }) {
			params = newParams;
		},
		destroy() {
			node.removeEventListener('mouseenter', handleFocus);
		}
	};
}
