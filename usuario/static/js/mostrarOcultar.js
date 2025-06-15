function crearFilaUsuario(usuario) {
  const fila = document.createElement('tr');
  const colorClase = usuario.activo ? 'rojo' : 'verde';
  const accionTexto = usuario.activo ? 'Desactivar Usuario' : 'Activar Usuario';

  let botones = '';

  if (usuario.activo) {
    botones += `
      <button class="btn verde" title="Editar contraseña" onclick="abrirModalContrasenia('${usuario.nikname}')">⋯</button>
      <button class="btn verde" title="Editar usuario" onclick="abrirModalUsuario(${usuario.idUsuario})">
        <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 10 10" fill="none">
          <path d="M9.83752 2.24552C10.0542 2.02888 10.0542 1.66782 9.83752 1.4623L8.5377 0.162477C8.33218 -0.0541591 7.97112 -0.0541591 7.75448 0.162477L6.7324 1.179L8.81544 3.26205M0 7.91696V10H2.08304L8.22664 3.85085L6.14359 1.76781L0 7.91696Z" fill="#FBFBFB"/>
        </svg>
      </button>
    `;
  }

  botones += `
    <button class="btn ${colorClase}" title="${accionTexto}" onclick="cambiarEstadoUsuario(${usuario.idUsuario})">🚫</button>
  `;

  fila.innerHTML = `
    <td>${usuario.idUsuario}</td>
    <td>${usuario.nikname}</td>
    <td>${usuario.empleado}</td>
    <td>${usuario.mail}</td>
    <td>${usuario.rol}</td>
    <td>${botones}</td>
  `;

  return fila;
}
