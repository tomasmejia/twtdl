# X (Twitter) / YT Video Downloader.

Built with Python (FastAPI) and yt-dlp.

There are two interfacess available:
1. *Web UI*: Browser interface to download videos.
2. *CLI*. Terminal command for quick download.


## Prerequisites

* Python 3.1
* [FFmpeg](https://www.ffmpeg.org/) (!)



##  Installation

1. Clone repo

2. Create virtual env
`python -m venv` or `python3 -m venv venv`

3. Install deps
`pip install -r requirements.txt`


## CLI Tool

```bash
# Basic usage
python cli.py "https://x.com/goo_vision/status/2007184035664277802"

# Specify a download folder
python cli.py "https://x.com/goo_vision/status/2007184035664277802" --path "my_videos"

# Get help
python cli.py --help
``` 
## Web Server

1. Start the FastAPI Server:
`uvicorn main:app -reload`
2. Go to http://127.0.0.1:8000/

### Routes
- `/` redirects to `/ui/`
- `/docs` Swagger for the routes
- `/ui/` UI interface

