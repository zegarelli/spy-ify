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

$("#testquery").change(function () {
    var query = $(this).val();
      console.log( query );

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
            'query': query
        },
        contentType: 'json',
        success: function (data) {
          console.log(data.filtered);
        }
    })
});