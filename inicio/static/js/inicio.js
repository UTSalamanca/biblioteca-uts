function reportMensual() {
    inputOptions = ['Este mes', 'Mes anterior'];
    Swal.fire({
        "title": '¿Descargar reporte?',
        "icon": 'question',
        "input": "select",
        "inputOptions": inputOptions,
        "showCancelButton": true,
        "cancelButtonText": "Cancelar",
        "confirmButtonText": "Confirmar",
        "reverseButtons": true,
        "confirmButtonColor": "#28a745",
    }).then(function (result) {
        if (result.isConfirmed) {
            // Envía la colocación del registro a eliminar
            location.href = '/inicio/report/' + result.value
        }
    })
}