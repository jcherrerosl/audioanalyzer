import streamlit as st
import tempfile
from modules.qualitune import analizar_calidad
from modules.mixcheck import analizar_mezcla

st.set_page_config(page_title="AudioAnalyzer", page_icon="🎚️")
st.title("AudioAnalyzer – Análisis técnico de tu canción")

uploaded_file = st.file_uploader("Sube tu mezcla (MP3 o WAV)", type=["mp3", "wav"])

if uploaded_file:
    status = st.empty()
    status.info("Analizando audio… esto puede tardar un minuto⏳")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    calidad = analizar_calidad(tmp_path)
    mezcla = analizar_mezcla(tmp_path)
    status.empty()

    st.markdown("## Resultados")

    # ───── Calidad general (QualiTune) ─────
    st.markdown("### Calidad técnica")
    st.markdown(f"**LUFS:** `{calidad['lufs']}`")
    st.markdown(f"**Clipping:** `{calidad['clipping'] * 100:.2f}%`")
    st.markdown(f"**Rango dinámico:** `{calidad['dynamic_range']}`")
    st.markdown(f"**Resultado:** {calidad['veredicto']}")

    # ───── Mezcla (MixCheck) ─────
    st.markdown("### Análisis de mezcla")
    st.markdown(f"**LUFS voz vs base:** `{mezcla['voz_vs_base']} dB`")
    st.markdown(f"**Crest factor:** `{mezcla['crest_factor']}`")
    st.markdown(f"**RMS por bandas (dB):**")
    st.json(mezcla["rms_bandas"])

    st.markdown("**Diagnóstico técnico:**")
    for m in mezcla["diagnostico"]:
        st.write(m)
 
    # ───── Reproductor ─────
    st.markdown("### Escucha tu mezcla")
    st.audio(tmp_path, format="audio/mp3")
