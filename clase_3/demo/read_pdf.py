from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

# Ruta del archivo (relativa a este script, no al directorio de trabajo)
BASE_DIR = Path(__file__).parent
file_path = BASE_DIR / "fundamentos_de_la_generacion_multimedia.pdf"

# Cargar el PDF
loader = PyPDFLoader(str(file_path))

paginas = loader.load()

content = ""

for i, page in enumerate(paginas):
    content += f"\n{page.page_content}\n\n"

txt_file_path = BASE_DIR / "content.txt"

# Guardar el contenido en un archivo de texto
with open(txt_file_path, "w", encoding="utf-8") as txt_file:
    txt_file.write(content)

print(f"Contenido del PDF guardado en: {txt_file_path}")