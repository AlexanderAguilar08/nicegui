from nicegui import ui

canciones = [
    'best.mp3',
    'oia.mp3',
    'UIA.mp3',
    'Corazón_Frío.mp3',
    'Trellas.mp3',
    'Morritas.mp3'
]

indice = 0
audio = None
titulo = None
visualizador = None


def activar_visualizador():
    visualizador.style('display:block')

    ui.run_javascript('''
        document.querySelectorAll(".visualizer div").forEach(barra => {
            barra.style.animationPlayState = "running";
        });
    ''')


def pausar_visualizador():
    ui.run_javascript('''
        document.querySelectorAll(".visualizer div").forEach(barra => {
            barra.style.animationPlayState = "paused";
        });
    ''')


def ocultar_visualizador():
    visualizador.style('display:none')


def cambiar_cancion(nuevo_indice):
    global indice
    indice = nuevo_indice
    audio.set_source(canciones[indice])
    titulo.text = canciones[indice]
    audio.play()
    activar_visualizador()


def cambiar_volumen(e):
    ui.run_javascript(f'''
        document.querySelector("audio").volume = {e.value / 100};
    ''')


def detener():
    audio.pause()
    ui.run_javascript('document.querySelector("audio").currentTime = 0;')
    ocultar_visualizador()


def pausar():
    audio.pause()
    pausar_visualizador()


def reproducir():
    titulo.text = canciones[indice]
    audio.set_source(canciones[indice])
    audio.play()
    activar_visualizador()


def siguiente():
    global indice
    indice = (indice + 1) % len(canciones)
    reproducir()


def anterior():
    global indice
    indice = (indice - 1) % len(canciones)
    reproducir()


with ui.column().classes('w-full h-screen items-center justify-center'):

    with ui.card().style(
        'width:600px; background-color:#96D5FF; padding:25px'
    ).classes('items-center'):

        ui.label("Music A1").style(
            'color:withe; font-size:28px; font-weight:bold'
        )

        titulo = ui.label(canciones[indice]).style()

        visualizador = ui.html('''
<div class="visualizer">
  <div></div>
  <div></div>
  <div></div>
  <div></div>
  <div></div>
  <div></div>
  <div></div>
</div>

<style>
.visualizer {
  display: flex;
  gap: 6px;
  align-items: end;
  height: 90px;
  margin: 20px;
}

.visualizer div {
  width: 14px;
  height: 25px;
  border-radius: 8px;
  background: linear-gradient(cyan, purple);
  animation: audioMove 0.8s infinite ease-in-out;
  animation-play-state: paused;
}

.visualizer div:nth-child(2) { animation-delay: 0.1s; }
.visualizer div:nth-child(3) { animation-delay: 0.2s; }
.visualizer div:nth-child(4) { animation-delay: 0.3s; }
.visualizer div:nth-child(5) { animation-delay: 0.4s; }
.visualizer div:nth-child(6) { animation-delay: 0.5s; }
.visualizer div:nth-child(7) { animation-delay: 0.6s; }

@keyframes audioMove {
  0%, 100% {
    height: 20px;
  }

  50% {
    height: 90px;
  }
}
</style>
''').style('display:none')

        for i, cancion in enumerate(canciones):
            ui.button(
                cancion,
                icon='music_note',
                color='Azure ',
                on_click=lambda i=i: cambiar_cancion(i)
            ).style('color:black; width:250px')

        audio = ui.audio(canciones[indice]).style('display:none')

        with ui.row().classes('justify-center no-wrap').style('gap:10px'):
            ui.button(
                'Anterior',
                icon='skip_previous',
                color='darkblue',
                on_click=anterior
            ).style('color:white')

            ui.button(
                'Play',
                icon='play_arrow',
                color='green',
                on_click=reproducir
            ).style('color:white')

            ui.button(
                'Pause',
                icon='pause',
                color='yellow',
                on_click=pausar
            ).style('color:white')

            ui.button(
                'Detener',
                icon='stop',
                color='salmon',
                on_click=detener
            ).style('color:white')

            ui.button(
                'Siguiente',
                icon='skip_next',
                color='darkblue',
                on_click=siguiente
            ).style('color:white')

        ui.label('Volumen').style('color:black')

        ui.slider(
            min=0,
            max=100,
            value=80,
            on_change=cambiar_volumen
        ).style('width:250px')


ui.run()