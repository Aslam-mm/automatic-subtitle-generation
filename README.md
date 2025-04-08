# 🎬 Auto Subtitle Generator using Whisper and Flask

This is a simple Flask web application that allows users to upload a video file and automatically generates subtitles using [OpenAI's Whisper](https://github.com/openai/whisper). It then burns the subtitles into the video and provides a downloadable `.mp4` file.

---

## 📦 Features

- Upload video files (`.mp4`, `.mov`, `.avi`, `.mkv`)
- Extract audio using `moviepy`
- Transcribe audio using OpenAI's Whisper
- Generate `.srt` subtitle file
- Burn subtitles into the video using `ffmpeg`
- Download the final video with hardcoded subtitles

---

## 🧰 Requirements

Make sure you have the following installed:

- Python 3.11
- ffmpeg (should be available in system PATH)

Install dependencies using:

```bash
pip install -r requirements.txt
