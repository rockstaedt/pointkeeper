let rangliste_ctx = $('#rangliste_chart')[0].getContext('2d');

let datasets_rangliste = [];

let eric_img = new Image(40,40);
let lucas_img = new Image(40,40);
let marco_img = new Image(40,40);
let peer_img = new Image(40,40);
let nils_img = new Image(40,40);

eric_img.src ='static/img/Eric.png';
lucas_img.src ='static/img/Lucas.png';
marco_img.src ='static/img/Marco.png';
peer_img.src ='static/img/Peer.png';
nils_img.src ='static/img/Nils.png';

let player_to_pic = {
    'Eric': eric_img,
    'Lucas': lucas_img,
    'Nils': nils_img,
    'Marco': marco_img,
    'Peer': peer_img
};

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
                            max: 5,
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
                            // TODO: Make the minimum of the x axis dynamic. So that only 6 games are shown.
                            min: 'Spiel 20',
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