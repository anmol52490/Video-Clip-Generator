# backend/app.py
# This is the FastAPI backend, optimized for Railway deployment.

import os
import uuid
import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import torch
from diffusers import AutoPipelineForText2Image
import cv2
import numpy as np
from PIL import Image
import imageio

# --- Configuration for Railway's Persistent Volume ---
# Railway mounts a persistent volume at /data. We'll use this to cache the model.
CACHE_DIR = "/data/huggingface_cache"
# The /tmp directory is for temporary files that can be deleted.
GENERATED_DIR = "/tmp/generated_videos_temp"
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)


# --- AI Model & Global State ---
ml_models = {}

# --- Lifespan Management (FastAPI Startup/Shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events. Loads the AI model on startup.
    It will load the model from the persistent volume if it exists, otherwise it downloads it.
    """
    model_id = "stabilityai/sd-turbo"
    print(f"Loading AI model ({model_id})...")
    print(f"Model cache directory: {CACHE_DIR}")
    
    try:
        pipe = AutoPipelineForText2Image.from_pretrained(
            model_id,
            torch_dtype=torch.float32,
            # This tells diffusers to use our persistent volume for caching
            cache_dir=CACHE_DIR
        )
        pipe.to("cpu")
        ml_models["text_to_image"] = pipe
        print("✅ AI model loaded successfully.")
    except Exception as e:
        print(f"❌ Failed to load AI model: {e}")
    
    yield
    
    ml_models.clear()
    print("AI model unloaded.")

# --- FastAPI App Initialization ---
app = FastAPI(
    title="AI Video Generator API",
    description="Backend API for generating AI videos.",
    lifespan=lifespan
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class VideoRequest(BaseModel):
    prompt: str

# --- Video Generation Logic ---
def create_animated_video(base_image: Image.Image, output_path: str, duration_secs=5, fps=24):
    img_np = np.array(base_image)
    height, width, _ = img_np.shape
    num_frames = duration_secs * fps
    
    print(f"Creating animation with {num_frames} frames...")
    
    with imageio.get_writer(output_path, mode='I', fps=fps, format='FFMPEG', codec='libx264') as writer:
        for i in range(num_frames):
            scale = 1.0 + (0.2 * i / num_frames)
            M = cv2.getRotationMatrix2D((width / 2, height / 2), 0, scale)
            zoomed_frame_np = cv2.warpAffine(img_np, M, (width, height))
            writer.append_data(zoomed_frame_np)
            
    print(f"✅ Video saved temporarily to {output_path}")

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "AI Video Generator API is running."}

@app.post("/generate-video")
async def generate_video_endpoint(request: VideoRequest):
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    if "text_to_image" not in ml_models:
        raise HTTPException(status_code=503, detail="AI model is not available or failed to load.")

    print(f"Generating video for prompt: '{prompt}'")
    try:
        pipe = ml_models["text_to_image"]
        image = pipe(prompt=prompt, num_inference_steps=2, guidance_scale=0.0).images[0]
        
        video_filename = f"{uuid.uuid4()}.mp4"
        video_path = os.path.join(GENERATED_DIR, video_filename)
        create_animated_video(image, video_path)
        
        with open(video_path, "rb") as video_file:
            video_base64 = base64.b64encode(video_file.read()).decode('utf-8')
        
        os.remove(video_path)
            
        return {"video_base64": video_base64, "status": "success"}
    except Exception as e:
        print(f"❌ Error during video generation: {str(e)}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")
