
function revealPersonalCollection() {
    if ($("#personal-collection").css("opacity") == 1) {
        $("#collection-toggle").css("opacity", "1");
        $("#personal-collection").css("opacity", "0");
    } else {
        $("#personal-collection").css("opacity", "1");
        $("#collection-toggle").css("opacity", "0");
    }
    return false;
}


function resizeModal(winHeight) {
    $('.reveal-modal').css('max-height', winHeight - 110 + 'px'); // 100 +10px to keep modal effect visible
    $('.reveal-modal > img').css("display", "block").css('max-height', winHeight - 200 + 'px');
}

/* Expandable lists */
function expandableList() {
    // expandable lists
    var collapsedClass = "fa fa-caret-right";
    var expandedClass = "fa fa-caret-down";
    $("section[data-section='expandable'] .list-header a.ctrl").click(function () {
        if ($(this).attr("data-collapsed-text")) {
            collapsedText = $(this).attr("data-collapsed-text");
        } else {
            collapsedText = '';
        }
        if ($(this).attr("data-expanded-text")) {
            expandedText = $(this).attr("data-expanded-text");
        } else {
            expandedText = '';
        }
        if ($(this).hasClass("expand")) {
            $(this).parent().parent().parent().find(".list-content").slideDown(400, function () {
                // finished
            });
            $(this).removeClass("expand").addClass("collapse");
            $(this).find("i").removeClass(collapsedClass).addClass(expandedClass);
            if (expandedText != '') {
                $(this).find(".ctrl-link-title").text(expandedText);
            }
        } else if ($(this).hasClass("collapse")) {
            $(this).parent().parent().parent().find(".list-content").slideUp();
            $(this).removeClass("collapse").addClass("expand");
            $(this).find("i").removeClass(expandedClass).addClass(collapsedClass);
            if (collapsedText != '') {
                $(this).find(".ctrl-link-title").text(collapsedText);
            }
        }

        return false;
    });
    // end expandable lists
}

/* Faceted browsing functions */
/* Update browse results */
function updateBrowseResults() {
    $("#loading").addClass("spinner-active");
    $("#results-section").addClass("overlay-active");
    setTimeout(function () {
        $("#results-section").removeClass("overlay-active");
        $("#loading").removeClass("spinner-active");
    }, 500);
    $("#no-filters").css("display", "none");

}

$(window).resize(function () {
    winHeight = $(window).height();
    resizeModal(winHeight);
});

$(document).ready(function () {

    /* Modal fix: https://github.com/zurb/foundation/issues/2971 */
    winHeight = $(window).height();
    resizeModal(winHeight);

    /* Annotations panel */
    $("a.ctrl.show-annotations").click(function () {
        $cpanel = $("#context-panel");
        if (!$cpanel.hasClass("slide-out")) {
            $cpanel.addClass("slide-out");
        } else {
            $cpanel.removeClass("slide-out").addClass("slide-in");
        }
    });
    $("#close-context-panel").click(function () {
        $("#context-panel").removeClass("slide-out");
    });

    $("a.ctrl.reply").click(function () {
        $(".reply-box").slideDown(400);
        $(this).css("display", "none");
    });

    /* save a comment */
    $(".ctrl.save-reply").click(function () {
        replyTo = $(this).attr("data-reply-to");
        replyArea = $('div[data-reply-area="' + replyTo + '"]');
        replyArea.find('.saving').css("display", "block");
        setTimeout(function () {
            replyArea.find('.saving').css("display", "none");
            if (!replyArea.attr("data-saved-reply")) {
                replyArea.slideUp(200);
                $('div[data-saved-reply="' + replyTo + '"]').css("display", "block");
            }
        }, 500);
    });

    /* edit a comment */
    $("a.ctrl.edit").click(function () {
        commentToEdit = $(this).attr("data-edit");
        textarea = $('textarea[data-reply-text="' + commentToEdit + '"]');
        if (textarea.hasClass("disabled")) {
            // alert("disabled");
            textarea.removeAttr("disabled").removeClass("disabled").focus();
            textarea.removeClass("disabled");
            $(this).parent().parent().parent().parent().find(".edit-actions").css("display", "block");
        } else {
            // alert("not disabled");
            textarea.attr("disabled", "").addClass("disabled");
            $(this).parent().parent().parent().parent().find(".edit-actions").css("display", "none");
        }
    });
    /* cancel editing */
    $("a.ctrl.cancel").click(function () {
        comment = $(this).attr("data-reply-to");
        $('textarea[data-reply-text="' + comment + '"]').attr("disabled", "").addClass("disabled").blur();
        $(this).parent().parent().css("display", "none");
    });

    /* collection toggle */
    /* toggle music stand */
    $("#collection-toggler").click(function () {
        revealPersonalCollection();
    });
    $("#controls-minimise").click(function () {
        if ($("#personal-collection").css("opacity", "1")) {
            $("#personal-collection").css("opacity", "0");
            $("#collection-toggle").css("opacity", "1");
        } else {
            $("#collection-toggle").css("opacity", "0");
            $("#personal-collection").css("opacity", "1");
        }
        return false;
    });
    $("#show-collection").click(function () {
        revealPersonalCollection('no');
        return false;
    })

    /* Add images to collection */
    $(".bar-images .ctrl.add").click(function () {
        $(this).removeClass("add").addClass("remove");
        $(this).find(".fa").removeClass("fa-plus-circle").addClass("fa-minus-circle");
        $(this).attr("title", "Remove from collection");
        $feedback = $(this).parent().parent().parent().find(".collection-feedback");
        $feedback.fadeIn();
        $("#personal-collection").css("opacity", "1");
        $("#collection-toggle").css("opacity", "0");
        $(".collection-images a.added").css("border", "2px solid #7d0000");
        setTimeout(function () {
            $(".collection-images a.added").css("border", "0");
            $(".feedback-message.image-added").fadeOut();
            $feedback.fadeOut();
        }, 4000);

    });

    /* Slick image carousel: http://kenwheeler.github.io/slick/ */
    $('.thumbnail-carousel').slick({
        centerMode: false,
        infinite: false,
        centerPadding: '60px',
        slidesToShow: 9,
        slidesToScroll: 3,
        responsive: [
            {
                breakpoint: 800,
                settings: {
                    slidesToshow: 5
                }
            }
        ]
    });
    /* page view comments */
    $(".ctrl.show-page-comment").click(function () {
        $(".annotation-box").toggleClass("fade-out");
        return false;
    });


});
