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

function search(){

}

function update_search() {
    var playquery = $("#playquery").val();
    var columns = $("#columns").val();

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

            var len = data.plays.length
            $('#result-count').empty()
            $('#result-count').append(len)
        }
    })
}

function download_csv() {
    var playquery = $("#playquery").val();
    var columns = $("#columns").val();

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
            data.plays.unshift(data.columns)
            console.log(data.plays)

            let csvContent = "data:text/csv;charset=utf-8,";
            data.plays.forEach(function(rowArray){
               let row = rowArray.join(",");
               csvContent += row + "\r\n";
               console.log(csvContent)
            });

            var encodedUri = encodeURI(csvContent);
            var link = document.createElement("a");
            window.open(encodedUri);

            var encodedUri = encodeURI(csvContent);
            var link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "my_data.csv");
            document.body.appendChild(link); // Required for FF

link.click();
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

$("#download").click(function(){
    download_csv()
});
