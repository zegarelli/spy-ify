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
    var songquery = $("#songquery").val();
    var artistquery = $("#artistquery").val();
    var albumquery = $("#albumquery").val();
    var columns = $("#columns").val();
    var columns_check = $("#column-checkbox").val();
      console.log( '    playquery:' + playquery );
      console.log( '    songquery:' + songquery );
      console.log( '    artistquery:' + artistquery );
      console.log( '    albumquery:' + albumquery );
      console.log( '    columns:' + columns );
      console.log( '    columns_check:' + columns_check );

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
            'songquery': songquery,
            'artistquery': artistquery,
            'albumquery': albumquery,
            'columns': columns,
            'columns_check': columns_check
        },
        dataType: 'html',
        success: function (data) {
          $('#search-results').html(data)
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
$("#songquery").change(function(){
    console.log('in songquery')
    update_search()
});
$("#artistquery").change(function(){
    console.log('in artistquery')
    update_search()
});
$("#albumquery").change(function(){
    console.log('in albumquery')
    update_search()
});
$("#columns").change(function(){
    console.log('in columns')
    update_search()
});
$("#columns_check").change(function(){
    console.log('in columns_check')
    update_search()
});
