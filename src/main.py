from yt_dlp import YoutubeDL
from settings import BASE_DIR

def download_video(video_url:str):
    ydl_opts = {
            "format": "mp4",
            "outtmpl": str(BASE_DIR / "mp4/%(title)s.%(ext)s"),
            "quiet": True,
    }

    if video_url == None or video_url.strip() == "":
        return None

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        download_file_path = ydl.prepare_filename(info)
    return download_file_path

print(
    download_video('https://www.youtube.com/watch?v=668nUCeBHyY&pp=ygUQc21hbGwgdmlkZW8gY2xpcA%3D%3D')
)