const API_PROYECTOS = "http://127.0.0.1:8000/proyectos/";

async function descargarReporteProyectosActivos() {
  try {
    const res = await fetch(`${API_PROYECTOS}reporte`);
    if (!res.ok) throw new Error("No se pudo generar el reporte");
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "reporte_proyectos_activos.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  } catch (e) {
    console.error(e);
    alert("Error generando el reporte de proyectos activos.");
  }
}


const btnRep = document.getElementById("btnReporteProyectos");
if (btnRep) btnRep.addEventListener("click", descargarReporteProyectosActivos);


async function guardarProyectoDesdeFormulario(e) {
  e.preventDefault();
  const id = document.getElementById("proyectoId").value;
  const payload = {
    nombre: document.getElementById("p_nombre").value.trim(),
    descripcion: document.getElementById("p_descripcion").value.trim(),
    estado: document.getElementById("p_estado").value,           
    presupuesto: parseFloat(document.getElementById("p_presupuesto").value),
    fecha_inicio: document.getElementById("p_fecha_inicio").value || null, 
    fecha_fin: document.getElementById("p_fecha_fin").value || null,
    id_gerente: document.getElementById("p_id_gerente").value ? parseInt(document.getElementById("p_id_gerente").value) : null,
  };

  const method = id ? "PUT" : "POST";
  const url = id ? `${API_PROYECTOS}${id}` : API_PROYECTOS;

  const res = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    console.error(err);
    return alert("Error guardando el proyecto");
  }

 
}
