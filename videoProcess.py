import os
import subprocess
from moviepy.editor import VideoFileClip

class VideoProcess:
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

    def AudioToText(self, wav_path):
        print(f"Transcribing {wav_path}...")
        # Add transcription logic here
