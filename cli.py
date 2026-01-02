import typer
import uuid
from typing import Annotated
from service import VideoDownloaderService

app = typer.Typer()

@app.command()
def download(
    url: str, 
    path: Annotated[str, typer.Option(help="Folder to save video")] = "downloads"
):
    """
    Download a video from X/Twitter to your local machine.
    """
    
    typer.echo(f"Starting download for: {url}")
    
    service = VideoDownloaderService(download_path=path)
    file_id = str(uuid.uuid4())

    try:
        final_path = service.download(url, file_id)
        
        typer.secho(f"Success. Saved to: {final_path}", fg=typer.colors.GREEN)
        
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)

if __name__ == "__main__":
    app()