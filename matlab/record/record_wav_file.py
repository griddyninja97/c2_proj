import os
import threading
import time
import wave

import keyboard
import pyaudio


class AudioRecorder:
    def __init__(self):
        self.chunk = 1024  
        self.format = pyaudio.paInt16  
        self.channels = 1  
        self.rate = 44100  

        self.frames = []
        self.recording = False
        self.audio = pyaudio.PyAudio()

    def start_recording(self):
        """Start recording"""
        self.recording = True
        self.frames = []

        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )

        print("Recording... Press Enter to stop")

        while self.recording:
            data = stream.read(self.chunk)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()

        print("Recording stopped")

    def stop_recording(self):
        """Stop recording"""
        self.recording = False

    def save_recording(self, filename):
        """Save recording data as WAV file"""
        if not self.frames:
            print("No recording data available")
            return

        wav_dir = "wav_files"
        if not os.path.exists(wav_dir):
            os.makedirs(wav_dir)

        filepath = os.path.join(wav_dir, filename)

        wf = wave.open(filepath, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b"".join(self.frames))
        wf.close()

        print(f"Recording saved as {filepath}")

    def cleanup(self):
        """Clean up resources"""
        self.audio.terminate()


def main():
    recorder = AudioRecorder()

    try:
        filename = input(
            "Enter filename for recording (without .wav extension): "
        ).strip()
        if not filename:
            filename = "recording"

        if not filename.endswith(".wav"):
            filename += ".wav"

        print(f"Filename set to: {filename}")
        print("Press Enter to start recording...")
        input()  

        recording_thread = threading.Thread(target=recorder.start_recording)
        recording_thread.start()

        keyboard.wait("enter")

        recorder.stop_recording()
        recording_thread.join()

        recorder.save_recording(filename)

    except KeyboardInterrupt:
        print("\nRecording interrupted")
        recorder.stop_recording()

    finally:
        recorder.cleanup()


if __name__ == "__main__":
    main()
