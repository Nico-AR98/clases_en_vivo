"""Agente de atención al cliente (reclamos) con Gemini y function calling.

Toma como guía la estructura de assistant2.py (bucle de conversación por
consola) y de gemini_assistant.py (configuración y llamada al modelo).

En función del mensaje que el usuario envíe, el agente decide si debe:
    - calcular un reintegro por días sin servicio,
    - iniciar el recupero de contraseña, o
    - simplemente responder como representante de atención al cliente.

Variables de entorno (archivo .env):
    API_KEY_GEMINI    clave de la API de Gemini (obligatoria).
    MODEL_GEMINI      modelo a usar (obligatoria).
    ASSISTANT_NAME    nombre del asistente (opcional).
"""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  # Cargamos las variables de entorno desde el archivo .env

# Costo diario del servicio, usado para calcular los reintegros.
COSTO_DIARIO = 2160

# Palabras con las que el usuario puede terminar la conversación.
SALIDAS = {"salir", "exit", "quit", "chau"}

# Rol del sistema: define el comportamiento del agente y cómo debe estimar el
# índice de malestar a partir de la forma en que se expresa el cliente.
SYSTEM_ROLE = """
Sos un representante de atención al cliente de una empresa de servicio de
internet. Atendés en español, con un trato amable, empático y breve.

Tenés dos herramientas disponibles y debés usarlas según lo que pida el cliente:

1. calcular_reintegro: usala cuando el cliente reclame un reintegro o una
   compensación por días sin servicio. Necesitás dos datos:
   - dias_sin_servicio: los días que el cliente estuvo sin servicio. Si no los
     menciona, preguntáselos antes de usar la herramienta.
   - indice_malestar: estimalo vos según el tono del mensaje, entre 1.0 y 2.0.
     1.0 = cliente tranquilo, informa el problema sin queja;
     1.3 = molesto pero cordial;
     1.6 = claramente enojado, insiste o reclama con firmeza;
     2.0 = muy enojado: mayúsculas, insultos, amenaza con dar de baja el
     servicio o con hacer un reclamo formal.

2. recuperar_contrasena: usala cuando el cliente no pueda entrar a su cuenta,
   haya olvidado la contraseña o pida restablecerla. Necesitás su correo
   electrónico; si no lo dio, pedíselo antes de usar la herramienta.

Después de usar una herramienta, explicale al cliente el resultado en lenguaje
natural. Si el mensaje no corresponde a ninguna de las dos herramientas,
respondé normalmente como representante de atención al cliente.
"""


def get_gemini_config():
    """Obtiene la configuración de Gemini desde las variables de entorno.

    Returns:
        dict: Diccionario con la api_key y el modelo a utilizar.
    """
    api_key = os.getenv("API_KEY_GEMINI")
    model = os.getenv("MODEL_GEMINI")

    # Validamos que las variables de entorno estén definidas
    if not api_key:
        raise ValueError("API_KEY_GEMINI no esta seteado en las variables de entorno.")
    if not model:
        raise ValueError("MODEL_GEMINI no esta seteado en las variables de entorno.")

    return {"api_key": api_key, "model": model}


# --------------------------------------------------------------------------- #
# Herramientas: funciones que el modelo puede invocar
# --------------------------------------------------------------------------- #

def calcular_reintegro(dias_sin_servicio: int, indice_malestar: float) -> dict:
    """Calcula el reintegro que le corresponde a un cliente por días sin servicio.

    El monto es: días sin servicio * costo diario del servicio * índice de
    insatisfacción del cliente.

    Args:
        dias_sin_servicio: Cantidad de días que el cliente estuvo sin servicio.
        indice_malestar: Índice de insatisfacción del cliente, de 1.0 (cliente
            tranquilo) a 2.0 (cliente muy molesto), estimado según la forma en
            que se expresa el cliente.

    Returns:
        dict: Detalle del cálculo con los días, el costo diario, el índice
            aplicado y el monto total del reintegro.
    """
    if dias_sin_servicio <= 0:
        raise ValueError("Los días sin servicio deben ser un número positivo.")

    # Acotamos el índice al rango válido para evitar reintegros desmedidos.
    indice = min(max(float(indice_malestar), 1.0), 2.0)

    monto = dias_sin_servicio * COSTO_DIARIO * indice

    print(
        f"[herramienta] calcular_reintegro -> {dias_sin_servicio} día(s) x "
        f"${COSTO_DIARIO} x índice {indice} = ${monto:,.2f}"
    )

    return {
        "dias_sin_servicio": dias_sin_servicio,
        "costo_diario": COSTO_DIARIO,
        "indice_malestar": indice,
        "monto_reintegro": round(monto, 2),
    }


