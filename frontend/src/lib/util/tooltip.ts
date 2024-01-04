import { tooltipState } from '$lib/stores';

export function tooltip(node: HTMLElement, params: { text: string }) {
	let isHovering = false;

	const handleFocus = function (e: MouseEvent) {
		isHovering = true;
		tooltipState.set({
			hover: true,
			mousePos: { x: e.clientX, y: e.clientY },
			text: params.text
		});
	};

	const handleMove = function (e: MouseEvent) {
		if (!isHovering) return;
		tooltipState.set({
			hover: true,
			mousePos: { x: e.clientX, y: e.clientY },
			text: params.text
		});
	};

	const handleBlur = function () {
		isHovering = false;
		tooltipState.set({ hover: false, mousePos: { x: 0, y: 0 }, text: undefined });
	};

	node.addEventListener('mouseenter', handleFocus);
	node.addEventListener('mouseleave', handleBlur);
	node.addEventListener('mousemove', handleMove);

	return {
		update(newParams: { text: string }) {
			params = newParams;
		},
		destroy() {
			node.removeEventListener('mouseenter', handleFocus);
			node.removeEventListener('mouseleave', handleBlur);
			node.removeEventListener('mousemove', handleMove);
		}
	};
}
