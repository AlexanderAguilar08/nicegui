import os
from dotenv import load_dotenv
from nicegui import ui
from openai import OpenAI

load_dotenv()

# Configurar el cliente usando la librería openai para Ollama Cloud
client = OpenAI(
    base_url='https://api.ollama.com/v1',
    api_key='3979262d85ec4537836009107e7f98fe.OkUtwNmcrshRu8XDTPfQxz5M'
)

@ui.page('/')
def main_page():
    ui.label('🤖 Chatbot con Inteligencia Artificial').classes('text-2xl font-bold mb-4 text-primary')
    
    # Contenedor del chat
    contenedor_chat = ui.column().classes('w-full border p-4 mb-4 h-80 overflow-y-auto rounded-lg shadow-sm')

    with contenedor_chat:
        ui.chat_message('¡Hola! :) Soy tu asistente de IA. ¿En qué te puedo ayudar hoy?', name='Asistente IA', stamp='Sistema')

    async def enviar_mensaje():
        texto_usuario = entrada.value.strip()
        if not texto_usuario:
            return

        # 1. Mostrar mensaje del usuario
        with contenedor_chat:
            ui.chat_message(texto_usuario, name='Tú', sent=True)
        
        entrada.value = ''

        # 2. Definir personalidad (Reto Final) y mensaje del usuario
        messages = [
            {'role': 'system', 'content': 'Responde como un profesor amable de programación.'},
            {'role': 'user', 'content': texto_usuario},
        ]

        # 3. Consultar a Ollama Cloud con la librería openai
        try:
            respuesta = client.chat.completions.create(
                model='gemma4:31b',
                messages=messages
            )
            texto_respuesta = respuesta.choices[0].message.content

            # Mostrar respuesta de la IA
            with contenedor_chat:
                ui.chat_message(texto_respuesta, name='Asistente IA')

        except Exception as e:
            with contenedor_chat:
                ui.chat_message(f'Error al conectar con la IA: {str(e)}', name='Sistema')

    # Campo de entrada y botón
    with ui.row().classes('w-full items-center gap-2'):
        entrada = ui.input(placeholder='Escribe tu pregunta aquí...').classes('flex-1').on('keydown.enter', enviar_mensaje)
        ui.button('Enviar', on_click=enviar_mensaje).props('color=primary')

# Ejecutar aplicación
ui.run(port=8080)