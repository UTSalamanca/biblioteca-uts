const datatable = (name_table) => {
    new DataTable('#' + name_table, {
        layout: {
            bottomEnd: {
                paging: {
                    boundaryNumbers: false
                }
            }
        },
        language:
        {
            "aria": {
                "sortAscending": "Activar para ordenar la columna de manera ascendente",
                "sortDescending": "Activar para ordenar la columna de manera descendente"
            },
            "infoThousands": ",",
            "loadingRecords": "Cargando...",
            "paginate": {
                "first": "Primero",
                "last": "Último",
                "next": "Siguiente",
                "previous": "Anterior"
            },
            "processing": "Procesando...",
            "search": "Buscar:",
            "searchPanes": {
                "clearMessage": "Borrar todo",
                "count": "{total}",
                "showMessage": "Mostrar Todo"
            },
            "thousands": ",",
            "datetime": {
                "previous": "Anterior",
                "hours": "Horas",
                "minutes": "Minutos",
                "seconds": "Segundos",
                "unknown": "-",
                "amPm": [
                    "am",
                    "pm"
                ],
                "next": "Siguiente",
                "months": {
                    "0": "Enero",
                    "1": "Febrero",
                    "10": "Noviembre",
                    "11": "Diciembre",
                    "2": "Marzo",
                    "3": "Abril",
                    "4": "Mayo",
                    "5": "Junio",
                    "6": "Julio",
                    "7": "Agosto",
                    "8": "Septiembre",
                    "9": "Octubre"
                },
                "weekdays": [
                    "Domingo",
                    "Lunes",
                    "Martes",
                    "Miércoles",
                    "Jueves",
                    "Viernes",
                    "Sábado"
                ]
            },
            "decimal": ".",
            "emptyTable": "No hay datos disponibles en la tabla",
            "zeroRecords": "No se encontraron coincidencias",
            "info": "Mostrando _START_ a _END_ de _TOTAL_ entradas",
            "infoFiltered": "(Filtrado de _MAX_ total de entradas)",
            "lengthMenu": "Mostrar _MENU_ entradas",
            "stateRestore": {
                "creationModal": {
                    "search": "Buscar",
                    "button": "Crear"
                },
            },
            "infoEmpty": "No hay datos para mostrar"
        },
        "order": [[ "desc" ]]
    })
}
