import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY_OPENAI")
MODEL = os.getenv("MODEL_VIDEO_OPENAI")

output_filename = "Perro_jugando_con_una_mariposa.mp4"

client = OpenAI(api_key=API_KEY)

video = client.videos.create_and_poll(
    model=MODEL,
    prompt="Perro jugando con una mariposa",
    seconds="4",
    size = "720x1280"
)

if video.status == "completed":
    content = client.videos.download_content(video.id, variant="video")
    content.write_to_file(output_filename)
    print(f"Video guardado en: {output_filename}")
else:
    print(f"La generación del video terminó con estado {video.status}. Error: {video.error}")