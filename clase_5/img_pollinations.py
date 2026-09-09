import requests, os
from dotenv import load_dotenv

load_dotenv()

def generate_pollination_image(prompt:str, file_name:str, output_folder:str = "images") -> str:
    
    # 1. Definir las rutas de las carpetas
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, output_folder)
    
    # 2. Crear el directorio de destino en caso de que no exista
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, file_name)
    
    #3 Llamamos al endpoint de pollinations ai
    pollinations_base_url = os.getenv("POLLINATIONS_BASE_URL")
    url = f"{pollinations_base_url}{prompt}"
    print(f"URL: {url}")
    response = requests.get(url, timeout=60)
    
    response.raise_for_status() # HTTPError en caso de que la request no sea exitosa
    
    with open(output_path, "wb") as f:
        f.write(response.content)
    
    return output_path

if __name__ == "__main__":
    prompt_example = "moon crashes Earth"
    saved_path = generate_pollination_image(
        prompt=prompt_example, 
        file_name="moon_crashes_earth.jpg",
        output_folder="images"
    )
    print(f"Imagen guardada exitosamente en {saved_path}")