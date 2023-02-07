'use strict'

function like(post_id) {
    $.ajax({
        type: 'post',
        url: `${ location.origin }/api/post/${ post_id }/like`,
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            $(`#rating_${ data.id }`).html(data.rating);
            let like_button = $(`#like_${ data.id }`);

            if ( data.result ) {
                like_button.addClass('active');
            } else {
                like_button.removeClass('active');
            }
        },
        error: function (data) { console.log(data.responseJSON.error); },
    });
}
