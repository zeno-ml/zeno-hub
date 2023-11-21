export function inViewport(e: HTMLElement, callback: () => void) {
	const observer = new IntersectionObserver((entries) => {
		if (entries[0].isIntersecting) {
			callback();
		}
	});

	observer.observe(e);
}
