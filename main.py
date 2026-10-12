import os
from dotenv import load_dotenv
from nicegui import ui
import ollama

# Cargar variables de entorno desde el archivo .env
load_dotenv()

MODELO = os.getenv('OLLAMA_MODEL', 'gemma4:31b-cloud')

# Historial del chat con instrucción de personalidad inicial
historial = [
    {
        'role': 'system',
        'content': 'Eres un asistente escolar amable, conciso y divertido que ayuda a estudiantes a aprender programación.'
    }
]

@ui.page('/')
def main_page():
    ui.label('🤖 Chatbot con Inteligencia Artificial').classes('text-2xl font-bold mb-4 text-primary')
    
    # Contenedor del chat
    contenedor_chat = ui.column().classes('w-full border p-4 mb-4 h-80 overflow-y-auto rounded-lg shadow-sm')

    # Mensaje de bienvenida inicial
    with contenedor_chat:
        ui.chat_message('¡Hola! :) Soy tu asistente de IA. ¿En qué te puedo ayudar hoy?', name='Asistente IA', stamp='Sistema')

    async def enviar_mensaje():
        texto_usuario = entrada.value.strip()
        if not texto_usuario:
            return

        # 1. Mostrar mensaje del usuario en pantalla
        with contenedor_chat:
            ui.chat_message(texto_usuario, name='Tú', sent=True)
        
        # Guardar en el historial
        historial.append({'role': 'user', 'content': texto_usuario})
        entrada.value = ''

        # 2. Consultar a Ollama Cloud
        try:
            respuesta = ollama.chat(
                model=MODELO,
                messages=historial
            )
            texto_respuesta = respuesta['message']['content']

            # Mostrar respuesta de la IA en pantalla
            with contenedor_chat:
                ui.chat_message(texto_respuesta, name='Asistente IA')

            # Guardar respuesta en el historial
            historial.append({'role': 'assistant', 'content': texto_respuesta})

        except Exception as e:
            with contenedor_chat:
                ui.chat_message(f'Error al conectar con la IA: {str(e)}', name='Sistema')

    # Campo de entrada y botón de enviar
    with ui.row().classes('w-full items-center gap-2'):
        entrada = ui.input(placeholder='Escribe tu pregunta aquí...').classes('flex-1').on('keydown.enter', enviar_mensaje)
        ui.button('Enviar', on_click=enviar_mensaje).props('color=primary')

# Ejecutar aplicación
puerto = int(os.getenv('NICEGUI_PORT', 8080))
ui.run(port=puerto)