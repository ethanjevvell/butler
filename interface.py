import tkinter as tk
import pyaudio
import wave
from pydub import AudioSegment
from butler import transcribe_and_submit

class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()

    def start_recording(self):
        self.recording = True
        self.frames.clear()
        stream = self.audio.open(format=pyaudio.paInt16,
                                 channels=1,
                                 rate=44100,
                                 input=True,
                                 frames_per_buffer=1024,
                                 stream_callback=self.callback)
        stream.start_stream()

    def stop_recording(self):
        self.recording = False

    def callback(self, in_data, frame_count, time_info, status):
        if self.recording:
            self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def save_audio(self, file_path):
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def convert_to_mp3(self, input_file, output_file):
        audio = AudioSegment.from_wav(input_file)
        audio.export(output_file, format="mp3")

def start_button_click():
    recorder.start_recording()

def stop_button_click():
    recorder.stop_recording()
    recorder.save_audio('output.wav')
    recorder.convert_to_mp3('output.wav', 'output.mp3')
    transcribe_and_submit()


recorder = AudioRecorder()

app = tk.Tk()
app.title("Audio Recorder")

start_button = tk.Button(app, text="Start Recording", command=start_button_click)
start_button.pack()

stop_button = tk.Button(app, text="Stop Recording", command=stop_button_click)
stop_button.pack()

app.mainloop()
