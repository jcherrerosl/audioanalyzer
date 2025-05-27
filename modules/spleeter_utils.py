import subprocess
import os
import librosa
import pyloudnorm as pyln

def separar_stems(audio_path):
    output_dir = audio_path + "_stems"
    subprocess.run(["spleeter", "separate", "-p", "spleeter:2stems", "-o", output_dir, audio_path])

    basename = os.path.splitext(os.path.basename(audio_path))[0]
    vocal_path = os.path.join(output_dir, basename, "vocals.wav")
    accomp_path = os.path.join(output_dir, basename, "accompaniment.wav")

    y_v, sr = librosa.load(vocal_path, sr=44100)
    y_b, _ = librosa.load(accomp_path, sr=44100)

    meter = pyln.Meter(sr)
    lufs_voz = meter.integrated_loudness(y_v)
    lufs_base = meter.integrated_loudness(y_b)

    return lufs_voz, lufs_base
