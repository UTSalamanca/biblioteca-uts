$(document).ready(function() {
    $('#catalogoTable').on('click', 'tbody tr td a#btnPedidoBook', function () {
        let data = $(this).closest('tr').data()
        let portada = 'data:image/png;base64,';
        // Convierte la imagen
        // portada_base64 = data.base64 != 'None' ? portada + data.base64 : portada + default_img()
        if (data.base64 != '') {
            $('#defult_in_portada').attr("style","display:none;");
            $('#content_portada').attr("style","display:block;");
            $('#content_portada').attr("src",portada + data.base64);
        }
        $('input[name=nom_libro]').val(data.titulo);
        $('input[name=nom_autor]').val(data.autor);
        $('input[name=edicion]').val(data.edicion);
        $('input[name=colocacion]').val(data.colocacion);
    });
    
    // Función para el borrado de elementos
    $('#prestamoTableAll').on('click', 'tbody td a#delivered', function (e) {
        let data = $(this).closest('#info_book').data();
        let cve_prestamo = data['cve_prestamo'];
        // let entrega = data['entrega'].trim().toLowerCase();
        let entrega = data['entrega']
        let text = entrega == "Proceso" ? "¿Marcar como entregado?" : "¿Marcar como devuelto?";
        let btn = entrega == "Proceso" ? "Marcar/entregado" : "Marcar/devuelto";
        let btn_color = entrega == "Proceso" ? "#28a745" : "#18632a";
        let icon = "question";
        let rute = 'catalogo/book_delivered/';
        if (entrega == 'Devuelto') {
            process('¡Ya realizó este proceso!');
        }
        else {
            // Llama el SweetAlert del script notification
            register_entrega(cve_prestamo, text, btn, btn_color, icon, rute, entrega);
        }
    });
    
    // Función para renovar el prestamo del libro
    $('#prestamoTableAll').on('click', 'tbody td a#renew_again', function (e) {
        let data = $(this).closest('#info_book').data();
        let cve_prestamo = data['cve_prestamo'];
        let cantidad_m = data['cantidad_m'];
        let cantidad_i = data['cantidad_i'];
        // let entrega = data['entrega'].trim().toLowerCase();
        let entrega = data['entrega'];
        let title = "¿Renovar préstamo?";
        let btn = "Renovar";
        // Validar si es posible eliminar
        let btn_color = "#28a745"; // Botón renovar
        let icon = "question";
        let rute = 'catalogo/renew_again/';
        // Llama el SweetAlert del script notification
        register_renew(cve_prestamo, title, btn, btn_color, icon, cantidad_i , cantidad_m, rute, entrega);
    });
    
    // Valida que todos los campos esten llenos antes de mandar el formulario
    $('#btnSendEstadias').on('click', function (event) {
        // Declaración de variables
        let matricula = $('input[name=matricula]').val(),
            titulo = $('input[name=nom_libro]').val(),
            nom_alumno = $('input[name=nom_alumno]').val(),
            colocacion = $('input[name=colocacion]').val(),
            cantidad = $('input[name=cantidad_i]').val(),
            carrera_grupo = $('input[name=carrera_grupo]').val();
         // Obliga a esperar que la información este completa
        if(matricula == '' && nom_alumno == '' && carrera_grupo == ''){
            event.preventDefault();
        }
        // Valida cantidades negativas
        if (cantidad <= 0) {
            event.preventDefault();
            process('¡Debes ingresar una cantidad mayor a 0!');
        } 
        else {
            event.preventDefault();
            data = {
                "titulo": titulo,
                "colocacion": colocacion,
            }
            $.ajax({
                url: 'cant_for_search/',
                data: data,
                type: 'GET',
                success: function (response) {
                    if (cantidad > response.cantidad) {
                        process('Cantidad disponible: ' + response.cantidad);
                    } 
                    else {
                        $('#tbl_registroP').submit()
                    }
                },
                error: function (error) { console.log(error); }
            });
        }
    
    })
    
    // Manejo para cambio de tabs
    $('#select_tabs').on('change', function() {
        $('#form_tab_select').submit();
    });

    $('#modal_catalogo').on('hidden.bs.modal', function () {
        $('#msg_search').attr('style', 'display:none');
        $('#msg_error').attr('style', 'display:none');
        $('#msg_success').attr('style', 'display:none');
        $('input[name=nom_libro]').val('');
        $('input[name=nom_autor]').val('');
        $('input[name=edicion]').val('');
        $('input[name=colocacion]').val('');
        $('input[name=cantidad]').val('');
        $('#defult_in_portada').attr("style","display:block");
        $('#content_portada').attr("style","display:none");
        $('#content_portada').removeAttr("src");
    });
    
    // Función para realizar salto de input con tecla Enter
    tabIndex_form('modal_catalogo', true);

});