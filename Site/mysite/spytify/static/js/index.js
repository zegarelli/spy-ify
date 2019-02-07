/************************************************
* FILENAME: index.js
* DESCRIPTION: main staic js holder for index.html
* file
*************************************************/

/*************************************************
 * FN NAME: get_day_str()
 * DESC: returns string of the day of the week
 *  given the supplied day index. Here, 0 represents
 *  Sunday, 1 represents Monday, and so on.
 *
 * If a number greater than 6 is supplied, we take
 * modulus of 7 and return that str
 *
 *************************************************/
function get_day_str( day_idx )
{
var days_of_the_week =
    [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
    ];
return days_of_the_week[ day_idx % days_of_the_week.length ]
}   /* get_day_str() */

/*************************************************
 * FN NAME: draw_history_chart()
 * DESC: draws a bootstrap styled line graph from
 *  supplied array num_plays
 *
 *  num_plays[] is expected to be arranged where the
 *  first value is the number of plays from current
 *  day, and the following values represent the plays
 *  for the preceding days. The chart maxes out at
 *  displaying information for the last 7 days
 *
 *  This fn draws a line graph as specified from
 *  the MDBootstrap library. A <canvas> element
 *  with an id of "lineChart" is expected
 *
 *************************************************/
function draw_history_chart( num_plays, days, num_artists ){
/*-----------------------------
VARS
-----------------------------*/
var date = new Date();
var ctxL = document.getElementById("lineChart").getContext('2d');
var date_label = [];

/*-----------------------------
Validate input
-----------------------------*/
if( num_plays.length > 50 ){
    throw "draw_history_chart: Invalid array length in var num_plays";
}
if( ctxL == null ){
    throw "draw_history_chart: unable to locate \"lineChart\" canvas element";
}

/*-----------------------------
Prepare Date Label Array
-----------------------------*/
for( var i = 0; i < num_plays.length; i++ ){
    date_label[i] = get_day_str( num_plays[i] );
}

var myLineChart = new Chart(ctxL, {
    type: 'line',
    data: {
//    labels: date_label,
    labels: days,
    datasets: [{
        label: "Plays",
        data: num_plays,
        backgroundColor: [
            'rgba(105, 0, 132, .2)',
            ],
        borderColor: [
            'rgba(200, 99, 132, .7)',
            ],
        borderWidth: 2
        },
        {
        label: "Artists",
        data: num_artists,
        backgroundColor: [
            'rgba(50, 100, 50, .2)',
            ],
        borderColor: [
            'rgba(50, 150, 100, .7)',
            ],
        borderWidth: 2
        },
    ]
    },
    options: {
        responsive: true
    }
});

}   /* END draw_history_chart() */

/*************************************************
 * FN NAME: csrfSafeMethod()
 * DESC:
 *************************************************/
function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}   /* END csrfSafeMethod() */

/*************************************************
 * FN NAME: getCookie()
 * DESC: Return django embedded cookie.
 *  To be used to validate POST AJAX requests
 *************************************************/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}   /* END getCookie */

/*************************************************
 * FN NAME: $.ready()
 * DESC: auto-called when the page is fully loaded
 *  This is to be treated as a main driver function
 *************************************************/
$(document).ready(function() {
    /*-----------------------------
    VARS
    -----------------------------*/
    var chart = null
    // get the value of CSRF token
    var csrftoken = getCookie('csrftoken');

    /*-----------------------------
    VARS
    -----------------------------*/
    if( csrftoken == null ){
        throw "$.ready(): token not loaded properly"
    }

    /*-----------------------------
    Setup our permissions for our POST call
    (this is not needed for GET)
    -----------------------------*/
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            // if not safe, set csrftoken
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    /*-----------------------------
    Excecute actual ajax POST call
    -----------------------------*/
    $.ajax({
        type: 'POST',
        url: 'example_query/',
        contentType: 'application/json',
    })
    .done( function( data, status ){
        /*----------------------------------
        TODO: REPLACE WITH REAL DATA ONCE
        THE BACKEND IS MIGRATED OVER
        -----------------------------------*/
        console.log(data.plays_per_day)
        console.log(data.days)
        console.log(data.artists_per_day)
        draw_history_chart( data.plays_per_day, data.days, data.artists_per_day);
    })
    .fail( function( data, status ){
        console.log( data );
    })

});