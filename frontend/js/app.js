
const API_URL = "http://127.0.0.1:8000/miembros/";

async function cargarMiembros() {
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error("Error al cargar miembros");
    const miembros = await res.json();

    const tabla = document.getElementById("tablaMiembros");
    tabla.innerHTML = "";

    miembros.forEach((m) => {
      tabla.innerHTML += `
        <tr>
          <td>${m.id}</td>
          <td>${m.nombre}</td>
          <td>${m.especialidad || "—"}</td>
          <td>${m.estado}</td>
          <td>
            <button onclick="editarMiembro(${m.id}, '${m.nombre}', '${m.especialidad || ""}', '${m.estado}')">✏️ Editar</button>
            <button onclick="eliminarMiembro(${m.id})">🗑️ Eliminar</button>
          </td>
        </tr>`;
    });
  } catch (error) {
    console.error(error);
    alert("No se pudo obtener la lista de miembros.");
  }
}

document.getElementById("formMiembro").addEventListener("submit", async (e) => {
  e.preventDefault();

  const id = document.getElementById("miembroId").value;
  const nombre = document.getElementById("nombre").value.trim();
  const especialidad = document.getElementById("especialidad").value.trim();
  const estado = document.getElementById("estado").value;

  const miembro = { nombre, especialidad, estado };
  const method = id ? "PUT" : "POST";
  const url = id ? `${API_URL}${id}` : API_URL;

  try {
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(miembro),
    });

    if (!res.ok) throw new Error("Error al guardar miembro");

    await cargarMiembros();
    resetForm();
  } catch (error) {
    console.error(error);
    alert("Error al guardar miembro");
  }
});

function editarMiembro(id, nombre, especialidad, estado) {
  document.getElementById("miembroId").value = id;
  document.getElementById("nombre").value = nombre;
  document.getElementById("especialidad").value = especialidad;
  document.getElementById("estado").value = estado;
}

async function eliminarMiembro(id) {
  if (!confirm("¿Deseas eliminar este miembro?")) return;

  try {
    const res = await fetch(`${API_URL}${id}?confirm=true`, { method: "DELETE" });
    if (!res.ok) throw new Error("Error al eliminar miembro");
    await cargarMiembros();
  } catch (error) {
    console.error(error);
    alert("Error al eliminar miembro.");
  }
}


function resetForm() {
  document.getElementById("miembroId").value = "";
  document.getElementById("nombre").value = "";
  document.getElementById("especialidad").value = "";
  document.getElementById("estado").value = "Activo";
}


window.onload = cargarMiembros;
