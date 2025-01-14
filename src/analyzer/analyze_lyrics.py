import json
import syncedlyrics
from utils.fetch_emotions import call_openai
from config import settings
import asyncio


LYRICS_BATCH_SIZE = settings.LYRICS_BATCH_SIZE

def start_analysis(metadata):
    asyncio.run(get_lyrics_emotion_list(metadata))

def parse_and_validate_json(json_data):
    try:
        # Intenta cargar el JSON
        data = json.loads(json_data) if isinstance(json_data, str) else json_data

        # Verifica que sea una lista de diccionarios
        if not isinstance(data, list):
            raise ValueError("El JSON debe ser una lista de objetos.")

        for index, item in enumerate(data):
            if not isinstance(item, dict):
                print(f"Elemento en índice {index} no es un objeto válido: {item}")
                continue

            print(f"\nValores del objeto en índice {index}:")
            for key, value in item.items():
                print(f"{key}: {value}")

    except json.JSONDecodeError:
        print("Error: JSON no válido.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def get_song_lyrics(metadata):
    try:
        print("Obteniendo letra de la canción...")
        lrc = syncedlyrics.search(f"{metadata.get('title')} {metadata.get('artist')}")
        return lrc
    except Exception as e:
        print(f"No se pudo obtener las lyrics: {e}")


async def get_lyrics_emotion_list(metadata):
    print("Analizando emociones de la letra de las canción...")

    lyrics = get_song_lyrics(metadata)

    if lyrics:
        batch_lyrics = divide_lyrics_in_batches(lyrics)
        tasks = [analyze_batch(current_batch) for current_batch in batch_lyrics]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Batch {i + 1} failed: {result}")
            else:
                print(f"Batch {i + 1} result: {result}")

    else:
        print("Error: no se pudo obtener la letra de la canción.")


def divide_lyrics_in_batches(lrc_text, batch_size = LYRICS_BATCH_SIZE):

    lyrics = lrc_text.strip().split("\n")

    groups = [lyrics[i:i + batch_size] for i in range(0, len(lyrics), batch_size)]

    return groups

async def analyze_batch(batch):
    try:
        # Convert the batch content into a literal template
        batch_content = "\n".join(batch)

        print(f"Analyzing batch:\n{batch_content}")
        response = call_openai(batch_content)
        return response
    except Exception as e:
        return {"error": str(e)}


