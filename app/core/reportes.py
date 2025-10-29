import os
from datetime import datetime

def generar_reporte_eliminados(miembros, proyectos):
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"reporte_eliminados_{fecha}.txt"
    ruta_carpeta = os.path.join(os.getcwd(), "reportes")
    ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)

    os.makedirs(ruta_carpeta, exist_ok=True)

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write("===== REPORTE DE ELEMENTOS ELIMINADOS =====\n\n")

        f.write("---- MIEMBROS ELIMINADOS ----\n")
        if miembros:
            for m in miembros:
                f.write(f"ID: {m.id} | Nombre: {m.nombre} | Especialidad: {m.especialidad}\n")
        else:
            f.write("No hay miembros eliminados.\n")

        f.write("\n---- PROYECTOS ELIMINADOS ----\n")
        if proyectos:
            for p in proyectos:
                f.write(f"ID: {p.id} | Nombre: {p.nombre} | Presupuesto: {p.presupuesto}\n")
        else:
            f.write("No hay proyectos eliminados.\n")

        f.write("\nGenerado el: " + fecha + "\n")

    return ruta_archivo
