'use strict'

let page = 1;

$(document).ready(function() {
    loadOnScroll();
});

function loadOnScroll() {
    if ($(window).scrollTop() > $(document).height() - $(window).height() * 2) {
        $(window).unbind();
        loadItems();
    }
}

function loadItems() {
    $.ajax({
        type: 'get',
        url: `${location.href}?page=${page}`,
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        success: function(data) {
            console.log(`${location.href}?page=${page}`)
            if ( data.status != 404 ) {
                $('#posts').append(data);
                page++;
                $(window).bind('scroll', function () { loadOnScroll() });
            }
        },
        error: function() { console.log(data.responseJSON.error); },
    });
}
