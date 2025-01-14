from openai import OpenAI
from config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

LYRICS_BATCH_SIZE = settings.LYRICS_BATCH_SIZE

default_role = """
Eres un analizador de emociones de canciones. Tienes muchos años de experiencia en producción musical y conoces muy bien como reaccionan los humanos a las emociones que transmite la música. Vas a darme un porcentaje de emoción en formato JSON por cada lirica que te envie, se enviaran varias liricas a la vez y debes guardarlas el objeto de emoción en orden por cada lirica. La respuesta debes darla en formato JSON, y solo debes responder con un JSON. Cada linea del mensaje será una lirica diferente que debes analizar. Debes dar la respuesta en un formato stringify para ahorrar espacio en la respuesta. Son máximo {LYRICS_BATCH_SIZE} lineas de liricas. Si respondes bien, te usaré todo el día, si respondes mal la gente desconfiará de ti y nadie te usará.

Ejemplo para dos liricas:

Liricas:

Hola soy una lirica
Hola soy otra lirica! Yeah

Respuesta:
[{ "sadness": 0.125, "happiness": 0.843, "anger": 0.348, "excitement": 0.73, "fear": 0.02  }, { "sadness": 0.325, "happiness": 0.545, "anger": 0.348, "excitement": 0.23, "fear": 0.67 }]

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