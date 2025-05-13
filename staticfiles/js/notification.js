const estadia_alert = (title, text, icon) => {
    Swal.fire({
        title: title,
        icon: icon,
        text: text,
        showConfirmButton: false,
        timer: 3000
    })
}

const register_deleteSwal = (title, coloca, text, icon, rute) => {
    Swal.fire({
        "title": title + ' - ' + coloca,
        "text": text,
        "icon": icon,
        "showCancelButton": true,
        //"allowOutsideClick": false,
        "cancelButtonText": "Cancelar",
        "confirmButtonText": "Eliminar",
        "reverseButtons": true,
        "confirmButtonColor": "#dc3545",
    })
        .then(function (result) {
            if (result.isConfirmed) {
                // Envía la colocación del registro a eliminar
                location.href = '/' + rute + coloca
            }
        })
}

const renew_again = (rute, cve_prestamo, cantidad, entrega) => {
    // Generar las opciones dinámicamente según la cantidad de libros
    const inputOptions = {};
    for (let i = 1; i <= cantidad; i++) {
        inputOptions[i] = i; // Por ejemplo, "Libro 1", "Libro 2", etc.
    }

    // Mostrar el SweetAlert con las opciones dinámicas
    Swal.fire({
        title: "Cantidad de libros a renovar",
        input: "select",
        inputOptions: inputOptions,
        showCancelButton: true,
        confirmButtonText: "Renovar",
        confirmButtonColor: "#28a745",
        reverseButtons: true,
        inputValidator: (value) => {
            return new Promise((resolve) => {
                if (value) {
                    resolve();
                } else {
                    resolve("Debe seleccionar un libro.");
                }
            });
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // Swal.fire(`Usted seleccionó: ${inputOptions[result.value]}`);
            location.href = '/' + rute + cve_prestamo + '/' + result.value + '/' + entrega
        }
    });
};

const register_renew = (cve_prestamo, title, btn, btn_color, icon, cantidad_i , cantidad_m, rute, entrega) => {
    Swal.fire({
        title: title,
        text: cve_prestamo,
        icon: icon,
        showCancelButton: true,
        //"allowOutsideClick": false,
        cancelButtonText: "Cancelar",
        confirmButtonText: btn,
        reverseButtons: true,
        confirmButtonColor: btn_color,
    })
        .then(function (result) {
            if (result.isConfirmed) {
                // Envía la colocación del registro a eliminar
                let cantidad;
                if (entrega == 'Devuelto') {
                    cantidad = cantidad_i
                } 
                else {
                    cantidad = cantidad_m
                }
                renew_again(rute, cve_prestamo, cantidad, entrega);

            }
        })
}

const register_entrega = (cve_prestamo, text, btn, btn_color, icon, rute, entrega) => {
    Swal.fire({
        title: text,
        text: cve_prestamo,
        icon: icon,
        showCancelButton: true,
        //"allowOutsideClick": false,
        cancelButtonText: "Cancelar",
        confirmButtonText: btn,
        reverseButtons: true,
        confirmButtonColor: btn_color,
    })
        .then(function (result) {
            if (result.isConfirmed) {
                location.href = '/' + rute + cve_prestamo + '/' + entrega
            }
        }); 
}

const action_alert = (text) => {
    Swal.fire({
        title: '¡Acción no permitida!',
        icon: 'warning',
        text: text,
        showConfirmButton: false,
        timer: 2100
    })
}


const process = (msg) => {
    Swal.fire({
        title: msg,
        icon: 'warning',
        showConfirmButton: false,
        timer: 2100
    })
}