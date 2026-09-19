import asyncio, time, httpx

async def api_local_asincrona(email:str):
    print(f" -- ASINCRONO -- Buscando datos de email: {email}")
    await asyncio.sleep(2)
    return {"email": email, "nombre": "Usuario demo"}

async def atender_usuario_asinc(user_id: int, email:str):
    inicio = time.time()
    print(f"Usuario {user_id} inicia consulta")
    await api_local_asincrona(email)
    tiempo_total = time.time() - inicio
    print(f"Usuario {user_id} atendido en {tiempo_total:.2f}s")


async def demo_asincrona():
    print("EJECUTANDO DEMO SINCRONA")
    inicio_total = time.time()
    await asyncio.gather(
        atender_usuario_asinc(1, "usuario1@gmail.com"),
        atender_usuario_asinc(2, "usuario2@gmail.com")
    ) 


    print(f"TOTAL TIEMPO ASINCRONO: {time.time() - inicio_total:.2f} segundos")


if __name__ == "__main__":
    asyncio.run(demo_asincrona())