import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Analizador de Sentimientos", page_icon="🧠")
st.title("🧠 Analizador de Sentimientos en Español")
st.write("Este analizador usa el modelo BETO entrenado para detectar sentimientos en español 🇪🇸")

texto = st.text_area("✏️ Escribe aquí tu frase en español:")

@st.cache_resource
def cargar_modelo():
    return pipeline("sentiment-analysis", model="finiteautomata/beto-sentiment-analysis")

analizador = cargar_modelo()

if st.button("🔍 Analizar sentimiento"):
    if texto:
        resultado = analizador(texto)[0]
        etiqueta = resultado['label']
        score = round(resultado['score'] * 100, 2)

        if etiqueta == 'POS':
            st.success(f"💚 Positivo ({score}%)")
        elif etiqueta == 'NEG':
            st.error(f"❤️‍🩹 Negativo ({score}%)")
        else:
            st.info(f"💬 Neutral ({score}%)")
    else:
        st.warning("¡Por favor escribe algo para analizar!")

