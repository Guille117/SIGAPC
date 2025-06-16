function initUsuarios() {
  const btnNuevoUsuario = document.getElementById("btnNuevoUsuario");
  const modalNuevoUsuario = document.getElementById("modalNuevoUsuario");
  const cerrarNuevoUsuario = document.getElementById("cerrarNuevoUsuario");
  const cerrarUsuario = document.getElementById("cerrarUsuario");
  const cerrarContrasenia = document.getElementById("cerrar");

  if (btnNuevoUsuario && modalNuevoUsuario && cerrarNuevoUsuario) {
    btnNuevoUsuario.addEventListener("click", () => {
      modalNuevoUsuario.style.display = "flex";
      cargarEmpleados();
    });

    cerrarNuevoUsuario.addEventListener("click", () => {
      modalNuevoUsuario.style.display = "none";
    });

    window.addEventListener("click", (e) => {
      if (e.target === modalNuevoUsuario) {
        modalNuevoUsuario.style.display = "none";
      }
      if (e.target === document.getElementById("modalUsuario")) {
        document.getElementById("modalUsuario").style.display = "none";
      }
      if (e.target === document.getElementById("modal")) {
        document.getElementById("modal").style.display = "none";
      }
    });
  }

  if (cerrarUsuario) {
    cerrarUsuario.addEventListener("click", () => {
      document.getElementById("modalUsuario").style.display = "none";
    });
  }

  if (cerrarContrasenia) {
    cerrarContrasenia.addEventListener("click", () => {
      document.getElementById("modal").style.display = "none";
    });
  }

  const btnEditar = document.getElementById("btnGuardarUsuario");
  if (btnEditar) {
    btnEditar.addEventListener("click", guardarEdicionUsuario);
  }

  const btnGuardar = document.getElementById("guarda");
  if (btnGuardar) {
    btnGuardar.addEventListener("click", crearUsuario);
  }

  document.getElementById("inactivos").addEventListener("click", cargarUsuariosInactivos);
  document.getElementById("busc").addEventListener("click", function () {
    cargarUsuariosPorRol();
    buscarUsu();
  });

  document.getElementById('itemsEmpleado').addEventListener('change', function () {
    const idSeleccionado = this.value;
    document.getElementById('idEmpleado').value = idSeleccionado;
  });

  cargarUsuarios();
  cargarRoles();
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
  if (!idRol || idRol === "Roles") {
    alert("Debe seleccionar un rol válido");
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

function crearUsuario() {
  const idEmpleado = document.getElementById("idEmpleado").value;
  const nikname = document.getElementById("usur").value.trim();
  const contrasenia = document.getElementById("con").value.trim();
  const idRol = document.getElementById("posRoles").value;

  if (!idEmpleado || !nikname || !contrasenia || !idRol) {
    alert("Todos los campos son obligatorios.");
    return;
  }

  const datos = {
    idEmpleado: parseInt(idEmpleado),
    nikname,
    contrasenia,
    idRol: parseInt(idRol)
  };

  fetch('/usuario/crear/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos)
  })
    .then(res => res.json().then(data => ({ status: res.status, body: data })))
    .then(({ status, body }) => {
      if (status === 201) {
        alert("Usuario creado correctamente.");
        document.getElementById("modalNuevoUsuario").style.display = "none";
        cargarUsuarios();
      } else {
        alert("Error: " + (body.error || "Error desconocido."));
      }
    })
    .catch(err => {
      console.error("Error al crear usuario:", err);
      alert("Error al conectar con el servidor.");
    });
}

function guardarEdicionUsuario() {
  const idUsuario = document.getElementById("idEditarUsuario").value;
  const nikname = document.getElementById("usuario").value.trim();
  const idRol = document.getElementById("rolEditarUsuario").value;

  if (!idUsuario || !nikname || !idRol) {
    alert("Todos los campos son obligatorios.");
    return;
  }

  const datos = {
    idUsuario: parseInt(idUsuario),
    nikname,
    idRol: parseInt(idRol)
  };


  fetch('/usuario/modificar/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos)
  })
    .then(res => res.json().then(data => ({ status: res.status, body: data })))
    .then(({ status, body }) => {
      if (status === 200) {
        alert("Usuario actualizado correctamente.");
        document.getElementById("modalUsuario").style.display = "none";
        cargarUsuarios();
      } else {
        alert("Error: " + (body.error || "Error desconocido."));
      }
    })
    .catch(err => {
      console.error("Error al guardar cambios:", err);
      alert("Error al conectar con el servidor.");
    });
}

