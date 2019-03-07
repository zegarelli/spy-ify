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

function update_search() {
    var playquery = $("#playquery").val();
    var columns = $("#columns").val();
      console.log( '    playquery:' + playquery );
      console.log( '    columns:' + columns );

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
        url: 'free_query',
        data: {
            'playquery': playquery,
            'columns': columns,
        },
        dataType: 'json',
        success: function (data) {
        // clear out to <div> surrounding the table
        $('#search-results').empty()

        // make table header
        var html = '<table class="table"><thead class="thead-default">'
        for (var i = 0, len = data.columns.length; i < len; ++i)
            html += '<th class="orderable"><a href="?sort=' + data.columns[i] + '">' + data.columns[i] + '</a></th>'

        html += '</thead><tbody class="thead-default">'

        // make table rows
        for (row in data.plays){
            html += '<tr>'
            for (cell in data.plays[row])
                html += '<td>' + data.plays[row][cell] + '</td>'

            html += '</tr>'
        }

        html += '</tbody>'

        $(html).appendTo('#search-results');
        }
    })
}

$(document).ready(function(){
    console.log('in document ready')
    update_search()
})

$("#playquery").change(function(){
    console.log('in playquery')
    update_search()
});

$("#columns").change(function(){
    console.log('in columns')
    update_search()
});


