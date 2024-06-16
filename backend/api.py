from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from contextlib import asynccontextmanager
import os

from database import Database
from model.image_processor import ImageProcessor


class SearchRequest(BaseModel):
    image_data: str  # Base64 encoded image data

class SearchResponse(BaseModel):
    image_urls: List
    label: int


# Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_loaded = False
    app.state.model_loaded = False


    def load_database():
        app.state.db = Database(db_path=os.path.join(os.getcwd(), "images.db"))
        app.state.db_loaded = True

    def load_model():
        app.state.model = ImageProcessor()
        app.state.model_loaded = True

    # Create a ThreadPoolExecutor to run the tasks concurrently
    with ThreadPoolExecutor() as executor:
        executor.submit(load_database)
        executor.submit(load_model)

        yield

    # Clean up resources if needed
    del app.state.db
    del app.state.model

# Configure CORS for the frontend application
origins = [
    "http://localhost:3000",  # React app URL
]

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    if app.state.db_loaded and app.state.model_loaded:
        return {"status": "healthy"}
    else:
        raise HTTPException(status_code=503, detail="Service initializing")


@app.post("/search", response_model=SearchResponse)
async def search_images(request: SearchRequest, background_tasks: BackgroundTasks):
    # 2. Use the model to classify the image and get the label
    label = classify_and_upload_image(background_tasks, request)

    # 2. Search for images by label in the database
    matching_images = app.state.db.search_images_by_label(label)

    # 3. Return the list of matching image URLs
    return SearchResponse(image_urls=matching_images, label=label)


def classify_and_upload_image(background_tasks, request):
    label = app.state.model.image_to_label(request.image_data)
    # 3. Add the task to save the image string and the predicted label to the database in the background
    background_tasks.add_task(
        app.state.db.save_label_and_string,
        label,
        request.image_data
    )
    return label


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
