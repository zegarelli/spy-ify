function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

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
}

function formatDate(date) {
    date = date.slice(0, 10)
    console.log(date)
    return date
}

function make_dates_table() {
    var csrftoken = getCookie('csrftoken')

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            // if not safe, set csrftoken
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
            url: 'api/posts',
            data: {
                    "test": "data"
                  },
            dataType: 'json',
            error: function (request, error) {
                console.log(" Can't do because: " + error)
            },
            success: function (data) {
                // make table header
                var html = '<table class="table"><thead class="thead-default">'
                html += '<th class="orderable">Date</th><th class="orderable">Summary</th><th class="orderable">Body</th><th class="orderable">Linked Posts</th>'
                html += '</thead><tbody class="thead-default">'

                // format dates
                for (date in data.dates){
                    data.dates[date][0] = formatDate(data.dates[date][0])
                }

                // make table rows
                for (row in data.dates){
                    html += '<tr>'
                    for (cell in data.dates[row])
                        html += '<td>' + data.dates[row][cell] + '</td>'

                    html += '</tr>'
                }

                html += '</tbody>'

                $(html).appendTo('#date-table');
            }
        })
}

$(document).ready(function() {
    make_dates_table()
    })