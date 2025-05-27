import librosa
import pyloudnorm as pyln
import numpy as np

def analizar_calidad(audio_path):
    y, sr = librosa.load(audio_path, sr=44100, mono=True)
    meter = pyln.Meter(sr)
    loudness = meter.integrated_loudness(y)
    clipping_ratio = np.sum(np.abs(y) > 0.99) / len(y)
    rms = librosa.feature.rms(y=y)[0]
    dynamic_range = np.std(rms)

    veredicto = "✅ Buena calidad general"
    if loudness < -24 or loudness > -6 or clipping_ratio > 0.01 or dynamic_range < 0.01:
        veredicto = "❌ Calidad deficiente"

    return {
        "lufs": round(loudness, 2),
        "clipping": round(clipping_ratio, 4),
        "dynamic_range": round(dynamic_range, 4),
        "veredicto": veredicto
    }
