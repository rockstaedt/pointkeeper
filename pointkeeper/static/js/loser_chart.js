function create_loser_chart(year) {

    let loser_ctx = $('#loser_chart')[0].getContext('2d');

    let datasets_loser = [];

    let loser_chart_data = $.get("/api/v1/get_data_loser/" + year);

    loser_chart_data.done(function (data) {

        $('#total_sum').text(data['total_sum'])

        let chart = new Chart(loser_ctx, {
            // The type of chart we want to create
            type: 'bar',

            // The data for our dataset
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: "#43DCA3",
                    borderColor: "#43DCA3",
                }]
            },

            // Configuration options go here
            options: {
                legend: {
                    display: false
                },
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    yAxes: [
                        {
                            ticks: {
                                min: 0,
                                stepSize: 1
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
                            barPercentage: 0.4,
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
                            enabled: false,
                            // Panning directions.
                            mode: 'xy',
                            speed: 3
                        },
                        zoom: {
                            enabled: true,
                            // Zooming directions.
                            mode: 'y'
                        }
                    }
                }
            }
        })
    })
}

year = $("#year_selector option:selected").text()

create_loser_chart(year);
