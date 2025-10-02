// reasoning_patch.js - ULTIMAI Reasoning Display Module

document.addEventListener('DOMContentLoaded', function() {
    const outputElement = document.getElementById('output');
    
    // Function to load reasoning result
    async function loadReasoningResult() {
        try {
            // Try to fetch the generated reasoning result
            const response = await fetch('REASONING_RESULT.md');
            
            if (response.ok) {
                const reasoningText = await response.text();
                outputElement.textContent = reasoningText;
            } else {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
        } catch (error) {
            console.error('Failed to load reasoning result:', error);
            outputElement.innerHTML = `
                <span style="color: #ff6b6b;">
                    ❌ Не удалось загрузить результат reasoning.<br>
                    Возможные причины:<br>
                    • Файл REASONING_RESULT.md не найден<br>
                    • Скрипт automate_process.py еще не выполнен<br>
                    • Проблемы с сетью или сервером<br><br>
                    Ошибка: ${error.message}
                </span>
            `;
        }
    }
    
    // Auto-refresh every 30 seconds to check for updates
    function startAutoRefresh() {
        setInterval(loadReasoningResult, 30000);
    }
    
    // Initial load
    loadReasoningResult();
    
    // Start auto-refresh
    startAutoRefresh();
    
    // Add manual refresh button
    const refreshButton = document.createElement('button');
    refreshButton.textContent = '🔄 Обновить';
    refreshButton.style.cssText = `
        background: #b3e14b;
        color: #191f23;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-family: monospace;
        font-weight: bold;
        cursor: pointer;
        margin-top: 20px;
    `;
    refreshButton.onclick = loadReasoningResult;
    
    document.body.appendChild(refreshButton);
});