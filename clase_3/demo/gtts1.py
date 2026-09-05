from gtts import gTTS
from gtts.tts import gTTSError
import os


text = "Hola ¿cómo estas? Soy Alexia. Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?"

# Gestion de rutas
carpeta_audios = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audios")
os.makedirs(carpeta_audios, exist_ok=True)
ruta_audio = os.path.join(carpeta_audios, "gtts1.mp3")

# Crear el objeto gTTS
try:
    tts = gTTS(text=text, lang='es', tld='com.mx', slow=False)
    # El argumento 'tld' cambia el acento de la voz. Ej: com.mx para acento mexicano, com.ar para acento argentino, com.co para acento colombiano, etc.
    tts.save(ruta_audio)
    print(f"Archivo de audio guardado en: {ruta_audio}")
except gTTSError as e:
    print(f"Error al crear el objeto gTTS: {e}")
except OSError as e:
    print(f"Error al guardar el archivo de audio: {e}")
except Exception as e:
    print(f"Error al crear el objeto gTTS: {e}")


print(f"Audio generado con éxito en: {ruta_audio}")