import os
from datetime import datetime

RUTA_REPORTE = os.path.join(os.getcwd(), "reportes_generados")
os.makedirs(RUTA_REPORTE, exist_ok=True)

def generar_reporte_txt(proyectos, proyectos_eliminados, miembros_eliminados):
    """
    Genera un reporte consolidado en formato TXT con información de:
      - Proyectos activos y eliminados
      - Miembros eliminados
    El archivo se guarda en /reportes_generados y se devuelve su ruta.
    """

    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nombre_archivo = f"reporte_gestion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    ruta_archivo = os.path.join(RUTA_REPORTE, nombre_archivo)

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("=== REPORTE DE GESTIÓN - MAN_GUITO ===\n")
        archivo.write(f"Fecha de generación: {fecha_actual}\n\n")

        archivo.write("=== PROYECTOS ACTIVOS ===\n")
        if proyectos:
            for p in proyectos:
                archivo.write(f"- {p.nombre} | Estado: {p.estado} | Presupuesto: ${p.presupuesto}\n")
        else:
            archivo.write("No hay proyectos activos registrados.\n")
        archivo.write("\n")

        archivo.write("=== PROYECTOS ELIMINADOS ===\n")
        if proyectos_eliminados:
            for p in proyectos_eliminados:
                archivo.write(f"- {p.nombre} (Eliminado)\n")
        else:
            archivo.write("No hay proyectos eliminados.\n")
        archivo.write("\n")

        archivo.write("=== MIEMBROS ELIMINADOS ===\n")
        if miembros_eliminados:
            for m in miembros_eliminados:
                archivo.write(f"- {m.nombre} | Especialidad: {m.especialidad} | Estado: {m.estado}\n")
        else:
            archivo.write("No hay miembros eliminados.\n")

        archivo.write("\n=== FIN DEL REPORTE ===\n")

    return ruta_archivo
