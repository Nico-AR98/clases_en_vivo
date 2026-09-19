import requests, time

def api_local_sincrona(email:str):
    print(f" -- SINCRONO -- Buscando datos de email: {email}")
    time.sleep(2)
    return {"email": email, "nombre": "Usuario demo"}

def atender_usuario_sinc(user_id: int, email:str):
    inicio = time.time()
    print(f"Usuario {user_id} inicia consulta")
    api_local_sincrona(email)
    tiempo_total = time.time() - inicio
    print(f"Usuario {user_id} atendido en {tiempo_total:.2f}s")


def demo_sincrona():
    print("EJECUTANDO DEMO SINCRONA")
    inicio_total = time.time()

    atender_usuario_sinc(1, "usuario1@gmail.com")
    atender_usuario_sinc(2, "usuario2@gmail.com")

    print(f"TOTAL TIEMPO SINCRONO: {time.time() - inicio_total:.2f} segundos")


if __name__ == "__main__":
    demo_sincrona()