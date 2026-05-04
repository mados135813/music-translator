import argparse
import itertools
import sys

import requests
from deep_translator import GoogleTranslator


def fetch_lyrics(artist: str, song: str) -> str:
    url = f"https://api.lyrics.ovh/v1/{artist}/{song}"
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as e:
        raise SystemExit(f"Error de red: {e}")

    if response.status_code == 404:
        raise SystemExit(f"No se encontró la canción '{song}' de '{artist}'.")
    if response.status_code != 200:
        raise SystemExit(f"Error al obtener la letra (HTTP {response.status_code}).")

    data = response.json()
    if "lyrics" not in data or not data["lyrics"].strip():
        raise SystemExit("La respuesta no contiene letra.")

    return data["lyrics"].replace("\r\n", "\n").replace("\r", "\n").strip()


def translate_lyrics(text: str, target_lang: str) -> str:
    translator = GoogleTranslator(source="auto", target=target_lang)
    chunks = text.split("\n\n")
    translated_chunks = []
    for chunk in chunks:
        if chunk.strip():
            try:
                translated_chunks.append(translator.translate(chunk))
            except Exception as e:
                raise SystemExit(f"Error de traducción: {e}")
        else:
            translated_chunks.append("")
    return "\n\n".join(translated_chunks)


def display_side_by_side(original: str, translated: str, lang: str) -> None:
    orig_lines = original.splitlines()
    trans_lines = translated.splitlines()

    col_width = max((len(line) for line in orig_lines), default=0)
    col_width = max(col_width, 40)

    label_orig = "ORIGINAL"
    label_trans = "TRADUCCION (-> ES)" if lang == "es" else "TRADUCCION (-> EN)"

    print(f"\n{label_orig:<{col_width}} | {label_trans}")
    print("-" * col_width + "-+-" + "-" * col_width)

    for orig_line, trans_line in itertools.zip_longest(orig_lines, trans_lines, fillvalue=""):
        print(f"{orig_line:<{col_width}} | {trans_line}")

    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Descarga la letra de una canción y la traduce lado a lado."
    )
    parser.add_argument("artist", help="Nombre del artista")
    parser.add_argument("song", help="Título de la canción")
    parser.add_argument(
        "--lang",
        choices=["es", "en"],
        default="es",
        help="Idioma destino de la traducción (default: es)",
    )
    args = parser.parse_args()

    print(f"Buscando letra de '{args.song}' — {args.artist}...")
    lyrics = fetch_lyrics(args.artist, args.song)

    print("Traduciendo...")
    translated = translate_lyrics(lyrics, args.lang)

    display_side_by_side(lyrics, translated, args.lang)


if __name__ == "__main__":
    main()
