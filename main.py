from nicegui import ui

encendido = False

def cambiar_estado():
    global encendido
    encendido = not encendido
    
    if encendido:
        estado.text = "Sistema: ACTIVO 🚀"
        estado.style('color: #00ffca; font-size: 26px; font-weight: bold')
        boton.set_text('Desactivar')
        boton.props('color=purple')
    else:
        estado.text = "Sistema: INACTIVO 💤"
        estado.style('color: #ff0055; font-size: 26px; font-weight: bold')
        boton.set_text('Activar')
        boton.props('color=dark')

with ui.column().classes('w-full h-screen items-center justify-center'):
    # Tarjeta personalizada con color de fondo y sombra diferente
    with ui.card().style(
        'width:320px; background-color:#1e1e2e; color:white; border-radius:15px;'
    ).classes('items-center p-5'):

        ui.label('Control de Estado').style(
            'font-size: 26px; font-weight: bold'
        )

        ui.image(
            'nice.png'
        ).style('width:230px')

        estado = ui.label(
            "Sistema: INACTIVO 💤"
        ).style(
            'color: #ff0055; font-size: 26px; font-weight: bold'
        )

        boton = ui.button(
            'Activar',
            icon='power_settings_new',
            color='dark',
            on_click=cambiar_estado
        ).style('color: white')

ui.run()