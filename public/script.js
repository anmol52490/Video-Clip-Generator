// public/script.js
document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generateBtn');
    const promptTextarea = document.getElementById('prompt');
    const resultContainer = document.getElementById('result-container');
    const btnText = document.querySelector('.btn-text');
    const spinner = document.querySelector('.spinner');

    // --- Theme Switcher Logic ---
    const themeToggle = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        if (currentTheme === 'dark') {
            themeToggle.checked = true;
        }
    } else {
        // Default to light theme
        document.documentElement.setAttribute('data-theme', 'light');
    }

    themeToggle.addEventListener('change', () => {
        if (themeToggle.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });

    // --- API Call Logic ---
    const generateVideo = async () => {
        const prompt = promptTextarea.value.trim();
        resultContainer.innerHTML = '';

        if (!prompt) {
            resultContainer.innerHTML = `<div class="error-message">Please enter a prompt.</div>`;
            return;
        }

        // Update UI to loading state
        generateBtn.disabled = true;
        btnText.textContent = 'Generating...';
        spinner.style.display = 'block';

        try {
            // IMPORTANT: Replace with your deployed backend URL
            const API_URL = '/api/generate-video'; // This works for Vercel deployment
            
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: prompt })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'An unknown server error occurred.');
            }
            
            const data = await response.json();
            
            if (data.video_base64) {
                const videoSrc = `data:video/mp4;base64,${data.video_base64}`;
                resultContainer.innerHTML = `<video controls autoplay loop src="${videoSrc}"></video>`;
            } else {
                throw new Error('No video data received from the server.');
            }

        } catch (error) {
            console.error('Error:', error);
            resultContainer.innerHTML = `<div class="error-message"><strong>Error:</strong> ${error.message}</div>`;
        } finally {
            // Revert UI from loading state
            generateBtn.disabled = false;
            btnText.textContent = 'Generate Video';
            spinner.style.display = 'none';
        }
    };

    generateBtn.addEventListener('click', generateVideo);
});
