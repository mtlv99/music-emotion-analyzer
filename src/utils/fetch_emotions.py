from openai import OpenAI
from config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

LYRICS_BATCH_SIZE = settings.LYRICS_BATCH_SIZE

default_role = """
Eres un analizador de emociones de canciones. Tienes muchos años de experiencia en producción musical y conoces muy bien como reaccionan los humanos a las emociones que transmite la música. Vas a darme un porcentaje de emoción en formato JSON por cada lirica que te envie, se enviaran varias liricas a la vez y debes guardarlas el objeto de emoción en orden por cada lirica. La respuesta debes darla en formato JSON, y solo debes responder con un JSON. Cada linea del mensaje será una lirica diferente que debes analizar. Las emociones son un valor decimal entre 0 y 1. Adicionalmente, si viene una lirica vacía (con timestamp pero sin letra), debes guardar todos los valores emocionales de esa lirica en 0.00. Es importante recordar que debe ser un JSON valido. Debes dar la respuesta en un formato stringify para ahorrar espacio en la respuesta, texto plano sin formato markdown. Son máximo {LYRICS_BATCH_SIZE} lineas de liricas. Si respondes bien, te usaré todo el día. Si respondes mal la gente desconfiará de ti y nadie te usará.

Utiliza la siguiente estructura:
{
  "[00:01.02]": {
    "sadness": 0.00,
    "happiness": 0.00,
    "anger": 0.00,
    "excitement": 0.00,
    "fear": 0.00
  }
}

Ejemplo para tres liricas:

Liricas:

[00:23.12] Hola soy una lirica
[00:24.58] Soy otra lirica! Yeah
[00:26.13] La lirica que sigue, wow

Respuesta de OpenAI (utiliza valores reales):
{"[00:23.12]":{"sadness":0.1,"happiness":0.1,"anger":0.1,"excitement":0.1,"fear":0.1},"[00:24.58]":{"sadness":0.1,"happiness":0.1,"anger":0.1,"excitement":0.1,"fear":0.1},"[00:26.13]":{"sadness":0.1,"happiness":0.1,"anger":0.1,"excitement":0.1,"fear":0.1}}
"""

def call_openai(prompt: str, developer_role: str = default_role, model: str = "gpt-4o") -> str:
    try:
        print("Consultando a OpenAI...")

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "developer", "content": developer_role},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating completion: {e}")
        return None