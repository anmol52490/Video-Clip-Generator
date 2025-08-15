# AI Video Forge (Render Edition) 🎬

A minimal but powerful web application that generates short, animated videos from a text prompt using AI. This project uses a FastAPI backend to run the `stabilityai/sd-turbo` model and a modern HTML/CSS/JavaScript frontend. It is configured for deployment on Render to support the large model size.

**Live Demo URL:** [Your Deployed Render Frontend URL Here]

## Features

-   **Text-to-Video Generation**: Uses the high-quality `sd-turbo` model.
-   **Persistent Model Caching**: Downloads the large AI model only once on Render's persistent disk, ensuring fast startups after the first launch.
-   **Aesthetic UI**: Clean, modern interface with a light/dark theme switcher.
-   **Deployment Ready**: Decomposed into separate frontend and backend services, configured for one-click deployment on Render.

## Tech Stack

-   **Backend**: Python, FastAPI, Gunicorn
-   **AI Model**: `stabilityai/sd-turbo` via Hugging Face Diffusers
-   **Video Processing**: Imageio, OpenCV
-   **Frontend**: HTML, CSS, JavaScript
-   **Deployment**: Render

## Project Structure


/
|-- /backend
|   |-- app.py
|   |-- requirements.txt
|   |-- start.sh
|-- /frontend
|   |-- index.html
|   |-- style.css
|   |-- script.js
|-- render.yaml
|-- README.md


## Deployment to Render (Step-by-Step)

This project is configured for a "Blueprint" deployment on Render.

### 1. Push to GitHub
Create a new repository on GitHub and push all the files in the structure above.

### 2. Create a New Blueprint on Render
-   Log in to your Render account.
-   Go to the "Blueprints" section and click **New Blueprint**.
-   Connect the GitHub repository you just created. Render will automatically detect and read your `render.yaml` file.

### 3. Configure the Services
-   Render will show you the two services it found in the `render.yaml` file: `ai-video-frontend` and `ai-video-backend`.
-   You do not need to change any settings. Just click **Apply**.

### 4. Wait for the First Deploy
-   The first deployment of the `ai-video-backend` service will take a long time (10-20 minutes). This is because it is downloading the 1.2 GB `sd-turbo` model and saving it to your new persistent disk. **This only happens once.**
-   You can watch the logs for the service to see the download progress.

### 5. Connect Frontend to Backend
-   Once both services are deployed, go to the settings for your `ai-video-backend` service on Render. Copy its public URL (it will look like `https://ai-video-backend-xxxx.onrender.com`).
-   Now, go to your local project code and open `frontend/script.js`.
-   Replace the placeholder `YOUR_RENDER_BACKEND_URL` with the URL you just copied.
    ```javascript
    // frontend/script.js
    const API_URL = '[https://ai-video-backend-xxxx.onrender.com/generate-video](https://ai-video-backend-xxxx.onrender.com/generate-video)'; 
    ```
-   Commit and push this change to your GitHub repository. Render will automatically detect the change and redeploy your frontend service very quickly.

### 6. Test Your Live App
-   Go to the public URL for your `ai-video-frontend` service.
-   The first time you generate a video, it will have a "cold start" and may take up to a minute to respond as the server wakes up and loads the model into memory. Subsequent requests will be much faster.
-   Congratulations, your application is live!

