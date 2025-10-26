const API = (p) => (p.startsWith('/') ? p : '/' + p);

async function api(path, opts={}) {
  const r = await fetch(API(path), { headers: { 'Content-Type': 'application/json' }, ...opts });
  if (!r.ok) { const e = await r.json().catch(()=>({detail:r.statusText})); throw new Error(e.detail || 'Error'); }
  return r.json().catch(()=> ({}));
}


async function crearMiembro(d){ return api('/api/miembros/', {method:'POST', body:JSON.stringify(d)}); }
async function listarMiembros(q={}){ const p=new URLSearchParams(q).toString(); return api('/api/miembros/' + (p?`?${p}`:'')); }
async function eliminarMiembro(id){ const r=await fetch(`/api/miembros/${id}`,{method:'DELETE'}); if(!r.ok){const j=await r.json(); throw new Error(j.detail);} }


async function crearProyecto(d){ return api('/api/proyectos/', {method:'POST', body:JSON.stringify(d)}); }
async function listarProyectos(q={}){ const p=new URLSearchParams(q).toString(); return api('/api/proyectos/' + (p?`?${p}`:'')); }
async function eliminarProyecto(id){ const r=await fetch(`/api/proyectos/${id}`,{method:'DELETE'}); if(!r.ok){const j=await r.json(); throw new Error(j.detail);} }


async function asignar(d){ return api('/api/asignaciones/', {method:'POST', body:JSON.stringify(d)}); }
async function desasignar(id){ const r=await fetch(`/api/asignaciones/${id}`,{method:'DELETE'}); if(!r.ok){const j=await r.json(); throw new Error(j.detail);} }


function el(q){ return document.querySelector(q); }
function mount(id, arr, render){ const c=el(id); c.innerHTML = arr.map(render).join(''); }


async function dashboardResumen(){
  try{
    const [proys, miembros] = await Promise.all([listarProyectos(), listarMiembros()]);
    const activos = proys.filter(p=>p.estado==='en_progreso').length;
    const finalizados = proys.filter(p=>p.estado==='finalizado').length;
    const presupuesto = proys.reduce((s,p)=>s+(p.presupuesto||0),0);
    el('#kpi-proy').textContent = proys.length;
    el('#kpi-act').textContent = activos;
    el('#kpi-fin').textContent = finalizados;
    el('#kpi-pres').textContent = `$${presupuesto.toFixed(2)}`;
    el('#kpi-miem').textContent = miembros.length;
  }catch(e){
    console.error(e);
  }
}

window.PMG = { crearMiembro, listarMiembros, eliminarMiembro, crearProyecto, listarProyectos, eliminarProyecto, asignar, desasignar, el, mount, dashboardResumen };