def recuperar_contrasena(email: str) -> dict:
    """Inicia el recupero de contraseña enviando un mail a la casilla del cliente.

    Args:
        email: Casilla de correo del cliente, donde se envía el enlace de
            recuperación.

    Returns:
        dict: Confirmación del envío del correo de recuperación.
    """
    if "@" not in email:
        raise ValueError("El correo electrónico no es válido.")

    print(
        f"[herramienta] recuperar_contrasena -> Se ha enviado un mail a la "
        f"casilla {email} con las instrucciones para restablecer la contraseña."
    )

    return {"email": email, "estado": "mail de recuperación enviado"}


# Herramientas que se le pasan al modelo. Gemini las invoca automáticamente
# cuando el mensaje del usuario lo requiere (automatic function calling).
HERRAMIENTAS = [calcular_reintegro, recuperar_contrasena]


# --------------------------------------------------------------------------- #
# Agente
# --------------------------------------------------------------------------- #

# El cliente se guarda a nivel de módulo: si fuera una variable local, Python
# lo destruiría al salir de la función y cerraría la conexión con la API.
_gemini_client = None


def get_gemini_client(gemini_config=None):
    """Devuelve el cliente de Gemini, creándolo una sola vez por proceso."""
    global _gemini_client

    if _gemini_client is None:
        if gemini_config is None:
            gemini_config = get_gemini_config()
        _gemini_client = genai.Client(api_key=gemini_config["api_key"])

    return _gemini_client


def crear_chat(gemini_config=None):
    """Crea la sesión de chat con el rol y las herramientas del agente.

    Usamos un chat (y no una llamada suelta) para que el agente recuerde los
    turnos anteriores: así puede pedir un dato que falta y usarlo después.
    """
    if gemini_config is None:
        gemini_config = get_gemini_config()

    gemini_client = get_gemini_client(gemini_config)

    return gemini_client.chats.create(
        model=gemini_config["model"],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_ROLE,
            tools=HERRAMIENTAS,
            temperature=0.3,  # Poca creatividad: es atención al cliente
            max_output_tokens=1024,
        ),
    )


def atender_reclamo(chat, mensaje):
    """Envía el mensaje del cliente al agente y devuelve su respuesta."""
    if not mensaje.strip():
        raise ValueError("El mensaje no puede estar vacío")

    try:
        response = chat.send_message(mensaje.strip())
        return response.text
    except Exception as e:
        return f"Error al obtener la respuesta de Gemini: {e}"


def get_user_input():
    """Solicita un mensaje al usuario."""
    return input("Cliente: ")


def main():
    assistant_name = os.getenv("ASSISTANT_NAME", "Atención al Cliente")
    chat = crear_chat()

    print(f"{assistant_name}: ¡Hola! ¿En qué puedo ayudarte hoy?")
    print("(escribí 'salir' para terminar)\n")

    mensaje = ""
    while mensaje.strip().lower() not in SALIDAS:
        try:
            mensaje = get_user_input()
            if mensaje.strip().lower() in SALIDAS:
                break

            respuesta = atender_reclamo(chat, mensaje)
            print(f"{assistant_name}: {respuesta}\n")

        except (KeyboardInterrupt, EOFError):
            print(f"\n{assistant_name}: sesión finalizada.")
            break
        except Exception as error:
            # El programa no se detiene: informa el error y sigue atendiendo.
            print(f"Error controlado: {error}\n")

    print(f"{assistant_name}: Gracias por comunicarte. ¡Hasta luego!")


if __name__ == "__main__":
    main()
