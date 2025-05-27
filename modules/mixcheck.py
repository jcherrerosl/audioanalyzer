import librosa
import numpy as np
import matplotlib.pyplot as plt
from modules.spleeter_utils import separar_stems

def calcular_crest_factor(y):
    rms = np.sqrt(np.mean(y**2))
    peak = np.max(np.abs(y))
    return peak / rms if rms > 0 else 0

def calcular_rms_bandas(y, sr):
    S = np.abs(librosa.stft(y, n_fft=2048))**2
    freqs = librosa.fft_frequencies(sr=sr)
    total_power = np.sum(S)

    def band_db(fmin, fmax):
        band = S[(freqs >= fmin) & (freqs <= fmax), :]
        if band.size == 0:
            return -120
        band_power = np.sum(band)
        ratio = band_power / total_power if total_power > 0 else 0.000001
        return round(10 * np.log10(ratio), 2)

    return {
        "low": band_db(20, 150),
        "mid": band_db(150, 5000),
        "high": band_db(5000, 16000)
    }


def evaluar_con_ia_lite(y, sr, rms_bandas):
    crest = calcular_crest_factor(y)
    mensajes = []

    if crest < 1.8:
        mensajes.append("❌ Mezcla muy comprimida, falta de dinámica")
    elif crest < 2.5:
        mensajes.append("⚠️ Mezcla comprimida, pero aceptable según el estilo")

    if rms_bandas["low"] > -2.5:
        mensajes.append("❌ Exceso de graves")
    elif (rms_bandas["low"] - rms_bandas["mid"]) > 10:
        mensajes.append("❌ Graves muy por encima de los medios")

    if rms_bandas["mid"] < -20:
        mensajes.append("❌ Falta de cuerpo en medios")
    if rms_bandas["high"] > -5:
        mensajes.append("❌ Agudos agresivos")

    if not mensajes:
        mensajes.append("✅ Mezcla equilibrada según análisis técnico")

    return crest, mensajes

def analizar_mezcla(audio_path):
    y, sr = librosa.load(audio_path, sr=44100, mono=True)
    voz_lufs, base_lufs = separar_stems(audio_path)
    voz_vs_base = round(voz_lufs - base_lufs, 2)
    rms_bandas = calcular_rms_bandas(y, sr)
    crest_factor, diagnostico = evaluar_con_ia_lite(y, sr, rms_bandas)

    return {
        "voz_vs_base": voz_vs_base,
        "crest_factor": round(crest_factor, 2),
        "rms_bandas": rms_bandas,
        "diagnostico": diagnostico,
    }
