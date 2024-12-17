var inFormOrLink;
// Detecta la interacción de cualquier etiqueta a
let pdfId = $('#pdfViewer').data('url_reporte')

function delete_pdf(pdfId) {
    console.log("entra#", pdfId);
    $.ajax({
        url: '/delete_pdf/',
        data: { "rute_pdf": pdfId },
        type: 'GET',
        success: function (response) {
            console.log(response);
        },
        error: function (error) {
            console.log(error);
        }
    })
}


$('a').on('click', function () {
    if (url_reporte != '') {
        delete_pdf(url_reporte)
    } else {
        console.log('No llega ninguna ruta');
    }
})
// $('form').on('submit', function () {
//     if (url_reporte != '') {
//         delete_pdf(url_reporte)
//     } else {
//         console.log('No llega ninguna ruta');
//     }
// })