import os
import yt_dlp
from typing import Any

class VideoDownloaderService:
    def __init__(self, download_path: str):
        self.download_path = download_path
        os.makedirs(self.download_path, exist_ok=True)

    def download(self, url: str, filename: str) -> str:
        output_template = f"{self.download_path}/{filename}.%(ext)s"
        
        ydl_opts: Any = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': output_template,
            'merge_output_format': 'mp4',
            'quiet': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        return f"{self.download_path}/{filename}.mp4"