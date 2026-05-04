import streamlit as st
from lyrics_translator import fetch_lyrics, translate_lyrics

st.title("Letra + Traduccion")

artist = st.text_input("Artista", placeholder="Ej: Shakira")
song = st.text_input("Cancion", placeholder="Ej: Waka Waka")
lang = st.selectbox("Idioma destino", options=["es", "en"], format_func=lambda x: "Espanol" if x == "es" else "English")

if st.button("Traducir"):
    if not artist.strip() or not song.strip():
        st.warning("Completa los campos de artista y cancion.")
    else:
        with st.spinner("Buscando y traduciendo..."):
            try:
                lyrics = fetch_lyrics(artist.strip(), song.strip())
                translated = translate_lyrics(lyrics, lang)
            except SystemExit as e:
                st.error(str(e))
                st.stop()

        col1, col2 = st.columns(2)
        label = "Traduccion al Espanol" if lang == "es" else "Translation to English"
        with col1:
            st.subheader("Original")
            st.text(lyrics)
        with col2:
            st.subheader(label)
            st.text(translated)
