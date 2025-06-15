// Código JavaScript completo con manejo de errores desde decorador 'rol_requerido'

function initUsuarios() {
  const btnNuevoUsuario = document.getElementById("btnNuevoUsuario");
  const modalNuevoUsuario = document.getElementById("modalNuevoUsuario");
  const cerrarNuevoUsuario = document.getElementById("cerrarNuevoUsuario");
  const nombreEmpleadoInput = document.getElementById("nombreEmpleado");
  const idEmpleadoInput = document.getElementById("idEmpleado");

  if (btnNuevoUsuario && modalNuevoUsuario && cerrarNuevoUsuario) {
    btnNuevoUsuario.addEventListener("click", () => {
      modalNuevoUsuario.style.display = "flex";
    });

    cerrarNuevoUsuario.addEventListener("click", () => {
      modalNuevoUsuario.style.display = "none";
    });

    window.addEventListener("click", (e) => {
      if (e.target === modalNuevoUsuario) {
        modalNuevoUsuario.style.display = "none";
      }
    });
  }

  function verificarError(data) {
    if (data.error) {
      alert("Error: " + data.error);
      return true;
    }
    return false;
  }

  function cargarUsuarios() {
    fetch('/usuario/mostrar/')
      .then(res => res.json())
      .then(data => {
        if (verificarError(data)) return;
        const tbody = document.querySelector('.tablaUsu tbody');
        tbody.innerHTML = '';
        data.usuarios.forEach(usuario => {
          const fila = crearFilaUsuario(usuario);
          tbody.appendChild(fila);
        });
      })
      .catch(err => {
        console.error("Error al cargar usuarios:", err);
        alert("Hubo un error al cargar los usuarios.");
      });
  }

  function cargarUsuariosInactivos() {
    fetch('/usuario/methInactivos/')
      .then(res => res.json())
      .then(data => {
        if (verificarError(data)) return;
        const tbody = document.querySelector('.tablaUsu tbody');
        tbody.innerHTML = '';

        if (!data.usuarios || data.usuarios.length === 0) {
          const fila = document.createElement('tr');
          fila.innerHTML = `<td colspan="6">No hay usuarios inactivos.</td>`;
          tbody.appendChild(fila);
          return;
        }

        data.usuarios.forEach(usuario => {
          const fila = crearFilaUsuario(usuario);
          tbody.appendChild(fila);
        });
      })
      .catch(err => {
        console.error("Error al cargar usuarios inactivos:", err);
        alert("Error al cargar los usuarios inactivos.");
      });
  }

  function cargarUsuariosPorRol() {
    let input = document.getElementById("inputUsuario");
    if (input.value.trim() !== "") return;

    const idRol = document.getElementById("select1").value;
    if (!idRol) {
      alert("Debe seleccionar un rol");
      return;
    }

    fetch('/usuario/mostrarPorRol/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idRol: idRol })
    })
    .then(res => res.json())
    .then(data => {
      if (verificarError(data)) return;
      const tbody = document.querySelector('.tablaUsu tbody');
      tbody.innerHTML = '';
      data.usuarios.forEach(usuario => {
        const fila = crearFilaUsuario(usuario);
        tbody.appendChild(fila);
      });
    })
    .catch(err => {
      console.error("Error al cargar usuarios por rol:", err);
      alert("Hubo un error al obtener los usuarios.");
    });
  }

  function buscarUsu() {
    let input = document.getElementById("inputUsuario");
    if (input.value.trim() === "") return;

    fetch('/usuario/methbuscarUsu/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nikname: input.value })
    })
    .then(res => res.json())
    .then(data => {
      if (verificarError(data)) return;
      const tbody = document.querySelector('.tablaUsu tbody');
      tbody.innerHTML = '';
      const fila = crearFilaUsuario(data);
      tbody.appendChild(fila);
    })
    .catch(err => {
      console.error("Error al buscar usuario:", err);
      alert("Hubo un error al buscar el usuario.");
    });

    input.value = "";
  }

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

document.addEventListener("DOMContentLoaded", () => {
  initUsuarios();
  mostrarNombreUsuario();  
});

  cargarUsuarios();

  document.getElementById("inactivos").addEventListener("click", cargarUsuariosInactivos);
  document.getElementById("busc").addEventListener("click", function() {
    cargarUsuariosPorRol();
    buscarUsu();
  });
}

