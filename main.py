from nicegui import ui

def calculoIMC():
    try:
        # 1. Obtener datos
        peso_num = float(peso.value)
        altura_num = float(altura.value)

        # 2. Calcular IMC
        imc = peso_num / (altura_num ** 2)

        # 3. Mostrar IMC
        resultado.text = f'Tu IMC es: {imc:.2f}'

        # 4. Evaluar resultado
        if imc < 18.5:
            mensaje_texto = "Actualmente estás bajo de peso"

        elif 18.5 <= imc <= 24.9:
            mensaje_texto = "Tu peso es normal"

        elif 25 <= imc <= 30:
            mensaje_texto = "Tienes sobrepeso"

        else:
            mensaje_texto = "Tienes obesidad"

        # 5. Mostrar mensaje
        mensaje.text = mensaje_texto

    except:
        resultado.text = "Ingresa números válidos"
        mensaje.text = ""

def limpiar():
    peso.value = ''
    altura.value = ''
    resultado.text = 'Resultado: 0'
    mensaje.text = ''

with ui.column().classes(
    'w-full h-screen items-center justify-center'
):

    with ui.card().style(
        'width:400px; background-color:#08233B;'
    ).classes('items-center'):

        ui.label(
            'Mi calculadora de IMC'
        ).style(
            'color:white; font-size:30px; font-weight:bold'
        )
        
        ui.image(
            'imc.PNG'
        ).style('width:250px')

        peso = ui.input('Ingresa tu peso en Kg').props(
            'dark outlined'
        ).style(
            'width:320px'
        )

        altura = ui.input('Ingresa tu estatura en metros').props(
            'dark outlined'
        ).style(
            'width:320px'
        )

        with ui.row().classes('w-full justify-center no-wrap').style('gap:24px'):

            ui.button(
                'Calcular IMC',
                icon='calculate',
                color='green',
                on_click=calculoIMC
            ).style(
                'color:white; width:140px'
            )

            ui.button(
                'LIMPIAR',
                icon='delete',
                color='red',
                on_click=limpiar
            ).style(
                'color:white; width:140px'
            )

        resultado = ui.label(
            'Resultado: 0'
        ).style(
            'color:white; font-size:20px'
        )

        mensaje = ui.label(
            ''
        ).style(
            'color:cyan; font-size:18px'
        )

ui.run()