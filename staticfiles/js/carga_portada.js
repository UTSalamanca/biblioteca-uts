function create_struc(id, titulo, edicion, anio, autor, formato) {
    let struct = '<div id="registro-'+ id +'" class="mb-3 border p-1" style="background-color:rgba(19, 66, 100, 0.04)">'
        + '<label for="proyecto">Título</label>'
        + '<div class="input-group mb-3">'
        + '<div class="input-group-prepend">'
        + '<span class="input-group-text"><i class="fas fa-book-open"></i></span>'
        + '</div>'
        + '<input type="text" class="form-control" id="title_portada" name="titulo-'+ id +'" value="'+ titulo +'" placeholder="Título del libro" readonly>'
        + '</div>'
        + '<label for="proyecto">Autor</label>'
        + '<div class="input-group mb-3">'
        + '<div class="input-group-prepend">'
        + '<span class="input-group-text"><i class="fas fa-book-open"></i></span>'
        + '</div>'
        + '<input type="text" class="form-control" id="title_portada" name="autor-'+ id +'" value="'+ autor +'" placeholder="Autor" readonly>'
        + '</div>'
        + '<label for="proyecto">Formato</label>'
        + '<div class="input-group mb-3">'
        + '<div class="input-group-prepend">'
        + '<span class="input-group-text"><i class="fas fa-book-open"></i></span>'
        + '</div>'
        + '<input type="text" class="form-control" id="title_portada" name="formato-'+ id +'" value="'+ formato +'" placeholder="Formato" readonly>'
        + '</div>'
        + '<div class="row">'
        + '<div class="col-xl-6">'
        + '<label for="edito">Edición</label>'
        + '<div class="input-group mb-3">'
        + '<div class="input-group-prepend">'
        + '<span class="input-group-text"><i class="fas fa-bookmark"></i></span>'
        + '</div>'
        + '<input type="text" class="form-control" id="edicion_portada" name="edicion-'+ id +'" value="'+ edicion +'" placeholder="Edición" readonly>'
        + '</div>'
        + '</div>'
        + '<div class="col-xl-6">'
        + '<label for="edito">Año</label>'
        + '<div class="input-group mb-3">'
        + '<div class="input-group-prepend">'
        + '<span class="input-group-text"><i class="fas fa-bookmark"></i></span>'
        + '</div>'
        + '<input type="text" class="form-control" id="anio_portada" name="anio-'+ id +'" value="'+ anio +'" placeholder="Año" readonly>'
        + '</div>'
        + '</div>'
        + '</div>'
        + '<input type="file" name="img_portada-'+ id +'" accept="image/png, image/jpeg, image/jpg" class="form-control">'
        + '</div>'

    return struct;
}

function delete_struc(cancel = false) {
    $('#prt_books').children().fadeOut(300, function () {
        $(this).remove(); // Elimina después de desvanecerse
    });
    $('#pack_btns').attr('style', 'display:none')
    if (cancel) {
        $('#inp_colocacion').val('')
    }
}

$('#btn_search_portada').on('click', function (e) {
    if ($('input[name=colocacion]').val() == '') {
        e.preventDefault();
        process('¡Debes ingresar la colocación!');
    }
    delete_struc()
    colocacion = $('input[name=colocacion').val();
    $.LoadingOverlay("show");
    $.ajax({
        url: '/catalogo/search_book/',
        data: { "colocacion": colocacion },
        type: 'GET',
        success: function (response) {
            // Muestra los botones
            $('#pack_btns').attr('style', 'display:block')
            let container = $('#prt_books');
            let data = response.books;
            let registroIdCounter = 1; // Para IDs únicos

            data.forEach(bookArray => {
                let titulo = bookArray.titulo;
                let autor = bookArray.autor;
                let anio = bookArray.anio;
                let edicion = bookArray.edicion;
                let formato = bookArray.formato;
                
                // container.append(create_struc(registroIdCounter++, titulo, edicion, anio, autor));
                // Añade al contenedor con animación
                let newElement = $(create_struc(registroIdCounter++, titulo, edicion, anio, autor, formato));
                newElement.css('opacity', 0); // Inicialmente invisible
                container.append(newElement);
                newElement.animate({ opacity: 1 }, 800); // Aparece lentamente
            });
            $.LoadingOverlay("hide")
        },
        error: function (error) {
            $.LoadingOverlay("hide")
            console.log(error);
        }
    });
});


// Función para realizar salto de input con Enter
tabIndex_form('', true);