document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('formulario');            // id de formulario

  form.addEventListener('submit', function (e) {
    e.preventDefault();  // Evita que el formulario recargue la página

    const username = document.getElementById('usuario').value;      // id de input usuario
    const password = document.getElementById('contrasena').value;       // id de input contraseña

    fetch('/usuario/methLogin/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username,
        password: password
      })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        // exitoso
        window.location.href = '/SIGAPC/home/';  
      } else {
        // incorrecto
        alert(data.error);
      }
    })
    .catch(err => {
      console.error('Error en la solicitud:', err);
      alert("Error al conectar con el servidor.");
    });
  });
});
