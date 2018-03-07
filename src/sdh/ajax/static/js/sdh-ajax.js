
AjaxConverter = {
    getCookie: function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    csrfSafeMethod: function(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    },

    sameOrigin: function(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    },

    convert: function(data) {
        var json_data = jQuery.parseJSON(data);

        if (json_data.status_code && json_data.extension && json_data.extension == 'sdh.ajax.accept_ajax') {
            switch (json_data.status_code) {
                case 200:
                    return json_data.content

                case 302:
                    if (json_data.headers.location) {
                        location.href = json_data.headers.location;
                    } else {
                        location.href = json_data.headers.location = '/'
                    }
                    break;

                case 500:
                    if (json_data.debug_msg) {

                        var debug_window = window.open();
                        debug_window.document.write(json_data.debug_msg);
                    } else {
                        console.log('Error');
                    }
                    break;

            };
            return {};
        }
        return json_data;
    }
};




$(function () {
    $.ajaxSetup({
        converters: {
            "text json": AjaxConverter.convert
        },
        beforeSend: function(xhr, settings) {
            if (!AjaxConverter.csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = AjaxConverter.getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }

    });
});

