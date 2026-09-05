from gtts import gTTS
from gtts.tts import gTTSError
import os

def generar_audio(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            texto = archivo.read()
        
        # Gestion de rutas
        carpeta_audios = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audios")
        os.makedirs(carpeta_audios, exist_ok=True)
        ruta_audio = os.path.join(carpeta_audios, nombre_archivo.replace(".txt", ".mp3"))

        # Crear el objeto gTTS
        tts = gTTS(text=texto, lang='es', tld='com', slow=False)

        tts.save(ruta_audio)

        print(f"Archivo de audio guardado en: {ruta_audio}")
    except Exception as e:
        print(f"Error al generar el audio: {e}")


generar_audio("content.txt")