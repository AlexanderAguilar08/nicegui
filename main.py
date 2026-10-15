import json
import os
import re

from dotenv import load_dotenv
from nicegui import ui
from ollama import AsyncClient

load_dotenv()

# Usar el modelo correcto y apuntar el host directamente a la nube
MODELO = os.getenv('OLLAMA_MODEL', 'gemma4:31b-cloud')

# Configuramos el cliente para que use la API en la nube y mande tu llave de autenticación
cliente_ollama = AsyncClient(
    host=os.getenv('OLLAMA_HOST', 'https://api.ollama.com'),
    headers={'Authorization': f"Bearer {os.getenv('OLLAMA_API_KEY')}"}
)

ultima_respuesta = ''


def sin_markdown(texto: str) -> str:
    """Quita el formato Markdown para que suene bien al leerlo."""
    texto = re.sub(r'```.*?```', ' ', texto, flags=re.DOTALL)
    texto = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', texto)
    return re.sub(r'[`*_#>~-]', ' ', texto)


async def leer() -> None:
    """Lee la última respuesta con la voz del navegador."""
    if not ultima_respuesta:
        ui.notify('Todavía no hay respuesta para leer.', type='warning')
        return

    await ui.run_javascript(f'''
        if (!('speechSynthesis' in window)) return false;
        speechSynthesis.cancel();
        const mensaje = new SpeechSynthesisUtterance({json.dumps(sin_markdown(ultima_respuesta), ensure_ascii=False)});
        mensaje.lang = 'es-MX';
        speechSynthesis.speak(mensaje);
        return true;
    ''')


async def detener() -> None:
    """Detiene la lectura que esté reproduciendo el navegador."""
    await ui.run_javascript('speechSynthesis?.cancel()')


async def enviar() -> None:
    """Envía la pregunta a Ollama y muestra la respuesta en la interfaz."""
    global ultima_respuesta

    texto = (entrada.value or '').strip()
    if not texto:
        ui.notify('Escribe una pregunta antes de enviarla.', type='warning')
        return

    boton.disable()
    resultado.set_content('⏳ Pensando...')
    try:
        respuesta = await cliente_ollama.chat(
            model=MODELO,
            messages=[{'role': 'user', 'content': texto}],
        )
        ultima_respuesta = respuesta.message.content or '(El modelo no devolvió texto)'
        resultado.set_content(ultima_respuesta)
        entrada.set_value('')
    except Exception as error:
        resultado.set_content(f'❌ Error: {error}')
    finally:
        boton.enable()


with ui.card().classes('w-full max-w-2xl mx-auto mt-8'):
    ui.label('🤖 Mi primer chatbot').classes('text-xl font-bold')
    entrada = ui.input(placeholder='Escribe algo').classes('w-full')
    with ui.row():
        boton = ui.button('Enviar', on_click=enviar, icon='send')
        ui.button('Leer respuesta', on_click=leer, icon='volume_up')
        ui.button('Detener', on_click=detener, icon='stop')
    entrada.on('keydown.enter', enviar)
    resultado = ui.markdown('').classes('w-full whitespace-pre-wrap')


puerto = int(os.getenv('PORT', os.getenv('NICEGUI_PORT', '8080')))
ui.run(title='Mi primer chatbot', port=puerto, host='0.0.0.0', storage_secret='secret')