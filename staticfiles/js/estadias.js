let response
response = $('#response_sweetalert').data('resp')

let title, text, icon
if (response == 'success') {
    title = 'Correcto'
    text = 'Registro exitoso'
    icon = 'success'
    estadia_alert(title, text, icon)
}

if (response == 'error') {
    title = 'Error'
    text = '¡Algo salio mal!'
    icon = 'error'
    estadia_alert(title, text, icon)
}

let iframe = $('#proyectos_preview')
if (iframe.length != 0) {
    // Función que evita el copiado de texto en la página del preview
    function notCopy() {
        action_alert('La acción de copiado no esta permitida');
    }
    // Función que evita la el click derecho dentro de la página del preview
    notClicRight = document.getElementById('iframe_card');
    page = document.getElementById('proyectos_preview');
    notClicRight.addEventListener('contextmenu', function (e) {
        e.preventDefault();
    });
    // Función para evitar la impresión de pantalla
    document.addEventListener('keydown', (event) => {
        if (event.ctrlKey) {
            if (event.keyCode == 80) {
                action_alert('La acción de impresión no esta permitida')
                event.preventDefault();
            }
        }
    });

    // Modo canvas para el pintado del reporte dentro de la página
    let url = $('#pdfViewer').data('url_reporte');
    var loadingTask = pdfjsLib.getDocument({ url: url });
    loadingTask.promise.then(function (pdf) {
        // Se obtiene el número total de páginas del PDF
        let total_pages = pdf.numPages;

        for (let i = 1; i <= total_pages; i++) {
            (function (pageNumber) {

                pdf.getPage(pageNumber).then(function (page) {
                    var scale = 0.8;
                    var viewport = page.getViewport({ scale: scale });

                    var canvas = document.createElement('canvas');
                    var context = canvas.getContext('2d');
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;

                    var renderContext = {
                        canvasContext: context,
                        viewport: viewport
                    };
                    page.render(renderContext).promise.then(function () {
                        console.log('Página renderizada');
                    });

                    document.getElementById('pdfViewer').appendChild(canvas);
                }).catch(function (error) {
                    console.log('Error al cargar la página ' + pageNumber + ' del PDF: ', error);
                });
            })(i);
        }
    }).catch(function (error) {
        console.log('Error al cargar el PDF: ', error);
    });
}
// Acción de busqueda de alumno
$('#modal_registro').on('shown.bs.modal', function () {
    $('#btn_search_matricula').on('click', function (e) {
        let matricula = $('#id_matricula').val()
        if (matricula != '') {
            $('#msg_search').attr('style', 'display:block')
            $.ajax({
                url: "/estadias/get_alumno/",
                data: { "matricula": matricula },
                type: 'GET',
                success: function (response) {
                    $('#msg_search').attr('style', 'display:none');
                    $('#msg_error').attr('style', 'display:none');
                    $('#msg_success').attr('style', 'display:block');
                    let nombre_completo = response['nombre'] + ' ' + response['apellido_paterno'] + ' ' + response['apellido_materno'];
                    let carrera = response['nombre_grupo'];
                    $('input[name=alumno]').val(nombre_completo);
                    $('input[name=carrera]').val(carrera);
                },
                error: function (error) {
                    $('#msg_success').attr('style', 'display:none');
                    $('#msg_search').attr('style', 'display:none');
                    $('#msg_error').attr('style', 'display:block');
                    $('input[name=alumno]').val('');
                    $('input[name=carrera]').val('');
                }
            })
        }
    })
})

// Manejo para cambio de tabs
$('#select_tabs').on('change', function() {
    $('#form_tab_select').submit();
});

// Función para vaciar los campos en el modal
$('#modal_registro').on('hidden.bs.modal', function () {
    $('#msg_search').attr('style', 'display:none');
    $('#msg_error').attr('style', 'display:none');
    $('#msg_success').attr('style', 'display:none');
    $('input[name=proyecto]').val('');
    $('input[name=matricula]').val('');
    $('input[name=alumno]').val('');
    $('input[name=carrera]').val('');
    $('input[name=generacion]').val('');
    $('input[name=empresa]').val('');
    $('input[name=asesor_orga]').val('');
    $('input[name=reporte]').val('');
})


function actualizarEstadia(estadiaId) {
    $.ajax({
        url: '/estadias/insert_consult/',
        data: { "user_id": estadiaId[0], "name_reporte": estadiaId[1], "id_reporte": estadiaId[2] },
        type: 'POST',
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value, // Incluye el token CSRF
        },
        success: function (response) {
            console.log(response);
        },
        error: function (error) {
            console.log(error);
        }
    })
    
}

// Función para la busqueda de reportes
function search_project() {
    let data_search = $('input[name=buscar]').val();
    console.log(data_search);
    $.ajax({
        url: '/estadias/getReporteFilter/',
        data: { "search": data_search },
        type: 'GET',
        success: function (response) {
            console.log(response);
        },
        error: function (error) {
            console.log(error);
        }
    })
}

// Función genera un delay
var sleepES5 = function(ms){
    var esperarHasta = new Date().getTime() + ms;
    while(new Date().getTime() < esperarHasta) continue;
};



// Función para realizar salto de input con Enter
tabIndex_form('modal_registro', true);