// reasoning_patch.js - Load and display ULTIMAI reasoning results

// Function to load the reasoning result
async function loadReasoningResult() {
  const outputElement = document.getElementById('output');
  
  try {
    // Attempt to fetch the generated reasoning file
    const response = await fetch('REASONING_RESULT.md');
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const text = await response.text();
    
    // Display the content
    outputElement.textContent = text;
    
  } catch (error) {
    console.error('Failed to load reasoning result:', error);
    outputElement.textContent = `❌ Ошибка загрузки reasoning файла.\n\nФайл REASONING_RESULT.md не найден или еще не сгенерирован.\nЗапустите automate_process.py для генерации нового reasoning patch.\n\nError: ${error.message}`;
  }
}

// Load the reasoning result when the page loads
loadReasoningResult();
