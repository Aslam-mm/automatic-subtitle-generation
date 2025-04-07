import os
import subprocess
import whisper
from moviepy.editor import VideoFileClip

class VideoProcess:
    SUPPORTED_MODELS = [
        'tiny.en', 'base.en', 'small.en', 'medium.en', 'large.en'
    ]

    def __init__(self, model_name='tiny.en'):
        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model '{model_name}'. Choose from: {self.SUPPORTED_MODELS}")
        self.model_name = model_name
        self.model = whisper.load_model(model_name)

    def runFile(self, filepath):
        base = os.path.splitext(filepath)[0]
        wav_output = f"{base}.wav"
        self.extractAudioToWav(filepath, wav_output)

    def extractAudioToWav(self, video_path, wav_output):
        try:
            video = VideoFileClip(video_path)
            if video.audio is None:
                print("No audio track found in video.")
                return
            video.audio.write_audiofile(wav_output, codec='pcm_s16le')
            self.AudioToText(wav_output)
        except Exception as e:
            print(f"Error extracting audio: {e}")

    def AudioToText(self, audio_path):
        try:
            print(f"Transcribing using model: {self.model_name}")
            result = self.model.transcribe(audio_path)
            self.generateSubtitle(result)
        except Exception as e:
            print(f"Error during transcription: {e}")

    def generateSubtitle(self, result):
        try:
            transcript = result.get('text', '') if isinstance(result, dict) else str(result)
            with open('transcription.txt', "w", encoding="utf-8") as f:
                f.write(transcript)
            print("Subtitle file 'transcription.txt' generated.")
        except Exception as e:
            print(f"Error writing subtitle: {e}")
