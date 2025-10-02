document.addEventListener('DOMContentLoaded', () => {
	const outputElement = document.getElementById('output');
	if (!outputElement) {
		return;
	}

	fetch('REASONING_RESULT.md', { cache: 'no-store' })
		.then(async (response) => {
			if (!response.ok) {
				throw new Error(`Failed to load REASONING_RESULT.md: ${response.status}`);
			}
			return await response.text();
		})
		.then((text) => {
			outputElement.textContent = text;
		})
		.catch((error) => {
			outputElement.textContent = `Ошибка загрузки reasoning: ${error.message}`;
		});
});

