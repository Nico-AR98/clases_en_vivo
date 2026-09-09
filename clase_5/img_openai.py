import os, requests, base64
from openai import OpenAI
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY_OPENAI")
MODEL = os.getenv("MODEL_IMAGE_OPENAI")

client = OpenAI(api_key=API_KEY)

response = client.responses.create(
    model=MODEL,
    input="Generate an image of gray cat hugging an other with red scarf",
    tools=[{"type": "image_generation"}]
)

image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]

if image_data:
    image_base64 = image_data[0]
    with open("other.png", "wb") as f:
        f.write(base64.b64decode(image_base64))


# librerias: openai==3.9.0
# pillow==12.3.0
# sniffio==1.3.1