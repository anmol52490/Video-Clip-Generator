# AI Video Forge 🎬

A minimal but powerful web application that generates short, animated videos from a text prompt using AI. This project uses a FastAPI backend to run a text-to-image model (`stabilityai/sd-turbo`) and a modern HTML/CSS/JavaScript frontend.

**Live Demo URL:** [Your Deployed App URL Here]

## Features

-   **Text-to-Video Generation**: Enter any creative prompt and get a short video.
-   **Local AI Model**: Runs a fast, CPU-friendly model, avoiding external API costs.
-   **Aesthetic UI**: Clean, modern interface with a light/dark theme switcher.
-   **Deployment Ready**: Decomposed into a frontend and backend, configured for easy deployment on Vercel.

## Tech Stack

-   **Backend**: Python, FastAPI
-   **AI Model**: `stabilityai/sd-turbo` via Hugging Face Diffusers
-   **Video Processing**: Imageio, OpenCV
-   **Frontend**: HTML, CSS, JavaScript (no frameworks)
-   **Deployment**: Vercel

## Project Structure

The project is structured as a monorepo, ready for Vercel deployment:


/
|-- /api                 # Contains the Python backend
|   |-- app.py
|   |-- requirements.txt
|-- /public              # Contains all static frontend files
|   |-- index.html
|   |-- style.css
|   |-- script.js
|-- vercel.json          # Vercel deployment configuration
|-- README.md


## Local Setup and Development

Follow these steps to run the application on your local machine.

### Prerequisites

-   Python 3.9+
-   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd peppo-video-app
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # On Windows
    python -m venv venv
    .\venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**
    Navigate to the `api` directory and install the required packages.
    ```bash
    cd api
    pip install -r requirements.txt
    cd .. 
    ```

### Running the Application

1.  **Start the backend server:**
    From the root directory of the project, run the following command to start the FastAPI server.
    ```bash
    uvicorn api.app:app --reload
    ```
    The backend will be running at `http://127.0.0.1:8000`.

2.  **Run the frontend:**
    The simplest way to run the frontend locally is to use a live server extension in your code editor (like VS Code's "Live Server"). Right-click on `public/index.html` and open it with Live Server.

    *Note: You will need to update the `API_URL` in `public/script.js` to `http://127.0.0.1:8000/api/generate-video` for local development.*

## Deployment to Vercel

This project is pre-configured for a seamless deployment to Vercel.

1.  **Push to GitHub**: Create a new repository on GitHub and push your code.

2.  **Import Project on Vercel**:
    -   Log in to your Vercel account.
    -   Click "Add New..." -> "Project".
    -   Import the GitHub repository you just created.

3.  **Configure the Project**:
    -   Vercel will automatically detect the project structure using the `vercel.json` file. It should recognize it as a "Vercel Functions" project with a Python backend.
    -   No special build commands are needed. The root directory should be the project root.
    -   Click **Deploy**.

4.  **Wait for Deployment**: The first deployment may take several minutes as Vercel's build process needs to download the AI model (~1.2 GB). Subsequent deployments will be much faster. Once complete, you will get a public URL for your live application.

