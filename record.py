# to record a sound and save it in the same directory. The record.py file contains the following code:

import wave
import pyaudio
import wave
import pyaudio
import os

recording = False

def record(cancelRecordingEvent):
  CHUNK = 1024
  FORMAT = pyaudio.paInt16
  CHANNELS = 2
  RATE = 44100
  WAVE_OUTPUT_FILENAME = "output.wav"

  p = pyaudio.PyAudio()

  stream = p.open(format=FORMAT,
          channels=CHANNELS,
          rate=RATE,
          input=True,
          frames_per_buffer=CHUNK)

  print("* recording")

  frames = []
  recording = True

  while not cancelRecordingEvent.is_set():
    data = stream.read(CHUNK)
    frames.append(data)

  print("* done recording")

  stream.stop_stream()
  stream.close()
  p.terminate()

  wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(p.get_sample_size(FORMAT))
  wf.setframerate(RATE)
  wf.writeframes(b''.join(frames))
  wf.close()

  return WAVE_OUTPUT_FILENAME
