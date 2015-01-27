$(document).ready(function() {
    $('svg').mouseover(function () {
        $title = $(this).find('title');
        $title.data('title', $title.text());
        $title.text('');
    }).mouseout(function () {
        $title = $(this).find('title');
        $title.text($title.data('title'));
    });
});
