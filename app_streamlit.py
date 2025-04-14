import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Analizador de Sentimientos", page_icon="🧠")

st.title("🧠 Analizador de Sentimientos")
st.write("Escribe un texto en español y detectaremos su sentimiento usando TextBlob.")

texto = st.text_area("✏️ Ingresa tu frase aquí:")

if st.button("🔍 Analizar"):
    if texto:
        blob = TextBlob(texto)
        polaridad = blob.sentiment.polarity

        if polaridad > 0:
            st.success("💚 Sentimiento positivo")
        elif polaridad < 0:
            st.error("❤️‍🩹 Sentimiento negativo")
        else:
            st.info("💬 Sentimiento neutral")
    else:
        st.warning("¡Escribe algo primero!")

