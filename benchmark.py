import whisper
import librosa
import time

AUDIO_FILE = '2086-149220-0033.wav'

# Load audio
audio = librosa.load(AUDIO_FILE, sr=16000)[0]

# Test CPU
print("Running on CPU...")
model_cpu = whisper.load_model("small", device="cpu")
start = time.time()
result_cpu = model_cpu.transcribe(audio)
cpu_time = time.time() - start
print(f"CPU time: {cpu_time:.2f} seconds")

# Test GPU
print("\nRunning on GPU...")
model_gpu = whisper.load_model("small", device="cuda")
start = time.time()
result_gpu = model_gpu.transcribe(audio)
gpu_time = time.time() - start
print(f"GPU time: {gpu_time:.2f} seconds")

print(f"\nSpeedup: {cpu_time/gpu_time:.2f}x faster on GPU")
print(f"Time saved: {cpu_time-gpu_time:.2f} seconds ({((cpu_time-gpu_time)/cpu_time*100):.1f}%)")
