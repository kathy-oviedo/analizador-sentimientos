import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Dashboard de Sentimientos", page_icon="📊")

st.title("📊 Análisis de Sentimientos en Tweets")
st.write("Datos procesados con el modelo BETO 🇪🇸")

# Cargar los datos
df = pd.read_csv("tweets_clasificados_con_fecha.csv")


st.write("📁 Tamaño del dataset:", df.shape)





import re

st.subheader("🔍 Buscar frases por palabra clave")

palabra_clave = st.text_input("Escribe una palabra o frase para buscar en los tweets:")

# Filtrar si se escribió algo
if palabra_clave:
    df_filtrado_busqueda = df[df["texto"].str.contains(palabra_clave, case=False, na=False)]
else:
    df_filtrado_busqueda = df.copy()

# Mostrar cantidad de resultados
st.markdown(f"Se encontraron **{len(df_filtrado_busqueda)}** tweets que coinciden con la búsqueda.")

# Función para resaltar palabra clave y COLOR
def resaltar_palabra(texto, palabra):
    try:
        estilo = "background-color:#e6ccff; padding:2px 4px; border-radius:3px; font-weight:bold;"
        return re.sub(f"({re.escape(palabra)})", rf"<span style='{estilo}'>\1</span>", texto, flags=re.IGNORECASE)
    except:
        return texto

# Mostrar tweets encontrados
if not df_filtrado_busqueda.empty:
    for _, fila in df_filtrado_busqueda.head(20).iterrows():
        texto = str(fila.get("texto", ""))
        texto_resaltado = resaltar_palabra(texto, palabra_clave) if palabra_clave else texto
        fecha = str(fila.get("Date", "")).split()[0]
        sentimiento = fila.get("sentimiento", "")
        usuario = fila.get("usuario", "")
        pais = fila.get("pais", "")

        st.markdown(f"""
        <div style="margin-bottom:10px; padding:10px; border-left:4px solid #aaa; background:#f9f9f9">
            <strong>📅 {fecha} | 😃 Sentimiento: {sentimiento}</strong><br>
            <em>🧑 Usuario: {usuario} | 🌍 País: {pais}</em><br><br>
            {texto_resaltado}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No se encontraron tweets con esa palabra.")







# Filtros
sentimiento = st.selectbox("Filtrar por sentimiento", options=["Todos"] + sorted(df["sentimiento"].unique().tolist()))
pais = st.selectbox("Filtrar por país", options=["Todos"] + sorted(df["pais"].dropna().unique().tolist()))

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])


st.subheader("📅 Evolución temporal de sentimientos")

df_agrupado = df.groupby([df["Date"].dt.date, "sentimiento"]).size().reset_index(name="cantidad")

grafico_tiempo = alt.Chart(df_agrupado).mark_line().encode(
    x="Date:T",
    y="cantidad:Q",
    color="sentimiento:N",
    tooltip=["Date", "sentimiento", "cantidad"]
).properties(width=700, height=400)

st.altair_chart(grafico_tiempo)




# Aplicar filtros
if sentimiento != "Todos":
    df = df[df["sentimiento"] == sentimiento]
if pais != "Todos":
    df = df[df["pais"] == pais]

# Visualización de proporciones
st.subheader("Distribución de sentimientos")
st.bar_chart(df["sentimiento"].value_counts())

st.subheader("📚 Comparación por tema")

# Asegurar que la columna 'tema' existe
if "tema" in df.columns:
    conteo_temas = df["tema"].value_counts().reset_index()
    conteo_temas.columns = ["tema", "cantidad"]

    grafico_temas = alt.Chart(conteo_temas).mark_bar().encode(
        x=alt.X("cantidad:Q", title="Cantidad de tweets"),
        y=alt.Y("tema:N", sort="-x", title="Tema"),
        tooltip=["tema", "cantidad"],
        color=alt.value("#a78bfa")  # Color lavanda suave
    ).properties(width=600, height=400)

    st.altair_chart(grafico_temas)
else:
    st.info("La columna 'tema' no está disponible en este dataset.")


st.subheader("🧑‍💻 Usuarios más activos")

# Asegurar que la columna 'usuario' existe
if "usuario" in df.columns:
    top_usuarios = df["usuario"].value_counts().head(10).reset_index()
    top_usuarios.columns = ["usuario", "tweets"]

    grafico_usuarios = alt.Chart(top_usuarios).mark_bar().encode(
        x=alt.X("tweets:Q", title="Cantidad de tweets"),
        y=alt.Y("usuario:N", sort="-x", title="Usuario"),
        tooltip=["usuario", "tweets"],
        color=alt.value("#f9a8d4")  # Color rosa pastel
    ).properties(width=600, height=400)

    st.altair_chart(grafico_usuarios)
else:
    st.info("La columna 'usuario' no está disponible en este dataset.")

st.subheader("📚 Sentimientos por tema")

if "tema" in df.columns and "sentimiento" in df.columns:
    agrupado = df.groupby(["tema", "sentimiento"]).size().reset_index(name="cantidad")

    grafico_apilado = alt.Chart(agrupado).mark_bar().encode(
        x=alt.X("cantidad:Q", title="Cantidad de tweets"),
        y=alt.Y("tema:N", sort="-x", title="Tema"),
        color=alt.Color("sentimiento:N", scale=alt.Scale(scheme="pastel1")),
        tooltip=["tema", "sentimiento", "cantidad"]
    ).properties(width=700, height=400)

    st.altair_chart(grafico_apilado)
else:
    st.info("No se encontraron columnas 'tema' y 'sentimiento'.")


# Tabla
st.subheader("Vista previa de datos")
st.dataframe(df.sample(10))
