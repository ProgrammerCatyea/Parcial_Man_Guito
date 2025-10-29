
const API_URL = "http://127.0.0.1:8000";

async function eliminarElemento(tipo, id) {
    const confirmar = confirm(`¿Estás seguro de que deseas eliminar este ${tipo}?`);
    if (!confirmar) return;

    try {
        const response = await fetch(`${API_URL}/${tipo}/${id}?confirm=true`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.mensaje || `${tipo} eliminado correctamente.`);
            location.reload();
        } else {
            alert(data.detail || data.mensaje || 'Error al eliminar.');
        }
    } catch (error) {
        console.error(error);
        alert('Error de conexión con el servidor.');
    }
}


async function cargarDatos(tipo, contenedorId) {
    try {
        const response = await fetch(`${API_URL}/${tipo}`);
        const data = await response.json();
        const contenedor = document.getElementById(contenedorId);
        contenedor.innerHTML = "";

        data.forEach(item => {
            const fila = document.createElement("tr");
            fila.innerHTML = `
                <td>${item.id}</td>
                <td>${item.nombre || item.titulo}</td>
                <td>${item.estado || 'N/A'}</td>
                <td>
                    <button onclick="eliminarElemento('${tipo}', ${item.id})" class="btn btn-danger btn-sm">Eliminar</button>
                </td>
            `;
            contenedor.appendChild(fila);
        });
    } catch (error) {
        console.error(error);
        alert("Error al cargar los datos desde el servidor.");
    }
}

function descargarReporte() {
    fetch("http://127.0.0.1:8000/reportes/generar")
        .then(response => {
            if (!response.ok) throw new Error("Error al generar el reporte");
            return response.blob();
        })
        .then(blob => {
            const enlace = document.createElement("a");
            enlace.href = URL.createObjectURL(blob);
            enlace.download = "reporte_general.txt";
            enlace.click();
        })
        .catch(error => alert("No se pudo generar el reporte: " + error.message));
}

