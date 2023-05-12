import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import whisper_timestamped
from yt_dlp import YoutubeDL

from settings import BASE_DIR
from utils import write_srt

MODEL_TYPES = ["tiny", "base", "small", "medium", "large"]


def download_video(video_url: str):
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


def extract_vocal(media: str):

    # media_extension = Path(media).suffix
    # media_new_filepath = tempfile.gettempdir() / Path(
    #     "tempfreesubtitle/main"
    # ).with_suffix(media_extension)

    # Path(media_new_filepath).parent.mkdir(parents=True, exist_ok=True)
    # shutil.copy(media, media_new_filepath)

    # demucs_directory = tempfile.gettempdir()

    # filename = Path(media).name

    # filename,*_=filename.split(".")

    media_new_filepath = media
    demucs_directory = str(BASE_DIR/'vocals')

    # sys.path.append(str(BASE_DIR/'ffmpeg/'))

    # "demucs --two-stems=vocals mp4/1min.mp4 -o tmp/ --filename {track}/{stem}.{ext}"" # FileName/VOCAL.wav
    cmd = rf'demucs --two-stems=vocals "{media_new_filepath}" -o "{demucs_directory}" --filename "{{stem}}.{{ext}}"'

    subprocess.run(cmd, check=True)


def create_srt():
    device = 'cpu'  # 'gpu'
    model_type = MODEL_TYPES[0]

    used_model = whisper_timestamped.load_model(model_type, device=device)
    result = whisper_timestamped.transcribe(
        model=used_model,
        audio=str(BASE_DIR/'vocals/htdemucs/vocals.wav'),
        vad=True,
        verbose=False,
    )
    write_srt(result["segments"], 'abcd.srt')


# media_filepath = download_video('https://www.youtube.com/watch?v=xmx07H3sn1w')


# $env:Path = "$pwd\ffmpeg;$env:Path"
# extract_vocal(
#     str(BASE_DIR / 'mp4/4 Easy Ways To Make Small Talk With People.mp4'))

create_srt()
