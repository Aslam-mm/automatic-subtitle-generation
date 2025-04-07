import os
import subprocess
import whisper
from moviepy.editor import VideoFileClip
from utils import write_srt

class VideoProcess:
    SUPPORTED_MODELS = [
        'tiny.en', 'base.en', 'small.en', 'medium.en', 'large.en'
    ]

    def __init__(self, filepath, model_name='tiny.en'):
        self.filepath = filepath
        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model '{model_name}'. Choose from: {self.SUPPORTED_MODELS}")
        self.model_name = model_name
        self.model = whisper.load_model(model_name)
        self.runFile()

    def runFile(self):
        self.base = os.path.splitext(self.filepath)[0]
        wav_output = f"{self.base}.wav"
        self.extractAudioToWav(self.filepath, wav_output)

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
            with open(f'{self.base}.srt', "w", encoding="utf-8") as srt:
                write_srt(result["segments"], file=srt)
            self.burnSubtitles()
            self.cleanup()
            print("Subtitle file generated.")
        except Exception as e:
            print(f"Error writing subtitle: {e}")
    
    def cleanup(self):
        """Delete the generated .wav file after processing."""
        try:
            wav_file = self.base + '.wav'
            if os.path.exists(wav_file):
                os.remove(wav_file)
                print("Deleted temporary file")
            else:
                print(f"No WAV file to delete: {wav_file}")
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def burnSubtitles(self):
        try:
            input_video = self.filepath
            subtitle_file = f"{self.base}.srt"
            output_video = f"{self.base}_subtitled.mp4"

            if not os.path.exists(subtitle_file):
                print(f"No subtitle file found at {subtitle_file}")
                return

            # Convert path for ffmpeg compatibility
            subtitle_path_ffmpeg = subtitle_file.replace(os.sep, '/').replace(':', '\\:')

            command = [
                'ffmpeg', '-y',
                '-i', input_video,
                '-vf', f"subtitles={subtitle_path_ffmpeg}",
                '-c:a', 'copy',
                output_video
            ]
            subprocess.run(command, check=True)
            print(f"Subtitled video saved as {output_video}")
        except subprocess.CalledProcessError as e:
            print(f"Error during subtitle burning: {e}")
