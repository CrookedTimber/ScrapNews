$(document).ready(function () {
    var $container = $(".masonry-container");

    $container.imagesLoaded().progress(function () {
        $container.masonry();
    });
});
