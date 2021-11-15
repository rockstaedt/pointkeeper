let rangliste_ctx = $('#rangliste_chart')[0].getContext('2d');

let datasets_rangliste = [];

function get_min_x_label(labels) {
  return labels[labels.length -10];
}

// Fetch data for chart.
let getData_rangliste = $.get("/api/v1/get_data_rangliste");
// Wait until fetching is done.
getData_rangliste.done(function(data) {

    let dataset;
    // Create a line for each player in the set.
    for (dataset of data.datasets) {
        datasets_rangliste.push(
            {
                label: dataset.label,
                tension: 0,
                backgroundColor: "#43DCA3",
                borderColor: "#43DCA3",
                borderWidth: 2,
                data: dataset.data,
                fill: false,
                pointRadius: dataset.pointRadius,
                pointHitRadius: dataset.pointHitRadius,
                pointStyle: dataset.pointStyle
            }
        )
    }

    // Add picture for last data point.
    for (dataset of datasets_rangliste) {
        dataset.pointRadius.push(1);
        dataset.pointHitRadius.push(10);
        dataset.pointStyle.push(player_to_pic[dataset.label])
    }

    // Create chart.
    let chart = new Chart(rangliste_ctx, {
        // The type of chart we want to create
        type: 'line',

        data: {
            labels: data.labels,
            datasets: datasets_rangliste,
        },

        options: {
            legend: {
                display: false
             },
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [
                    {
                        ticks : {
                            reverse : true,
                            padding: 20,
                            max: 6,
                            min: 1,
                            callback: function(value, index, values) {
                                if (Math.floor(value) === value) {
                                    return Math.round(value);
                                }
                            }
                        },
                        gridLines: {
                            display: false
                        },
                    }
                ],
                xAxes: [
                    {
                        ticks: {
                            min: get_min_x_label(data.labels),
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
                        mode: 'x',
                        speed: 3
                    },
                    zoom: {
                        enabled: true,
                        // Zooming directions.
                        mode: 'x'
                    }
                }
            }
        }
    });
});