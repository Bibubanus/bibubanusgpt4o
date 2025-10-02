document.addEventListener('DOMContentLoaded', async () => {
	const outputElement = document.getElementById('output');
	try {
		const response = await fetch('REASONING_RESULT.md', { cache: 'no-store' });
		if (!response.ok) {
			throw new Error(`HTTP ${response.status}`);
		}
		const text = (await response.text()).trim();
		outputElement.textContent = text || '[Файл REASONING_RESULT.md пуст]';
	} catch (error) {
		outputElement.textContent = `Не удалось загрузить REASONING_RESULT.md: ${error.message}`;
	}
});

