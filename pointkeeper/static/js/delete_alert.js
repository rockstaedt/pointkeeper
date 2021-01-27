function show_delete_alert(get_game_date_url, delete_game_url, days_for_delete)
{

    var date_check = new Date();

    date_check.setDate(date_check.getDate() - days_for_delete);

    $.ajax({
        url: get_game_date_url,
        success: function(result){
            var date_game = new Date(result.game_date);

            if (date_game > date_check){
                swal({
                    title: "Bist du sicher?",
                    text: "Einmal gelöscht, verschwindet das Spiel ins Nichts.",
                    icon: "warning",
                    buttons: ["Abbrechen", "Löschen"],
                    dangerMode: true,
                  })
                  .then((willDelete) => {
                    if (willDelete) {
                      swal("Spiel gelöscht", {
                        icon: "success",
                      })
                      .then((deleted) => {
                          if (deleted) {
                            window.location.href = delete_game_url
                          }
                      });
                    }
                  });
            } else {
                swal({
                    text: "Spiel kann nicht mehr gelöscht werden.",
                    icon: "info"
                });
            };
        }
    });
};