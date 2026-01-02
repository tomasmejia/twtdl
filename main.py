import os
import uuid
import asyncio
from typing import Annotated, Any
from concurrent.futures import ThreadPoolExecutor

# Third-party imports
import yt_dlp
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel, HttpUrl
from fastapi.staticfiles import StaticFiles

# Local imports
from service import VideoDownloaderService

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Thread pool executor for handling blocking tasks (like downloading!)
executor = ThreadPoolExecutor(max_workers=3)

app = FastAPI(title="X video downloader API")
app.mount("/ui", StaticFiles(directory="static", html=True), name="static")

# Services
class VideoRequest(BaseModel):
    url: HttpUrl

# deps
def get_video_service() -> VideoDownloaderService:
    return VideoDownloaderService(DOWNLOAD_DIR)

def remove_file(path: str):
    try:
        os.remove(path)
        print(f"Removed file: {path}")
    except Exception as e:
        print(f"Error removing file {path}: {str(e)}")

# routes 
@app.get("/")
async def root():
    return RedirectResponse(url="/ui/")

@app.post("/download", response_class=FileResponse)
async def download_video(
    request: VideoRequest,
    background_tasks: BackgroundTasks,
    service: Annotated[VideoDownloaderService, Depends(get_video_service)]
):
    file_id = str(uuid.uuid4())
    # Run the blocking download in a separate thread so the server remains responsive
    loop = asyncio.get_event_loop()
    
    try: 
        file_path = await loop.run_in_executor(
            executor,
            service.download,
            str(request.url),
            file_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    background_tasks.add_task(remove_file, file_path)

    return FileResponse(path=file_path, filename=f"video_{file_id}.mp4", media_type='video/mp4')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0", port=8000)