function cargarEmpleados() {
  fetch('/usuario/methEmpleados/')
    .then(res => res.json())
    .then(data => {
      if (verificarError(data)) return;
      const select = document.getElementById('itemsEmpleado');
      document.getElementById('idEmpleado').value = "";
      document.getElementById('usur').value = "";
      document.getElementById('con').value = "";
      select.innerHTML = '<option value="">Seleccione un empleado</option>';
      data.empleados.forEach(emp => {
        const option = document.createElement('option');
        option.value = emp.idEmpleado;
        option.textContent = emp.nombre;
        select.appendChild(option);
      });
    })
    .catch(err => {
      console.error("Error cargando empleados:", err);
    });
}

function cargarRoles() {
  fetch('/usuario/methRoles/')
    .then(res => res.json())
    .then(data => {
      const selects = document.querySelectorAll('select.rol');
      selects.forEach(select => {
        select.innerHTML = '<option value="">Seleccione un rol</option>';
        data.roles.forEach(rol => {
          const option = document.createElement('option');
          option.value = rol.id;
          option.textContent = rol.nombre;
          select.appendChild(option);
        });
      });
    })
    .catch(err => {
      console.error("Error al cargar roles:", err);
    });
}

function cambiarContrasenia() {
  const btn = document.getElementById("btnGuardarContrasenia");
  const username = btn.dataset.username;

  const actual = document.getElementById("contraseniaActual").value.trim();
  const nueva = document.getElementById("nuevaContrasenia").value.trim();
  const confirmar = document.getElementById("confirmarContrasenia").value.trim();

  if (!actual || !nueva || !confirmar) {
    alert("Todos los campos son obligatorios.");
    return;
  }

  if (nueva !== confirmar) {
    alert("La nueva contraseña y su confirmación no coinciden.");
    return;
  }

  const datos = {
    username: username,
    contraseniaActual: actual,
    nuevaContrasenia: nueva,
    confirmarContrasenia: confirmar
  };

  fetch('/usuario/methContra/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos)
  })
  .then(res => res.json().then(data => ({ status: res.status, body: data })))
  .then(({ status, body }) => {
    if (status === 200 && body.success) {
      alert("Contraseña actualizada correctamente.");
      cerrarModalContrasenia();
    } else {
      alert("Error: " + (body.error || "Error desconocido."));
    }
  })
  .catch(err => {
    console.error("Error al cambiar contraseña:", err);
    alert("Error al conectar con el servidor.");
  });
}

function cambiarContrasenia() {
  const btn = document.getElementById("btnGuardarContrasenia");
  const username = btn.dataset.username;

  const actual = document.getElementById("contraseniaActual").value.trim();
  const nueva = document.getElementById("nuevaContrasenia").value.trim();
  const confirmar = document.getElementById("confirmarContrasenia").value.trim();

  if (!actual || !nueva || !confirmar) {
    alert("Todos los campos son obligatorios.");
    return;
  }

  if (nueva !== confirmar) {
    alert("La nueva contraseña y su confirmación no coinciden.");
    return;
  }

  const datos = {
    username: username,
    contraseniaActual: actual,
    nuevaContrasenia: nueva,
    confirmarContrasenia: confirmar
  };

  fetch('/usuario/methContra/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos)
  })
  .then(res => res.json().then(data => ({ status: res.status, body: data })))
  .then(({ status, body }) => {
    if (status === 200 && body.success) {
      alert("Contraseña actualizada correctamente.");
      cerrarModalContrasenia();
    } else {
      alert("Error: " + (body.error || "Error desconocido."));
    }
  })
  .catch(err => {
    console.error("Error al cambiar contraseña:", err);
    alert("Error al conectar con el servidor.");
  });
}

function cerrarModalContrasenia() {
  const modal = document.getElementById("modal");
  modal.style.display = "none";
  document.getElementById("contraseniaActual").value = "";
  document.getElementById("nuevaContrasenia").value = "";
  document.getElementById("confirmarContrasenia").value = "";
  document.getElementById("btnGuardarContrasenia").dataset.username = "";
}

document.getElementById("btnGuardarContrasenia").addEventListener("click", cambiarContrasenia);
document.getElementById("cerrar").addEventListener("click", cerrarModalContrasenia);

window.addEventListener("click", function (e) {
  const modal = document.getElementById("modal");
  if (e.target === modal) {
    cerrarModalContrasenia();
  }
});


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
      opt.selected = opt.textContent === rolTexto;
    });

    modal.style.display = "flex";
  }
};

window.cambiarEstadoUsuario = function (idUsuario) {
  fetch('/usuario/methActivar/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ idUsuario })
  })
    .then(res => res.json())
    .then(() => cargarUsuarios())
    .catch(err => {
      console.error("Error al cambiar estado:", err);
      alert("Error al cambiar el estado del usuario.");
    });
};

document.addEventListener("DOMContentLoaded", initUsuarios);




/**
 * 
 * function initUsuarios() {
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


 */