import { tooltipState } from '$lib/stores';

export function tooltip(node: HTMLElement, params: { text: string }) {
	function handleFocus(e: MouseEvent) {
		tooltipState.set({ hover: true, mousePos: { x: e.clientX, y: e.clientY }, text: params.text });

		node.addEventListener('mouseleave', handleBlur);
		node.addEventListener('mousemove', handleMove);
		node.removeEventListener('mouseenter', handleFocus);
	}

	function handleMove(e: MouseEvent) {
		tooltipState.set({ hover: true, mousePos: { x: e.clientX, y: e.clientY }, text: params.text });
	}

	function handleBlur() {
		tooltipState.set({ hover: false, mousePos: { x: 0, y: 0 }, text: undefined });

		node.removeEventListener('mouseleave', handleBlur);
		node.removeEventListener('mousemove', handleMove);
		node.addEventListener('mouseenter', handleFocus);
	}

	node.addEventListener('mouseenter', handleFocus);

	return {
		destroy() {
			node.removeEventListener('mouseenter', handleFocus);
		}
	};
}
