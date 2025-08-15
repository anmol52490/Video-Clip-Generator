# AI Video Forge (Railway Edition) 🎬

A minimal but powerful web application that generates short, animated videos from a text prompt using AI. This project uses a FastAPI backend to run the `stabilityai/sd-turbo` model and a modern HTML/CSS/JavaScript frontend. It is configured for deployment on **Railway** to support the large model size via persistent volumes.

**Live Demo URL:** [Your Deployed Frontend URL Here]

## Features

-   **Text-to-Video Generation**: Uses the high-quality `sd-turbo` model.
-   **Persistent Model Caching**: Downloads the large AI model only once on Railway's persistent volume, ensuring fast startups after the first launch.
-   **Aesthetic UI**: Clean, modern interface with a light/dark theme switcher.
-   **Deployment Ready**: Decomposed into separate frontend and backend services, configured for easy deployment on Railway.

## Tech Stack

-   **Backend**: Python, FastAPI, Gunicorn
-   **AI Model**: `stabilityai/sd-turbo` via Hugging Face Diffusers
-   **Video Processing**: Imageio, OpenCV
-   **Frontend**: HTML, CSS, JavaScript (served via a simple web server)
-   **Deployment**: Railway

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
|-- railway.json
|-- README.md


## Deployment to Railway (Step-by-Step)

### 1. Push to GitHub
Create a new repository on GitHub and push all the files in the structure above.

### 2. Create a New Project on Railway
-   Log in to your Railway account.
-   Click **New Project** and select **Deploy from GitHub repo**.
-   Connect the GitHub repository you just created. Railway will automatically detect the `railway.json` file and configure the backend service.

### 3. Add a Persistent Volume (Crucial Step)
-   Once the backend service is created, go to its **Settings** tab.
-   Scroll down to the "Volumes" section.
-   Click **Add Volume**.
-   Set the **Mount Path** to exactly `/data`. This is the folder where our application will cache the AI model.

### 4. Wait for the First Deploy
-   Go to the **Deployments** tab for your service. The first deployment will take a long time (10-20 minutes) as it downloads the 1.2 GB `sd-turbo` model to your new volume. **This only happens once.**
-   You can watch the live logs to see the download progress.

### 5. Add a Frontend Service
-   Go back to your Railway project dashboard.
-   Click **New** -> **Empty Service**.
-   Go to the new service's **Settings** tab.
-   Under "Build", set the **Root Directory** to `/frontend`.
-   Under "Deploy", set the **Start Command** to `python -m http.server $PORT`. This is a simple way to serve our static HTML file.
-   Go to the "Networking" section and click **Generate Domain** to get a public URL for your frontend.

### 6. Connect Frontend to Backend
-   Go to the settings for your `backend` service on Railway and copy its public URL.
-   Go to your local project code and open `frontend/script.js`.
-   Replace the placeholder `YOUR_RAILWAY_BACKEND_URL` with the URL you just copied.
    ```javascript
    // frontend/script.js
    const API_URL = '[https://your-backend-service-name.up.railway.app/generate-video](https://your-backend-service-name.up.railway.app/generate-video)'; 
    ```
-   Commit and push this change to GitHub. Railway will automatically redeploy your services.

### 7. Test Your Live App
-   Go to the public URL for your `frontend` service.
-   The first time you generate a video, it will have a "cold start" and may take up to a minute. Subsequent requests will be much faster.
-   Congratulations, your application is live!

