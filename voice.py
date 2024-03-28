import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
import numpy as np
import soundfile as sf

import time

start_time = time.time()


device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
model_id = "openai/whisper-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)


processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)

print("Time taken to load model", (time.time() - start_time))
dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")

print("Time taken to load dataset", (time.time() - start_time))

def load(filename):

    start_time = time.time()    
    if(filename == None):
        filename = "Recording.mp3"
    audio, sampling_rate = sf.read(filename)
    print("Time taken to read", (time.time() - start_time))




    # Check if the audio is stereo
    if len(audio.shape) > 1 and audio.shape[1] == 2:
        # Convert to mono by averaging the two channels
        audio = np.mean(audio, axis=1)

    # Create the dictionary
    sample = {
        "raw": np.array(audio),
        "sampling_rate": sampling_rate
    }
    result = pipe(sample)

    print("Time taken to run model", (time.time() - start_time))


    print(result)

    result = result['text']

    return result

if __name__ == '__main__':
    load()
else:
    print("Voice module loaded")