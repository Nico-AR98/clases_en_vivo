'''
Ejercicio 5
Objetivo del Ejercicio

Crear un script en Python que interactúe con la API para consultar usuarios, filtrar publicaciones (posts), procesar los datos utilizando estructuras de Python y manejar posibles errores de red.

Realiza una petición GET al endpoint: https://jsonplaceholder.typicode.com/users

Requisitos:

A. Valida que el código de estado (status_code) sea 200 antes de procesar la información.

B. Imprime en consola el nombre y el correo electrónico de cada usuario obtenido.
'''

import requests

response = requests.get("https://jsonplaceholder.typicode.com/users")

if response.status_code == 200:
    users = response.json()
    for user in users:
        print(f"Nombre: {user['name']}, Correo: {user['email']}")
else:
    print("Error al obtener los usuarios.")