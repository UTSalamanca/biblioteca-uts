// Llama función para DataTable
datatable('tbl_prestamo_es');

// Creación de gráfica de pastel
// Se obtienen los estados registrados
let states = $('#chartPie').data('states');
if (states != 'undefined') {
    Highcharts.chart('container', {
        chart: {
            type: 'pie'
        },
        title: {
            text: 'Cantidad por estado del libro',
            align: 'left'
        },
        accessibility: {
            announceNewData: {
                enabled: false
            },
        },
        plotOptions: {
            series: {
                borderRadius: 5,
                dataLabels: [{
                    enabled: true,
                    distance: '15%',
                    format: '{point.name}'
                }, {
                    enabled: true,
                    distance: '-30%',
                    filter: {
                        property: 'percentage',
                        operator: '>',
                        value: 5
                    },
                    format: '{point.y:.0f}',
                    style: {
                        fontSize: '0.9em',
                        textOutline: 'none',
                        textDecoration: 'none'
                    }
                }]
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: ' +
                '<b>{point.y:.0f}</b> libro(s)<br/>'
        },
        series: [
            {
                name: 'Estatus',
                colorByPoint: true,
                data: [
                    {
                        name: 'Excelente',
                        y: states[0],
                        drilldown: 'Excelente',
                        color: '#2ed255'
                    },
                    {
                        name: 'Bueno',
                        y: states[1],
                        drilldown: 'Bueno',
                        color: '#d26812'
                    },
                    {
                        name: 'Regular',
                        y: states[2],
                        drilldown: 'Regular',
                        color: '#ede057'
                    },
                    {
                        name: 'Malo',
                        y: states[3],
                        drilldown: 'Malo',
                        color: '#ff0000'
                    }
                ]
            }
        ]
    });
}

// Creación de gráfica de barras
let libros = $('#chartColum').data('libros');
let discos = $('#chartColum').data('discos');
if (libros != 'undefined' && discos != 'undefined') {
    Highcharts.chart('container_colum', {
        chart: {
            type: 'column'
        },
        title: {
            align: 'left',
            text: 'Tipo de ejemplar'
        },
        subtitle: {
            align: 'left',
            text: 'Se muestra la cantidad de libros con respecto a la cantidad de discos registrados'
        },
        accessibility: {
            announceNewData: {
                enabled: true
            }
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            title: {
                text: 'Total de elementos'
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    format: '{point.y:.0f}'
                }
            },
            text: {
              style: {
                textDecoration: 'none'
              }
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: ' +
                '<b>{point.y:.0f}</b> en total<br/>'
        },
        series: [
            {
                data: [
                    {
                        name: 'libros',
                        y: libros,
                        drilldown: 'Libros',
                        color: 'red'
                    },
                    {
                        name: 'Discos',
                        y: discos,
                        drilldown: 'Discos',
                        color: '#007bff'
                    }
                ]
            }
        ]
    });
}

let value_adqui = $('#chartColumAdqui').data('valueadqui');
let name_cole = $('#chartColumAdqui').data('nameadqui');
let spt_1 = name_cole.split('[')
let spt_2 = spt_1[1].split(']')
let name_value = spt_2[0].split(',')

Highcharts.chart('adqui_colum', {
    chart: {
        type: 'column'
    },
    title: {
        align: 'left',
        text: 'Tipo de adquisición'
    },
    subtitle: {
        align: 'left',
        text: 'Se muestra la cantidad el tipo de adquisición que se ha usado'
    },
    accessibility: {
        announceNewData: {
            enabled: true
        }
    },
    xAxis: {
        type: 'category'
    },
    yAxis: {
        title: {
            text: 'Total de elementos'
        }
    },
    legend: {
        enabled: false
    },
    plotOptions: {
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y:.0f}'
            }
        },
        text: {
          style: {
            textDecoration: 'none'
          }
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: ' +
            '<b>{point.y:.0f}</b> en total<br/>'
    },
    series: [
        {
            data: [
                {
                    name: name_value[0],
                    y: value_adqui[0],
                    drilldown: name_value[0],
                    color: 'red'
                },
                {
                    name: name_value[1],
                    y: value_adqui[1],
                    drilldown: name_value[1],
                    color: 'blue'
                },
                {
                    name: name_value[2],
                    y: value_adqui[2],
                    drilldown: name_value[2],
                    color: 'brown'
                },
                {
                    name: name_value[3],
                    y: value_adqui[3],
                    drilldown: name_value[3],
                    color: 'orange'
                },
            ]
        }
    ]
});


// $('#btn_report').on('click', function (e) {
//     e.preventDefault()
//     Swal.fire({
//         "title": '¿Descargar reporte?',
//         "icon": 'question',
//         "showCancelButton": true,
//         "cancelButtonText": "Cancelar",
//         "confirmButtonText": "Confirmar",
//         "reverseButtons": true,
//         "confirmButtonColor": "#28a745",
//     }).then(function (result) {
//             if (result.isConfirmed) {
//                 // Envía la colocación del registro a eliminar
//                 // location.href = '/report/'
//                 $('#btn_report').submit()
//             }
//         })
// })