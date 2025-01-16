import json
import re
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

        all_merged_results = {}

        for i, (current_batch, result) in enumerate(zip(batch_lyrics, results)):
            if isinstance(result, Exception):
                print(f"Batch {i + 1} failed: {result}")
                emotion_response = None
            else:
                print(f"Batch {i + 1} result: {result}")
                emotion_response = result

            merged_result = merge_lyrics_batch_and_emotion_response("\n".join(current_batch), emotion_response)
            print(f"Merged result for batch {i + 1}: {merged_result}")

            # Concatenate the merged result into all_merged_results
            all_merged_results.update(merged_result)

        all_merged_results_str = json.dumps(all_merged_results, indent=4, ensure_ascii=False)
        print(f"All merged results: {all_merged_results_str}")

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
        return json.loads(response)
    except Exception as e:
        return {"error": str(e)}


def merge_lyrics_batch_and_emotion_response(lyrics_batch_item, emotion_response):
    # Dividir las líneas del texto de las letras
    lyrics_lines = lyrics_batch_item.strip().split("\n")

    # Crear un diccionario para almacenar el resultado
    merged_result = {}

    for line in lyrics_lines:
        # Usar una expresión regular para separar el timestamp y la letra
        match = re.match(r'(\[\d{2}:\d{2}\.\d{2}\])\s*(.*)', line)
        if match:
            timestamp = match.group(1)
            lyric = match.group(2)

            # Si el timestamp también está en emotion_response, combinar los datos
            if timestamp in emotion_response:
                merged_result[timestamp] = {
                    "lyric": lyric,
                    **emotion_response[timestamp]  # Desempaquetar las emociones
                }
            else:
                # Si no está en emotion_response, asignar valores de emociones en 0.00
                merged_result[timestamp] = {
                    "lyric": lyric,
                    "sadness": -1.00,
                    "happiness": -1.00,
                    "anger": -1.00,
                    "excitement": -1.00,
                    "fear": -1.00
                }

    return merged_result