document.addEventListener("DOMContentLoaded", initUsuarios);



/*
function initUsuarios() {
  const btnNuevoUsuario = document.getElementById("btnNuevoUsuario");
  const modalNuevoUsuario = document.getElementById("modalNuevoUsuario");
  const cerrarNuevoUsuario = document.getElementById("cerrarNuevoUsuario");
  const nombreEmpleadoInput = document.getElementById("nombreEmpleado");
  const idEmpleadoInput = document.getElementById("idEmpleado");

  if (btnNuevoUsuario && modalNuevoUsuario && cerrarNuevoUsuario) {
    btnNuevoUsuario.addEventListener("click", () => {
      modalNuevoUsuario.style.display = "flex";
    });

    cerrarNuevoUsuario.addEventListener("click", () => {
      modalNuevoUsuario.style.display = "none";
    });

    window.addEventListener("click", (e) => {
      if (e.target === modalNuevoUsuario) {
        modalNuevoUsuario.style.display = "none";
      }
    });
  }

  function cargarUsuarios() {
    fetch('/usuario/mostrar/')
      .then(res => res.json())
      .then(data => {
        const tbody = document.querySelector('.tablaUsu tbody');
        tbody.innerHTML = '';

        data.usuarios.forEach(usuario => {
          const fila = document.createElement('tr');
          const colorClase = usuario.activo ? 'rojo' : 'verde';
          const accionTexto = usuario.activo ? 'Desactivar Usuario' : 'Activar Usuario';

          let botones = `
            <button class="btn verde" title="Editar contraseña" onclick="abrirModalContrasenia('${usuario.nikname}')">⋯</button>
            <button class="btn verde" title="Editar usuario" onclick="abrirModalUsuario(${usuario.idUsuario})">
              <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 10 10" fill="none">
                <path d="M9.83752 2.24552C10.0542 2.02888 10.0542 1.66782 9.83752 1.4623L8.5377 0.162477C8.33218 -0.0541591 7.97112 -0.0541591 7.75448 0.162477L6.7324 1.179L8.81544 3.26205M0 7.91696V10H2.08304L8.22664 3.85085L6.14359 1.76781L0 7.91696Z" fill="#FBFBFB"/>
              </svg>
            </button>
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

          tbody.appendChild(fila);
        });
      })
      .catch(err => console.error("Error al cargar usuarios:", err));
  }

  function cargarUsuariosInactivos() {
    const tbody = document.querySelector('.tablaUsu tbody');
    tbody.innerHTML = '';

    fetch('/usuario/methInactivos/')
      .then(res => res.json())
      .then(data => {
        if (!data.usuarios || data.usuarios.length === 0) {
          const fila = document.createElement('tr');
          fila.innerHTML = `<td colspan="6">No hay usuarios inactivos.</td>`;
          tbody.appendChild(fila);
          return;
        }

        data.usuarios.forEach(usuario => {
          const fila = document.createElement('tr');
          const colorClase = usuario.activo ? 'rojo' : 'verde';
          const accionTexto = usuario.activo ? 'Desactivar Usuario' : 'Activar Usuario';

          let botones = `
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

          tbody.appendChild(fila);
        });
      })
      .catch(err => console.error("Error al cargar usuarios inactivos:", err));
  }

  function cargarUsuariosPorRol() {
    const idRol = document.getElementById("select1").value;

    if (!idRol) {
      alert("Debe seleccionar un rol");
      return;
    }

    const tbody = document.querySelector('.tablaUsu tbody');
    tbody.innerHTML = '';

    fetch('/usuario/mostrarPorRol/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idRol: idRol })
    })
      .then(res => res.json())
      .then(data => {
        data.usuarios.forEach(usuario => {
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

          tbody.appendChild(fila);
        });
      })
      .catch(err => {
        console.error("Error al cargar usuarios por rol:", err);
        alert("Hubo un error al obtener los usuarios.");
      });
  }

  window.cambiarEstadoUsuario = function (idUsuario) {
    fetch('/usuario/methActivar/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idUsuario })
    })
      .then(res => res.json())
      .then(() => cargarUsuarios())
      .catch(err => console.error("Error al cambiar estado:", err));
  };

  window.abrirModalContrasenia = function (username) {
    const modal = document.getElementById("modal");
    const btn = document.getElementById("btnGuardarContrasenia");
    if (modal && btn) {
      btn.dataset.username = username;
      modal.style.display = "flex";
    }
  };

  window.abrirModalUsuario = function (idUsuario) {
    const modal = document.getElementById("modalUsuario");
    const inputId = document.getElementById("idEditarUsuario");
    const inputUsuario = document.getElementById("usuario");
    const selectRol = document.getElementById("rolEditarUsuario");

    const fila = [...document.querySelectorAll(".tablaUsu tbody tr")]
      .find(row => row.children[0].textContent === idUsuario.toString());

    if (fila) {
      const nikname = fila.children[1].textContent;
      const rolTexto = fila.children[4].textContent;

      inputId.value = idUsuario;
      inputUsuario.value = nikname;

      [...selectRol.options].forEach(opt => {
        if (opt.textContent === rolTexto) {
          opt.selected = true;
        }
      });

      modal.style.display = "flex";
    }
  };

  const cerrarContrasenia = document.getElementById("cerrar");
  const modal = document.getElementById("modal");
  if (cerrarContrasenia && modal) {
    cerrarContrasenia.addEventListener("click", () => {
      modal.style.display = "none";
    });
    window.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.style.display = "none";
      }
    });
  }

  const cerrarUsuario = document.getElementById("cerrarUsuario");
  const modalUsuario = document.getElementById("modalUsuario");
  if (cerrarUsuario && modalUsuario) {
    cerrarUsuario.addEventListener("click", () => {
      modalUsuario.style.display = "none";
    });
    window.addEventListener("click", (e) => {
      if (e.target === modalUsuario) {
        modalUsuario.style.display = "none";
      }
    });
  }

  cargarUsuarios();

  document.getElementById("inactivos").addEventListener("click", cargarUsuariosInactivos);
  document.getElementById("busc").addEventListener("click", cargarUsuariosPorRol);

  fetch('/usuario/methRoles/')
    .then(res => res.json())
    .then(data => {
      const selects = document.querySelectorAll('select.rol');
      selects.forEach(select => {
        data.roles.forEach(rol => {
          const option = document.createElement('option');
          option.value = rol.id;
          option.textContent = rol.nombre;
          select.appendChild(option);
        });
      });
    })
    .catch(err => console.error("Error al cargar roles:", err));
}

document.addEventListener("DOMContentLoaded", initUsuarios);

document.getElementById("btnGuardarContrasenia").addEventListener("click", function () {
  const username = this.dataset.username;
  const actual = document.getElementById("contraseniaActual").value.trim();
  const nueva = document.getElementById("nuevaContrasenia").value.trim();
  const confirmar = document.getElementById("confirmarContrasenia").value.trim();

  if (!username || !actual || !nueva || !confirmar) {
    alert("Todos los campos son obligatorios");
    return;
  }

  fetch('/usuario/methContra/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username,
      contraseniaActual: actual,
      nuevaContrasenia: nueva,
      confirmarContrasenia: confirmar
    })
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        document.getElementById("modal").style.display = "none";
        alert("Contraseña actualizada correctamente");
      } else {
        alert("Error: " + data.error);
      }

      document.getElementById("contraseniaActual").value = "";
      document.getElementById("nuevaContrasenia").value = "";
      document.getElementById("confirmarContrasenia").value = "";
    })
    .catch(err => console.error("Error al cambiar contraseña:", err));
});

document.querySelector("#modalUsuario .btn-guardar").addEventListener("click", function () {
  const idUsuario = parseInt(document.getElementById("idEditarUsuario").value);
  const nuevoNick = document.getElementById("usuario").value.trim();
  const idRol = parseInt(document.getElementById("rolEditarUsuario").value);

  if (!idUsuario || !nuevoNick || !idRol || isNaN(idUsuario) || isNaN(idRol)) {
    alert("Todos los campos son obligatorios y deben ser válidos.");
    return;
  }

  fetch('/usuario/modificar/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      idUsuario: idUsuario,
      nikname: nuevoNick,
      idRol: idRol
    })
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        document.getElementById("modalUsuario").style.display = "none";
        alert("Usuario actualizado correctamente");
        location.reload();
      } else {
        alert("Error: " + data.error);
      }
    })
    .catch(err => {
      console.error("Error al modificar usuario:", err);
      alert("Error inesperado al modificar el usuario.");
    });
});

*/


