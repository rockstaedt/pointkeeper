let punkte_ctx = $('#punkte_chart')[0].getContext('2d');

let datasets_punkte = [];

let getData_punkte = $.get("/api/v1/get_data_punktehistorie");

getData_punkte.done(function(data) {

    let dataset;

    for (dataset of data.datasets) {
        datasets_punkte.push(
            {
                label: dataset.label,
                backgroundColor: player_to_color[dataset.label],
                tension: 0.2,
                borderColor: player_to_color[dataset.label],
                borderWidth: 2,
                data: dataset.data,
                fill: false,
                pointRadius: dataset.pointRadius,
                pointHitRadius: dataset.pointHitRadius,
                pointStyle: dataset.pointStyle
            }
        )
    }

    let chart = new Chart(punkte_ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: data.labels,
            datasets: datasets_punkte,
        },

        // Configuration options go here
        options: {
            legend: {
                display: true
             },
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [
                    {
                        ticks : {
                            padding: 20,
                            callback: function(value, index, values) {
                                return Math.round(value);
                            }
                        },
                        gridLines: {
                            display: true,
                            color: '#797979',
                            linewidth: 0.5,
                            drawBorder: false,
                        },
                    }
                ],
                xAxes: [
                    {
                        ticks: {
                            padding: 20,
                        },
                        gridLines: {
                            display: false,
                        },
                    }
                ],
            },
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                        // Panning directions.
                        mode: 'xy',
                        speed: 3
                    },
                    zoom: {
                        enabled: true,
                        // Zooming directions.
                        mode: 'xy'
                    }
                }
            }
        }
    });
})