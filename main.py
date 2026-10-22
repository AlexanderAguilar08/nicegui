import os
from nicegui import ui

datos = []

columnas = [
    {"name": "nombre", "label": "Alumno", "field": "nombre"},
    {"name": "calificacion", "label": "Calificación", "field": "calificacion"},
]

def actualizar_grafica():
    nombres = [d["nombre"] for d in datos]
    calificaciones = [d["calificacion"] for d in datos]

    # Tu código original para la gráfica de barras
    grafica.options["xAxis"]["data"] = nombres
    grafica.options["series"][0]["data"] = calificaciones
    grafica.update()

    # NUEVO: Actualizar la gráfica circular
    grafica_circular.options["series"][0]["data"] = [
        {"name": d["nombre"], "value": d["calificacion"]} for d in datos
    ]
    grafica_circular.update()

    # NUEVO: Calcular y mostrar promedio, máxima y mínima
    if calificaciones:
        prom = sum(calificaciones) / len(calificaciones)
        lbl_promedio.text = f"Promedio: {prom:.2f}"
        lbl_maxima.text = f"Calificación máxima: {max(calificaciones)}"
        lbl_minima.text = f"Calificación mínima: {min(calificaciones)}"

def registrar():
    if not nombre.value or calificacion.value is None:
        ui.notify("Completa todos los campos")
        return

    datos.append({
        "nombre": nombre.value,
        "calificacion": calificacion.value
    })

    tabla.rows = datos
    tabla.update()
    actualizar_grafica()
    ui.notify("Alumno registrado")

    nombre.value = ""
    calificacion.value = None

with ui.column().classes("w-full items-center"):
    ui.label("Registro de Calificaciones").style(
        "font-size: 28px; font-weight: bold"
    )

    nombre = ui.input("Nombre del alumno").style("width: 320px")
    calificacion = ui.number("Calificación").style("width: 320px")

    ui.button("Registrar", on_click=registrar)

    # NUEVO: Etiquetas solicitadas por el reto
    lbl_promedio = ui.label("Promedio: -")
    lbl_maxima = ui.label("Calificación máxima: -")
    lbl_minima = ui.label("Calificación mínima: -")

    tabla = ui.table(columns=columnas, rows=datos).style("width: 520px")

    grafica = ui.echart({
        "xAxis": {"type": "category", "data": []},
        "yAxis": {"type": "value"},
        "series": [{
            "type": "bar",
            "data": []
        }]
    }).style("width: 520px; height: 320px")

    # NUEVO: Gráfica circular solicitada por el reto
    grafica_circular = ui.echart({
        "series": [{
            "type": "pie",
            "data": []
        }]
    }).style("width: 520px; height: 320px")

ui.run(
    host='0.0.0.0',
    port=int(os.environ.get('PORT', 8080))
)