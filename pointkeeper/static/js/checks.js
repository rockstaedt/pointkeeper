function check_form(){
    // This function checks if the form contains an empty field. Returns
    // boolean.

    inputs = $('input');
    player_names = $('select');

    empty = false;

    for (input of inputs){
        if (input.value == "") {
            empty = true;
            break;
        };
    };
    for (player_name of player_names){
        if (player_name.value == ""){
            empty = true;
            break;
        };
    };
    return empty;
};

function check_player_names(){
    // This function checks if a player is selected multiple times. Opens an
    // alert if a player was selected multiple times.
    name_to_occurence = {};
    $("#id_player_1 option").each(function(){
        if ($(this).html() != "Wähle...") {
            name_to_occurence[$(this).html()] = 0;
        };
    });
    selects_player = $('select');
    for (select_player of selects_player){
        name_player = $('#' + select_player.id + ' option:selected').text()
        name_to_occurence[name_player] ++;
        if (name_to_occurence[name_player] > 1){
            swal({
                title: 'Doppelter Spieler',
                text: "Spieler " + name_player + ' wurde mehrmals ausgewählt.',
                icon: "warning"
            });
            return false;
        };
    };
    return true;
};

function check_points(){
    // This function checks that the sum of all entered points is zero. Opens
    // an alert if entered points are not zero. Returns boolean.
    inputs_points = $('.points');
    sum = 0;
    for (input_points of inputs_points){
        sum = sum + Number(input_points.value)
    }
    if (sum != 0){
        swal({
            title: 'Falsche Summe',
            text: "Die Summe der Punkte beträgt nicht 0.",
            icon: "warning"
        });
        return false;
    } else {
        return true;
    }
};